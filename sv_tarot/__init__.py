from hoshino import Service
import random,json,base64,datetime

tarot_help = """
[塔罗牌] 抽一张影之诗塔罗牌
*图片资源来自bili@南_某人
"""

cache_data = {
    "date" : str(datetime.date.today()),
    "data" :[]
}

sv = Service("sv_tarot")

name = {
    0:"【0】愚者(THE FOOL)",
    1:"【I】魔术师(THE MAGICIAN)",
    2:"【II】女祭司(THE HIGH PRIESTESS)",
    3:"【III】女皇(THE EMPRESS)",
    4:"【IV】皇帝(THE EMPEROR)",
    5:"【V】教皇(THE HIEROPHANT)",
    6:"【VI】恋人(THE LOVERS)",
    7:"【VII】战车(THE CHARIOT)",
    8:"【VIII】力量(STRENGTH)",
    9:"【IX】隐士(THE HERMIT)",
    10:"【X】命运之轮(THE WHEEL OF FORTUNE)",
    11:"【XI】正义(JUSTICE)",
    12:"【XII】倒吊人(THE HANGED MAN)",
    13:"【XIII】死神(DEATH)",
    14:"【XIV】节制(TEMPERANCE)",
    15:"【XV】恶魔(THE DEVIL)",
    16:"【XVI】高塔(THE TOWER)",
    17:"【XVII】星星(THE STAR)",
    18:"【XVIII】月亮(THE MOON)",
    19:"【XIX】太阳(THE SUN)",
    20:"【XX】审判(JUDGEMENT)",
    21:"【XXI】世界(THE WORLD)"
}

pos = {
    0:"正位",
    1:"逆位"
}

