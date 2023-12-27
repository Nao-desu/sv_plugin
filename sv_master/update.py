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
deck_url = "https://shadowversemaster.com/archetype/"
deck_img_url = "https://d3n08lmbrfojvo.cloudfront.net/archetypes/rotation/"
deckdata_r = []
deckdata_l = []
deckname_num_r = {}
deckname_num_l = {}

def hashtolist(hash:str):
    cardlist = []
    for card_hash in hash.split(".")[2:]:
        cardlist.append(hashToID(card_hash))
    return cardlist

def placement2wins(num:int,num2):
    if num > 1000:
        return num-1000
    elif num == 10:
        return 'JCG winner'
    elif num == 7:
        return 'JCG 2nd Place'
    elif num == 3:
        return 'JCG Top 4'
    elif num == 2:
        return 'JCG TOP 8'
    elif num == 1:
        return 'JCG TOP 16'
    else:
        if num2 == 3:
            return 'JCG Top 32'
        elif num2 == 2:
            return 'JCG Top 64'
        elif num2 == 1:
            return 'JCG Top 128'
        elif num2 == 0:
            return 'JCG Top 256'
        else:
            return 'JCG Participant'
         

async def get_deck_data(name,tag):
    async with AsyncClient() as client:
        while(1):
            try:
                if tag=='r':
                    req = await client.get(url=f'{deck_url}{name}/rotation/__data.json',timeout=None)
                else:
                    req = await client.get(url=f'{deck_url}{name}/unlimited/__data.json',timeout=None)
                break
            except:
                pass
        d = json.loads(req.text)['nodes'][1]['data']
        decks_map = d[d[0]['decks']]
        if decks_map:
            if tag=='r':
                global deckname_num_r
                deckname_num_r[name] = len(decks_map)
            else:
                global deckname_num_l
                deckname_num_l[name] = len(decks_map)
            for i in decks_map:
                deck = {}
                deck_map = d[i]
                if "placement" in deck_map:
                    deck["deck_name"] = name
                    deck["cards"] = hashtolist(d[deck_map["hash"]])
                    deck["clan"] = int(d[deck_map["craft_id"]])
                    deck["auther"] = d[deck_map["player_name"]]
                    deck["creat_time"] = d[deck_map["created_at"]][1][:10]
                    deck["wins"] = placement2wins(d[deck_map["placement"]],d[deck_map["total_wins"]])
                else:
                    deck["deck_name"] = name
                    deck["cards"] = hashtolist(d[deck_map["hash"]])
                    deck["clan"] = int(d[deck_map["clanId"]])
                    deck["auther"] = d[deck_map["player_name"]]
                    deck["creat_time"] = d[deck_map["createdAt"]][1][:10]
                    deck["wins"] = d[deck_map["wins"]]
                s = d[deck_map["source"]]
                if s:
                    deck["from"] = s
                else:
                    deck["from"] = d[deck_map["deck_tournament"]]
                if tag == 'r':
                    global deckdata_r
                    deckdata_r.append(deck)
                else:
                    global deckdata_l
                    deckdata_l.append(deck)


async def deck_update():
    print("开始更新卡组数据")
    global deckname_num_r
    global deckname_num_l
    global deckdata_r
    global deckdata_l
    deckname_num_r = await get_deck_name('r')
    deckname_num_l = await get_deck_name('l')
    tasks = []
    for deckname in deckname_num_r:
        tasks.append(get_deck_data(deckname,'r'))
    for deckname in deckname_num_l:
        tasks.append(get_deck_data(deckname,'l'))
    await asyncio.wait(tasks)
    with open(join(MOUDULE_PATH,'data','deck3.json'),'w',encoding="utf-8") as f:
        json.dump(deckdata_r, f, indent=4, ensure_ascii=False)
    with open(join(MOUDULE_PATH,'data','deck1.json'),'w',encoding="utf-8") as f:
        json.dump(deckdata_l, f, indent=4, ensure_ascii=False)
    with open(join(MOUDULE_PATH,'data','unlimited_deck.json'),'w',encoding="utf-8") as f:
        json.dump(deckname_num_l, f, indent=4, ensure_ascii=False)
    with open(join(MOUDULE_PATH,'data','rotation_deck.json'),'w',encoding="utf-8") as f:
        json.dump(deckname_num_r, f, indent=4, ensure_ascii=False)
    deckdata_r = []
    deckdata_l = []
    deckname_num_r = {}
    deckname_num_l = {}
    print("卡组数据更新完毕")

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
    tasks = [rating_update(),deck_update()]
    await asyncio.wait(tasks)

