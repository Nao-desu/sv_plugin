from ..info import clan2w
from ..config import GAME_TIME
from ..info import MOUDULE_PATH
from PIL import Image
from os.path import join
from io import BytesIO
import random,base64
from ..MDgen import *
from ...image_host import upload_img
from uuid import uuid4

async def guess_paint(bot,ev,limited,clan,answer):
    w1 = '指定' if limited else ''
    w2 = '' if not clan else clan2w[clan]
    url,size = await pic_corp(answer)
    button = [{"buttons":[button_gen(False,'我要回答','')]}]
    msg = MD_gen([f'猜猜这张图片来自哪张{w1}{w2}卡牌？',f'img#{size[0]}px #{size[1]}px',url,f'{GAME_TIME}秒后公布答案','艾特我+你的答案参与游戏'],button)
    await bot.send(ev,msg)

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
    url = await upload_img(uuid4().hex + '.jpg',buf)
    return url,(250,250)