keyword = {
    0:{
        0:"新的起点，不能再等了，自由，好奇，本能，无意识，现在正是好时机，开始，开端，起源，清白，无辜，无罪，天真，纯真，单纯，自发性，自然，自由精神，不拘一格",
        1:"情绪低落，时机不对，陷入停顿，遭受失败，漫无目的的四处流浪，行为散漫，愚昧的行动退缩，自负，固执，轻率，鲁莽，大意，不顾一切，粗心大意，冒险，承担风险",
    },
    1:{
        0:"受好奇心驱使展开调查研究，具有独创性，具备发展潜力，展开新的计划并获得成功，幸福的开始，显现，表现，显化，表征，机智，足智多谋，智慧，丰富资源，控制力，影响力，操纵力，统治，政权，能力，机会，驱动，推动，迅速移动，快速前进，灵感",
        1:"犹豫未定，因学艺不精而败北，看待事物过于消极，易受骗上当，遇事言而不行，操作，操纵，操控，推拿，处理，计划不周，人算不如天算，百密一疏，怀才不遇，有潜力",
    },
    2:{
        0:"有知己的，文静的，知性的，理性的，富有研究精神，具备敏锐的洞察力，有正确的时机或人将出现的预感，直觉，第六感，天启，启示，天象，圣女，气质，女神，潜意识",
        1:"粗心大意，易紧张，神经质，意气用事，因精神压抑以致歇斯底里，缺乏理性思维能力，秘密，机密，诀窍，秘诀，奥秘，奥妙，没感觉，撤走，收回，取回，不再参加，退出，提款，取款，寂静，安全，无声，沉默，缄默，默不作声，缄口不谈，拒绝回答，压制，冷场",
    },
    3:{
        0:"优雅，富贵，女权主义，女性化，女人味，女性特质，美人，美物，好榜样，典型的例子，自然界，自在坦然，天性，本性，性格，养育，养护，培养，扶持，帮助，支持，滋长，助长，量产，丰盛，充裕，丰富",
        1:"困惑，轻浮，损失，缺乏上进心，爱慕虚荣，无灵感，依靠，依赖，依存，上瘾，性关系，炮友，堕落，附庸，跟班，被动",
    },
    4:{
        0:"魄力十足，万众瞩目，男性化，基本功扎实，富有责任感，充满阳刚之气，出众的领导才能，权力，威权，地位，职权，批准，授权，机构，大型组织，企业，旅馆，当权派，权势集团，权威人士，建立，创立，确立，结构，构造，精心组织，周密安排，形成体系，系统安排，父亲角色",
        1:"幼稚，寡欲，不负责任，率性妄为，蛮横霸道，缺乏治理能力，统治，支配，主宰，占有欲强，没有训练，没有训导，无纪律，风纪差，没有训练方法，行为准则，符合准则的行为，无自制力，不遵守纪律，不接受惩罚，没有处罚，自我控制能力差，没有严格要求自己，僵硬，缺乏灵活性，呆滞，较真",
    },
    5:{
        0:"值得信赖的，得到援助的，良好的建言者，有贡献的，心胸宽广的，有宗教情绪的，精神内在，智慧，才智，精明，明智，知识，学问，修士，修女，出家人，宗教信仰，遵从，遵守，传统，慈善机构",
        1:"失去信赖，多管闲事，过于依靠他人，心胸狭隘，被强迫倾销，孤立无援，个人信仰，看法，想法，自由，质疑权威，挑战现况，改变现在",
    },
    6:{
        0:"幸福的相遇，同心协力，情投意合，感情丰富，前途光明，坠入爱河，整理思绪，爱，热爱，慈爱，爱情，恋爱，喜好，喜爱，喜欢，很愿意，融洽，和睦，和声，和谐，协调，关系，联系，情爱关系，性爱关系，价值观，价值取向，选择，挑选，抉择，选择权，入选者，被选中",
        1:"伤离别，关系结束，无助，遭遇险阻，转移目标，爱好没有办法持久，无精打采，表里不一，易受诱惑，自爱，自恋，不协调，不和谐，不一致，失衡，不平衡，不公平，价值观不一致，价值观错位",
    },
    7:{
        0:"高效率，把握先机，以积极的心态面对事物，获得胜利，取得驾照，搬家，指挥，控制，掌管，支配，限制，限定，阻止蔓延，意志，成功，胜利，发财，成名，成功的人，必须要做，务必完成，决心，果断，坚定，决定，确定，规定，查明，测定，计算",
        1:"失控，发生意外，胡作非为，失败，止步不前，固执己见，注意力散漫，遇突发事件而不知所措，自律，自我约束，律己，自律能力，反对，反抗，对抗，对手，敌人，竞争者，没有方向，没有领导，反对派，在野党",
    },
    8:{
        0:"精神抖擞，不屈不挠，意志坚定，潜力十足，胆识过人，信念坚定，体力，力气，力量，强度，毅力，坚强决心，意志力量，勇气，勇敢，无畏，胆量，说服力，劝说，影响力，同情，怜悯",
        1:"精力不足，急躁不安，丧失信心，忍耐力不足，自私自大，内功，内在力量，自我怀疑，自我否定，不自信，精神不振，能力低下，兽性，原欲，靠本能处理问题，做事凭感觉",
    },
    9:{
        0:"自信，理智，脚踏实地，不喜形于色，中肯的建议，坚持不懈，沉着冷静，闭门静思，养精蓄锐，深刻反省，自我检查，自我纠正，自省，孤独，独自，独居，独立，单独，单身，孤苦伶仃，无依无靠，孤独，寂寞，内在引导行为，精神引导行为，谋定而后动",
        1:"口无遮拦，俗气，神经质，为人刻薄，行事不够理智，多疑，隔离状态，孤立状态，撤走，收回，取回，不再参加，退出组织",
    },
    10:{
        0:"把控时机，机会降临，转变期，意外的收获，当机立断，幸运降临，恢复原状，好运，因果报应，善恶有报，生命周期，生活周期，命运，天理，天命，天数，主宰事物的力量，命运之神，转折点",
        1:"判定错误，情绪低落，运气不佳，左右为难，稍安毋躁，一时的幸福，爽约，倒霉，霉运，真倒霉，运气不好，拒绝改变，反对改变，抗拒变革的心理，抗拒改革，变革阻力，循环终止，循环断裂",
    },
    11:{
        0:"老实，公证，为他人调解争端，维系平衡，兼顾事业与家庭（学业与恋情），爱好和平，公平，公正，公道，合理，公平合理，司法制度，法律制裁，审判，真相，实情，事实，真实情况，真实，真实性，真理，因果关系",
        1:"不公平，有始无终，以自己的意见去断定，事事不能两全，不均衡，不公平性，显失公平，不公，没有责任感，没有义务，不诚实，欺诈",
    },
    12:{
        0:"进退两难，牺牲，因祸得福，遭遇困难磨练以致心智成熟，以不同的角度看待事物，暂停，停顿，延长记号，暂停键，投降，被迫放弃，交出，屈服，屈从，交出，解雇，解聘，被动离职，新视野，新观点，新视角",
        1:"希望破灭，因私欲而受罚，做无用功，没有必要的付出，自我毁灭，缺乏实施能力，事如泡影，延时，延迟，延误，误点，反对，抵制，抗拒，抵抗，反抗，熄火，抛锚，故意拖延，拖住，拉锯战，无决断力，优柔寡断，自私自利",
    },
    13:{
        0:"失败，恶运连连，走进死胡同，绝望，遗失，没有办法逃离，无疾而终，努力成为泡影，有苦说不出，结尾，结局，结束，终结，最后部分，词尾，改变，变化，变更，变革，替代，转变，变迁，更迭，新阵代谢，替代物，过渡",
        1:"改变计划，变更形象，东山再起，走出低谷，脱胎换骨，勇于开拓，精神抖擞，拒绝改变，反对变革，不想结束，强行续命，内心净化，念头通达，境界提升",
    },
    14:{
        0:"进展顺利，为他人排解争端，整理思路与情绪，净化心灵，反复调研找寻关键所在，关注自我需求的同时兼顾他人意愿，勤于节俭，相互协助，保持平衡，立稳，相抵，抵消，同等重视，适中，合理，耐心，忍耐，毅力，坚忍，恒心，意图，目的，用途，目标，情势的需要，重要意义，有价值的意义，有意，打算，企图，决意",
        1:"缺乏自我调节的能力，开销过大，遗忘初衷，精力消耗殆尽，毫无节制，烦闷的说教，失衡，不平衡，心态失衡，不均衡，失调，超过，过度，过分，过多的量，超过的量，超额，额外，附加，自我修复，自愈，自疗，自我愈合，校验，调整",
    },
    15:{
        0:"受到拘束深感不安，卑躬屈膝，沦为欲望的俘虏，颓废的生活，隐瞒事实真相，遭遇诱惑的陷阱，固执己见，贪婪成性，自我投影，依恋，爱慕，信念，信仰，忠诚，拥护，上瘾，入迷，鬼迷心窍，限制，约束，性欲，性行为，约炮",
        1:"摆脱不良诱惑，与酒肉朋友断交，抛弃欲望，有走出困境的机会，摆脱束缚，重获自由，解除负担，能够表达自己的意志，释放，探索思想，贤者时间，思考内心中的阴暗，超然，超脱，冷漠，公正，客观，独立",
    },
    16:{
        0:"麻烦不断，遭遇逆境，遭受打击，原有信念崩溃，遭遇突发事件，多管闲事，与人发生纷争，骤变，剧变，激变，动乱，动荡，突然，没有征兆，混乱，乱套，启示，内幕显现，揭露秘密，苏醒，醒悟，觉醒，开悟，感到",
        1:"悬崖勒马，遭遇口舌之灾，发生内部纠纷，风暴前的寂静，个人转变，害怕转变，避灾，逃难，远离是非之地，远离是非之人，不立危墙之下，择良木而栖，情况紧急",
    },
    17:{
        0:"愿望得以实现，充满创造力，萌发灵感，理想主义者，前途光明，希望，期望，希望的东西，期望的事情，被寄予希望的，信任，相信，信心，意图，目的，用途，目标，情势的需要，意义重大，恢复，更新，重新开始，续约，续订，改进，复兴，振兴，灵性",
        1:"缺乏想象力，幻想幻灭，好高骛远，错失良机，固执己见，理想与现实没有办法兼顾，缺乏信心，信任不足，不可相信，绝望，失去希望，失去信心，切断，舍弃",
    },
    18:{
        0:"幻想，谎言，不安，动摇，迷惑，暧昧不清，重伤他人或为人中伤，顾及两边，优柔寡断，受人感化，没有办法发挥潜能，幻想，错觉，意淫，害怕，畏惧，惧怕，担心，担忧，恐怕，焦虑，忧虑，渴望，潜意识，直觉",
        1:"状况逐渐好转，时间可以冲淡一切，疑虑渐消，幸免遇害，排解恐惧，释放压力，镇定，心里没底，想不通，猜不透，看不清",
    },
    19:{
        0:"远景明朗，活力充沛，欲望强烈，得贵人相助，阳光普照，积极，确实如此，享乐，乐趣，快乐，嬉戏，逗乐，玩笑，温暖，热情，友情，成功，胜利，发财，成名，活力，激情",
        1:"意志消沉，约会取消，情绪低落，事事没有办法持久，性格不开朗，感到无助，生活不稳定，孩子气，情绪低落，消极，慵懒，冷漠，无所谓，过度乐观",
    },
    20:{
        0:"复活的喜悦，命运好转，作品公然发表，得到好消息，信仰宗教，自信，判断，识别，看法，意见，评价，判决，裁决，新生，复活，复兴，再生，心声，赦罪，赦免，无罪",
        1:"一蹶不振，尚未开始便已结束，犹豫未定，行为不妥，生活散漫，良心发现内心颇感罪恶，自我怀疑，没有把握，不确实，良心受到谴责，不予理睬，佯装未见，坏消息",
    },
    21:{
        0:"愿望达成，精神高昂，幸福时光，达到巅峰，到达目的地，获得成功，完成，结束，完成交易，完成交割，结合，整合，一体化，混合，融合，成就，成绩，才艺，技艺，专长，完成，长途行走，旅行，游历，转送，传播，不变质，长途运输",
        1:"没有办法全身心地投入，杞人忧天，事事不顺，不安现状，情绪低迷，思维颇显幼稚，寻求自我完整，晚点，迟到，延误，耽误，延迟，延期，推迟，走捷径，跳过，未完成，失败",
    }
}

