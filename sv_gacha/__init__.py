from hoshino import Service
from hoshino.util import DailyNumberLimiter
from ..info import check_set
from .gacha import gachaing
from .img_gen import draw_result_1,draw_result_2
from ..config import max_400,max_coin
import traceback

sv_help = '''
`sv抽卡` 抽一包卡牌
`sv十连` 抽十包卡牌
`sv井` 抽一井卡牌
以上指令均需@bot触发
默认抽最新卡包，可在指令后加卡包名或卡包ID抽指定卡包
'''

sv = Service('sv_gacha',help_=sv_help)

clmt = DailyNumberLimiter(max_coin)
tlmt = DailyNumberLimiter(max_400)
jlmt = DailyNumberLimiter(1)

@sv.on_prefix('sv抽卡','影之诗抽卡',only_to_me=True)
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
            return
        leadercard,card,result = await gachaing(card_set,1,False)
        msg = await draw_result_1(leadercard,card)
        # msg += '\n进行了1次抽卡,获得:'
        # if leadercard:
        #     msg += f'\n异画x{len(leadercard)}'
        # if result[1]:
        #     msg += f'\n传说卡x{result[1]}'
        # if result[2]:
        #     msg += f'\n黄金卡x{result[2]}'
        # if result[3]:
        #     msg += f'\n白银卡x{result[3]}'
        # if result[4]:
        #     msg += f'\n青铜卡x{result[4]}'
        # msg += f'\n获得以太{result[1]*1000+result[2]*250+result[3]*50+result[4]*10}'
        clmt.increase(f'{uid}',100)
        await bot.send(ev,msg,at_sender = True)
    except Exception as e:
        await bot.send(ev,f'发送失败：{e}')
        traceback.print_exc()

@sv.on_prefix('sv十连','影之诗十连','sv十包','影之诗十包',only_to_me=True)
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
            return
        leadercard,card,result = await gachaing(card_set,10,False)
        msg = await draw_result_2(leadercard,card,False)
        msg += '\n进行了10次抽卡,获得:'
        if leadercard:
            msg += f'\n异画x{len(leadercard)}'
        if result[1]:
            msg += f'\n传说卡x{result[1]}'
        # if result[2]:
        #     msg += f'\n黄金卡x{result[2]}'
        # if result[3]:
        #     msg += f'\n白银卡x{result[3]}'
        # if result[4]:
        #     msg += f'\n青铜卡x{result[4]}'
        msg += f'\n获得以太{result[1]*1000+result[2]*250+result[3]*50+result[4]*10}'
        await bot.send(ev,msg,at_sender = True)
        clmt.increase(f'{uid}',1000)
    except Exception as e:
        await bot.send(ev,f'发送失败：{e}')
        traceback.print_exc()

@sv.on_prefix('sv井','影之诗井','sv一井','影之诗一井','SV一井',only_to_me=True)
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
            return
        roll_time = 400 if  not jlmt.get_num(f'{uid}{card_set}') else 300
        leadercard,card,result = await gachaing(card_set,roll_time,True)
        msg = await draw_result_2(leadercard,card,True)
        msg += f'\n进行了{roll_time}次抽卡,获得:'
        if leadercard:
            msg += f'\n异画x{len(leadercard)}'
        if result[1]:
            msg += f'\n传说卡x{result[1]}'
        # if result[2]:
        #     msg += f'\n黄金卡x{result[2]}'
        # if result[3]:
        #     msg += f'\n白银卡x{result[3]}'
        # if result[4]:
        #     msg += f'\n青铜卡x{result[4]}'
        msg += f'\n获得以太{result[1]*1000+result[2]*250+result[3]*50+result[4]*10}'
        await bot.send(ev,msg,at_sender = True)
        tlmt.increase(f'{uid}')
        jlmt.increase(f'{uid}{card_set}')
    except Exception as e:
        await bot.send(ev,f'发送失败：{e}')
        traceback.print_exc()