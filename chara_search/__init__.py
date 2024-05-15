from hoshino import Service,aiorequests
from .msgs import csh_msg,bakaga_omae,result_msg
from httpx import AsyncClient
from uuid import uuid4
from json import loads
import re,html

sv = Service('chara_search')

s_url = 'https://aiapiv2.animedb.cn/ai/api/detect'

async def get_pic(ev):
    pic = None
    match = re.findall(r'(\[CQ:image,file=.*?,url=.*?\])', html.unescape(str(ev.message)))
    if not match:
        return pic
    url = re.search(r"\[CQ:image,file=(.*),url=(.*)\]", match[0]).group(2)
    resp = await aiorequests.get(url)
    pic = await resp.content
    return pic

@sv.on_fullmatch("TA是谁")
async def cs_help(bot,ev):
    await bot.send(ev,csh_msg)

@sv.on_prefix('动漫角色搜索')
async def anime_search(bot,ev):
    pic = await get_pic(ev)
    if not pic:
        await bot.send(ev,bakaga_omae)
        return
    file_name = uuid4().hex + '.jpg'
    async with AsyncClient() as client:
        req1 = await client.post(url=s_url,params={'model':'pre_stable','ai_detect':1,},files={'image':(file_name,pic)},timeout=None)        
        req2 = await client.post(url=s_url,params={'model':'anime_model_lovelive','ai_detect':1,},files={'image':(file_name,pic)},timeout=None)
    data1 = loads(req1.text)
    data2 = loads(req2.text)
    await result_msg([data1,data2],pic,ev,bot)
    return

@sv.on_prefix('gal角色搜索')
async def gal_search(bot,ev):
    pic = await get_pic(ev)
    if not pic:
        await bot.send(ev,bakaga_omae)
        return
    file_name = uuid4().hex + '.jpg'
    async with AsyncClient() as client:
        req1 = await client.post(url=s_url,params={'model':'game_model_kirakira','ai_detect':1,},files={'image':(file_name,pic)},timeout=None)        
    data = loads(req1.text)
    await result_msg([data],pic,ev,bot)
    return