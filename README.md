# SV-plugin

适用于[hoshino](https://github.com/Ice9Coffee/HoshinoBot)的影之诗插件合集
> 卡牌信息来自[shadowverse-portal](https://shadowverse-portal.com)  
> 卡牌原图和语音来自[SVGDB](https://svgdb.me/)  
> 部分数据来自[shadowversemaster](https://shadowversemaster.com/)  

## 本仓库链接

<https://github.com/Nao-desu/sv_index>

## 插件功能

### 卡牌信息查询

- `svcard id` 查询对应id的卡牌信息  
- `sv查卡 #条件 关键词` 查询卡牌信息，条件前要加#号进行区分,支持多条件,但是要在每个条件前都加#,关键词在卡牌名称与卡牌技能中匹配  
 支持的条件有:  
- `#3c` 指定费用为3  
- `#AOA` 指定卡包为遥久学园，也可用文字或文字简写(注意，token为单独的token卡包，不属于其附属卡的中)
- `#token` 指定为token卡  
- `#皇家` 指定职业为皇家  
- `#学园` 指定种类为学院  
- `#随从` 指定为随从卡  
- `#atk3` 指定攻击力为3  
- `#life3` 指定生命值为3  
- `#虹卡` 指定卡牌稀有度为传说
- `#指定`,`#指定系列` 指定为指定系列卡包
- `#333` 指定费用身材为333的卡牌(费用加身材一定要写全)
- `#小野友树` 指定cv为小野有树的卡牌

例如 `sv查卡 #aoa #皇 #323 #虹`可以精确查找到`校舍的黃昏‧莉夏與奈諾`  
(特别地`sv查卡 #鱼 #土之印`这种搜索会精确检索到类型为`全部`的`萬物見證者‧潔蒂絲`)
你也可以将条件和卡牌关键词混用  
例如 `sv查卡 #指定 李霞`也可以精确查找到`校舍的黃昏‧莉夏與奈諾`(注意这里的名字搜索只要拼音正确即可)  
> 当发现多张卡牌时，bot将给出最多20张检索卡牌的列表（按费用排序）以及卡牌的id，你可以使用`svcard id`来查看具体卡牌

### 抽卡

- `sv抽卡` 抽一包卡牌
- `sv十连` 抽十包卡牌
- `sv井` 抽一井卡牌
以上指令均需@bot触发  
默认抽最新卡包，可在指令后加卡包名或卡包ID抽指定卡包

### 二维码识别

当群内发送含世界服卡组二维码图片时，自动发送卡组信息

### 猜卡牌游戏

- `sv猜卡面` 猜猜bot随机发送的卡面的一小部分来自哪张影之诗卡牌
- `sv猜语音` 猜猜bot随机发送的语音来自哪张影之诗卡牌
- `重置游戏` 卡住时用此指令重置
默认为指定模式卡牌
在指令后添加`无限`可以猜所有卡牌
在指令后添加职业名可以猜特定职业卡牌

### 影之诗数据

- `Ratings` 查看Ratings统计数据
- `卡组一览` 查看所有卡组，指令后加无限可查看无限卡组一览
- `来一套` 来一套卡组，指令后加无限查询无限卡组

### 塔罗牌

- `塔罗牌` 抽一张塔罗牌，图片来自[影之诗《命运诸神》自制塔罗牌](https://www.bilibili.com/read/cv14931262/) 已授权
