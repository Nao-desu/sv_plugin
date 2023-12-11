from ..info import find_decks
from .img_gen import deck_img_gen
from io import BytesIO
import random,base64

async def get_deck_data(text):
    decks = find_decks(text)
    if decks:
        img = deck_img_gen(random.choice(decks))
        buf = BytesIO()
        img.save(buf, format='JPEG')
        base64_str = f'base64://{base64.b64encode(buf.getvalue()).decode()}'
        msg = f'[CQ:image,file={base64_str}]'
        return msg,len(decks)
    else:
        msg = ''
        return msg,0