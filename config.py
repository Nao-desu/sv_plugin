'''
插件仓库地址：https://github.com/Nao-desu/sv_plugin
作者： Nao_desu
下面的配置可以按需更改
'''

##是否自动更新数据
auto_update=True

#绘制卡牌信息时各职业边框颜色
clan_color = {0:(220,220,220),
              1:(54,84,27),
              2:(116,105,31),
              3:(33,80,118),
              4:(117,73,27),
              5:(71,26,108),
              6:(123,29,48),
              7:(128,118,94),
              8:(50,127,157)}

#绘制卡牌时文字颜色
text_color = (255,255,255)

#抽卡时高于此稀有度卡牌出现概率，单位万分之一，前七张(prob1)和第八张(prob2)概率不同
prob1 = {
    1:150,
    2:750,
    3:3250,
    4:10000
}
prob2 = {
    1:150,
    2:600,
    3:10000,
    4:10000
}

max_400 = 5#一天抽井的次数
max_coin = 10000#一天使用金币抽卡的数量

GAME_TIME = 60#猜卡牌小游戏回答时间