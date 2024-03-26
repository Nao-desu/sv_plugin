from PIL import Image,ImageDraw,ImageFont
from ..config import text_color
from ..info import MOUDULE_PATH,clan2w,get_cards,get_deck_trans,en_clan,get_deck_name,idToHash
from os.path import join
from ..config import clan_color
import qrcode

async def qr_img_gen(deck:list,flag,clan:int):
    qr = qrcode.QRCode(
    version=5,  # 二维码的大小，取值1-40
    box_size=1, # 二维码最小正方形的像素数量
    error_correction=qrcode.constants.ERROR_CORRECT_H, # 二维码的纠错等级
    border=2 # 白色边框的大小
    )
    if flag:
        url = "https://shadowverse-portal.com/deck/3."
    else:
        url = "https://shadowverse-portal.com/deck/1."
    url += f'{clan}'
    for i in deck:
        url += f'.{idToHash(i)}'
    url += '?lang=ja'
    qr.add_data(url)
    return qr.make_image()

async def daily_ratings_img(time:str,data:dict):
    img = Image.new("RGBA",(1250,1460),(0,0,0))
    x,y = 1210,1260
    square = Image.new("RGBA",(x+6,y+6),(255,255,255,0))
    draw = ImageDraw.Draw(square)
    draw.rounded_rectangle((0,0,x,y),15,(0,0,0,0),(200,200,200),1)
    img.paste(square,(20,150),square)
    draw = ImageDraw.Draw(img)
    for i in range(1,9):
        draw.line([(20,150+140*i),(1230,150+140*i)],(200,200,200),1)
    draw.line([(430,150),(430,1410)],(200,200,200),1)
    draw.line([(830,150),(830,1410)],(200,200,200),1)
    font1 = ImageFont.truetype(join(MOUDULE_PATH,'font/font2.ttc'),size = 70)
    font2 = ImageFont.truetype(join(MOUDULE_PATH,'font/font2.ttc'),size = 30)
    font3 = ImageFont.truetype(join(MOUDULE_PATH,'font/font2.ttc'),size = 50)
    font4 = ImageFont.truetype(join(MOUDULE_PATH,'font/font2.ttc'),size = 20)
    draw.text((20,10),'Ratings最新数据',text_color,font1)
    draw.text((20,100),f'最后统计日期 ({time})',text_color,font2)
    draw.text((50,220),'职业',text_color,font3,'lm')
    draw.text((450,220),'胜率',text_color,font3,'lm')
    draw.text((850,220),'使用率',text_color,font3,'lm')
    draw.text((635,1430),'Code by Nao-desu & Data by shadowversemaster.com & Created by koharu',(200,200,200),font4,'mm')
    for i in range(1,9):
        pic = Image.open(join(MOUDULE_PATH,f'img/clan/r_{i}.png'))
        img.paste(pic,(30,170+i*140),pic)
        draw.text((140,220+140*i),clan2w[i],text_color,font3,'lm')
        if data[str(i)][0] > 50:
            color = (127,255,0)
        elif data[str(i)][0] < 50:
            color = (255,0,0)
        else:
            color = text_color
        draw.text((450,220+140*i),f'{data[str(i)][0]}%',color,font3,'lm')
        draw.text((850,220+140*i),f'{data[str(i)][1]}%',text_color,font3,'lm')
    return img

async def ten_ratings_img(data:dict):
    img = Image.new("RGBA",(1120,880),(0,0,0))
    x,y = 1080,680
    square = Image.new("RGBA",(x+6,y+6),(255,255,255,0))
    draw = ImageDraw.Draw(square)
    draw.rounded_rectangle((0,0,x,y),10,(0,0,0,0),(200,200,200),2)
    img.paste(square,(20,150),square)
    draw = ImageDraw.Draw(img)
    for i in range(0,10):
        draw.line([(20,230+60*i),(1100,230+60*i)],(200,200,200),2)
    for i in range(0,8):
        draw.line([(140+120*i,150),(140+120*i,830)],(200,200,200),2)
        draw.line([(200+120*i,230),(200+120*i,830)],(200,200,200),1)
    time = list(data.keys())[:10]
    font1 = ImageFont.truetype(join(MOUDULE_PATH,'font/font2.ttc'),size = 25)
    font2 = ImageFont.truetype(join(MOUDULE_PATH,'font/font2.ttc'),size = 70)
    font3 = ImageFont.truetype(join(MOUDULE_PATH,'font/font2.ttc'),size = 30)
    font4 = ImageFont.truetype(join(MOUDULE_PATH,'font/font2.ttc'),size = 20)
    draw.text((20,10),'近10日Ratings数据',text_color,font2)
    draw.text((20,100),f'最后统计日期 ({time[0]}),表格中左侧为胜率,右侧为使用率',text_color,font3)
    draw.text((560,855),'Code by Nao-desu & Data by shadowversemaster.com & Created by koharu',(200,200,200),font4,'mm')
    y0 = 260
    for i in time:
        draw.text((80,y0),i[5:].replace('-','/'),text_color,font1,'mm')
        y0 += 60
    for i in range(1,9):
        pic = Image.open(join(MOUDULE_PATH,f'img/clan/{i}.png'))
        img.paste(pic,(50+120*i,160),pic)
        y0 = 260
        try:
            for j in time:          
                if data[j][str(i)][0] > 50:
                    color = (127,255,0)
                elif data[j][str(i)][0] < 50:
                    color = (255,0,0)
                else:
                    color = text_color
                draw.text((50+120*i,y0),str(data[j][str(i)][0]),color,font1,'mm')
                draw.text((110+120*i,y0),str(data[j][str(i)][1]),text_color,font1,'mm')
                y0+=60
        except:pass
    return img

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
    card_ids = deck['cards']
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
    img = Image.new('RGB',(1080,92*line),(0,0,0))
    draw = ImageDraw.Draw(img)
    count = 1
    font = ImageFont.truetype(join(MOUDULE_PATH,'font/font.ttf'),size = 30)
    for c in range(0,31):
        for i in cards:
            if cards[i]['cost'] == c:
                rol = count % 2
                if rol == 0:
                    rol = 2
                row = (count-1)//2 + 1
                lcard = Image.open(join(MOUDULE_PATH,f'img/L/L_{i}.jpg'))
                lcard = lcard.resize((540, int(lcard.size[1] * 540 / lcard.size[0])))
                img.paste(lcard,((rol-1)*540,(row-1)*92))
                costimg = Image.open(join(MOUDULE_PATH,f'img/cost/{cards[i]["cost"]}.png'))
                costimg = costimg.resize((60,60))
                img.paste(costimg,((rol-1)*540+20,(row-1)*92+20),costimg)
                y = font.getsize(cards[i]['name'])[1]
                draw_text_psd_style(draw=draw,xy=((rol-1)*540+90,int((row-1)*92+46-y/2)),text=cards[i]['name'],font=font,tracking=-60)
                draw.text(((rol)*540-20,(row-1)*92+46),f'x{cards[i]["num"]}',(255,255,255),font,'rm')
                count +=1
    return img

