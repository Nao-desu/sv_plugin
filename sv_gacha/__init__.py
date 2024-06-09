from hoshino import Service
from hoshino.util import DailyNumberLimiter
from ..info import check_set,card_set
from .gacha import gachaing
from .img_gen import draw_result_1,draw_result_2
from ..config import max_400,max_coin
import traceback
from ..MDgen import *

gacha_help = '''
`sv抽卡` 抽一包卡牌
`sv十连` 抽十包卡牌
`sv井` 抽一井卡牌
默认抽最新卡包，可在指令后加卡包名或卡包ID抽指定卡包
'''

sv = Service('sv_gacha',help_=gacha_help)

clmt = DailyNumberLimiter(max_coin)
tlmt = DailyNumberLimiter(max_400)
jlmt = DailyNumberLimiter(1)

@sv.on_prefix('sv抽卡')
async def gacha1(bot,ev):
    try:
        uid = ev.user_id
        if not clmt.check(f'{uid}'):
            await bot.send(ev,f'今天已经抽过{max_coin}金币啦,请明天再来',at_sender = True)
            return
        text:str = ev.message.extract_plain_text().strip()
        card_set_gacha:int = check_set(text)
        if not card_set_gacha:
            await bot.send(ev,'不存在此卡包！',at_sender= True)
            return
        leadercard,card,_ = await gachaing(card_set_gacha,1,False)
        url,size = await draw_result_1(leadercard,card)
        clmt.increase(f'{uid}',100)
        button = [{"buttons":[button_gen(False,'单抽','sv抽卡'),button_gen(False,'十连','sv十连'),button_gen(False,'一井','sv井')]}]
        msg = MD_gen(['抽卡结果',f'img#{size[0]}px #{size[1]}px',url,'下次运气会更好！',f'抽取卡包:{card_set[card_set_gacha]}'],button)
        await bot.send(ev,msg)
    except Exception as e:
        await bot.send(ev,f'发送失败：{e}')
        traceback.print_exc()

@sv.on_prefix('sv十连')
async def gacha10(bot,ev):
    try:
        uid = ev.user_id
        if not clmt.check(f'{uid}'):
            await bot.send(ev,f'今天已经抽过{max_coin}金币啦,请明天再来',at_sender = True)
            return
        text:str = ev.message.extract_plain_text().strip()
        card_set_gacha:int = check_set(text)
        if not card_set_gacha:
            await bot.send(ev,'不存在此卡包！',at_sender= True)
            return
        leadercard,card,result = await gachaing(card_set_gacha,10,False)
        msg = '进行了10次抽卡,获得:'
        if leadercard:
            msg += f'  \r异画x{len(leadercard)}'
        if result[1]:
            msg += f'  \r传说卡x{result[1]}'
        if result[2]:
            msg += f'  \r黄金卡x{result[2]}'
        if result[3]:
            msg += f'  \r白银卡x{result[3]}'
        if result[4]:
            msg += f'  \r青铜卡x{result[4]}'
        msg += f'  \r获得以太{result[1]*1000+result[2]*250+result[3]*50+result[4]*10}'
        url,size = await draw_result_2(leadercard,card,False)
        button = [{"buttons":[button_gen(False,'单抽','sv抽卡'),button_gen(False,'十连','sv十连'),button_gen(False,'一井','sv井')]}]
        msg = MD_gen(['抽卡结果',f'img#{size[0]}px #{size[1]}px',url,msg,f'抽取卡包:{card_set[card_set_gacha]}'],button)
        await bot.send(ev,msg)
        clmt.increase(f'{uid}',1000)
    except Exception as e:
        await bot.send(ev,f'发送失败：{e}')
        traceback.print_exc()

@sv.on_prefix('sv井')
async def gacha400(bot,ev):
    try:
        uid = ev.user_id
        if not tlmt.check(f'{uid}'):
            await bot.send(ev,f'今天已经抽过{max_400}井啦,请明天再来',at_sender = True)
            return
        text:str = ev.message.extract_plain_text().strip()
        card_set_gacha:int = check_set(text)
        if not card_set_gacha:
            await bot.send(ev,'不存在此卡包！',at_sender= True)
            return
        roll_time = 400 if  not jlmt.get_num(f'{uid}{card_set_gacha}') else 300
        leadercard,card,result = await gachaing(card_set_gacha,roll_time,True)
        msg = f'进行了{roll_time}次抽卡,获得:'
        if leadercard:
            msg += f'  \r异画x{len(leadercard)}'
        if result[1]:
            msg += f'  \r传说卡x{result[1]}'
        if result[2]:
            msg += f'  \r黄金卡x{result[2]}'
        if result[3]:
            msg += f'  \r白银卡x{result[3]}'
        if result[4]:
            msg += f'  \r青铜卡x{result[4]}'
        msg += f'  \r获得以太{result[1]*1000+result[2]*250+result[3]*50+result[4]*10}'
        url,size = await draw_result_2(leadercard,card,True)
        button = [{"buttons":[button_gen(False,'单抽','sv抽卡'),button_gen(False,'十连','sv十连'),button_gen(False,'一井','sv井')]}]
        msg = MD_gen(['抽卡结果',f'img#{size[0]}px #{size[1]}px',url,msg,f'抽取卡包:{card_set[card_set_gacha]}'],button)
        await bot.send(ev,msg)
        tlmt.increase(f'{uid}')
        jlmt.increase(f'{uid}{card_set_gacha}')
    except Exception as e:
        await bot.send(ev,f'发送失败：{e}')
        traceback.print_exc()