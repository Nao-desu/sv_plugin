from hoshino import Service
from .ratings import get_ratings_data
from .decks import get_deck_data

sv = Service('sv_master')

@sv.on_prefix('Ratings')
async def ratings_info(bot,ev):
    msg1,msg2 = await get_ratings_data()
    await bot.send(ev,msg1)
    await bot.send(ev,msg2)

@sv.on_prefix('来一套')
async def deck_info(bot,ev):
    text = ev.message.extract_plain_text().strip()
    msg,num = await get_deck_data(text)
    if num:
        await bot.send(ev,msg)
    else:
        await bot.send(ev,"无法识别卡组名\n如果要查询无限制卡组，请在指令中加上'无限'")