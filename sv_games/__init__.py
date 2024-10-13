from hoshino import Service
from ..info import get_lim,get_answer,get_cards,MOUDULE_PATH,clan2w,get_condition,card_set,skill2w
from os.path import join,exists
from .sv_voice_gess import guess_voice
from .sv_paint_guess import guess_paint
from ..config import GAME_TIME
from PIL import Image
from io import BytesIO
import asyncio,zhconv,random
from xpinyin import Pinyin
from hoshino.image_host import upload_img
from uuid import uuid4
from .database import db
from ...groupmaster.switch import sdb
from hoshino.MD import *

p = Pinyin()

game_help = """
[sv猜卡面] 猜猜bot随机发送的卡面的一小部分来自哪张影之诗卡牌
[sv猜语音] 猜猜bot随机发送的语音来自哪张影之诗卡牌
回答时需要at机器人，回答卡牌名的前后缀均可
默认为指定模式卡牌
在指令后添加[无限]可以猜所有卡牌
在指令后添加[职业名]可以猜特定职业卡牌
支持的回答方式（以殘酷的媚貓‧帷为例）
[殘酷的媚貓‧帷][殘酷的媚貓][帷][殘酷的媚貓帷][213]
"""
sv = Service('sv_games',help_=game_help)

class GM:
    def __init__(self):
        self.playing = {}
        self.answer = {}
        self.answerpic = {}
        self.msg_id = {}

    def is_playing(self, gid):
        return gid in self.playing

    def start_game(self, gid,answer):
        self.playing[gid] = answer
        card = get_cards()[str(answer)]
        a0 = card["card_name"]
        a1 = [p.get_pinyin(text) for text in a0.split('‧')]
        a2 = a0.strip('詠唱：')
        a3 = ''.join(a1)
        self.answer[gid] = a1
        if a0 not in self.answer[gid]:
            self.answer[gid].append(a0)
        if a2 not in self.answer[gid]:
            self.answer[gid].append(a0)
        if a3 not in self.answer[gid]:
            self.answer[gid].append(a0)
        if card["char_type"] == 1:
            self.answer[gid].append(f'{card["cost"]}{card["atk"]}{card["life"]}')
        return

    def get_ans(self,gid):
        if gid in self.playing:
            return self.playing[gid]
        else:
            return None

    def check_ans(self,gid,text):
        if gid in self.playing:
            if p.get_pinyin(text) in self.answer[gid]:
                return True
        return False

    def add_pic(self,gid,url,size):
        self.answerpic[gid] = (url,size)

    def add_msg_id(self,gid,msg_id):
        if gid not in self.msg_id:
            self.msg_id[gid] = [msg_id]
        else:
            self.msg_id[gid].append(msg_id)

    def get_msg_id(self,gid):
        if gid in self.msg_id:
            return self.msg_id[gid]
        else:
            return None

    async def end_game(self,bot,ev,gid):
        if gid in self.playing:
            del self.playing[gid]
            del self.answer[gid]
            del self.answerpic[gid]
            for i in gm.get_msg_id(gid):            
                await bot.delete_msg(self_id=ev.self_id,group_id=gid,message_id=i)
            del self.msg_id[gid]
    
    def get_pic(self,gid):
        if gid in self.answerpic:
            return self.answerpic[gid]
        else:
            return (None,None)

gm = GM()

async def get_hint(card,clan):
    hint = {}
    if clan != None:
        hint['职业'] = clan2w[clan]
    hint['费用'] = card ['cost']
    hint['稀有度'] = get_condition()["rarity"][str(card['rarity'])][2]
    hint['所属卡包'] = card_set[card['card_set_id']]
    if card["cv"] != "-":
        hint['CV'] = card['cv']
    if card['tribe_name'] != "-":
        hint['类型'] = card['tribe_name']
    skill = []
    s = card['skill'].split(',')
    for i in s:
        ss = i.split(':')
        for j in ss:
            if j.split('@')[0] not in skill:
                skill.append(j.split('@')[0])
    if skill:
        hint['能力'] = []
        for i in skill:
            if i in skill2w:
                hint['能力'].append(skill2w[i])
    return hint

