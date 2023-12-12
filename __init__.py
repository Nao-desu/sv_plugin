from hoshino import Service
from .config import auto_update
from .update import update_main
from .sv_index import index_help
from .sv_games import game_help
from .sv_gacha import gacha_help
from .sv_master import master_help
from os.path import join,abspath
from .info import MOUDULE_PATH
from .sv_master.update import master_update

sv = Service('sv_auto_update',visible=False)

filepath = join(MOUDULE_PATH,f'img\chqr.jpg')
sv_help = f"""
影之诗相关查询机器人
艾特我，发送以下指令查看具体功能帮助
[sv查卡帮助]
[抽卡帮助]
[小游戏帮助]
[实用数据帮助]
更多功能正在制作中。。。
bug反馈/功能建议/bot试用请扫码加入官方频道
(频道用户也可点击头像直接加入官方频道)[CQ:image,file=file:///{abspath(filepath)}]
"""

@sv.on_fullmatch('sv帮助')
async def sv_helper(bot,ev):
    await bot.send(ev,sv_help,at_sender = True)

@sv.on_fullmatch('sv查卡帮助')
async def index_helper(bot,ev):
    await bot.send(ev,index_help,at_sender = True)

@sv.on_fullmatch('抽卡帮助')
async def gacha_helper(bot,ev):
    await bot.send(ev,gacha_help,at_sender = True)

@sv.on_fullmatch('小游戏帮助')
async def game_helper(bot,ev):
    await bot.send(ev,game_help,at_sender = True)

@sv.on_fullmatch('实用数据帮助')
async def game_helper(bot,ev):
    await bot.send(ev,master_help,at_sender = True)

@sv.scheduled_job('cron',hour = '*/3')
async def auto_updater():
    if auto_update:
        await master_update()

@sv.on_fullmatch('手动更新sv数据')
async def sv_data_update(bot,ev):
    await bot.send(ev,'准备更新，请耐心等待')
    await master_update()
    await update_main(False)