#848x1024
link = {
    0:{
        0:"https://i0.hdslb.com/bfs/article/05a91e270348864406c477d7430ba9de7081dac6.jpg",
        1:"https://i0.hdslb.com/bfs/article/0bb03c9c03ea13fb34757bb62f5028f94a8e1d05.jpg"
    },
    1:{
        0:"https://i0.hdslb.com/bfs/article/a09ba647afb7a1370e5dcb2436abdcf40a4ccb08.jpg",
        1:"https://i0.hdslb.com/bfs/article/9df7d975299286c42c4d01693d032cc5432f4ca6.jpg"
    },
    2:{
        0:"https://i0.hdslb.com/bfs/article/cf51062721edd45a2d539e65161483b2f4c8cf58.jpg",
        1:"https://i0.hdslb.com/bfs/article/273140615b2b6dafe30ff9077ecefe691dfa1a60.jpg"
    },
    3:{
        0:"https://i0.hdslb.com/bfs/article/458c331992c793aa92ac7b016af0bfef5a6da117.jpg",
        1:"https://i0.hdslb.com/bfs/article/77e35640dc29fd82c23eb3245af63c8ad704f09c.jpg"
    },
    4:{
        0:"https://i0.hdslb.com/bfs/article/e05715ac76283ea7412c1264ea79976c470354d8.jpg",
        1:"https://i0.hdslb.com/bfs/article/c5a2e0b53b7f98c85543c3d8cf189317d5a5c21c.jpg"
    },
    5:{
        0:"https://i0.hdslb.com/bfs/article/763c134e1e2296291f14042a08ada8df1f542e39.jpg",
        1:"https://i0.hdslb.com/bfs/article/a8d99f93d141e276d9666a10c3681ce2476be800.jpg"
    },
    6:{
        0:"https://i0.hdslb.com/bfs/article/154bec31f403c80cf771371efdf89b7f8bd1a3e3.jpg",
        1:"https://i0.hdslb.com/bfs/article/76a727275ac5aca26bdbd979b6abbfacb8c2d22b.jpg"
    },
    7:{
        0:"https://i0.hdslb.com/bfs/article/14241e28de46f4c009fd99c58882497406cbac29.jpg",
        1:"https://i0.hdslb.com/bfs/article/a2d504e82114bcb2ff50bb274fb44022e595f186.jpg"
    },
    8:{
        0:"https://i0.hdslb.com/bfs/article/86a3619537a901d3abf6030d1c7a7b4961f82b01.jpg",
        1:"https://i0.hdslb.com/bfs/article/5546a6cecd694f5efd79bfd9044abb5a8b2a4db4.jpg"
    },
    9:{
        0:"https://i0.hdslb.com/bfs/article/06e30e98170ddb08e7388575f2cd08e6de9c8ca0.jpg",
        1:"https://i0.hdslb.com/bfs/article/193c3df8781c23441d8ac9aa5bdb42a45f46d724.jpg"
    },
    10:{
        0:"https://i0.hdslb.com/bfs/article/164a38ea9c323c07f71ba6c87c430ea3b1d1a39e.jpg",
        1:"https://i0.hdslb.com/bfs/article/fb4a1f4d7beca54fe40ff934e84642edbbedd953.jpg"
    },
    11:{
        0:"https://i0.hdslb.com/bfs/article/8a254601e7f72fe7448ebc9341c156bca1d52dce.jpg",
        1:"https://i0.hdslb.com/bfs/article/540adbe66946d4e7b6b527cff5fac1ea009485fd.jpg"
    },
    12:{
        0:"https://i0.hdslb.com/bfs/article/90111ce038b5b4409e1597920c8598bd86e80c88.jpg",
        1:"https://i0.hdslb.com/bfs/article/e51fa322ead7df535b78cefb7daab9345f982edd.jpg"
    },
    13:{
        0:"https://i0.hdslb.com/bfs/article/a972326ad72fd160ca02abcf62d5b1dc3752c610.jpg",
        1:"https://i0.hdslb.com/bfs/article/f6ae70c2b21905e5e1912823f077aff6be0b9879.jpg"
    },
    14:{
        0:"https://i0.hdslb.com/bfs/article/4ae8c739504fc3525b45b8a25eeeb68c71af8e85.jpg",
        1:"https://i0.hdslb.com/bfs/article/d7edff6edbbf8a953fd41d8cd50caf36e2ec8040.jpg"
    },
    15:{
        0:"https://i0.hdslb.com/bfs/article/df25fd44e39ac861a7f817636ae178f0f135eebc.jpg",
        1:"https://i0.hdslb.com/bfs/article/ca340b2d96598875234c25ad4908a228a2d5283f.jpg"
    },
    16:{
        0:"https://i0.hdslb.com/bfs/article/9bcc97a229f7d6b15a5232c2d882c855cad1a396.jpg",
        1:"https://i0.hdslb.com/bfs/article/d64bc2fdbc6079ad0d0c222c9fc1f5e3dc9c8cfc.jpg"
    },
    17:{
        0:"https://i0.hdslb.com/bfs/article/eed6e62ac3467e926bb74102ff3dcc1bc9bc9070.jpg",
        1:"https://i0.hdslb.com/bfs/article/d6ebf77ef583e00393f71c1ed6021758c846698a.jpg"
    },
    18:{
        0:"https://i0.hdslb.com/bfs/article/74f8173c4d50636572f97728414d0d1db3080801.jpg",
        1:"https://i0.hdslb.com/bfs/article/6e165d955660ab121c508105335f40e0bd6bdd67.jpg"
    },
    19:{
        0:"https://i0.hdslb.com/bfs/article/c5eb1c8ebeb12e24ff3e46c4cfa6ca8170685e0f.jpg",
        1:"https://i0.hdslb.com/bfs/article/b4f335d634f894993a055fae84766586f58f040c.jpg"
    },
    20:{
        0:"https://i0.hdslb.com/bfs/article/fc633a58cda49610a156998677e2b48d3f4e0198.jpg",
        1:"https://i0.hdslb.com/bfs/article/96996d2647595b4bc721867d2445e6d0886858db.jpg"
    },
    21:{
        0:"https://i0.hdslb.com/bfs/article/719456cb16585305c98603c768647c3333780707.jpg",
        1:"https://i0.hdslb.com/bfs/article/c2c0282a73f48fb585a4bcebf251f590b2e5eb88.jpg"
    }
}

