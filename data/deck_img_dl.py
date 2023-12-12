from httpx import AsyncClient
from PIL import Image
from os.path import join,exists
from os import makedirs
import io,os,asyncio,json
r = {}
l = {}
PATH = os.path.dirname(__file__)
deck_img_url_r = 'https://d3n08lmbrfojvo.cloudfront.net/archetypes/rotation/'
deck_img_url_l = 'https://d3n08lmbrfojvo.cloudfront.net/archetypes/unlimited/'


async def deck_img_dl(url,path,flag,name):
    print(f'download {url}')
    async with AsyncClient() as client:
        while(1):
            try:
                req = await client.get(url,timeout=None)
                break
            except:
                pass
    if req.status_code == 200:
        if flag == 'r':
            global r
            r[name] = 0
        else:
            global l
            l[name] = 0
        img = Image.open(io.BytesIO(req.content))
        img = img.resize((200,200))
        img = img.convert("RGB")
        img.save(path,format="JPEG")
        print(f'{url} success')
    else :
        print(f'{url} failed')

async def deck_img_update():
    if not exists(join(PATH,'deck')):
        makedirs(join(PATH,'deck'))
    with open('en2cn.json','r',encoding='utf-8') as f:
        deck_name = list(json.load(f).keys())
    tasks = []
    for name in deck_name:
        tasks.append(deck_img_dl(deck_img_url_r+name,join(PATH,'deck',f'r_{name}.jpg'),"r",name))
        tasks.append(deck_img_dl(deck_img_url_l+name,join(PATH,'deck',f'l_{name}.jpg'),"l",name))
    if tasks:await asyncio.wait(tasks)
    with open('rotation_deck.json','w',encoding='utf-8') as f:
        json.dump(r,f,indent=4,ensure_ascii=False)
    with open('unlimited_deck.json','w',encoding='utf-8') as f:
        json.dump(l,f,indent=4,ensure_ascii=False)    
    print("卡组图片下载完毕")

if __name__ == '__main__':
    asyncio.run(deck_img_update()) 