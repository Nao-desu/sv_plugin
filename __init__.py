import hoshino
from hoshino import Service,get_bot,get_self_ids
from .config import auto_update
from .update import update_main

sv = Service('sv_auto_update',visible=False)

@sv.scheduled_job('cron',hour=15)
async def sv_data_autoupdate():
    if auto_update:
        bot = get_bot()
        uid = hoshino.config.SUPERUSERS[0]
        try:
            new,change= await update_main(True)
            if new or change:
                for sid in get_self_ids():
                    await bot.send_private_msg(self_id=sid,user_id=uid,message=f'sv数据更新成功：\n添加{len(new)}张卡牌\n{len(change)}张卡牌数据变动')
            else:
                for sid in get_self_ids():
                    await bot.send_private_msg(self_id=sid,user_id=uid,message=f'sv数据无更新')
        except Exception as e:
            for sid in get_self_ids():
                await bot.send_private_msg(self_id=sid,user_id=uid,message=f'sv数据自动更新失败：{e}')

@sv.on_fullmatch('手动更新sv数据')
async def sv_data_update(bot,ev):
    await bot.send(ev,'准备更新，请耐心等待')
    try:
        new,change= await update_main(False)
        if new or change:
            await bot.send(ev,f'sv数据更新成功：\n添加{len(new)}张卡牌\n{len(change)}张卡牌数据变动')
        else:
            await bot.send(ev,f'sv数据更新成功')
    except Exception as e:
        await bot.send(ev,f'sv数据自动更新失败：{e}')