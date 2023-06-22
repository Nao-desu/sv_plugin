from hoshino import Service
from ..info import text2cards,get_cards,judge_card
from .img_gen import card_img_gen,cardlist_img_gen
sv = Service('sv-index')

@sv.on_prefix('sv查卡','查卡','影之诗查卡','SV查卡')
async def sv_card_index(bot,ev):
    text = ev.message.extract_plain_text().replace(' #','#').replace('#', ' #').strip()
    try:
        if text == '':
            await bot.send(ev,'请输入条件&关键词!',at_sender=True)
            return
        cards:list = await text2cards(text)
        judge = judge_card(cards)
        if judge:
            cards = judge
        if len(cards) == 0:
            await bot.send(ev,'抱歉,未查询到符合条件的卡牌',at_sender = True)
        elif len(cards) == 1:
            card = cards[0]['card']
            img = await card_img_gen(card)
            await bot.send(ev,f'{card["card_name"]}\n匹配度{cards[0]["score"]}\n{img}',at_sender = True)
        elif len(cards) > 20:
            await bot.send(ev,f'查询到近似结果{len(cards)}张\n只显示匹配度最高的20张\n使用svcard+id可以查看卡牌详细信息',at_sender = True)
            cards_sorted = sorted(cards,key = lambda x : x['score'],reverse=True)[:20] 
            img = await cardlist_img_gen(cards_sorted)
            await bot.send(ev,img)
        else:
            await bot.send(ev,f'查询到如下{len(cards)}张可能结果\n使用svcard+id可以查看卡牌详细信息',at_sender = True)
            cards_sorted = sorted(cards,key = lambda x : x['score'],reverse=True)
            img = await cardlist_img_gen(cards_sorted)
            await bot.send(ev,img)
    except Exception as e:
        await bot.send(ev,f'查询失败：{e}')

@sv.on_prefix('svcard')
async def svcard_info(bot,ev):
    id = ev.message.extract_plain_text().strip()
    card_dict = get_cards()
    try:
        if id not in card_dict:
            await bot.send(ev,'id错误',at_sender = True)
        else:
            card = card_dict[id]
            img = await card_img_gen(card)
            await bot.send(ev,img,at_sender = True)
    except Exception as e:
        await bot.send(ev,f'发送失败：{e}',at_sender = True)
    