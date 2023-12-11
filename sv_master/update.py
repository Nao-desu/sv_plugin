"""
自动获取&分析shadowversemaster.com的数据
"""
import asyncio,json,io
from httpx import AsyncClient
from os.path import join,exists
from os import makedirs
from PIL import Image
from ..info import MOUDULE_PATH,hashToID,get_deck_name

rating_url = "https://shadowversemaster.com/ratings/__data.json?x-sveltekit-invalidated=01"
deck3_url = "https://shadowversemaster.com/decks/__data.json?&format=3"
deck1_url = "https://shadowversemaster.com/decks/__data.json?&format=1"
deck_img_url = "https://d3n08lmbrfojvo.cloudfront.net/archetypes/rotation/"

def hashtolist(hash:str):
    cardlist = []
    for card_hash in hash.split(".")[2:]:
        cardlist.append(hashToID(card_hash))
    return cardlist

async def data_to_deck(data:list):
    map = data[1]
    decks = []
    for i in map:
        deck = {}
        deckmap = data[i]
        deck["deck_name"] = data[deckmap["archetypeId"]]
        deck["cards"] = hashtolist(data[deckmap["hash"]])
        deck["clan"] = int(data[deckmap["clanId"]])
        deck["auther"] = data[deckmap["playerName"]]
        deck["creat_time"] = data[deckmap["createdAt"]][1][:10]
        if "tournament" in deckmap:
            deck["wins"] = 'winner'
            deck["from"] = data[deckmap["tournament"]]
        else:
            deck["wins"] = data[deckmap["wins"]]
            deck["from"] = data[deckmap["source"]]
        decks.append(deck)
    return decks

async def deck_update():
    print("开始更新卡组数据")
    async with AsyncClient() as client:
        while(1):
            try:
                req1 = await client.get(url=deck3_url,timeout=None)
                req2 = await client.get(url=deck1_url,timeout=None)
                break
            except:
                pass
        d = json.loads(req1.text)['nodes'][1]['data']
        d = await data_to_deck(d)
        with open(join(MOUDULE_PATH,'data','deck3.json'),'w',encoding="utf-8") as f:
            json.dump(d, f, indent=4, ensure_ascii=False)
        d = json.loads(req2.text)['nodes'][1]['data']
        d = await data_to_deck(d)
        with open(join(MOUDULE_PATH,'data','deck1.json'),'w',encoding="utf-8") as f:
            json.dump(d, f, indent=4, ensure_ascii=False)
    print("卡组数据更新完毕")

async def deck_img_dl(url,path):
    async with AsyncClient() as client:
        while(1):
            try:
                req = await client.get(url,timeout=None)
                break
            except:
                pass
        try:
            img = Image.open(io.BytesIO(req.content))
        except:
            img = Image.new("RGB",(200,200),(0,0,0))
        img = img.resize((200,200))
        img = img.convert("RGB")
        img.save(path,format="JPEG")

async def deck_img_update():
    print("开始更新卡组图片")
    if not exists(join(MOUDULE_PATH,'img','deck')):
        makedirs(join(MOUDULE_PATH,'img','deck'))
    deck_name = get_deck_name()
    tasks = []
    for name in deck_name:
        if not exists(join(MOUDULE_PATH,'img','deck',f'{name}.jpg')):
            tasks.append(deck_img_dl(deck_img_url+name,join(MOUDULE_PATH,'img','deck',f'{name}.jpg')))
    if tasks:await asyncio.wait(tasks)
    print("卡组图片更新完毕")



async def rating_update():
    print("开始更新Ratings")
    async with AsyncClient() as client:
        while(1):
            try:
                req = await client.get(url=rating_url,timeout=None)
                break
            except:
                pass
    d = json.loads(req.text)['nodes'][1]['data']
    realdata = {}
    alldata_map = d[0]["craftData"]
    map = d[alldata_map]
    for i in map:
        clanmap = d[map[i]]
        clanmap.sort(reverse=False)
        for datamap in clanmap:
            data = d[datamap]
            time = d[data["updated_at"]][1][:10]
            if time not in realdata:
                realdata[time] = {}
            realdata[time][i] = [d[data["win_rate"]],d[data["play_rate"]]]
    with open(join(MOUDULE_PATH,'data','ratings.json'),'w',encoding="utf-8") as f:
        json.dump(realdata, f,indent=4,ensure_ascii=False)
    print("Ratings更新完毕")


async def master_update():
    tasks = [rating_update(),deck_update(),deck_img_update()]
    await asyncio.wait(tasks)