async def deck_img(deck:dict,flag):
    try:
        img = await deck_img_gen(deck)
        x,y = img.size 
        pic = Image.new("RGB",(x+40,y+280),(0,0,0))
        draw = ImageDraw.Draw(pic)
        deck_name_dict = await get_deck_trans()
        font1 = ImageFont.truetype(join(MOUDULE_PATH,'font/font2.ttc'),size = 70)
        font2 = ImageFont.truetype(join(MOUDULE_PATH,'font/font2.ttc'),size = 25)
        font3 = ImageFont.truetype(join(MOUDULE_PATH,'font/font2.ttc'),size = 20)
        if deck["deck_name"] in deck_name_dict:
            deck_name = deck["deck_name"]
        else:
            deck_name = 'other_' + en_clan[deck["clan"]]
        if flag:
            pic0 = Image.open(join(MOUDULE_PATH,'img','deck',f'l_{deck_name}.jpg'))
        else:
            pic0 = Image.open(join(MOUDULE_PATH,'img','deck',f'r_{deck_name}.jpg'))
        mask = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
        draw2 = ImageDraw.Draw(mask)
        draw2.ellipse((0, 0, 200, 200), fill=(255, 255, 255, 225))
        draw.ellipse((17, 17, 223, 223), fill=clan_color[int(deck['clan'])])
        pic.paste(pic0,(20,20),mask)
        draw.text((240,20),deck_name_dict[deck_name][0],text_color,font1)
        if type(deck['wins']) == int:
            if deck['wins'] != 0:
                draw.text((240,110),f"{deck['auther']} | {deck['wins']}连胜 | {deck['creat_time']}",text_color,font2)
            else:
                draw.text((240,110),f"{deck['auther']} | {deck['creat_time']}",text_color,font2)
        else:
            draw.text((240,110),f"{deck['auther']} | {deck['wins']} | {deck['creat_time']}",text_color,font2)
        if len(deck['from']) < 35:
            fr = deck['from']
        else:fr = deck['from'][:35] +'...'
        draw.text((240,160),f"from:{fr}",(150,150,150),font2)
        pic.paste(img,(20,230))
        draw.text((int(x/2+20),y+250),f"Code by Nao-desu & Data by shadowversemaster.com & Created by koharu",(150,150,150),font3,'mm')
        qr_img = await qr_img_gen(deck['cards'],flag,deck['clan'])
        qr_img = qr_img.resize((200,200))
        pic.paste(qr_img,(900,10),qr_img)
    except:pass
    return pic

async def all_deck_list_img(flag):
    try:
        decklist = await get_deck_name(flag)
        for i in list(decklist.keys()):
            if not decklist[i]:
                del decklist[i]
        font1 = ImageFont.truetype(join(MOUDULE_PATH,'font/font2.ttc'),size = 70)
        font2 = ImageFont.truetype(join(MOUDULE_PATH,'font/font2.ttc'),size = 30)
        font3 = ImageFont.truetype(join(MOUDULE_PATH,'font/font2.ttc'),size = 20)
        rol = len(decklist) // 5 +1
        if len(decklist) % 5 == 0:
            rol -= 1
        img = Image.new('RGB',(1160,150+250*rol))
        deck_name = list(decklist.keys())
        draw = ImageDraw.Draw(img)
        if flag == 'r':
            draw.text((20,10),'指定卡组列表',text_color,font1)
        else:
            draw.text((20,10),'无限卡组列表',text_color,font1)
        draw.text((580,120+250*rol),f"Code by Nao-desu & Data by shadowversemaster.com & Created by koharu",(150,150,150),font3,'mm')
        for i in range(0,len(decklist)):
            name = deck_name[i]
            cn_name_list = await get_deck_trans()
            cn_name = cn_name_list[name][0]
            if flag == 'r':
                pic=Image.open(join(MOUDULE_PATH,'img','deck',f'r_{name}.jpg'))
            else:
                pic=Image.open(join(MOUDULE_PATH,'img','deck',f'l_{name}.jpg'))
            img.paste(pic,(20+230*(i%5),100+(i//5)*250))
            draw.text((120+230*(i%5),325+(i//5)*250),f'{cn_name}({decklist[name]})',text_color,font2,'mm')
    except:pass
    return img