async def give_hint(hint:dict,bot,ev,n):
    #提高能力出现概率
    if '能力' in hint and random.randint(1,3) == 1:
        key = '能力'
    else:key = random.choice(list(hint.keys()))
    value = hint[key]
    if type(value) == list:
        value = random.choice(value)
    if n <=2:
        data = [f'提示{n}',f'这张卡牌的{key}是：{value}  \r',f'{int(GAME_TIME/4)}秒后有新的提示']
    else:
        data = [f'提示{n}',f'这张卡牌的{key}是：{value}  \r',f'{int(GAME_TIME/4)}秒后公布答案']
    button = [[button_gen('我要回答',' ',style=4),button_gen('帮助','https://www.koharu.cn/docs/shadowverse/shadowverse.html#%E7%8C%9C%E5%8D%A1%E6%B8%B8%E6%88%8F',style = 0,type_int=0)]]
    button = generate_buttons(button)
    msg = generate_md(3,data,button)
    _send = await bot.send(ev,msg)
    gm.add_msg_id(ev.group_id,_send['message_id'])
    if key != '能力':
        del hint[key]
    else:
        if len(hint['能力']) == 1:
            del hint['能力']
        else:
            hint['能力'].remove(value)
    return hint

@sv.on_prefix('sv猜语音')
async def voice_guess(bot,ev):
    if ev.real_message_type == 'guild':
        return
    status = sdb.get_status(ev.real_group_id,'sv猜卡')
    if not status:
        return
    gid = ev.group_id
    try:
        if gm.is_playing(ev.group_id):
            _send = await bot.send(ev, "游戏仍在进行中…")
            gm.add_msg_id(ev.group_id,_send['message_id'])
            return
        lim = ev.message.extract_plain_text().strip()
        limited,clan = get_lim(lim)
        answer = await get_answer(limited,clan,'voice')
        gm.start_game(gid,answer)
        id1,id2 = await guess_voice(bot,ev,limited,clan,answer)
        gm.add_msg_id(gid,id1)
        gm.add_msg_id(gid,id2)
        if exists(join(MOUDULE_PATH,f"img\\full\\{answer}0.jpg")):
            img_path = join(MOUDULE_PATH,f"img\\full\\{answer}0.jpg")
        else:
            img_path = join(MOUDULE_PATH,f"img\\full\\{answer}0.png")
        url,size = await change_img(img_path)
        gm.add_pic(gid,url,size)
        card = get_cards()[str(answer)]
        hint = await get_hint(card,clan)
        sleep_time = GAME_TIME/4
        n = 1
        while n<4:
            await asyncio.sleep(sleep_time)
            if gm.is_playing(ev.group_id):
                if gm.get_ans(gid) != answer:
                    return
            else:return
            hint = await give_hint(hint,bot,ev,n)
            n += 1
        await asyncio.sleep(sleep_time)
        if gm.is_playing(ev.group_id):
            if gm.get_ans(gid) != answer:
                return
            await gm.end_game(bot,ev,gid)
            button = [[button_gen("猜卡面","sv猜卡面"),button_gen("猜语音","sv猜语音"),button_gen("这是什么卡？",f"svcard {answer}"),button_gen("帮助","https://www.koharu.cn/docs/shadowverse/shadowverse.html#%E7%8C%9C%E5%8D%A1%E6%B8%B8%E6%88%8F",type_int=0)]]
            if ev.real_message_type == 'group':
                button.append([button_gen("排行榜","sv排行榜"),button_gen("总排行","sv总排行")])
            button = generate_buttons(button)
            data = [f"正确答案是:{get_cards()[str(answer)]['card_name']}",f"img#{size[0]}px #{size[1]}px",url,"很遗憾,没有人答对","图片数据来自SVGDB"]
            msg = generate_md(2,data,button)
            await bot.send(ev,msg)
        return
    except Exception as e:
        await gm.end_game(bot,ev,gid)
        await bot.send(ev,f'游戏发生错误，自动终止\n{e}')

