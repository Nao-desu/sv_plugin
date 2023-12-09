from hoshino import Service
from hoshino.typing import MessageSegment as Seg
from ..info import get_lim,get_answer,get_cards,MOUDULE_PATH
from os.path import join
from .sv_voice_gess import guess_voice
from .sv_paint_guess import guess_paint
from ..config import GAME_TIME
from PIL import Image
from io import BytesIO
import asyncio,zhconv,base64,random
from xpinyin import Pinyin
p = Pinyin()

game_help = """
[sv猜卡面] 猜猜bot随机发送的卡面的一小部分来自哪张影之诗卡牌
[sv猜语音] 猜猜bot随机发送的语音来自哪张影之诗卡牌
回答时需要at机器人，回答卡牌名的前后缀均可
默认为指定模式卡牌
在指令后添加[无限]可以猜所有卡牌
在指令后添加[职业名]可以猜特定职业卡牌
注意：频道bot无法发送语音
"""
sv = Service('sv_games',help_=game_help)

class GM:
    def __init__(self):
        self.playing = {}
        self.answer = {}

    def is_playing(self, gid):
        return gid in self.playing

    def start_game(self, gid,answer):
        self.playing[gid] = answer
        a0 = get_cards()[str(answer)]["card_name"]
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

    def end_game(self,gid):
        if gid in self.playing:
            del self.playing[gid]
            del self.answer[gid]

gm = GM()

@sv.on_prefix('sv猜语音')
async def voice_guess(bot,ev):
    gid = ev.group_id
    try:
        if gm.is_playing(ev.group_id):
            await bot.send(ev, "游戏仍在进行中…")
            return
        lim = ev.message.extract_plain_text().strip()
        limited,clan = get_lim(lim)
        answer = await get_answer(limited,clan,'voice')
        gm.start_game(gid,answer)
        await guess_voice(bot,ev,limited,clan,answer)
        await asyncio.sleep(GAME_TIME)
        if gm.is_playing(ev.group_id):
            if gm.get_ans(gid) != answer:
                return
            img_path = join(MOUDULE_PATH,f"img\\full\\{answer}0.png")
            img = await change_img(img_path)
            gm.end_game(gid)
            await bot.send(ev, f"正确答案是:{get_cards()[str(answer)]['card_name']}{img}\n很遗憾,没有人答对")
        return
    except Exception as e:
        gm.end_game(gid)
        await bot.send(ev,f'游戏发生错误，自动终止\n{e}')

@sv.on_prefix('sv猜卡面')
async def paint_guess(bot,ev):
    gid = ev.group_id
    try:
        if gm.is_playing(ev.group_id):
            await bot.send(ev, "游戏仍在进行中…")
            return
        lim = ev.message.extract_plain_text().strip()
        limited,clan = get_lim(lim)
        answer = await get_answer(limited,clan,False)
        gm.start_game(gid,answer)
        await guess_paint(bot,ev,limited,clan,answer)
        await asyncio.sleep(GAME_TIME)
        if gm.is_playing(ev.group_id):
            if gm.get_ans(gid) != answer:
                return
            img_path = join(MOUDULE_PATH,f"img\\full\\{answer}0.png")
            img = await change_img(img_path)
            gm.end_game(gid)
            await bot.send(ev, f"正确答案是:{get_cards()[str(answer)]['card_name']}{img}\n很遗憾,没有人答对")
        return
    except Exception as e:
        gm.end_game(gid)
        await bot.send(ev,f'游戏发生错误，自动终止\n{e}')

@sv.on_message()
async def on_input_chara_name(bot, ev):
    gid = ev.group_id
    if  not gm.is_playing(gid):
        return
    answer = gm.get_ans(gid)
    if gm.check_ans(gid,zhconv.convert(ev.message.extract_plain_text(),'zh-tw')):
        gm.end_game(gid)
        img_path = join(MOUDULE_PATH,f"img\\full\\{answer}0.png")
        img = await change_img(img_path)
        msg = f"{Seg.at(ev.user_id)}猜对了，真厉害！\n正确答案是:{get_cards()[str(answer)]['card_name']}{img}"
        await bot.send(ev, msg)

@sv.on_fullmatch('重置游戏')
async def reset_games(bot,ev):
    gm.end_game(ev.group_id)
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
    img.convert('RGB')
    img.save(buf, format='jpeg')
    base64_str = f'base64://{base64.b64encode(buf.getvalue()).decode()}'
    return f'[CQ:image,file={base64_str}]'