description = {
    0:{
        0:"其《全能》知曉絕對，沐浴於傲慢。  \r那「愚蠢」即為必然性。  \r與「無聊」所支配的她一起。  \r將「已知」的一切化為灰色。",
        1:"其《無知》的特權是，能獲得智慧。  \r那「純真」即為可能性。  \r去「挑戰」吧，與她一起。  \r而「未知」的財寶就在盡頭等待。"
    },
    1:{
        0:"──其名為《魔術師》，所示為《創造》。  \r自思考產生想像，從想像誕生構築。  \r滿懷自信做出的作品，才會蘊藏令人著迷的力量。",
        1:"──其為魔導的使役者，將思想形意具現的存在。  \r他的原動力是無邊無際、永不厭煩的上進心。  \r滿溢的自信不懂何謂碰壁，就只是持續不斷地創造。"
    },
    2:{
        0:"──其為《女祭司》，所示為《聰穎》。  \r她毫不動搖，看清這千變萬化的人世。  \r在何時何地的判斷，皆為千思萬慮後所做出的選擇。",
        1:"──其為聖職者，向人們宣揚啟示的存在。  \r遵從自己的決定，為迷途眾生展現其信仰。  \r她所帶來的救贖，無疑是不贅的正確之事。"
    },
    3:{
        0:"──其名為《女帝》，所示為《母性》。  \r崇敬著憐愛、養育以及守護。  \r在慈愛中被養育的孩子們，將化為包覆敵意之盾。",
        1:"──其為孕育者，以慈愛懷抱一切的存在。  \r她對名為戰場的搖籃，傾注滿懷母性的眼神。  \r真正嚴峻的環境，才能養育出真正健壯的孩子。"
    },
    4:{
        0:"──其名為《皇帝》，所示為《權威》。  \r土塊即為僕臣，是忠實的使魔。以威嚴統率之。  \r伸手一指，便可築起一個魔導的王國。",
        1:"──其為支配者，以魔力統治一切的存在。  \r魔導具、詠唱皆為其僕人，皆能輕易地差遣與掌控。  \r集所有魔導之力於一身，化為成就霸業之基石。"
    },
    5:{
        0:"──其為《教皇》，所示為《慈悲》。  \r打開其內心門扉的鑰匙，僅有體諒。  \r奔向他身旁的，正是開啟門扉之人。",
        1:"──其為指導者，佇立於神聖領域的存在。  \r對違反法律者降下制裁。  \r但他並未遺忘溫柔，同樣給予被制裁者再起的機會。"
    },
    6:{
        0:"很渴望「比翼」的關係呢，屬於我的你。  \r賜予你「機緣」吧。我是《戀人》，掌管《相愛》。  \r若興起「風情」便無法分離，你將受那思慕吸引。  \r展現那「愛執」吧。你將會遠離孤獨的未來。",
        1:"想成為「連理」的共犯呢，屬於我的你。  \r聯繫起「奇遇」吧。我是《戀人》，掌管《誘惑》。  \r就算離「月意」而去，多少新伴侶我都能幫你找來。  \r展現那「染著」吧。你渴望什麼顏色的愛呢？"
    },
    7:{
        0:"汝為受載運的負荷，而「吾為」牽引的悍馬！  \r吾正是《戰車》！掌管「汝之」《直行》！  \r現在，戰場即為筆直之霸道！以「武器」裝飾之道！  \r那麼，向前進吧！將「不屬實」之榮耀化為現實！",
        1:"《暴走》為純粹的疾馳。  \r汝僅須遠觀那結局。  \r吾為汝之武器，不屬實。  \r汝才是，吾之武器。"
    },
    8:{
        0:"請聽這個代替打招呼的咆哮！準備，嘎喔～！  \r呵呵。怎麼樣呀？人家是《力量》，掌管《活力》！  \r想變強、想要力量！我就是被那種願望召喚來的！  \r來，讓我幫你引導出那潛藏在你體內的勇氣！",
        1:"毫。  \r無。  \r《力量》。"
    },
    9:{
        0:"──其名為《隱者》，所示為《熟慮》。  \r慎重、冷靜且沉著，給予煩惱者建言。  \r深思後所告知他人的建言，簡單而有效。",
        1:"──其為沉思者，潛藏於草木之蔭的存在。  \r大樹、林蔭以及森林裡的所有一切，皆為其草堂。  \r他神出鬼沒，是位躲藏隱匿並遠離紛爭的哲人。"
    },
    10:{
        0:"……試看看吧。請問呀，主人啊主人。  \r我是《命運之輪》，掌管《幸運》，  \r可以帶給主人您美好又驚異的體驗。  \r也就是說，告訴我您的願望……",
        1:"……試試，您看。變成這樣了，主人啊主人。  \r我掌管《不幸》，也就是能將災難轉嫁給他人。  \r快看快看，好悲慘！托它的福，幸運跑來這裡了。  \r這也是主人的幸福對吧？那不然，換個願望……"
    },
    11:{
        0:"吾之友人啊，聆聽那聲吶喊吧。  \r我是《正義》，掌管《平等》。  \r自狹小的牢籠解放至藍天之際。  \r一視同仁的律法在此展翅高飛。",
        1:"吾之友人啊，聽進那絲細語吧。  \r我是《正義》，掌管《不公》。  \r既是清白之法，亦是彈劾之劍。  \r必須將所有邪惡之人斬草除根。"
    },
    12:{
        0:"《自我犧牲》這種事情，一點意義都沒有！  \r……你應該不會相信這種話吧？  \r我是《倒吊人》！掌管《自我犧牲》！  \r顛倒，欺騙，完全相反！",
        1:"顛倒，欺騙，完全相反！  \r什麼是真實，什麼是謊言，都是由自己決定！  \r……被這樣講的時候可別相信喔？你要連我也懷疑！  \r世間一切都不過是瑣事！有你的《自我滿足》就好！"
    },
    13:{
        0:"──其名為《死神》，所示為《轉變》。  \r以生的不確定性來克服死的苦難。  \r命運的潛移，默化來自四面八方的阻礙。",
        1:"──其為搬運者，降下不可避死亡的存在。  \r死亡不分外表、不論貴賤，不會放過任何生命。  \r那馬蹄會造訪一切眾生，一視同仁地使之化為蒼白。"
    },
    14:{
        0:"連真理也毫無用處。現在，你的世界已被翻新。  \r我正是《節制》，掌管《節儉》。  \r因為有所必要而追求，  \r真。",
        1:"請用你的眼觀察，這滿溢無用與無謂的世界。  \r有其必要的是心臟鼓動、活著。  \r愛、憤怒及悲傷皆是，  \r無。"
    },
    15:{
        0:"──其為《惡魔》，所示為《暴力》。  \r私慾，刺激。不論理由如何，皆肯定暴虐之存在。  \r伴隨著苦痛，帶來痛楚，奪去其追求之物。",
        1:"──其為災厄，欲求不止且狂暴的存在。  \r那對翅膀及其僕從，皆為在肆虐後所奪取之物。  \r以自己的苦痛為由，不斷給予他人痛楚。"
    },
    16:{
        0:"──其為《塔》，所示為《崩壞》。  \r他所前行之處災害四起，慘劇之雷將性命一分為二。  \r若將恐懼埋於瓦礫之中，至少能洗刷這屈辱吧。",
        1:"──其為破壞者，訕笑並高展龍翼的存在。  \r將赤紅雷電環繞於身，散播著毀壞及慘劇。  \r愉悅與快感，使龍人為了折磨他人而揮舞利爪。"
    },
    17:{
        0:"──其名為《星》，所示為《希望》。  \r她賜予懷抱願望的開拓者無數的光芒。  \r而散落在虛空的無數星光，將化為點亮希望的燈火。",
        1:"──其為虛空之主，俯瞰著大地運行的存在。  \r她掌管星之光芒，自天上照耀而不出手援助。  \r僅微笑著遠望那受其光芒所輝映之人。"
    },
    18:{
        0:"──其為《月亮》，所示為《不安》。  \r現身於懼怕的人身旁，將自己的身軀用於防備。  \r即便她年幼且尚未成熟，仍是隻吞噬膽怯的野獸。",
        1:"──其為防備者，將恐懼踐踏在地的存在。  \r雖然幼小卻勇敢的她，於月光下兇猛地咆哮。  \r在認定的主人面前，狼人即是獨一無二的守衛。"
    },
    19:{
        0:"──其名為《太陽》，所示為《成就》。  \r升起的太陽毫無困惑，化為滿溢活力之日輪。  \r光燦的太陽連陰影處亦會照耀，  \r沒有事物會無為而逝。",
        1:"──其為喚來豐收者，成就出顯赫發展的存在。  \r龍尾若歡喜地擺動，吉兆之日便會升起。  \r沐浴於龍之聖光者，將獲得幸福氣息的吹拂。"
    },
    20:{
        0:"──其為《審判》，所示為《復活》。  \r修正狀態，孤獨地調整。小動物們隨心所欲地玩耍。  \r雖然那裡沒有任何人的助力，  \r但是總有一天也夠修復破損。",
        1:"──其為調律者。將一切恢復原狀的存在。  \r等待救援實在無聊。靜待時機也相當無趣。  \r能借助的幫手不存在任何一處，  \r只能靠自己來傳達。"
    },
    21:{
        0:"吾之《世界》為掌。  \r管理《完成》，汝，以及無法逃離之創世。",
        1:"終結即《未完》，創世之預兆。  \r一切皆在《世界》的掌握之中。"
    }
}