@sv.on_prefix('sv猜卡面')
async def paint_guess(bot,ev):
    status = sdb.get_status(ev.real_group_id,'sv猜卡')
    if not status:
        return
    gid = ev.group_id
    try:
        if gm.is_playing(ev.group_id):
            _send = await bot.send(ev, "游戏仍在进行中…")
            gm.add_msg_id(ev.group_id,_send['message_id'])
            return
        lim = ev.message.extract_plain_text().strip()
        limited,clan = get_lim(lim)
        answer = await get_answer(limited,clan,False)
        gm.start_game(gid,answer)
        id1,id2 = await guess_paint(bot,ev,limited,clan,answer)
        gm.add_msg_id(gid,id1)
        gm.add_msg_id(gid,id2)
        if exists(join(MOUDULE_PATH,f"img\\full\\{answer}0.jpg")):
            img_path = join(MOUDULE_PATH,f"img\\full\\{answer}0.jpg")
        else:
            img_path = join(MOUDULE_PATH,f"img\\full\\{answer}0.png")
        url,size = await change_img(img_path)
        gm.add_pic(gid,url,size)
        card = get_cards()[str(answer)]
        hint = await get_hint(card,clan)
        sleep_time = GAME_TIME/4
        n = 1
        while n<4:
            await asyncio.sleep(sleep_time)
            if gm.is_playing(ev.group_id):
                if gm.get_ans(gid) != answer:
                    return
            else:return
            hint = await give_hint(hint,bot,ev,n)
            n += 1
        await asyncio.sleep(sleep_time)
        if gm.is_playing(ev.group_id):
            if gm.get_ans(gid) != answer:
                return
            await gm.end_game(bot,ev,gid)
            button = [[button_gen("猜语音","sv猜语音"),button_gen("猜卡面","sv猜卡面"),button_gen("这是什么卡？",f"svcard {answer}"),button_gen("帮助","https://www.koharu.cn/docs/shadowverse/shadowverse.html#%E7%8C%9C%E5%8D%A1%E6%B8%B8%E6%88%8F",type_int=0)]]
            if ev.real_message_type == 'group':
                button.append([button_gen("排行榜","sv排行榜"),button_gen("总排行","sv总排行")])
            button = generate_buttons(button)
            data = [f"正确答案是:{get_cards()[str(answer)]['card_name']}",f"img#{size[0]}px #{size[1]}px",url,"很遗憾,没有人答对","图片数据来自SVGDB"]
            msg = generate_md(2,data,button)
            await bot.send(ev,msg)
        return
    except Exception as e:
        await gm.end_game(bot,ev,gid)
        await bot.send(ev,f'游戏发生错误，自动终止\n{e}')

@sv.on_message()
async def on_input_chara_name(bot, ev):
    status = sdb.get_status(ev.real_group_id,'sv猜卡')
    if not status:
        return
    gid = ev.group_id
    if  not gm.is_playing(gid):
        return
    answer = gm.get_ans(gid)
    if gm.check_ans(gid,zhconv.convert(ev.message.extract_plain_text(),'zh-tw')):
        url,size = gm.get_pic(gid)
        await gm.end_game(bot,ev,gid)
        if exists(join(MOUDULE_PATH,f"img\\full\\{answer}0.jpg")):
            img_path = join(MOUDULE_PATH,f"img\\full\\{answer}0.jpg")
        else:
            img_path = join(MOUDULE_PATH,f"img\\full\\{answer}0.png")
        if not url:
            url,size = await change_img(img_path)
        button = [[button_gen("猜卡面","sv猜卡面"),button_gen("猜语音","sv猜语音"),button_gen("这是什么卡？",f"svcard {answer}"),button_gen("帮助","https://www.koharu.cn/docs/shadowverse/shadowverse.html#%E7%8C%9C%E5%8D%A1%E6%B8%B8%E6%88%8F",type_int=0)]]
        if ev.real_message_type == 'group':
            button.append([button_gen("排行榜","sv排行榜"),button_gen("总排行","sv总排行")])
        button = generate_buttons(button)
        data = [f"<@{ev.real_user_id}>猜对了，真厉害！",f"img#{size[0]}px #{size[1]}px",url,f"正确答案是:{get_cards()[str(answer)]['card_name']}","图片数据来自SVGDB"]
        msg = generate_md(2,data,button)
        await bot.send(ev, msg)
        db.add_record(ev.real_user_id,ev.real_group_id)

@sv.on_fullmatch('重置游戏')
async def reset_games(bot,ev):
    status = sdb.get_status(ev.real_group_id,'sv猜卡')
    if not status:
        return
    await gm.end_game(bot,ev,ev.group_id)
    await bot.send(ev,'已重置')

