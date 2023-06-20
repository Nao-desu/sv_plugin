"""
获取各种数据
"""

from os.path import join
from fuzzywuzzy.fuzz import partial_ratio as ratio
import json,os,zhconv,re
MOUDULE_PATH = os.path.dirname(__file__)

def text_changeline(text:str) -> str:
    """
    按限制换行,textwrap不好用
    """
    new_text = ''
    count = 1
    for word in text:
        if count != 25:
            new_text += word
            count += 1
        else:
            new_text += word+'\n'
            count = 1
    return new_text

def text_split(text):
    """
    文字排版
    """
    t_list = text.replace("<br>","\n").split("\n")
    t_list = [text_changeline(i) for i in t_list]
    text = '\n'.join(t_list)
    return text

def get_cards() -> dict:
    """
    返回卡牌字典
    """
    with open(join(MOUDULE_PATH,'data/cards.json'),'r', encoding='UTF-8') as f:
        cards = json.load(f)
    return cards

def get_card_list() -> list:
    """
    返回卡牌列表
    """
    with open(join(MOUDULE_PATH,'data/cardlist.json'),'r', encoding='UTF-8') as f:
        cards = json.load(f)
    return cards

def get_condition() -> dict:
    """
    返回condition字典
    """
    with open(join(MOUDULE_PATH,'data/condition.json'),'r', encoding='UTF-8') as f:
        con = json.load(f)
    return con

def get_latest_set() -> int:
    """
    获取最新卡包id
    """
    con = get_condition()
    return int(list(con["card_set_id"].keys())[-1])

def check_condition(i:str) -> tuple:
    """
    输入卡包名/职业/稀有度/类型/种类
    查找对应条件
    """
    condition = get_condition()
    for kind in condition:
        for value in condition[kind]:
            if i in condition[kind][value]:
                return kind,int(value)
    return False

def check_score(text:str) -> int:
    """
    根据关键词长度返回匹配阈值
    """
    l = len(text)
    if l <= 3:
        return 100
    elif l <= 7:
        return 70
    else:
        return int(100*(l-3)/l)

def get_textcolor_pos(text:str) -> list:
    """
    获取换色文字的位置
    """
    pos = []
    _text = text.replace('<br>','').split('[u][ffcd45]')
    for part in _text:
        part = part.replace('[-][/u]','')
    count = 0
    ntext = []
    for part in _text:
        if '[-][/u]' in part:
            ntext.append(part.split('[-][/u]')[0])
            ntext.append(part.split('[-][/u]')[1])
        else:
            ntext.append(part)
    for i in range(0,len(ntext)):
        if i % 2 == 0:
            count += len(ntext[i])
        else:
            for j in range(0,len(ntext[i])):
                pos.append(count)
                count += 1
    return pos

def hashToID(hash:str) -> int:
    """
    卡牌哈希值转id
    """
    id = 0
    for i in range(len(hash)):
        if '0' <= hash[i] and hash[i] <= '9':
            id = id * 64 + ord(hash[i]) - ord('0')
        if 'A' <= hash[i] and hash[i] <= 'Z':
            id = id * 64 + ord(hash[i]) - ord('A') + 10
        if 'a' <= hash[i] and hash[i] <= 'z':
            id = id * 64 + ord(hash[i]) - ord('a') + 36
        if hash[i] == '-':
            id = id * 64 + 62
        if hash[i] == '_':
            id = id * 64 + 63
    return id

def clear_pun(text:str) -> str:
    """
    去除文字内换行符和标点
    """
    return text.replace('<br>','').replace('。','').replace('，','').replace('：','').replace('；','').replace(' ','')

def get_related_cards(card:dict) -> list:
    """
    获取相关卡牌
    """
    related = []
    idmatch = r'\d{9}'
    related_id = re.findall(idmatch,card["skill_option"])
    cards = get_cards()
    for i in related_id:
        if i in cards and cards[i] not in related and int(i) != card["card_id"]:
            related.append(cards[i])
    return related

def judge_card(cards:list):
    """
    判断是否为异画
    """
    if not cards:
        return False
    base_id = cards[0]['card']["base_card_id"]
    for i in cards:
        if i['card']["base_card_id"] != base_id:
            return False
    card_dict = get_cards()
    card = card_dict[str(base_id)]
    return {'card':card,'score':cards[0]['score']}

def find_all_card(id:int)->list:
    """
    返回此卡牌的所有异画id
    """
    card_dict = get_cards()
    relist = []
    base_id = card_dict[str(id)]["base_card_id"]
    for cardid in card_dict:
        if card_dict[cardid]["base_card_id"] == base_id and card_dict[cardid]["card_id"] != id:
            relist.append(cardid)
    return relist


