from PIL import Image,ImageDraw,ImageFont
from ..info import MOUDULE_PATH
from os.path import join
from io import BytesIO
from hoshino.image_host import upload_img
from os.path import exists

font = ImageFont.truetype(join(MOUDULE_PATH,'font/font.ttf'),size = 50)

async def draw_result_1(leadercard:list,card:dict)->str:
    """
    绘制8张卡牌构成的图片,返回图床链接和图片尺寸
    """
    img = Image.new("RGBA",(536*4,698*2),(255,255,255,100))
    cards = leadercard
    for i in card:
        for j in card[5-i]:
            cards.append(j)
    for i in range(0,2):
        for j in range(0,4):
            id = cards[j+i*4]
            if exists(join(MOUDULE_PATH,f'img/C/C_{id}.webp')):
                card_pic = Image.open(join(MOUDULE_PATH,f'img/C/C_{id}.webp'))
            else:
                card_pic = Image.open(join(MOUDULE_PATH,f'img/C/C_{id}.png'))
            img.paste(card_pic,(j*536,i*698),card_pic)
    img.resize((536,349))
    img = img.convert('RGB')
    buf = BytesIO()
    img.save(buf, format='JPEG')
    url = await upload_img(buf)
    return url,(536,349)

async def draw_result_2(leadercard:list,card:dict,only_leader:bool)->str:
    """
    绘制仅包含传说卡牌和异画的抽卡结果,返回图床链接和图片尺寸
    """
    cards ={}
    cardlist = []
    if only_leader and not leadercard:
        img = None
    if not leadercard and not card[1]:
        img = None
    else:
        for i in leadercard:
            if i in cards:
                cards[i]+=1
            else:
                cards[i]=1
                cardlist.append(i)
        if not only_leader:
            for i in card[1]:
                if i in cards:
                    cards[i]+=1
                else:
                    cards[i]=1
                    cardlist.append(i)
        num = len(cards)
        line = (num+4)//5
        if line==1:
            img = Image.new("RGBA",(536*num,698),(255,255,255,100))
        else:img = Image.new("RGBA",(536*5,698*line),(255,255,255,100))
        draw = ImageDraw.Draw(img)
        for i in range(0,line):
            for j in range(0,5):
                if j+i*5 >= len(cardlist):
                    break
                id = cardlist[j+i*5]
                if exists(join(MOUDULE_PATH,f'img/C/C_{id}.webp')):
                    card_pic = Image.open(join(MOUDULE_PATH,f'img/C/C_{id}.webp'))
                else:
                    card_pic = Image.open(join(MOUDULE_PATH,f'img/C/C_{id}.png'))
                img.paste(card_pic,(j*536,i*698),card_pic)
                draw.text((j*536+450,i*698+20),f'x{cards[id]}',(0,0,0),font)
            if j+i*5 >= len(cardlist):
                break
    if not img:
        img = Image.new("RGBA",(536,698),(255,255,255,100))
    x,y = img.size
    img.resize((x//8,y//8))
    img = img.convert('RGB')
    buf = BytesIO()
    img.save(buf, format='JPEG')
    url = await upload_img(buf)
    return url,(x//8,y//8)