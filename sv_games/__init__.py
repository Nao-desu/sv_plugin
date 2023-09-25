from hoshino import Service
from hoshino.typing import MessageSegment as Seg
from ..info import get_lim,get_answer,get_cards,MOUDULE_PATH
from os.path import join,abspath
from .sv_voice_gess import guess_voice
from .sv_paint_guess import guess_paint
from ..config import GAME_TIME
import asyncio,zhconv

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
            img = f'[CQ:image,file=file:///{abspath(img_path)}]'
            await bot.send(ev, f"正确答案是:{get_cards()[str(answer)]['card_name']}\n{img}\n很遗憾,没有人答对")
            return
        gm.end_game(gid)
    except Exception as e:
        await bot.send(ev,f'游戏发生错误，自动终止')
        gm.end_game(gid)

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
            img = f'[CQ:image,file=file:///{abspath(img_path)}]'
            await bot.send(ev, f"正确答案是:{get_cards()[str(answer)]['card_name']}\n{img}\n很遗憾,没有人答对")
            return
        gm.end_game(gid)
    except Exception as e:
        await bot.send(ev,f'游戏发生错误，自动终止')
        gm.end_game(gid)

@sv.on_message()
async def on_input_chara_name(bot, ev):
    gid = ev.group_id
    if  not gm.is_playing(gid):
        return
    answer = gm.get_ans(gid)
    if gm.check_ans(gid,zhconv.convert(ev.message.extract_plain_text(),'zh-tw')):
        img_path = join(MOUDULE_PATH,f"img\\full\\{answer}0.png")
        img = f'[CQ:image,file=file:///{abspath(img_path)}]'
        msg = f"正确答案是:{get_cards()[str(answer)]['card_name']}\n{img}\n{Seg.at(ev.user_id)}猜对了，真厉害！\n(此轮游戏将在几秒后自动结束，请耐心等待)"
        await bot.send(ev, msg)
        gm.end_game(gid)