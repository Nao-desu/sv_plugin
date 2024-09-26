from hoshino import Service
from .config import auto_update
from .update import update_main
from .sv_master.update import master_update

sv = Service('sv_auto_update',visible=False)

@sv.scheduled_job('cron',hour = '*/6')
async def auto_updater():
    if auto_update:
        await master_update()

@sv.on_fullmatch('手动更新sv数据')
async def sv_data_update(bot,ev):
    await bot.send(ev,'准备更新，请耐心等待')
    await master_update()
    await update_main(False)