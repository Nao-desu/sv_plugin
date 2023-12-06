import hoshino
from hoshino import Service,get_bot,get_self_ids
from .config import auto_update
from .update import update_main
from .sv_index import index_help
from .sv_games import game_help
from .sv_gacha import gacha_help

sv = Service('sv_auto_update',visible=False)

sv_help = """
影之诗相关查询机器人
艾特我，发送以下指令查看具体功能帮助
[查卡帮助]
[抽卡帮助]
[小游戏帮助]
bug反馈/功能建议请加群1045372728
"""

@sv.on_fullmatch('sv帮助')
async def sv_helper(bot,ev):
    await bot.send(ev,sv_help,at_sender = True)

@sv.on_fullmatch('查卡帮助')
async def index_helper(bot,ev):
    await bot.send(ev,index_help,at_sender = True)

@sv.on_fullmatch('抽卡帮助')
async def gacha_helper(bot,ev):
    await bot.send(ev,gacha_help,at_sender = True)

@sv.on_fullmatch('小游戏帮助')
async def game_helper(bot,ev):
    await bot.send(ev,game_help,at_sender = True)

@sv.scheduled_job('cron',hour=15)
async def sv_data_autoupdate():
    if auto_update:
        bot = get_bot()
        uid = hoshino.config.SUPERUSERS[0]
        try:
            new,change= await update_main(True)
            # if new or change:
            #     for sid in get_self_ids():
            #         await bot.send_private_msg(self_id=sid,user_id=uid,message=f'sv数据更新成功：\n添加{len(new)}张卡牌\n{len(change)}张卡牌数据变动')
            # else:
            #     for sid in get_self_ids():
            #         await bot.send_private_msg(self_id=sid,user_id=uid,message=f'sv数据无更新')\
            pass
        except Exception as e:
            # for sid in get_self_ids():
            #     await bot.send_private_msg(self_id=sid,user_id=uid,message=f'sv数据自动更新失败：{e}')
            pass

@sv.on_fullmatch('手动更新sv数据')
async def sv_data_update(bot,ev):
    await bot.send(ev,'准备更新，请耐心等待')
    try:
        new,change= await update_main(False)
        if new or change:
            #await bot.send(ev,f'sv数据更新成功：\n添加{len(new)}张卡牌\n{len(change)}张卡牌数据变动')
            pass
        else:
            #await bot.send(ev,f'sv数据更新成功')
            pass
    except Exception as e:
        #await bot.send(ev,f'sv数据自动更新失败：{e}')
        pass