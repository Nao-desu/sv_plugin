from .img_gen import deck_img,all_deck_list_img
from io import BytesIO
import random,base64

async def get_deck_data(decks,flag):
    img = await deck_img(random.choice(decks),flag)
    buf = BytesIO()
    img.save(buf, format='JPEG')
    base64_str = f'base64://{base64.b64encode(buf.getvalue()).decode()}'
    msg = f'[CQ:image,file={base64_str}]'
    return msg

async def get_all_decks(flag):
    img = await all_deck_list_img(flag)
    buf = BytesIO()
    img.save(buf, format='JPEG')
    base64_str = f'base64://{base64.b64encode(buf.getvalue()).decode()}'
    msg = f'[CQ:image,file={base64_str}]'
    return msg