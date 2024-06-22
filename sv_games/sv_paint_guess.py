from ..info import clan2w
from ..config import GAME_TIME
from ..info import MOUDULE_PATH
from PIL import Image
from os.path import join
from io import BytesIO
import random,base64
from ..MDgen import *

async def guess_paint(bot,ev,limited,clan,answer):
    w1 = '指定' if limited else ''
    w2 = '' if not clan else clan2w[clan]
    img = await pic_corp(answer)
    button = [{"buttons":[button_gen(False,'我要回答','')]}]
    msg = MD_gen1([f'猜猜这张图片来自哪张{w1}{w2}卡牌？',f'{GAME_TIME}秒后公布答案  \r','艾特我+你的答案参与游戏'],button)
    _send1 = await bot.send(ev,msg)
    _send2 = await bot.send(ev,img)
    return _send1["message_id"],_send2["message_id"]

async def pic_corp(answer):
    """
    随机裁剪
    """
    img = Image.open(join(MOUDULE_PATH,f'img/full/{answer}0.png'))
    w, h = img.size
    x = random.randint(0, w - 250)
    y = random.randint(0, h - 250)
    region = img.crop((x, y, x + 250, y + 250))
    region = region.convert('RGB')
    buf = BytesIO()
    region.save(buf, format='JPEG')
    base64_str = f'base64://{base64.b64encode(buf.getvalue()).decode()}'
    return f'[CQ:image,file={base64_str}]'