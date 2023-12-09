"""
自动获取&分析shadowversemaster.com的数据
"""
import asyncio,json
from httpx import AsyncClient
from os.path import join
from ..info import MOUDULE_PATH

rating_url = "https://shadowversemaster.com/ratings/__data.json?x-sveltekit-invalidated=01"

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
    tasks = [rating_update()]
    await asyncio.wait(tasks)