async def change_img(path:str):
    """
    图片防吞
    """
    # 读取图片并转换为numpy数组
    img = Image.open(path)
    # 获取图片大小
    width, height = img.size
    # 获取一个可修改的像素对象
    pix = img.load()
    # 生成一个随机的坐标
    x = random.randint(0, width - 1)
    y = random.randint(0, height - 1)
    # 生成一个随机的颜色值（RGB）
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    # 修改该坐标处的像素值
    pix[x, y] = (r, g, b,100)
    buf = BytesIO()
    img = img.convert('RGB')
    img.save(buf, format='jpeg')
    url = await upload_img(buf)
    return url,(width,height)

@sv.on_fullmatch('sv排行榜')
async def rank(bot,ev):
    if ev.real_message_type != 'group':
        return
    status = sdb.get_status(ev.real_group_id,'sv猜卡')
    if not status:
        return
    records = await db.get_records_and_rankings(ev.real_group_id)
    button = [[button_gen("猜卡面","sv猜卡面"),button_gen("猜语音","sv猜语音"),button_gen("帮助","https://www.koharu.cn/docs/shadowverse/shadowverse.html#%E7%8C%9C%E5%8D%A1%E6%B8%B8%E6%88%8F",type_int=0)]]
    if ev.real_message_type == 'group':
        button.append([button_gen("排行榜","sv排行榜"),button_gen("总排行","sv总排行")])
    button = generate_buttons(button)
    if not records:
        msg = generate_md(3,["暂无排行榜","此群还没有人答对过问题  \r","点击下方按钮参与游戏吧！"],button)
        await bot.finish(ev,msg)
    else:
        for i in records:
            if i[0] == ev.real_user_id:
                num = i[1]
                rank = i[2]
                msg = generate_md(3,[f"<@{ev.real_user_id}>,你已经答对了{num}次，群排名第{rank}！",f"此群共有{len(records)}人参与游戏  \r", "群排名(最多显示10名)  \r"+"  \r".join([f"{i[2]}:<@{i[0]}> 答对{i[1]}次" for i in records[:10]])],button)
                await bot.send(ev,msg)
                return
        msg = generate_md(3,[f"<@{ev.real_user_id}>,你还没有答对过问题",f"此群共有{len(records)}人参与游戏  \r", "群排名(最多显示10名)  \r"+"  \r".join([f"{i[2]}:<@{i[0]}> 答对{i[1]}次" for i in records[:10]])],button)
        await bot.send(ev,msg)

@sv.on_fullmatch('sv总排行')
async def total_rank(bot,ev):
    if ev.real_message_type != 'group':
        return
    status = sdb.get_status(ev.real_group_id,'sv猜卡')
    if not status:
        return
    records = await db.get_total_records_and_rankings()
    button = [[button_gen("猜卡面","sv猜卡面"),button_gen("猜语音","sv猜语音"),button_gen("帮助","https://www.koharu.cn/docs/shadowverse/shadowverse.html#%E7%8C%9C%E5%8D%A1%E6%B8%B8%E6%88%8F",type_int=0)]]
    if ev.real_message_type == 'group':
        button.append([button_gen("排行榜","sv排行榜"),button_gen("总排行","sv总排行")])
    button = generate_buttons(button)
    if not records:
        msg = generate_md(3,["暂无总排行","还没有人答对过问题  \r","点击下方按钮参与游戏吧！"],button)
        await bot.finish(ev,msg)
    else:
        for i in records:
            if i[0] == ev.real_user_id:
                num = i[1]
                rank = i[2]
                msg = generate_md(3,[f"<@{ev.real_user_id}>,你已经答对了{num}次，排名第{rank}！",f"共有{len(records)}人参与游戏  \r", "总排名(最多显示20名)  \r"+"  \r".join([f"{i[2]}:<@{i[0]}> 答对{i[1]}次" for i in records[:20]])],button)
                await bot.send(ev,msg)
                return
        msg = generate_md(3,[f"<@{ev.real_user_id}>,你还没有答对过问题",f"共有{len(records)}人参与游戏  \r", "总排名(最多显示20名)  \r"+"  \r".join([f"{i[2]}:<@{i[0]}> 答对{i[1]}次" for i in records[:20]])],button)
        await bot.send(ev,msg)