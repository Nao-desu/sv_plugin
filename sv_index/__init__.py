from hoshino import Service
from ..info import text2cards,get_cards,judge_card,find_all_card,get_related_cards
from .img_gen import card_img_gen,cardlist_img_gen
from ..MDgen import *
from ...groupmaster.switch import sdb
sv = Service('sv-index')

@sv.on_prefix('sv查卡')
async def sv_card_index(bot,ev):
    status = sdb.get_status(ev.real_group_id,'sv查卡')
    if not status:
        return
    text = ev.message.extract_plain_text().replace(' #','#').replace('#', ' #').strip()
    if text == "帮助":
        return
    try:
        if text == '':
            await bot.send(ev,'请输入条件&关键词!\n',at_sender=True)
            return
        cards:list = await text2cards(text)
        judge = judge_card(cards)
        if judge:
            cards = judge
        if len(cards) == 0:
            await bot.send(ev,'抱歉,未查询到符合条件的卡牌\n',at_sender = True)
        elif len(cards) == 1:
            card = cards[0]['card']
            url,size = await card_img_gen(card)
            button = []
            relist = find_all_card(card["card_id"])
            if relist:
                leng = len(relist)
                while leng > 4:
                    button.append({"buttons":[button_gen(False,f'异画' if int(j) in range(700000000,800000000) else '原画' if int(j) < 200000000 else f'其它版本',f'svcard {j}') for j in relist[:4]]})
                    relist = relist[4:]
                    leng -= 4
                else:
                    button.append({"buttons":[button_gen(False,f'异画' if int(j) in range(700000000,800000000) else '原画' if int(j) < 200000000 else f'其它版本',f'svcard {j}') for j in relist]})
            related_cards = get_related_cards(card)
            if related_cards:
                leng = len(related_cards)
                while leng > 4:
                    button.append({"buttons":[button_gen(False,i["card_name"],f'svcard {i["card_id"]}') for i in related_cards[:4]]})
                    related_cards=related_cards[4:]
                    leng -= 4
                else:
                    button.append({"buttons":[button_gen(False,i["card_name"],f'svcard {i["card_id"]}') for i in related_cards]})
            button.append({"buttons":[button_gen(False,'查卡','sv查卡'),link_button('帮助','https://www.koharu.cn/docs/shadowverse/shadowverse.html#sv%E6%9F%A5%E5%8D%A1')]})
            msg = MD_gen([f'{card["card_name"]}',f'img#{size[0]}px #{size[1]}px',url,f'匹配度{cards[0]["score"]}','data from shadowverse-portal'],button)
            await bot.send(ev,msg)
        elif len(cards) > 50:
            await bot.send(ev,f'匹配到超过{len(cards)}张卡牌，请缩小范围\n',at_sender = True)
        elif len(cards) > 16:
            cards_sorted = sorted(cards,key = lambda x : x['score'],reverse=True)[:16] 
            url,size = await cardlist_img_gen(cards_sorted)
            button = []
            leng = len(cards_sorted)
            while leng > 4:
                button.append({"buttons":[button_gen(False,i['card']["card_name"],f'svcard {i["card"]["card_id"]}') for i in cards_sorted[:4]]})
                cards_sorted=cards_sorted[4:]
                leng -= 4
            else:
                button.append({"buttons":[button_gen(False,i['card']["card_name"],f'svcard {i["card"]["card_id"]}') for i in cards_sorted]})
            button.append({"buttons":[button_gen(False,'查卡','sv查卡'),link_button('帮助','https://www.koharu.cn/docs/shadowverse/shadowverse.html#sv%E6%9F%A5%E5%8D%A1')]})
            msg = MD_gen([f'匹配到{len(cards)}张卡牌，只显示匹配度最高的16张',f'img#{size[0]}px #{size[1]}px',url,f'点击下方按钮查看卡牌详细信息','data from shadowverse-portal'],button)
            await bot.send(ev,msg)
        else:
            cards_sorted = sorted(cards,key = lambda x : x['score'],reverse=True)
            url,size = await cardlist_img_gen(cards_sorted)
            button = []
            leng = len(cards_sorted)
            while leng > 4:
                button.append({"buttons":[button_gen(False,i['card']["card_name"],f'svcard {i["card"]["card_id"]}') for i in cards_sorted[:4]]})
                cards_sorted=cards_sorted[4:]
                leng -= 4
            else:
                button.append({"buttons":[button_gen(False,i['card']["card_name"],f'svcard {i["card"]["card_id"]}') for i in cards_sorted]})
            button.append({"buttons":[button_gen(False,'查卡','sv查卡'),link_button('帮助','https://www.koharu.cn/docs/shadowverse/shadowverse.html#sv%E6%9F%A5%E5%8D%A1')]})
            msg = MD_gen([f'匹配到{len(cards)}张卡牌',f'img#{size[0]}px #{size[1]}px',url,f'点击下方按钮查看卡牌详细信息','data from shadowverse-portal'],button)
            await bot.send(ev,msg)
    except Exception as e:
        await bot.send(ev,f'查询失败：{e}')

@sv.on_prefix('svcard')
async def svcard_info(bot,ev):
    status = sdb.get_status(ev.real_group_id,'sv查卡')
    if not status:
        return
    id = ev.message.extract_plain_text().strip()[:9]
    card_dict = get_cards()
    try:
        if id not in card_dict:
            await bot.send(ev,'9位id错误',at_sender = True)
        else:
            card = card_dict[id]
            url,size = await card_img_gen(card)
            button = []
            relist = find_all_card(card["card_id"])
            if relist:
                leng = len(relist)
                while leng > 4:
                    button.append({"buttons":[button_gen(False,f'异画' if int(j) in range(700000000,800000000) else '原画' if int(j) < 200000000 else f'其它版本',f'svcard {j}') for j in relist[:4]]})
                    relist = relist[4:]
                    leng -= 4
                else:
                    button.append({"buttons":[button_gen(False,f'异画' if int(j) in range(700000000,800000000) else '原画' if int(j) < 200000000 else f'其它版本',f'svcard {j}') for j in relist]})
            related_cards = get_related_cards(card)
            if related_cards:
                leng = len(related_cards)
                while leng > 4:
                    button.append({"buttons":[button_gen(False,i["card_name"],f'svcard {i["card_id"]}') for i in related_cards[:4]]})
                    related_cards=related_cards[4:]
                    leng -= 4
                else:
                    button.append({"buttons":[button_gen(False,i["card_name"],f'svcard {i["card_id"]}') for i in related_cards]})
            button.append({"buttons":[button_gen(False,'查卡','sv查卡'),link_button('帮助','https://www.koharu.cn/docs/shadowverse/shadowverse.html#sv%E6%9F%A5%E5%8D%A1')]})
            msg = MD_gen([f'{card["card_name"]}',f'img#{size[0]}px #{size[1]}px',url,f'{card["card_id"]}','data from shadowverse-portal'],button)
            await bot.send(ev,msg)
    except Exception as e:
        await bot.send(ev,f'发送失败：{e}',at_sender = True)
    
