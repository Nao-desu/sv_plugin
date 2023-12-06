from hoshino import Service
from ..info import text2cards,get_cards,judge_card
from .img_gen import card_img_gen,cardlist_img_gen

sv_help= """
——————————————————————
艾特我，发送【查卡帮助】
可以查看sv查卡的帮助信息
——————————————————————
"""

index_help = """
——————————————
    指令说明
——————————————
-sv查卡 #tag 关键词
    查询卡牌信息，tag前要加#号进行区分,支持多tag
    关键词在卡牌名和卡牌能力中匹配
支持的tag有:
#3c     [费用]
#AOA    [卡包]
#token  [token]
#皇家   [职业]
#学园   [种类]
#随从   [卡牌类型]
#atk3   [攻击力]
#life3  [生命值]
#虹     [稀有度]
#指定   [在指定卡牌中筛选]
#333    [费用身材]
（例如【sv查卡 #aoa #皇 #323 #虹】可以精确查找到校舍的黃昏‧莉夏與奈諾）
——————————————
"""

sv = Service('sv-index',help_=index_help)

@sv.on_prefix('sv查卡')
async def sv_card_index(bot,ev):
    text = ev.message.extract_plain_text().replace(' #','#').replace('#', ' #').strip()
    try:
        if text == '':
            await bot.send(ev,'请输入条件&关键词!\n'+sv_help,at_sender=True)
            return
        cards:list = await text2cards(text)
        judge = judge_card(cards)
        if judge:
            cards = judge
        if len(cards) == 0:
            await bot.send(ev,'抱歉,未查询到符合条件的卡牌\n'+sv_help,at_sender = True)
        elif len(cards) == 1:
            card = cards[0]['card']
            img = await card_img_gen(card)
            await bot.send(ev,f'{card["card_name"]}\n匹配度{cards[0]["score"]}{img}',at_sender = True)
        elif len(cards) > 50:
            await bot.send(ev,f'匹配到超过{len(cards)}张卡牌，请缩小范围\n'+sv_help,at_sender = True)
        elif len(cards) > 20:
            await bot.send(ev,f'查询到近似结果{len(cards)}张\n只显示匹配度最高的20张\n使用/svcard+id可以查看卡牌详细信息',at_sender = True)
            cards_sorted = sorted(cards,key = lambda x : x['score'],reverse=True)[:16] 
            img = await cardlist_img_gen(cards_sorted)
            await bot.send(ev,img)
        else:
            await bot.send(ev,f'查询到如下{len(cards)}张可能结果\n使用/svcard+id可以查看卡牌详细信息',at_sender = True)
            cards_sorted = sorted(cards,key = lambda x : x['score'],reverse=True)
            img = await cardlist_img_gen(cards_sorted)
            await bot.send(ev,img)
    except Exception as e:
        await bot.send(ev,f'查询失败：{e}')

@sv.on_prefix('svcard')
async def svcard_info(bot,ev):
    id = ev.message.extract_plain_text().strip()[:9]
    card_dict = get_cards()
    try:
        if id not in card_dict:
            await bot.send(ev,'9位id错误',at_sender = True)
        else:
            card = card_dict[id]
            img = await card_img_gen(card)
            await bot.send(ev,img,at_sender = True)
    except Exception as e:
        await bot.send(ev,f'发送失败：{e}',at_sender = True)
    
