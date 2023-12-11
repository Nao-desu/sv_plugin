from PIL import Image,ImageDraw,ImageFont
from ..config import text_color
from ..info import MOUDULE_PATH,clan2w,get_cards,get_deck_name,en_clan
from os.path import join
from ..sv_qrcr import deck_img_gen

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
    img = Image.new('RGB',(1080,92*line),(255,255,255))
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
                costimg = costimg.resize((540, int(costimg.size[1] * 540 / costimg.size[0])))
                img.paste(costimg,((rol-1)*540+20,(row-1)*92+20),costimg)
                y = font.getsize(cards[i]['name'])[1]
                draw_text_psd_style(draw=draw,xy=((rol-1)*540+90,int((row-1)*92+46-y/2)),text=cards[i]['name'],font=font,tracking=-60)
                draw.text(((rol)*540-20,(row-1)*92+46),f'x{cards[i]["num"]}',(255,255,255),font,'rm')
                count +=1
    return img

async def get_round_pic(name):
    pic = Image.open((MOUDULE_PATH,'img','deck',f'{name}.jpg'))
    mask = Image.new("RGBA", (200, 200), (0, 0, 0, 0))
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, 200, 200), fill=(255, 255, 255, 100))
    pic.paste(mask, (0, 0), mask)
    return pic

async def deck_img(deck:dict):
    img = await deck_img_gen(deck["cards"])
    x,y = img.size 
    pic = Image.new("RGB",(x+40,y+280))
    draw = ImageDraw.Draw(pic)
    deck_name_dict = get_deck_name()
    font1 = ImageFont.truetype(join(MOUDULE_PATH,'font/font2.ttc'),size = 70)
    font2 = ImageFont.truetype(join(MOUDULE_PATH,'font/font2.ttc'),size = 30)
    if deck["deck_name"] in deck_name_dict:
        deck_name = deck["deck_name"]
    else:
        deck_name = 'other_' + en_clan[deck["clan"]]
    head_img = await get_round_pic(deck_name)
    pic.paste(head_img,(20,20),head_img)
    draw.text((240,20),deck_name_dict[deck_name][0],text_color,font1)
    if type(deck['wins']) == int:
        draw.text((240,110),f"{deck['auther']}|{deck['wins']}|{deck['creat_time']}",text_color,font2)
    else:
        draw.text((240,110),f"{deck['auther']}|JCG winner",text_color,font2)
    draw.text((240,160),f"from{deck['from']}",(150,150,150),font2)
    pic.paste(img,(20,230),img)
    draw.text((int(x/2+20),y+250),f"Code by Nao-desu & Data by shadowversemaster.com & Created by koharu",(150,150,150),font2)
    return pic