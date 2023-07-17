# SV-plugin

适用于[hoshino](https://github.com/Ice9Coffee/HoshinoBot)的影之诗插件合集
> 卡牌信息来自[shadowverse-portal](https://shadowverse-portal.com)

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

## 插件安装

1. git clone本插件（注：一定要git clone，不要下载压缩包，另外请确保git环境变量正常）：

    在 HoshinoBot\hoshino\modules 目录下使用以下命令拉取本项目

    ```shell
    git clone https://github.com/Nao-desu/sv_plugin.git
    ```

2. 安装依赖：

    到HoshinoBot\hoshino\modules\sv-plugin目录下，管理员方式打开powershell

    ```shell
    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple --user
    ```

3. 在 HoshinoBot\hoshino\config\ `__bot__.py` 文件的 MODULES_ON 加入 'sv-plugin'

4. 下载图片资源(约4GB)：

    - 启动update.bat，自动下载(更新图片资源时也要用到它,会自动删除能力变更的卡牌并更新)

5. 重启HoshinoBot
