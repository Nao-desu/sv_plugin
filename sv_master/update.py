"""
自动获取&分析shadowversemaster.com的数据
"""
import asyncio,json
from httpx import AsyncClient
from os.path import join
from ..info import MOUDULE_PATH,hashToID,get_deck_name

deck_url = "https://shadowversemaster.com/archetype/"
deckdata_r = []
deckdata_l = []
deckname_num_r = {}
deckname_num_l = {}

def hashtolist(hash:str):
    cardlist = []
    for card_hash in hash.split(".")[2:]:
        cardlist.append(hashToID(card_hash))
    return cardlist

async def get_deck_data(name,tag,sem):
    async with sem:
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
            global deckname_num_r
            global deckname_num_l
            if decks_map:
                if tag=='r':
                    deckname_num_r[name] = len(decks_map)
                else:
                    deckname_num_l[name] = len(decks_map)
                for i in decks_map:
                    deck = {}
                    deck_map = d[i]
                    if d[deck_map["placementText"]]:
                        deck["deck_name"] = name
                        deck["cards"] = hashtolist(d[deck_map["hash"]])
                        deck["clan"] = int(d[deck_map["clanId"]])
                        deck["auther"] = d[deck_map["playerName"]]
                        deck["creat_time"] = d[deck_map["createdAt"]][1][:10]
                        deck["wins"] = d[deck_map["placementText"]]
                        deck["from"] = d[deck_map["tournament"]]
                    else:
                        deck["deck_name"] = name
                        deck["cards"] = hashtolist(d[deck_map["hash"]])
                        deck["clan"] = int(d[deck_map["clanId"]])
                        deck["auther"] = d[deck_map["playerName"]]
                        deck["creat_time"] = d[deck_map["createdAt"]][1][:10]
                        deck["wins"] = d[deck_map["wins"]]
                        deck["from"] = d[deck_map["source"]]
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
    sem = asyncio.Semaphore(5)
    deckname_num_r = await get_deck_name('r')
    deckname_num_l = await get_deck_name('l')
    for i in deckname_num_r:
        deckname_num_r[i] = 0
    for i in deckname_num_l:
        deckname_num_l[i] = 0
    tasks = []
    for deckname in deckname_num_r:
        tasks.append(get_deck_data(deckname,'r',sem))
    for deckname in deckname_num_l:
        tasks.append(get_deck_data(deckname,'l',sem))
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


async def master_update():
    tasks = [deck_update()]
    await asyncio.wait(tasks)

