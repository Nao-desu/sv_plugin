from hoshino import Service
from hoshino.typing import MessageSegment as Seg
from ..info import get_lim,get_answer,get_cards,MOUDULE_PATH
from os.path import join,abspath
from .sv_voice_gess import guess_voice
from .sv_paint_guess import guess_paint
from ..config import GAME_TIME
from PIL import Image
from io import BytesIO
import asyncio,zhconv,base64
import numpy as np

sv_help = """
[sv猜卡面] 猜猜bot随机发送的卡面的一小部分来自哪张影之诗卡牌
[sv猜语音] 猜猜bot随机发送的语音来自哪张影之诗卡牌
默认为指定模式卡牌
在指令后添加‘无限’可以猜所有卡牌
在指令后添加职业名可以猜特定职业卡牌
"""
sv = Service('sv_games',help_=sv_help)

class GM:
    def __init__(self):
        self.playing = {}
        self.answer = {}

    def is_playing(self, gid):
        return gid in self.playing

    def start_game(self, gid,answer):
        self.playing[gid] = answer
        self.answer[gid] = get_cards()[str(answer)]["card_name"].split('‧')
        return

    def get_ans(self,gid):
        if gid in self.playing:
            return self.playing[gid]
        else:
            return None

    def check_ans(self,gid,text):
        if gid in self.playing:
            if text in self.answer[gid]:
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
            await bot.send(ev, f"正确答案是:{get_cards()[str(answer)]['card_name']}\n{img}\n很遗憾,没有人答对")
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
            await bot.send(ev, f"正确答案是:{get_cards()[str(answer)]['card_name']}\n{img}\n很遗憾,没有人答对")
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
        msg = f"正确答案是:{get_cards()[str(answer)]['card_name']}\n{img}\n{Seg.at(ev.user_id)}猜对了，真厉害！"
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
    img = Image.open("example.jpg")
    img_arr = np.array(img)

    # 生成一个随机的行索引和列索引
    row = np.random.randint(0, img_arr.shape[0])
    col = np.random.randint(0, img_arr.shape[1])

    # 生成一个随机的颜色值
    color = np.random.randint(0, 256, 3)

    # 将图片数组中对应位置的像素值替换为随机颜色值
    img_arr[row, col] = color
    new_img = Image.fromarray(img_arr)
    region = new_img.convert('RGB')
    buf = BytesIO()
    region.save(buf, format='JPEG')
    base64_str = f'base64://{base64.b64encode(buf.getvalue()).decode()}'
    return f'[CQ:image,file={base64_str}]'