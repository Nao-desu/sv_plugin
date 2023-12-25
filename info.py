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

def check_set(text:str) -> int:
    """
    获取卡包
    """
    latest_set = get_latest_set()
    if not text:
        return latest_set
    if text.isdigit():
        if int(text)<=latest_set-10000:
            text += 10000
        if int(text) in range(10000,latest_set+1):
            return int(text)
        else:return False
    cond = get_condition()
    card_set = cond["card_set_id"]
    text = zhconv.convert(text,'zh-tw')
    for id in card_set:
        if text in card_set[id]:
            return int(id)
    return False

def get_card_set(id:int):
    """
    获取卡包内容，包括异画
    """
    with open(join(MOUDULE_PATH,'data/gacha.json'),'r', encoding='UTF-8') as f:
        aa = json.load(f)
    leader = {1:{},2:{},3:{},4:{}}
    alternate = {1:{},2:{},3:{},4:{}}
    cards = {1:[],2:[],3:[],4:[]}
    aa = aa[str(id)]
    for cardid in aa:
        if aa[cardid][2] == 1:
            leader[aa[cardid][1]][int(cardid)] = aa[cardid][0]
        elif aa[cardid][2] == 0:
            alternate[aa[cardid][1]][int(cardid)] = aa[cardid][0]
    card_dict = get_cards()
    for card_id in card_dict:
        if int(card_id) in range(100000000,200000000) and card_dict[card_id]["card_set_id"] == id:
            cards[5 - card_dict[card_id]["rarity"]].append(int(card_id))
    return leader,alternate,cards

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

def get_ratings() -> dict:
    """
    返回ratings数据
    """
    with open(join(MOUDULE_PATH,'data/ratings.json'),'r', encoding='UTF-8') as f:
        ratings = json.load(f)
    return ratings

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