"""
类型名
"""
tribe_name = ["指揮官","士兵","土之印","馬納利亞","創造物","財寶","機械","雷維翁","自然","宴樂","英雄","武裝","西洋棋","八獄","學園","全部"]
"""
卡包名
"""
card_set = {
    10000:"基本卡",
    10001:"經典卡包",
    10002:"暗影進化",
    10003:"巴哈姆特降臨",
    10004:"諸神狂嵐",
    10005:"夢境奇想",
    10006:"星神傳說",
    10007:"時空轉生",
    10008:"起源之光‧終焉之闇",
    10009:"蒼空騎翔",
    10010:"滅禍十傑",
    10011:"扭曲次元",
    10012:"鋼鐵的反叛者",
    10013:"榮耀再臨",
    10014:"森羅咆哮",
    10015:"極鬥之巔",
    10016:"那塔拉的崩壞",
    10017:"命運諸神",
    10018:"勒比盧的旋風",
    10019:"十天覺醒",
    10020:"暗黑的威爾薩",
    10021:"物語重歸",
    10022:"超越災禍者",
    10023:"十禍鬥爭",
    10024:"天象樂土",
    10025:"極天龍鳴",
    10026:"示天龍劍",
    10027:"八獄魔境‧阿茲弗特",
    10028:"遙久學園",
    70001:"主題牌組 第1彈",
    70002:"主題牌組 第2彈",
    70003:"Anigera合作",
    70004:"劇場版Fate[HF]合作",
    70005:"主題牌組 第4彈",
    70006:"主題牌組 第5彈",
    70008:"超異域公主連結！Re:Dive合作",
    70009:"一拳超人合作",
    70010:"Re：從零開始的異世界生活合作",
    70011:"主題牌組 第6彈",
    70012:"Love Live! 學園偶像祭合作",
    70013:"涼宮春日的憂鬱合作",
    70014:"主題牌組 第7彈",
    70016:"尼爾：自動人形合作",
    70017:"CODE GEASS 反叛的魯路修合作",
    70018:"闇影詩章‧霸者之戰合作",
    70019:"闇影詩章‧霸者之戰套組",
    70020:"碧藍幻想合作",
    70021:"對戰通行證",
    70022:"輝夜姬想讓人告白？合作",
    70023:"偶像大師 灰姑娘女孩合作",
    70024:"通靈王合作",
    70025:"賽馬娘Pretty Derby合作",
    70026:"吉伊卡哇合作",
    70027:"闇影詩章F合作",
    70028:"初音未來合作",
    20001:"初音未來合作",
    90000:"token"
}

clan2w = {
    0:"中立",
    1:"精靈",
    2:"皇家護衛",
    3:"巫師",
    4:"龍族",
    5:"死靈法師",
    6:"吸血鬼",
    7:"主教",
    8:"復仇者"
}

async def text2cards(text:str) -> list:
    """
    通过输入的文字筛选卡牌，返回卡牌列表
    """
    text:list = zhconv.convert(text,'zh-tw').split(' ')
    condition = []
    for i in text:
        if i[:1] == '#':
            condition.append(i[1:])
    for i in condition:
        text.remove('#'+i)
    text:str = ''.join(text).strip()
    cards:list = get_card_list()
    costmatch = r'^\d{1,2}c$'
    lifematch = r'^life\d{1,2}$'
    atkmatch = r'^atk\d{1,2}$'
    for i in condition:
        select = []
        if i in ['指定','指定模式']:
            for card in cards:
                latset = get_latest_set()
                if card['card_set_id'] in range(latset-4,latset+1):
                    select.append(card)
        elif i.isdigit():
            for card in cards:
                if str(card['cost'])+str(card['atk'])+str(card['life']) == i:
                    select.append(card)
        elif re.match(costmatch,i):
            cost = int(i[:-1])
            for card in cards:
                if card['cost'] == cost:
                    select.append(card)
        elif re.match(lifematch,i):
            life = int(i[4:])
            for card in cards:
                if card['life'] == life:
                    select.append(card)
        elif re.match(atkmatch,i):
            atk = int(i[3:])
            for card in cards:
                if card['atk'] == atk:
                    select.append(card)
        elif i in tribe_name:
            for card in cards:
                if i in card['tribe_name'] or card['tribe_name'] == '全部':
                    select.append(card)
        elif check_condition(i):
            kind,value = check_condition(i)
            for card in cards:
                if card[kind] == value:
                    select.append(card)
        else:
            select = []
        cards = select
    result = []
    if not text:
        result = [{'card':card,'score':1.00} for card in cards]
        return result
    number = re.findall(r'\d+',text)#对关键词的数字要严格匹配
    if number:
        unselect = []
        for card in cards:
            for num in number:
                if num not in card["skill_disc"] and num not in card["evo_skill_disc"]:
                    unselect.append(card)
                    break
        for card in unselect:
            cards.remove(card)
    for card in cards:
        ratio1 = ratio(card["card_name"],text)
        if len(text) > len(card["card_name"]):
            ratio1 = 0
        ratio2 = ratio(clear_pun(card["skill_disc"]),text)
        ratio3 = ratio(clear_pun(card["evo_skill_disc"]),text)
        score = max(ratio1,ratio2,ratio3)
        if score >= check_score(text):
            result.append({'card':card,'score':score/100})
    return result