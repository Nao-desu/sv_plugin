from os.path import join,exists
from os import makedirs
from tqdm import tqdm
from io import BytesIO
import requests,json
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

def cardinfo_dl():
    """
    下载卡牌信息
    """
    if not exists(join(MOUDULE_PATH,'data')):
        makedirs(join(MOUDULE_PATH,'data'))
    print('下载卡牌信息')
    cardinfo = r.get(cardinfo_url,params={"format":"json","lang":"zh-tw"})
    cardlist = json.loads(cardinfo.text)["data"]["cards"]
    print("下载完成,正在处理卡牌信息")
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
    with open(join(MOUDULE_PATH,"data/cards.json"),'w', encoding="utf-8") as f:
        json.dump(card_dict, f, indent=4, ensure_ascii=False)
    with open(join(MOUDULE_PATH,"data/cardlist.json"),'w', encoding="utf-8") as f:
        json.dump(cardlist, f, indent=4, ensure_ascii=False)
    print('保存完成')
    return card_dict

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

def img_dl(card_dict):
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
    num = 31
    for i in card_dict:
        if card_dict[i]["char_type"] != 1:
            num += 2
        else:
            num += 3
    with tqdm(total= num,unit='img',desc='下载图片',position=0) as pbar:
        for i in range(0,31):
            if not exists(join(MOUDULE_PATH,f'img/cost/{i}.png')):
                cost_pic = r.get(f'{cost_url}{i}.png')
                with open(join(MOUDULE_PATH,f'img/cost/{i}.png',),'wb') as img:
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
            if card_dict[id]["char_type"] == 1:
                if not exists(join(MOUDULE_PATH,f'img/E/E_{id}.png')):
                    card_pic = r.get(f'{img_url_e}{id}.png')
                    card_name = r.get(f'{img_url_n}{id}.png')
                    pic = img_gen(Image.open(BytesIO(card_pic.content)),Image.open(BytesIO(card_name.content)))
                    pic.save(join(MOUDULE_PATH,f'img/E/E_{id}.png'),'PNG')
                pbar.update()
            if not exists(join(MOUDULE_PATH,f'img/L/L_{id}.jpg')):
                card_pic = r.get(f'{img_url_l}{id}.jpg')
                with open(join(MOUDULE_PATH,f'img/L/L_{id}.jpg',),'wb') as img:
                    img.write(card_pic.content)
            pbar.update()

def update():
    """
    需要下载资源时调用此函数
    """
    cards = cardinfo_dl()
    img_dl(cards)
    latest_set = get_latest_set()
    for card in cards:
        if int(cards[card]["card_set_id"])>latest_set and int(cards[card]["card_set_id"])<20000:
            print('发现卡包更新，请尝试更新插件')
    print('已下载所有资源') 

                

