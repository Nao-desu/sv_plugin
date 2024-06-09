from hoshino import Service
from .ratings import get_ratings_data
from .decks import get_deck_data,get_all_decks
from ..info import find_decks

master_help = """
查询来自shadowversemaster的各种数据
[卡组一览] -查看所有卡组，指令后加无限可查看无限卡组一览
[来一套] -来一套卡组，指令后加无限查询无限卡组
"""

sv = Service('sv_master')

@sv.on_prefix('Ratings')
async def ratings_info(bot,ev):
    msg1,msg2 = await get_ratings_data()
    await bot.send(ev,msg1)
    await bot.send(ev,msg2)

@sv.on_prefix('来一套')
async def deck_info(bot,ev):
    text = ev.message.extract_plain_text().strip()
    if not text:
        await bot.send(ev,"请指定卡组名,指令中加上'无限'可以查询无限制卡组")
        return
    decks,flag = await find_decks(text)
    if decks == -1:
        await bot.send(ev,"当前版本暂无此卡组数据")
        return
    elif decks == -2:
        await bot.send(ev,"当前版本暂无此卡组数据\n如果你正在查询同名无限卡组，请在指令中加上'无限'")
        return
    elif decks == -3:
        await bot.send(ev,"无法识别此卡组,请发送`卡组一览 无限`查看当前版本的所有卡组")
        return
    elif decks == -4:
        await bot.send(ev,"无法识别此卡组,请发送`卡组一览`查看当前版本的所有卡组")
        return        
    msg = await get_deck_data(decks,flag)
    await bot.send(ev,msg)

@sv.on_prefix('卡组一览')
async def all_decks_info(bot,ev):
    text = ev.message.extract_plain_text().strip()
    if '无限' in text:
        msg = await get_all_decks('l')
    else:
        msg = await get_all_decks('r')
    await bot.send(ev,msg)