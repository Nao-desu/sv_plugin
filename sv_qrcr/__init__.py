from hoshino import Service
from .check_pic import get_pic,check_QR
from .img_gen import deck_img_gen
from ..info import clan2w,get_code
sv = Service('sv-QRcode')

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
            try:
                code = await get_code(deck)
                msg = f'职业：{clan2w[deck["clan"]]}{img}\n国服永久码{code}'
            except:
                msg = f'职业：{clan2w[deck["clan"]]}{img}'
            await bot.send(ev,msg)            
    except Exception as e:
        await bot.send(ev,f'生成失败{e}')
        return
        