async def MDgen(id,po,ev) -> str:
    data = {
        "markdown":{
            "custom_template_id": "102021217_1708318285",
            "params":[
                {
                    "key":"text_1",
                    "values":[f"<@{ev.real_user_id}>今日的塔罗牌是：  \r{name[id]}({pos[po]})   \r"]
                },
                {
                    "key":"text_2",
                    "values":[keyword[id][po]]
                },
                {
                    "key":"img_dec",
                    "values":["img#848px #1024px"]
                },
                {
                    "key":"img_url",
                    "values":[link[id][po]]
                },
                {
                    "key":"text_4",
                    "values":[description[id][po]]
                }
            ]
        },        
        "keyboard": {
            "content" :{
                "rows": [
                    {
                        "buttons": [
                            {
                                "id": "1",
                                "render_data": {
                                    "label": "我也要抽",
                                    "visited_label": "我也要抽"
                                },
                                "action": {
                                    "type": 2,
                                    "permission": {
                                        "type": 2,
                                    },
                                    "enter":True,
                                    "unsupport_tips": "兼容文本",
                                    "data": "塔罗牌",
                                    "at_bot_show_channel_list": True
                                }
                            }
                        ]
                    }
                ]
            }
        }
    }
    raw_data = json.dumps(data,ensure_ascii=False).replace("\\r","\r")
    return f'[CQ:markdown,data=base64://{base64.b64encode(str(raw_data).encode("unicode_escape")).decode("utf-8")}]'

@sv.on_fullmatch('塔罗牌')
async def tarot(bot,ev):
    global cache_data
    if cache_data["date"] != str(datetime.date.today()):
        cache_data = {
        "date" : str(datetime.date.today()),
        "data" : {}
        }
    if ev.real_user_id in cache_data["data"]:
            t_id = cache_data["data"][ev.real_user_id]["id"]
            t_pos = cache_data["data"][ev.real_user_id]["pos"]
    else:
        t_id = random.randint(0,21)
        t_pos = random.randint(0,1)
        cache_data["data"][ev.real_user_id]["id"] = t_id
        cache_data["data"][ev.real_user_id]["pos"] = t_pos
    msg = await MDgen(t_id,t_pos,ev)
    await bot.send(ev,msg)
    return