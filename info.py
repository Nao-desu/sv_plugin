"""
获取各种数据
"""
from xpinyin import Pinyin
p = Pinyin()
from os.path import join,exists
from fuzzywuzzy.fuzz import partial_ratio as ratio
import json,os,zhconv,re,random
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
    获取指定卡包id
    """
    return 10008

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

def idToHash(id: int) -> str:
    """
    卡牌id转哈希值
    """
    characters = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_"
    hash = ""
    while id > 0:
        hash = characters[id % 64] + hash
        id //= 64
    return hash


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

def check_set(text:str):
    """
    获取卡包
    """
    latest_set = get_latest_set()
    if not text:
        return latest_set,True
    if text.isdigit():
        if int(text)<=latest_set-10000:
            text += 10000
        if int(text) in range(10000,latest_set+1):
            return int(text),False
        else:return False,False
    cond = get_condition()
    card_set = cond["card_set_id"]
    text = zhconv.convert(text,'zh-tw')
    for id in card_set:
        if text in card_set[id]:
            return int(id),False
    return False,False

def get_card_set(id:int,is_rot:bool):
    """
    获取卡包内容，包括异画
    """
    with open(join(MOUDULE_PATH,'data/gacha.json'),'r', encoding='UTF-8') as f:
        aa = json.load(f)
    leader = {1:{},2:{},3:{},4:{}}
    alternate = {1:{},2:{},3:{},4:{}}
    cards = {1:[],2:[],3:[],4:[]}
    if is_rot:
        b = [aa[str(i)] for i in range(id-4,id+1)]
        for cardset in b:
            for cardid in cardset:
                if cardset[cardid][2] == 1:
                    leader[cardset[cardid][1]][int(cardid)] = cardset[cardid][0]//5
                elif cardset[cardid][2] == 0:
                    alternate[cardset[cardid][1]][int(cardid)] = cardset[cardid][0]//5
    else:
        b = aa[str(id)]
        for cardid in b:
            if b[cardid][2] == 1:
                leader[b[cardid][1]][int(cardid)] = b[cardid][0]
            elif b[cardid][2] == 0:
                alternate[b[cardid][1]][int(cardid)] = b[cardid][0]
    card_dict = get_cards()
    if is_rot:
        for card_id in card_dict:
            if int(card_id) in range(100000000,200000000) and card_dict[card_id]["card_set_id"] in range(id-4,id+1):
                cards[5 - card_dict[card_id]["rarity"]].append(int(card_id))
    else:
        for card_id in card_dict:
            if int(card_id) in range(100000000,200000000) and card_dict[card_id]["card_set_id"] == id:
                cards[5 - card_dict[card_id]["rarity"]].append(int(card_id))
    return leader,alternate,cards

def get_legend_card_set():
    with open(join(MOUDULE_PATH,'data/gacha.json'),'r', encoding='UTF-8') as f:
        aa = json.load(f)
    leader = {1:{},2:{},3:{},4:{}}
    alternate = {1:{},2:{},3:{},4:{}}
    cards = {1:[],2:[],3:[],4:[]}
    id = get_latest_set()
    b = [aa[str(i)] for i in range(id-4,id+1)]
    for cardset in b:
        for cardid in cardset:
            if cardset[cardid][2] == 1:
                leader[cardset[cardid][1]][int(cardid)] = cardset[cardid][0]
            elif cardset[cardid][2] == 0 and cardset[cardid][1] == 1:
                alternate[cardset[cardid][1]][int(cardid)] = cardset[cardid][0]
    card_dict = get_cards()
    for card_id in card_dict:
        if int(card_id) in range(100000000,200000000) and card_dict[card_id]["card_set_id"] in range(id-4,id+1) and card_dict[card_id]["rarity"] == 4:
            cards[5 - card_dict[card_id]["rarity"]].append(int(card_id))
    return leader,alternate,cards

def get_all_leadercard() -> list:
    """
    获取所有异画卡
    """
    with open(join(MOUDULE_PATH,'data/gacha.json'),'r', encoding='UTF-8') as f:
        aa = json.load(f)
    leadercard = []
    for cardset in aa:
        for cardid in aa[cardset]:
            if aa[cardset][cardid][2] == 1:
                leadercard.append(int(cardid))
    return leadercard


def judge_card(cards:list):
    """
    判断是否为异画
    """
    if not cards or len(cards)==1:
        return False
    base_id = cards[0]['card']["base_card_id"]
    for i in cards:
        if i['card']["base_card_id"] != base_id:
            return False
    card_dict = get_cards()
    card = card_dict[str(base_id)]
    return [{'card':card,'score':cards[0]['score']}]

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

async def get_deck_name(tag) -> dict:
    """
    返回卡组名
    'r'指定，'l'无限
    """
    if tag == 'r':
        with open(join(MOUDULE_PATH,'data/rotation_deck.json'),'r', encoding='UTF-8') as f:
            return json.load(f)
    elif tag == 'l':
        with open(join(MOUDULE_PATH,'data/unlimited_deck.json'),'r', encoding='UTF-8') as f:
            return json.load(f)

async def get_deck_trans() -> dict:
    """
    返回卡组翻译
    """
    with open(join(MOUDULE_PATH,'data/en2cn.json'),'r', encoding='UTF-8') as f:
        return json.load(f)

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
    10029:"密斯塔爾西亞的英雄",
    10030:"變革的恆規",
    10031:"傳說復甦",
    10032:"闇影詩章：英雄群起",
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
    70029:"三麗鷗明星合作",
    70030:"SPY×FAMILY合作",
    20001:"初音未來合作",
    20002:"SPY×FAMILY合作",
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

en_clan = {
    "1":"forest",
    "2":"sword",
    "3":"rune",
    "4":"dragon",
    "5":"shadow",
    "6":"blood",
    "7":"haven",
    "8":"portal"
}

skill2w = {
    "draw":"抽卡",
    "damage":"直接造成伤害",
    "possess_ep_modifier":"回复EP",
    "pp_modifier":"回复pp",
    "destroy":"破坏",
    "heal":"治疗",
    "attach_skill":"赋予主站者能力",
    "banish":"消失",
    "powerup":"增加身材",
    "pp_fixeduse":"爆能强化",
    "summon_token":"召唤token到场上",
    "play_count_change":"改变用牌数",
    "rush":"突进",
    "quick":"疾驰",
    "lose":"沉默",
    "update_deck" :"向牌堆添加卡牌",
    "shortage_deck_win":"天使牌",
    "clear_destroyed_card_list":"移除被破坏卡牌",
    "token_draw":"向手牌添加token",
    "summon_card":"顺念召唤",
    "cost_change":"改变卡牌费用",
    "power_down":"减少身材",
    "guard":"守护",
    "change_affiliation":"改变卡牌类型",
    "choice":"命运抉择",
    "discard":"弃牌",
    "transform":"转变手牌",
    "evolve":"进化",
    "shield":"免疫伤害",
    "independent":"免疫其他卡牌能力",
    "consume_ep_modifier":"不消耗EP即可进化",
    "special_win":"特殊胜利",
    "metamorphose":"变身",
    "sneak":"潜行",
    "ignore_guard":"无视守护",
    "chant_count_change":"改变护符倒数",
    "return_card":"返回手牌",
    "cant_attack":"无法攻击",
    "token_draw_modifier":"增加token数量",
    "killer":"必杀",
    "drain":"吸血",
    "fusion":"融合",
    "attack_count":"增加攻击次数",
    "indestructible":"无法破坏",
    "not_be_attacked":"无法被攻击",
    "untouchable":"无法被能力指定",
    "spell_charge":"魔力增幅",
    "damage_modifier":"改变伤害",
    "cant_evolution":"无法用EP进化",
    "stack_white_ritual":"蓄积",
    "change_cemetery":"改变墓场数",
    "change_union_burst_count":"必杀技",
    "remove_by_banish":"离场时消失",
    "invoke_skill":"发动其他卡牌能力",
    "damage_cut":"减少伤害",
    "fusion_metamorphose":"融合变身",
    "power_modifier":"改变身材",
    "cant_activate_fanfare":"无法发动入场曲",
    "cant_play":"无法出牌",
    "force_skill_target":"强制指定目标",
    "change_skybound_art_count":"奥义",
    "change_super_skybound_art_count":"解放奥义",
    "damage@3":"造成3次伤害",
    "change_white_ritual_stack":"改变蓄积",
    "remove_by_destroy":"消失时转变为破坏",
    "special_lose":"特殊失败",
    "force_berserk":"进入复仇状态",
    "attack_by_life":"攻击依生命值造成伤害",
    "unite":"合体",
    "geton":"操纵",
    "copy_skill":"复制能力",
    "force_avarice":"进入渴望状态",
    "force_wrath":"进入狂乱状态",
    "reflection":"伤害反射",
    "turn_start_fixed_pp":"回合开始不再增加最大pp",
    "extra_turn":"额外回合"
}
with open(join(MOUDULE_PATH,'data/cardlist.json'),'r',encoding='utf-8') as f:
    cards = list(json.load(f))
cv = []
for i in cards:
    if i['cv'] != "-":
        cvv = i['cv'].split('/')
        for j in cvv:
            if j not in cv:
                cv.append(j)

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
        elif i in cv:
            for card in cards:
                if i in card['cv']:
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
        ratio1_1 = ratio(p.get_pinyin('-'+card["card_name"])+'-','-'+p.get_pinyin(text)+'-')
        ratio1 = 100 if ratio1_1 == 100 else ratio1
        if len(text) > len(card["card_name"]):
            ratio1 = 0
        ratio2 = ratio(clear_pun(card["skill_disc"]),text)
        ratio3 = ratio(clear_pun(card["evo_skill_disc"]),text)
        score = max(ratio1,ratio2,ratio3)
        if score >= check_score(text):
            result.append({'card':card,'score':score/100})
    return result

def get_lim(lim:str):
    """
    查找限制条件
    """
    limite = True
    clan = None
    if '无限' in lim:
        limite = False
    con = get_condition()
    for id in con["clan"]:
        for clanw in con["clan"][id]:
            if clanw in lim:
                clan = int(id)
                break
    return limite,clan

async def get_answer(limite,clan,flag)->int:
    """
    筛选符合条件的卡牌作为答案
    """
    cards = get_cards()
    choose = []
    if clan != None:
        clanc = [clan]
    else:
        clanc = range(0,9)
    if limite:
        for card in cards:
            last = get_latest_set()
            if cards[card]["card_set_id"]>=last-4 and cards[card]["card_set_id"] <= last and cards[card]["clan"] in clanc:
                choose.append(cards[card])
    else:
        for card in cards:
            if cards[card]["clan"] in clanc:
                choose.append(cards[card])
    answer = random.choice(choose)["card_id"]
    if flag == 'voice':
        while not exists(join(MOUDULE_PATH,f'voice/{answer}')):
            answer = await get_answer(limite,clan,'voice')
        while not os.listdir(join(MOUDULE_PATH,f'voice/{answer}')):
            answer = await get_answer(limite,clan,'voice')
    while not exists(join(MOUDULE_PATH,f'img/full/{answer}0.png')):
        answer = await get_answer(limite,clan,None)
    return answer

async def find_decks(text:str):
    if "无限" in text:
        file = 'deck1.json'
        file2 = 'unlimited_deck.json'
        flag = 1
    else:
        file = 'deck3.json'
        file2 = 'rotation_deck.json'
        flag = 0
    with open(join(MOUDULE_PATH,'data/en2cn.json'),'r', encoding='UTF-8') as f:
        deck_name = json.load(f)
    with open(join(MOUDULE_PATH,'data',file),'r', encoding='UTF-8') as f:
        decks = json.load(f)
    with open(join(MOUDULE_PATH,'data',file2),'r', encoding='UTF-8') as f:
        deck_num = json.load(f)
    search_deck = None
    result = []
    search_deck = []
    for i in deck_name:
        for name in deck_name[i]:
            if name in text:
                search_deck.append(i)
    if search_deck:
        for i in search_deck:
            if deck_num[i]:
                for deck in decks:
                    if deck["deck_name"] == i:
                        result.append(deck)
    else:return -4 + flag,flag
    if len(result):
        return result,flag
    else:return -2 + flag,flag