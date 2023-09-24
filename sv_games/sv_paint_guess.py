from ..info import clan2w
from ..config import GAME_TIME
from ..info import MOUDULE_PATH
from PIL import Image
from os.path import join
from io import BytesIO
import random,base64

async def guess_paint(bot,ev,limited,clan,answer):
    w1 = '指定' if limited else ''
    w2 = '' if not clan else clan2w[clan]
    msg = pic_corp(answer)
    await bot.send(ev,f'猜猜这张图片来自哪张{w1}{w2}卡牌?\n{GAME_TIME}秒后公布答案\n{msg}')

def pic_corp(answer):
    """
    随机裁剪
    """
    img = Image.open(join(MOUDULE_PATH,f'img/full/{answer}0.png'))
    w, h = img.size
    x = random.randint(0, w - 100)
    y = random.randint(0, h - 100)
    region = img.crop((x, y, x + 250, y + 250))
    region = region.convert('RGB')
    buf = BytesIO()
    region.save(buf, format='JPEG')
    base64_str = f'base64://{base64.b64encode(buf.getvalue()).decode()}'
    return f'[CQ:image,file={base64_str}]'