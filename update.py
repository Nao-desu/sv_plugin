from os.path import join,exists
from os import makedirs
from tqdm import tqdm
from io import BytesIO
import requests,json,os,aiohttp
from requests.adapters import HTTPAdapter
from PIL import Image
try:
    from .info import MOUDULE_PATH,get_latest_set
except:
    from info import MOUDULE_PATH,get_latest_set
r = requests.Session()
r.mount('https://',HTTPAdapter(max_retries=5))
cardinfo_url = 'https://shadowverse-portal.com/api/v1/cards'
img_url_c = 'https://shadowverse-portal.com/image/card/phase2/common/C/C_'
img_url_l = 'https://shadowverse-portal.com/image/card/phase2/common/L/L_'
img_url_e = 'https://shadowverse-portal.com/image/card/phase2/common/E/E_'
img_url_n = 'https://shadowverse-portal.com/image/card/phase2/zh-tw/N/N_'
cost_url = 'https://shadowverse-portal.com/public/assets/image/common/global/cost_'
voice_api = 'https://svgdb.me/api/voices/'
voice_url = 'https://svgdb.me/assets/audio/jp/'
img_url_f = 'https://svgdb.me/assets/fullart/'

async def download_file(url, save_path,pbar):
    if not exists(save_path):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                with open(save_path, 'wb') as f:
                    while True:
                        chunk = await response.content.read(1024)
                        if not chunk:
                            break
                        f.write(chunk)
    pbar.update()


async def cardinfo_dl():
    """
    下载卡牌信息
    """
    if not exists(join(MOUDULE_PATH,'data')):
        makedirs(join(MOUDULE_PATH,'data'))
    print('下载卡牌信息')
    cardinfo = r.get(cardinfo_url,params={"format":"json","lang":"zh-tw"})
    cardlist = json.loads(cardinfo.text)["data"]["cards"]
    with tqdm(total= 2*len(cardlist),unit='card',desc='处理卡牌信息',position=0) as pbar:#构建进度条
        nonamecard=[]
        for card in cardlist:
            if card["card_name"] == None:#移除无名卡牌，一般是正常卡牌的激奏或者结晶卡
                nonamecard.append(card)
            else:
                if card["char_type"]==3:#倒数护符和普通护符有区分，这里不需要这个特性
                    card["char_type"] = 2
            pbar.update()
        for card in nonamecard:
            cardlist.remove(card)
            pbar.update()
        card_dict = {}#下载的卡牌内容为list,用card_id为key把卡牌信息保存为dict
        for card in cardlist:
            card_dict[str(card["card_id"])] = card
            pbar.update()
    new_card = []
    changed_card = []
    if exists(join(MOUDULE_PATH,'data/cardlist.json')):
        print('发现已存在的卡牌信息，检查更新')
        with open(join(MOUDULE_PATH,"data/cards.json"),'r', encoding="utf-8") as f:
            card_dict_old = json.load(f)
        for id in card_dict:
            if id in card_dict_old and card_dict_old[id] != card_dict[id]:
                if exists(join(MOUDULE_PATH,f'img/C/C_{id}.png')):
                    os.remove(join(MOUDULE_PATH,f'img/C/C_{id}.png'))
                if exists(join(MOUDULE_PATH,f'img/E/E_{id}.png')):
                    os.remove(join(MOUDULE_PATH,f'img/E/E_{id}.png'))
                if exists(join(MOUDULE_PATH,f'img/L/L_{id}.png')):
                    os.remove(join(MOUDULE_PATH,f'img/L/L_{id}.png'))
                print(f'    卡牌【{card_dict_old[id]["card_name"]}】数据变动，已删除原卡图')
                changed_card.append(id)
            if id not in card_dict_old:
                print(f'    添加新卡牌【{card_dict[id]["card_name"]}】')
                new_card.append(id)
        if not new_card and not changed_card:
            print('卡牌信息已是最新版本！')
    with open(join(MOUDULE_PATH,"data/cards.json"),'w', encoding="utf-8") as f:
        json.dump(card_dict, f, indent=4, ensure_ascii=False)
    with open(join(MOUDULE_PATH,"data/cardlist.json"),'w', encoding="utf-8") as f:
        json.dump(cardlist, f, indent=4, ensure_ascii=False)
    return card_dict,new_card,changed_card

def img_gen(pic,name):
    """
    将卡图与文字合成
    """
    xn,yn = name.size
    k = 40/yn
    newsize = (int(xn*k), 40)
    move = False
    if xn*k >= 300:
        k = 340/xn
        newsize = (340,int(yn*k))
        move = True
    name = name.resize(newsize, resample=Image.LANCZOS)
    xn,yn = name.size
    if move:
        left = int(290 - xn/2)
    else:
        left = int(268 - xn/2)
    top = int(95 - yn/2)
    pic.paste(name,(left,top),name)
    return pic

