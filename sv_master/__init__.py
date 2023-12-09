from hoshino import Service
from .ratings import get_ratings_data

sv = Service('sv_master')

@sv.on_prefix('Ratings')
async def ratings_info(bot,ev):
    msg1,msg2 = await get_ratings_data()
    await bot.send(ev,msg1)
    await bot.send(ev,msg2)