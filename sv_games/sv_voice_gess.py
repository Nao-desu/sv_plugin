from ..info import clan2w
from ..config import GAME_TIME
from ..info import MOUDULE_PATH
from os.path import join
from nonebot import MessageSegment
from hoshino.MD import *
import random,os

async def guess_voice(bot,ev,limited,clan,answer):
    w1 = '溯时指定' if limited else ''
    w2 = '' if not clan else clan2w[clan]
    voice = random.choice(os.listdir(join(MOUDULE_PATH,f"voice\\{answer}")))
    rec = MessageSegment.record(f'file:///{MOUDULE_PATH}/voice/{answer}/{voice}')
    button = [[button_gen('我要回答',' ',style=4),button_gen('帮助','https://www.koharu.cn/docs/shadowverse/shadowverse.html#%E7%8C%9C%E5%8D%A1%E6%B8%B8%E6%88%8F',style = 0,type_int=0)]]
    button = generate_buttons(button)
    msg = generate_md(3,[f'猜猜这段语音来自哪张{w1}{w2}卡牌？',f'{GAME_TIME}秒后公布答案  \r','艾特我+你的答案参与游戏'],button)
    _send1 = await bot.send(ev,msg)
    _send2 = await bot.send(ev,rec)
    return _send1["message_id"], _send2["message_id"]