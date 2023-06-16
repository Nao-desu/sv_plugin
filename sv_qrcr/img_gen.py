from ..info import get_cards,MOUDULE_PATH
from os.path import join
from PIL import Image,ImageDraw,ImageFont
from io import BytesIO
import base64

font = ImageFont.truetype(join(MOUDULE_PATH,'font/font.ttf'),size = 15)

async def deck_img_gen(deck:dict)->str:
    """
    通过卡组列表生成卡组图片
    """
    card_ids = deck['deck']
    all_cards = get_cards()
    cards = {}
    for id in card_ids:
        if id in cards:
            cards[id]['num'] += 1
        else:
            card = all_cards[str(id)]
            cards[id] = {'num':1,'name':card['card_name'],'cost':card['cost']}
    n_card = len(cards)
    line = n_card//2 + 1
    if n_card%2 == 0:
        line -= 1 
    img = Image.new('RGB',(540,46*line),(255,255,255))
    draw = ImageDraw.Draw(img)
    count = 1
    for c in range(0,31):
        for i in cards:
            if cards[i]['cost'] == c:
                rol = count % 2
                if rol == 0:
                    rol = 2
                row = (count-1)//2 + 1
                lcard = Image.open(join(MOUDULE_PATH,f'img/L/{i}.jpg'))
                img.paste(lcard,((rol-1)*270,(row-1)*46))
                costimg = Image.open(join(MOUDULE_PATH,f'img/cost/{cards[i]["cost"]}.png'))
                img.paste(costimg,((rol-1)*270+10,(row-1)*46+10),costimg)
                draw.text(((rol-1)*270+50,(row-1)*46+23),cards[i]['name'],(255,255,255),font,'lm')
                draw.text(((rol)*270-10,(row-1)*46+23),f'x{cards[i]["num"]}',(255,255,255),font,'rm')
                count +=1
    img = img.convert('RGB')
    buf = BytesIO()
    img.save(buf, format='JPEG')
    base64_str = f'base64://{base64.b64encode(buf.getvalue()).decode()}'
    img = f'[CQ:image,file={base64_str}]'
    return img