from PIL import Image,ImageFont,ImageDraw
from io import BytesIO
from os.path import join
from ..info import text_split,card_set,clan2w,MOUDULE_PATH,get_textcolor_pos,get_related_cards,find_all_card
from ..config import clan_color,text_color
import base64
font = ImageFont.truetype(join(MOUDULE_PATH,'font/font.ttf'),size = 30)
def draw_rr(x,y,clan)-> Image:
    """
    绘制圆角矩形
    """
    square = Image.new("RGBA",(x+6,y+6),(255,255,255,0))
    draw = ImageDraw.Draw(square)
    draw.rounded_rectangle((3,3,x-3,y-3),15,(15,15,20),clan_color[clan],3)
    return square

def draw_text_mulcolour(draw:ImageDraw.ImageDraw,x:int,y:int,text:str,pos:list,is_follower:bool):
    """
    绘制不同颜色的字体
    """
    texts = text.split('\n')
    count = -3 if is_follower else 0
    for text in texts:
        _x = x
        for word in text:
            if count in pos:
                draw.text((_x,y),text=word,fill=(255,205,69),font=font)
            else:
                draw.text((_x,y),text=word,fill=text_color,font=font)
            _x += font.getsize(word)[0]
            count += 1
        y += font.getsize(text)[1]

def img_gen_1(card) -> Image:
    """
    绘制从者卡
    """
    skill = "進化前\n" + text_split(card["skill_disc"])
    eskill = "進化后\n" + text_split(card["evo_skill_disc"])
    des = text_split(card["description"])
    edes = text_split(card["evo_description"])
    cv = 'cv:' + card["cv"]
    card_info = '卡包:' + card_set[card["card_set_id"]] + '|類型:' + card["tribe_name"] + '|職業:' + clan2w[card["clan"]]
    y1 = font.getsize_multiline(des)[1]
    y2 = font.getsize_multiline(edes)[1]
    y3 = font.getsize_multiline(skill)[1]
    y4 = font.getsize_multiline(eskill)[1]
    xcv = font.getsize_multiline(cv)[0]
    id = card["card_id"]
    #绘制左侧
    left = Image.new("RGBA",(1100,810+y1+y2),(255,255,255,0))
    C_pic = Image.open(join(MOUDULE_PATH,f'img/C/C_{id}.png'))
    E_pic = Image.open(join(MOUDULE_PATH,f'img/E/E_{id}.png'))
    left.paste(C_pic,(0,0),C_pic)
    left.paste(E_pic,(560,0),E_pic)
    C_pic.close()
    E_pic.close()
    square = draw_rr(1100,90+y1+y2,card["clan"])
    left.paste(square,(0,720),square)
    square.close()
    ldraw = ImageDraw.Draw(left)
    ldraw.text((50,740),des,text_color,font)
    ldraw.text((50,790+y1),edes,text_color,font)
    ldraw.line([(45,765+y1),(1055,765+y1)],text_color,1)
    ldraw.text((1050-xcv,770+y1+y2),cv,text_color,font)
    #绘制右侧
    right = Image.new("RGBA",(1000,550+y3+y4),(255,255,255,0))
    square = draw_rr(1000,120,card["clan"])
    right.paste(square,(0,0),square)
    square.close()
    rdraw = ImageDraw.Draw(right)
    rdraw.text((500,30),card["card_name"],text_color,font,'mm')
    rdraw.line([(45,55),(955,55)],text_color,1)
    rdraw.text((500,75),card_info,text_color,font,'mm')
    square = draw_rr(1000,310+y3+y4,card["clan"])
    right.paste(square,(0,140),square)
    square.close()
    draw_text_mulcolour(rdraw,50,240,skill,get_textcolor_pos(card["org_skill_disc"]),True)
    draw_text_mulcolour(rdraw,50,350+y3,eskill,get_textcolor_pos(card["org_evo_skill_disc"]),True)
    rdraw.line([(45,295+y3),(955,295+y3)],text_color,1)
    bg = Image.open(join(MOUDULE_PATH,'img/bg/bg.jpg'))
    bg.paste(left,(30,30),left)
    bg.paste(right,(1170,30),right)
    ym = max(810+y1+y2,550+y3+y4)
    bg = bg.crop((0,0,2200,ym+80))
    bgdraw = ImageDraw.Draw(bg)
    x,y = bg.size
    bgdraw.text((x-300,y-100),f'id:{id}\ncode by Nao-desu\ngenerate by ddbot',text_color,font)
    return bg

