"""
配置md使用的图床
"""
from hoshino import Service
from os.path import exists,join
from ..config import token
from ..info import MOUDULE_PATH
from httpx import AsyncClient
import json

sv = Service('image_host')

path = join(MOUDULE_PATH,'image_host','imagelist.json')

upload_url = 'https://www.imgtp.com/api/upload'
delete_url = 'https://www.imgtp.com/api/delete'
headers = {'Token': token}

if not exists(path):
    with open(path,'w', encoding="utf-8") as f:
        a = []
        json.dump(a,f)

async def memo_id(id):
    with open(path,'r+', encoding="utf-8") as f:
        id_list:list = json.load(f)
        json.dump(id_list.append(id),f)
    return

async def delete_list():
    with open(path,'r+', encoding="utf-8") as f:
        id_list:list = json.load(f)
        json.dump(id_list[-100:],f)
    de_list = id_list[:-100][:50]
    if de_list:
        return ','.join(de_list)
    return 0

async def upload_img(img_name,img):
    async with AsyncClient() as client:
        req = await client.post(url=upload_url,headers=headers,files={'image':(img_name,img)},timeout=None)
    data = json.loads(req.text)
    await memo_id(data["data"]["id"])
    return data["data"]["url"]

@sv.scheduled_job('cron',hour = '*/2')
async def delete_img():
    print("准备清理图床")
    d_l = await delete_list()
    if d_l:
        print(d_l)
        async with AsyncClient() as client:
            await client.post(url=delete_url,params={'id':d_l},headers=headers,timeout=None)
    else:
        print("无需清理")
    return