async def img_dl(card_dict:dict):
    """
    下载卡牌图片
    """
    print("准备下载图片")
    if not exists(join(MOUDULE_PATH,'img/C')):
        makedirs(join(MOUDULE_PATH,'img/C'))
    if not exists(join(MOUDULE_PATH,'img/E')):
        makedirs(join(MOUDULE_PATH,'img/E'))
    if not exists(join(MOUDULE_PATH,'img/L')):
        makedirs(join(MOUDULE_PATH,'img/L'))
    if not exists(join(MOUDULE_PATH,'img/cost')):
        makedirs(join(MOUDULE_PATH,'img/cost'))
    if not exists(join(MOUDULE_PATH,'img/full')):
        makedirs(join(MOUDULE_PATH,'img/full'))
    num = 31
    for i in card_dict:
        if card_dict[i]["char_type"] != 1:
            num += 3
        else:
            num += 5
    with tqdm(total= num,unit='file',desc='下载图片',position=0) as pbar:
        for i in range(0,31):
            if not exists(join(MOUDULE_PATH,f'img/cost/{i}.png')):
                cost_pic = r.get(f'{cost_url}{i}.png')
                with open(join(MOUDULE_PATH,f'img/cost/{i}.png'),'wb') as img:
                    img.write(cost_pic.content)
            pbar.update()
        for id in card_dict:
            if not exists(join(MOUDULE_PATH,f'img/C/C_{id}.png')):
                if id == '910441030':
                    card_pic = r.get(f'{img_url_c}{int(id)-10}.png')
                else:
                    card_pic = r.get(f'{img_url_c}{id}.png')
                card_name = r.get(f'{img_url_n}{id}.png')
                pic = img_gen(Image.open(BytesIO(card_pic.content)),Image.open(BytesIO(card_name.content)))
                pic.save(join(MOUDULE_PATH,f'img/C/C_{id}.png'),'PNG')
            pbar.update()
            if not exists(join(MOUDULE_PATH,f'img/full/{id}0.png')):
                if id == '910441030':
                    card_pic = r.get(f'{img_url_f}{int(id)-10}0.png')
                else:
                    card_pic = r.get(f'{img_url_f}{id}0.png')
                if card_pic.status_code == 200:
                    with open(join(MOUDULE_PATH,f'img/full/{id}0.png',),'wb') as img:
                            img.write(card_pic.content)
            pbar.update()
            if card_dict[id]["char_type"] == 1:
                if not exists(join(MOUDULE_PATH,f'img/E/E_{id}.png')):
                    card_pic = r.get(f'{img_url_e}{id}.png')
                    card_name = r.get(f'{img_url_n}{id}.png')
                    pic = img_gen(Image.open(BytesIO(card_pic.content)),Image.open(BytesIO(card_name.content)))
                    pic.save(join(MOUDULE_PATH,f'img/E/E_{id}.png'),'PNG')
                pbar.update()
                if not exists(join(MOUDULE_PATH,f'img/full/{id}1.png')):
                    card_pic = r.get(f'{img_url_f}{id}1.png')
                    if card_pic.status_code == 200:
                        with open(join(MOUDULE_PATH,f'img/full/{id}1.png',),'wb') as img:
                            img.write(card_pic.content)
                pbar.update()
            if not exists(join(MOUDULE_PATH,f'img/L/L_{id}.jpg')):
                card_pic = r.get(f'{img_url_l}{id}.jpg')
                with open(join(MOUDULE_PATH,f'img/L/L_{id}.jpg',),'wb') as img:
                    img.write(card_pic.content)
            pbar.update()

async def voice_dl(card:dict):
    """
    下载卡牌语音
    """
    print("准备下载语音")
    if not exists(join(MOUDULE_PATH,'voice')):
        makedirs(join(MOUDULE_PATH,'voice'))
    num = len(card)
    with tqdm(total= num,unit='file',desc='下载语音',position=0) as pbar:
        for id in card:
            if not exists(join(MOUDULE_PATH,f'voice/{id}')):
                req = r.get(f'{voice_api}{id}')
                if req.status_code == 200:
                    voice_dict:dict = json.loads(req.content.decode())
                    makedirs(join(MOUDULE_PATH,f'voice/{id}'))
                    for act in voice_dict:
                        for filename in voice_dict[act]:
                            voice = r.get(f'{voice_url}{filename}')
                            if voice.status_code == 200:
                                filename = filename.replace('|','_')
                                with open(join(MOUDULE_PATH,f'voice/{id}/{filename}',),'wb') as img:
                                    img.write(voice.content)
            pbar.update()
            
            


async def update_main(flag:bool):
    """
    需要下载资源时调用此函数
    """
    cards,new_card,changed_card = await cardinfo_dl()
    if flag and not new_card and not changed_card:
        return new_card,changed_card
    await img_dl(cards)
    await voice_dl(cards)
    print('已下载所有资源')
    return new_card,changed_card 

                

