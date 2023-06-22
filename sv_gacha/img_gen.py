from PIL import Image,ImageDraw,ImageFont
from ..info import MOUDULE_PATH
from os.path import join
from io import BytesIO
import base64

font = ImageFont.truetype(join(MOUDULE_PATH,'font/font.ttf'),size = 50)

async def draw_result_1(leadercard:list,card:dict)->str:
    """
    绘制8张卡牌构成的图片
    """
    img = Image.new("RGBA",(536*4,698*2),(255,255,255,100))
    cards = leadercard
    for i in card:
        for j in card[5-i]:
            cards.append(j)
    for i in range(0,2):
        for j in range(0,4):
            id = cards[j+i*4]
            card_pic = Image.open(join(MOUDULE_PATH,f'img/C/C_{id}.png'))
            img.paste(card_pic,(j*536,i*698),card_pic)
    img.resize((536,349))
    img = img.convert('RGB')
    buf = BytesIO()
    img.save(buf, format='JPEG')
    base64_str = f'base64://{base64.b64encode(buf.getvalue()).decode()}'
    msg = f'[CQ:image,file={base64_str}]'
    return msg

async def draw_result_2(leadercard:list,card:dict)->str:
    """
    绘制仅包含传说卡牌和异画的抽卡结果
    """
    cards ={}
    cardlist = []
    if not leadercard and not card[1]:
        img = Image.new("RGBA",(536*5//4,698//2),(255,255,255,100))
    else:
        for i in leadercard:
            if i in cards:
                cards[i]+=1
            else:
                cards[i]=1
                cardlist.append(i)
        for i in card[1]:
            if i in cards:
                cards[i]+=1
            else:
                cards[i]=1
                cardlist.append(i)
        num = len(cards)
        line = (num+4)//5
        img = Image.new("RGBA",(536*5,698*line),(255,255,255,100))
        draw = ImageDraw.Draw(img)
        for i in range(0,line):
            for j in range(0,5):
                if j+i*5 >= len(cardlist):
                    break
                id = cardlist[j+i*5]
                card_pic = Image.open(join(MOUDULE_PATH,f'img/C/C_{id}.png'))
                img.paste(card_pic,(j*536,i*698),card_pic)
                draw.text((j*536+450,i*698+20),f'x{cards[id]}',(0,0,0),font)
            if j+i*5 >= len(cardlist):
                break
    x,y = img.size
    img.resize((x//8,y//8))
    img = img.convert('RGB')
    buf = BytesIO()
    img.save(buf, format='JPEG')
    base64_str = f'base64://{base64.b64encode(buf.getvalue()).decode()}'
    msg = f'[CQ:image,file={base64_str}]'
    return msg