def img_gen_2(card) -> Image:
    """
    绘制法术卡
    """
    skill = text_split(card["skill_disc"])
    des = text_split(card["description"])
    cv = 'cv:' + card["cv"]
    card_info = '卡包:' + card_set[card["card_set_id"]] + '|類型:' + card["tribe_name"] + '|職業:' + clan2w[card["clan"]]
    y1 = font.getsize_multiline(skill)[1]
    y2 = font.getsize_multiline(des)[1]
    xcv = font.getsize_multiline(cv)[0]
    id = card["card_id"]
    #绘制左侧
    left = Image.new("RGBA",(540,700),(255,255,255,0))
    C_pic = Image.open(join(MOUDULE_PATH,f'img/C/C_{id}.png'))
    left.paste(C_pic,(0,0),C_pic)
    C_pic.close()
    #绘制右侧
    right = Image.new("RGBA",(1000,350+y1+y2),(255,255,255,0))
    square = draw_rr(1000,120,card["clan"])
    right.paste(square,(0,0),square)
    square.close()
    rdraw = ImageDraw.Draw(right)
    rdraw.text((500,30),card["card_name"],text_color,font,'mm')
    rdraw.line([(45,55),(955,55)],text_color,1)
    rdraw.text((500,75),card_info,text_color,font,'mm')
    square = draw_rr(1000,210+y1+y2,card["clan"])
    right.paste(square,(0,140),square)
    square.close()
    draw_text_mulcolour(rdraw,50,190,skill,get_textcolor_pos(card["org_skill_disc"]),False)
    rdraw.text((50,300+y1),des,text_color,font)    
    rdraw.text((950-xcv,510+y1+y2),cv,text_color,font)
    rdraw.line([(45,245+y1),(955,245+y1)],text_color,1)
    bg = Image.open(join(MOUDULE_PATH,'img/bg/bg2.jpg'))
    bg.paste(left,(30,30),left)
    bg.paste(right,(610,30),right)
    ym = max(700,450+y1+y2)
    bg = bg.crop((0,0,1640,ym+30))
    bgdraw = ImageDraw.Draw(bg)
    x,y = bg.size
    bgdraw.text((x-300,y-100),f'id:{id}\ncode by Nao-desu\ngenerate by ddbot',text_color,font)
    return bg

async def card_img_gen(card:dict) -> str:
    """
    通过卡牌信息生成图片
    返回图片的cq码
    """
    if card["char_type"] == 1:
        img = img_gen_1(card)
    else:
        img = img_gen_2(card)
    img = img.convert('RGB')
    buf = BytesIO()
    img.save(buf, format='JPEG')
    base64_str = f'base64://{base64.b64encode(buf.getvalue()).decode()}'
    msg = f'[CQ:image,file={base64_str}]'
    related = get_related_cards(card)
    if related:
        msg += '关联卡牌：\n'
        for i in related:
            if i["char_type"] == 1:
                img = img_gen_1(i)
            else:
                img = img_gen_2(i)
            img = img.convert('RGB')
            buf = BytesIO()
            img.save(buf, format='JPEG')
            base64_str = f'base64://{base64.b64encode(buf.getvalue()).decode()}'
            msg += f'[CQ:image,file={base64_str}]'
    diff_card = find_all_card(card["card_id"])
    if diff_card:
        msg += '\n※此卡牌存在其他卡面：'
        for id in diff_card:
            msg += '\n  id:' + id
    return msg

async def cardlist_img_gen(cards:list) -> str:
    """
    通过卡牌列表，返回图片cq码
    """
    img = Image.open(join(MOUDULE_PATH,'img/bg/bg3.png'))
    card_num = len(cards)
    line = card_num//4
    if card_num % 4 ==0:
        line -= 1
    draw = ImageDraw.Draw(img)
    count = 0
    for i in range(0,line+1):
        for j in range(0,4):
            if j+i*4 == card_num:
                break
            card = cards[j+i*4]['card']
            score = cards[j+i*4]['score']
            id = card['card_id']
            name = card['card_name']
            text = f'id:{id}|匹配度:{score}'
            C_img = Image.open(join(MOUDULE_PATH,f'img/C/C_{id}.png'))
            img.paste(C_img,(30+j*570,30+i*800),C_img)
            count +=1
            draw.text((300+j*570,740+i*800),name,(0,0,0),font,'mm')
            draw.text((300+j*570,770+i*800),text,(0,0,0),font,'mm')
        if j+i*4 == card_num:
            break
    img = img.crop((0,0,2310,860+800*line))
    img = img.convert('RGB')
    buf = BytesIO()
    img.save(buf, format='JPEG')
    base64_str = f'base64://{base64.b64encode(buf.getvalue()).decode()}'
    img = f'[CQ:image,file={base64_str}]'
    return img