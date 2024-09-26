from hoshino import Service
from hoshino.util import DailyNumberLimiter
from ..info import check_set,card_set,get_latest_set,get_all_leadercard
from .gacha import gachaing,gachalegend
from .img_gen import draw_result_1,draw_result_2
import traceback
from ..MDgen import *
from ...groupmaster.switch import sdb
import random

sv = Service('sv_gacha')

jlmt = DailyNumberLimiter(1)

@sv.on_prefix('sv抽卡')
async def gacha1(bot,ev):
    status = sdb.get_status(ev.real_group_id,'sv抽卡')
    if not status:
        return
    try:
        text:str = ev.message.extract_plain_text().strip()
        card_set_gacha,is_rot = check_set(text)
        if not card_set_gacha:
            await bot.send(ev,'不存在此卡包！',at_sender= True)
            return
        leadercard,card,_ = await gachaing(card_set_gacha,1,False,is_rot)
        url,size = await draw_result_1(leadercard,card)
        button = [{"buttons":[button_gen(False,'单抽','sv抽卡'),button_gen(False,'十连','sv十连'),button_gen(False,'一井','sv井'),link_button('帮助','https://www.koharu.cn/docs/shadowverse/shadowverse.html#%E6%A8%A1%E6%8B%9F%E6%8A%BD%E5%8D%A1')]}]
        if is_rot:
            msg = MD_gen(['抽卡结果',f'img#{size[0]}px #{size[1]}px',url,'下次运气会更好！',f'抽取卡包:溯时指定'],button)
        else:
            msg = MD_gen(['抽卡结果',f'img#{size[0]}px #{size[1]}px',url,'下次运气会更好！',f'抽取卡包:{card_set[card_set_gacha]}'],button)
        await bot.send(ev,msg)
    except Exception as e:
        await bot.send(ev,f'发送失败：{e}')
        traceback.print_exc()

@sv.on_prefix('sv十连')
async def gacha10(bot,ev):
    status = sdb.get_status(ev.real_group_id,'sv抽卡')
    if not status:
        return
    try:
        text:str = ev.message.extract_plain_text().strip()
        card_set_gacha,is_rot = check_set(text)
        if not card_set_gacha:
            await bot.send(ev,'不存在此卡包！',at_sender= True)
            return
        leadercard,card,result = await gachaing(card_set_gacha,10,False,is_rot)
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
        msg += f'  \r获得以太{result[1]*1000+result[2]*250+result[3]*50+result[4]*10}  \r'
        url,size = await draw_result_2(leadercard,card,False)
        button = [{"buttons":[button_gen(False,'单抽','sv抽卡'),button_gen(False,'十连','sv十连'),button_gen(False,'一井','sv井'),link_button('帮助','https://www.koharu.cn/docs/shadowverse/shadowverse.html#%E6%A8%A1%E6%8B%9F%E6%8A%BD%E5%8D%A1')]}]
        if is_rot:
            msg = MD_gen(['抽卡结果',f'img#{size[0]}px #{size[1]}px',url,msg,f'抽取卡包:溯时指定'],button)
        else:msg = MD_gen(['抽卡结果',f'img#{size[0]}px #{size[1]}px',url,msg,f'抽取卡包:{card_set[card_set_gacha]}'],button)
        await bot.send(ev,msg)
    except Exception as e:
        await bot.send(ev,f'发送失败：{e}')
        traceback.print_exc()

@sv.on_prefix('sv井')
async def gacha400(bot,ev):
    status = sdb.get_status(ev.real_group_id,'sv抽卡')
    if not status:
        return
    try:
        uid = ev.user_id
        text:str = ev.message.extract_plain_text().strip()
        card_set_gacha,is_rot = check_set(text)
        if not card_set_gacha:
            await bot.send(ev,'不存在此卡包！',at_sender= True)
            return
        roll_time = 400 if  not jlmt.get_num(f'{uid}{card_set_gacha}') else 300
        leadercard,card,result = await gachaing(card_set_gacha,roll_time,True,is_rot)
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
        msg += f'  \r获得以太{result[1]*1000+result[2]*250+result[3]*50+result[4]*10}  \r'
        url,size = await draw_result_2(leadercard,card,True)
        button = [{"buttons":[button_gen(False,'单抽','sv抽卡'),button_gen(False,'十连','sv十连'),button_gen(False,'一井','sv井'),link_button('帮助','https://www.koharu.cn/docs/shadowverse/shadowverse.html#%E6%A8%A1%E6%8B%9F%E6%8A%BD%E5%8D%A1')]}]
        if is_rot:
            msg = MD_gen(['抽卡结果',f'img#{size[0]}px #{size[1]}px',url,msg,f'抽取卡包:溯时指定'],button)
        else:msg = MD_gen(['抽卡结果',f'img#{size[0]}px #{size[1]}px',url,msg,f'抽取卡包:{card_set[card_set_gacha]}'],button)
        await bot.send(ev,msg)
        jlmt.increase(f'{uid}{card_set_gacha}')
    except Exception as e:
        await bot.send(ev,f'发送失败：{e}')
        traceback.print_exc()