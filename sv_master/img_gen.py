from PIL import Image,ImageDraw,ImageFont
from ..config import text_color
from ..info import MOUDULE_PATH,clan2w
import matplotlib.pyplot as plt
from os.path import join


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