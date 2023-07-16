from hoshino import Service
from ..info import text2cards,get_cards,judge_card
from .img_gen import card_img_gen,cardlist_img_gen

sv_help = 'svcard id: 查询对应id的卡牌信息\n\
    sv查卡 #条件 卡牌名/关键词:查询卡牌信息，条件前要加#号进行区分,支持多条件,每个条件前都加#号\n\
	当前支持的检索条件如下:\n\
    `#3c` 指定费用为3\n\
    `#AOA` 指定卡包为遥久学园，也可用文字或文字简写\n\
    `#皇家` 指定职业为皇家\n\
    `#学园` 指定种类为学院\n\
    `#随从` 指定为随从卡\n\
    `#atk3` 指定攻击力为3\n\
    `#life3` 指定生命值为3\n\
    `#虹卡` 指定卡牌稀有度为传说\n\
    `#333` 指定费用身材为3-3-3的随从\n\
    `#指定` 只在指定系列中搜索卡牌'

sv = Service('sv-index',help_=sv_help)

@sv.on_fullmatch('sv帮助')
async def get_help(bot, ev):
    await bot.send(ev, sv_help)

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
    