cv = ['小野友樹', '金元壽子', '中田讓治', '淺川悠', '大塚芳忠', '優木かな', '種崎敦美', '田村ゆかり', '保志總一朗', '後 藤邑子', '石田彰', '石塚運昇', '石上靜香', '堀江由衣', '置鮎龍太郎', '茅野愛衣', '佐倉薰', '悠木碧', '石原夏織', '杉田智和', '鳥海浩輔', '田所あずさ', '野水伊織', '小倉唯', '水瀨いのり', '釘宮理惠', '水橋かおり', '諏訪部順一', '佐倉綾音', '柚木涼香', '井上喜久子', '金田朋子', '麻倉もも', '大關英里', '潘めぐみ', '田中美海', '村川梨衣', 'ブリドカットセーラ惠美', '小野涼子', '淵上舞', '佐藤利奈', '名塚佳織', '柿原徹也', '神谷浩史', '森川智之', '後藤ヒロキ', 'KENN', '井上雄貴', '藤田曜子', '佐藤元', '內田雄馬', '榊原優希', '土屋李央', '村瀨步', '高木涉', '伊瀨茉莉也', '坂本真綾', '櫻井孝宏', '津田健次郎', '清水愛', '寺崎裕香', '小山剛志', '辻あゆみ', '門脇舞以', '緒乃冬華', '大龜あすか', '高橋美佳子', '中村和正', '下田麻美', '山口勝平', '廣橋涼', '豊田萌繪', '日笠陽子', '淺倉杏美', '藤田笑', '大空直美', '明坂聰美', '伊藤美來', '金子有希', '安元洋貴', '麥人', '山村響', '堀江瞬', '近藤玲奈', '藤村步', 'ゆかな', '石川界人', '保村真', '小野坂昌也', '平野綾', '子安武人', '鬼頭明里', '富田美憂', '中井和哉', 'いのくちゆか', '山下七海', '日高里菜', '前野智昭', '上坂すみれ', '林勇', '內山夕實', '關根明良', '伊藤健太郎', '武田羅梨沙多胡', '川澄綾子', '諏訪彩花', '村上裕哉', '井上和彥', '赤崎千夏', '井上麻里奈', '赤羽根健治', '三木真一郎', '東山奈央', '生天目仁美', '野島健兒', '島崎信長', '青山桐子', '矢作紗友里', '古賀葵', '能登麻美子', '濱野大輝', '小山力也', '丹下櫻', '內田真禮', '福原綾香', '佳村はるか', '細谷佳正', '和氣あず未', '加瀨康之', '福原香織', '久保ユリカ', '拜真之介', '鈴木崚汰', '會沢紗彌', '田中涼子', '綠川光', '原紗友里', '朴璐美', '上村祐翔', '白井悠介', '原由實', '雨宮天', '山下誠一郎', '市來光弘', '豊永利行', '玉城仁菜', '浦和希', '山根綺', '加藤英美里', '恒松あゆみ', '喜多村英梨', '上田燿司', '加隈亞衣', '植田佳奈', '篠原侑', '大原さやか', 'ひと美', '神奈延年', '米澤圓', '小原好美', '小松昌平', '大塚剛央', '杜野まこ', '今井麻美', '長谷川育美', '井口裕香', '武內駿輔', '逢坂良太', '德井青空', '平田廣明', '檜山修之', '藤原夏海', '關智一', '桑島法子', '鈴村健一', '西明日香', '篠田みなみ', '岸尾だいすけ', '大坪由佳', 'こやまきみこ', '齋藤千和', '桐谷蝶々', '千葉繁', '三宅麻理惠', '早見沙織', '夏川椎菜', '前田剛', '沢城みゆき', '國立幸', '石見舞菜香', '黑木ほの香', '伊藤靜', '花江夏樹', '藤原貴弘', '成田劍', '花澤香菜', '小澤亞李', '立花慎之介', '大久保瑠美', '浪川大輔', '松岡禎丞', '蓮岳大', '森久保祥太郎', '蒼井翔太', '大橋彩香', '沼倉愛美', '小清水亞美', '山崎たくみ', '內田彩', '高橋英則', '青木瑠璃子', '吉永拓斗', '畠中祐', '田谷隼', '長繩まりあ', '齊藤壯馬', '竹內良太', '小野賢章', '佐原誠', '堀內賢雄', '福山潤', '峯田大夢', '宮下榮治', '前田佳織里', '皆口裕子', '佐武宇綺', '小岩井ことり', '雨宮夕夏', '遠藤綾', '菊池紗矢香', '戶松遙', '安野希世乃', '三澤紗千香', '水沢史繪', 'ゆきのさつき', '森田成一', '齋藤桃子', '伊藤かな惠', '安濟知佳', '代永翼', '津田美波', '洲崎綾', '島田敏', '田邊留依', '芹澤優', '淺沼晋太郎', '阿澄佳奈', '關俊彥', '伊波杏樹', '岡本信彥', '水島大宙', '立木文彥', '小林由美子', '町山芹菜', '鳥越まあや', '赤尾ひかる', '岡笑美保', '羊宮妃那', '木戶衣吹', '新谷真弓', '木島隆一', '本渡楓', 'うえだゆうじ', '小松史法', '丸山美紀', '河西健吾', '江原正士', '鈴木達央', '園部啟一', '高階俊嗣', '浜田賢二', '駒田航', '原田ひとみ', '高橋廣樹', '阿部敦', 'ファイルーズあい', '仲村宗悟', '大本真基子', '高木美佑', '岡部涼音', '高梨謙吾', '佐々木望', '內山昂輝', '稻田徹', '田澤茉純', '川崎芽衣子', '牧野由依', '豊口めぐみ', 'M‧A‧O', '三石琴乃', '中村悠一', '加藤將之', '茶風林', '梶裕貴', '深見梨加', '上田麗奈', '中博史', '野中藍', '羽多野涉', '森嶋秀太', '菅生隆之', '原田彩楓', '前田玲奈', '天崎滉平', '佐藤聰美', '大泊貴揮', ' 坂泰斗', '榎吉麻彌', '水樹奈々', '集貝はな', '高橋李依', '桐井大介', '柴田秀勝', '中島ヨシキ', '茅原實里', '山下大輝', '高森奈津美', '新垣樽助', '增田俊樹', '今野宏美', '藤田茜', '三宅健太', '江口拓也', '福圓美里', '矢野妃菜喜', '木野日菜', '首藤志奈', '井澤詩織', '佐藤拓也', '河瀨茉希', '中村繪里子', '梶原岳人', '杉山紀彰', '佳月大人', '田中理惠', '折笠愛', 'ささきのぞみ', '內田直哉', '下屋則子', '大西沙織', '久川綾', '阪口大助', '西山宏太朗', '內野孝聰', '立花理香', '富樫美鈴', '淺井孝行', '山本希望', '木內秀信', '高坂知也', '小林ゆう', '鶴岡聰', '內田夕夜', 'GEMS COMPANY 長谷みこと', '矢野 獎吾', '白石涼子', '影山燈', '小林千晃', '伊藤節生', '榎木淳彌', '田中正彥', 'Lynn', '八代拓', '南條愛乃', '下野紘', '長妻樹里', '速水獎', '小市真琴', '井口祐一', '久保田未夢', '中尾隆聖', '千菅春香', '井澤美香子', '立花日菜', '若本規夫', '沢海陽子', '寸石和弘', 'てらそままさき', '甲斐田裕子', '三森すずこ', '桃井はるこ', '照井春佳', '相坂優歌', '大谷育江', 'たかはし智秋', '石川英郎', '高山みなみ', '森なな子', '久野美笑', '潘惠子', '緒方惠美', '興津和幸', '若林直美', '嶋村侑', '後藤沙緒里', '小形滿', '白石稔', '齋賀みつき', '水田わさび', '宮本充', '石井マーク', '田中あいみ', '森谷里美', '伊東健人', 'かないみか', '井上倫宏', '布施川一寬', '古川慎', '高尾奏音', '福間竣兵', '青木遙', '諏訪ななか', '南央美', '巽悠衣子', '遠藤大智', '木村珠莉', '小林親弘', '榊原良子', '山寺宏一', '齊藤朱夏', '中原麻衣', '高野麻美', '淺見春那', '樫井笙人', '林原めぐみ', '小宮有紗', '降幡愛', '種田梨沙', '山田菜々', '近藤孝行', '斧アツシ', '松岡由貴', '廣瀨大介', '大河元氣', '又吉愛', '大友龍三郎', '鈴木愛奈', '清水理沙', '中谷一博', '長江里加', '黑田崇矢', '木村昴', '梅原裕一郎', '小林愛香', '川田紳司', '小松未可子', '相馬康一', '高槻かなこ', 'もこう', '瀨戶麻沙美', '櫻川めぐ', '田中ちえ美', '逢田梨香子', '山路和弘', '吉野裕行', '原優子', '竹本英史', '池田秀一', 'けそポテト', '石川由依', '淺利遼太', '大川透', '草の人', '國府田マリ子', '木村良平', 'となりの坂田。', '末柄里惠', '澤城千春', '天月', '益山武明', '遠近孝一', '最上嗣生', '藤井ゆきよ', '小島幸子', '三浦祥朗', '上田瞳', '小野大輔', '高野麻里佳', '橫島亘', '小杉十郎太', 'はねむーん', '岩永洋昭', '淵崎ゆり子', '宇垣秀成', '大塚明夫', 'Machico', '田中敦子', '高垣彩陽', '東地宏樹', 'そらる', '銀河万丈', '皆川純子', '田中 誠人', '梁田清之']

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
    if clan:
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
    for i in deck_name:
        for name in deck_name[i]:
            if name in text:
                search_deck = i
                break
    if search_deck:
        if deck_num[search_deck]:
            for deck in decks:
                if deck["deck_name"] == search_deck:
                    result.append(deck)
            return result,flag
        else:return -2 + flag,flag
    else:return -4 + flag,flag