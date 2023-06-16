from ..info import get_cards,MOUDULE_PATH
from os.path import join
from PIL import Image,ImageDraw,ImageFont
from io import BytesIO
import base64

font = ImageFont.truetype(join(MOUDULE_PATH,'font/font.ttf'),size = 15)

def draw_text_psd_style(draw, xy, text, font, tracking=0, leading=None, **kwargs):
    """
    usage: draw_text_psd_style(draw, (0, 0), "Test", 
                tracking=-0.1, leading=32, fill="Blue")

    Leading is measured from the baseline of one line of text to the
    baseline of the line above it. Baseline is the invisible line on which most
    letters—that is, those without descenders—sit. The default auto-leading
    option sets the leading at 120% of the type size (for example, 12‑point
    leading for 10‑point type).

    Tracking is measured in 1/1000 em, a unit of measure that is relative to 
    the current type size. In a 6 point font, 1 em equals 6 points; 
    in a 10 point font, 1 em equals 10 points. Tracking
    is strictly proportional to the current type size.
    """
    def stutter_chunk(lst, size, overlap=0, default=None):
        for i in range(0, len(lst), size - overlap):
            r = list(lst[i:i + size])
            while len(r) < size:
                r.append(default)
            yield r
    x, y = xy
    font_size = font.size
    lines = text.splitlines()
    if leading is None:
        leading = font.size * 1.2
    for line in lines:
        for a, b in stutter_chunk(line, 2, 1, ' '):
            w = font.getlength(a + b) - font.getlength(b)
            # dprint("[debug] kwargs")
            print("[debug] kwargs:{}".format(kwargs))
                
            draw.text((x, y), a, font=font, **kwargs)
            x += w + (tracking / 1000) * font_size
        y += leading
        x = xy[0]

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
                lcard = Image.open(join(MOUDULE_PATH,f'img/L/L_{i}.jpg'))
                img.paste(lcard,((rol-1)*270,(row-1)*46))
                costimg = Image.open(join(MOUDULE_PATH,f'img/cost/{cards[i]["cost"]}.png'))
                img.paste(costimg,((rol-1)*270+10,(row-1)*46+10),costimg)
                y = font.getsize(cards[i]['name'])[1]
                draw_text_psd_style(draw=draw,xy=((rol-1)*270+50,int((row-1)*46+23-y/2)),text=cards[i]['name'],font=font,tracking=-1000)
                draw.text(((rol)*270-10,(row-1)*46+23),f'x{cards[i]["num"]}',(255,255,255),font,'rm')
                count +=1
    img = img.convert('RGB')
    buf = BytesIO()
    img.save(buf, format='JPEG')
    base64_str = f'base64://{base64.b64encode(buf.getvalue()).decode()}'
    img = f'[CQ:image,file={base64_str}]'
    return img