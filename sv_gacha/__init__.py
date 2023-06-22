from hoshino import Service
from hoshino.util import DailyNumberLimiter
from ..info import check_set
from .gacha import gachaing
from .img_gen import draw_result_1,draw_result_2
from ..config import max_400,max_coin

sv = Service('sv_gacha')

clmt = DailyNumberLimiter(max_coin)
tlmt = DailyNumberLimiter(max_400)

@sv.on_prefix('sv抽卡','影之诗抽卡')
async def gacha1(bot,ev):
    try:
        uid = ev.user_id
        if not clmt.check(f'{uid}'):
            await bot.send(ev,f'今天已经抽过{max_coin}金币啦,请明天再来',at_sender = True)
            return
        text:str = ev.message.extract_plain_text().strip()
        card_set:int = check_set(text)
        if not card_set:
            await bot.send(ev,'不存在此卡包！',at_sender= True)
        leadercard,card,result = await gachaing(card_set,1)
        msg = await draw_result_1(leadercard,card)
        clmt.increase(f'{uid}',100)
        await bot.send(ev,msg,at_sender = True)
    except Exception as e:
        await bot.send(ev,f'发送失败：{e}')

@sv.on_prefix('sv十连','影之诗十连','sv十包','影之诗十包')
async def gacha10(bot,ev):
    try:
        uid = ev.user_id
        if not clmt.check(f'{uid}'):
            await bot.send(ev,f'今天已经抽过{max_coin}金币啦,请明天再来',at_sender = True)
            return
        text:str = ev.message.extract_plain_text().strip()
        card_set:int = check_set(text)
        if not card_set:
            await bot.send(ev,'不存在此卡包！',at_sender= True)
        leadercard,card,result = await gachaing(card_set,10)
        msg = await draw_result_2(leadercard,card)
        msg += '\n获得:'
        if leadercard:
            msg += f'\n异画x{len(leadercard)}'
        if result[1]:
            msg += f'\n传说卡x{result[1]}'
        if result[2]:
            msg += f'\n黄金卡x{result[2]}'
        if result[3]:
            msg += f'\n白银卡x{result[3]}'
        if result[4]:
            msg += f'\n青铜卡x{result[4]}'
        await bot.send(ev,msg,at_sender = True)
        clmt.increase(f'{uid}',1000)
    except Exception as e:
        await bot.send(ev,f'发送失败：{e}')

@sv.on_prefix('sv井','影之诗井','sv井','影之诗井')
async def gacha400(bot,ev):
    try:
        uid = ev.user_id
        if not tlmt.check(f'{uid}'):
            await bot.send(ev,f'今天已经抽过{max_400}井啦,请明天再来',at_sender = True)
            return
        text:str = ev.message.extract_plain_text().strip()
        card_set:int = check_set(text)
        if not card_set:
            await bot.send(ev,'不存在此卡包！',at_sender= True)
        leadercard,card,result = await gachaing(card_set,400)
        msg = await draw_result_2(leadercard,card)
        msg += '\n获得:'
        if leadercard:
            msg += f'\n异画x{len(leadercard)}'
        if result[1]:
            msg += f'\n传说卡x{result[1]}'
        if result[2]:
            msg += f'\n黄金卡x{result[2]}'
        if result[3]:
            msg += f'\n白银卡x{result[3]}'
        if result[4]:
            msg += f'\n青铜卡x{result[4]}'
        await bot.send(ev,msg,at_sender = True)
        tlmt.increase(f'{uid}')
    except Exception as e:
        await bot.send(ev,f'发送失败：{e}')