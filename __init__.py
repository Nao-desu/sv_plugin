from hoshino import Service
from .config import auto_update
from .update import update_main
from .sv_index import index_help
from .sv_games import game_help
from .sv_gacha import gacha_help
from .sv_master import master_help
from .sv_tarot import tarot_help
from .info import MOUDULE_PATH
from .sv_master.update import master_update

sv = Service('sv_auto_update',visible=False)

@sv.on_fullmatch('sv查卡帮助')
async def index_helper(bot,ev):
    await bot.send(ev,index_help,at_sender = True)

@sv.on_fullmatch('抽卡帮助')
async def gacha_helper(bot,ev):
    await bot.send(ev,gacha_help,at_sender = True)

@sv.on_fullmatch('小游戏帮助')
async def game_helper(bot,ev):
    await bot.send(ev,game_help,at_sender = True)

@sv.on_fullmatch('卡组查询帮助')
async def game_helper(bot,ev):
    await bot.send(ev,master_help,at_sender = True)

@sv.on_fullmatch('塔罗牌帮助')
async def tarot_helper(bot,ev):
    await bot.send(ev,tarot_help,at_sender = True)

@sv.scheduled_job('cron',hour = '*/3')
async def auto_updater():
    if auto_update:
        await master_update()

@sv.on_fullmatch('手动更新sv数据')
async def sv_data_update(bot,ev):
    await bot.send(ev,'准备更新，请耐心等待')
    await master_update()
    await update_main(False)