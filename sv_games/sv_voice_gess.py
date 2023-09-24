from ..info import clan2w
from ..config import GAME_TIME
from ..info import MOUDULE_PATH
from os.path import join
import random,os

async def guess_voice(bot,ev,limited,clan,answer):
    w1 = '指定' if limited else ''
    w2 = '' if not clan else clan2w[clan]
    voice_path = join(MOUDULE_PATH,f'voive\\{random.choice(os.listdir(join(MOUDULE_PATH,f"voice{answer}")))}')
    rec = f'[CQ:record,file=file:///{os.path.abspath(voice_path)}]'
    await bot.send(ev,f'猜猜这段语音来自哪张{w1}{w2}卡牌?\n{GAME_TIME}秒后公布答案')
    await bot.send(ev,rec)