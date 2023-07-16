from hoshino import Service
from .check_pic import get_pic,check_QR
from .img_gen import deck_img_gen
from ..info import clan2w
import traceback

sv_help = """
被动技：当识别到世界服二维码时自动输出卡组信息
"""

sv = Service('sv-QRcode',help_=sv_help)

@sv.on_message('group')
async def sv_QRCR(bot,ev):
    pic = await get_pic(ev)
    if not pic:
        return
    decks = await check_QR(pic)
    if not decks:
        return
    try:
        await bot.send(ev,'发现世界服二维码！')
        for deck in decks:
            img = await deck_img_gen(deck)
            msg = f'职业：{clan2w[deck["clan"]]}{img}'
            await bot.send(ev,msg)            
    except Exception as e:
        traceback.print_exc()
        await bot.send(ev,f'生成失败{e}')
        return
        

