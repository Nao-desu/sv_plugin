from ..info import get_ratings
from .img_gen import daily_ratings_img,ten_ratings_img
from io import BytesIO
import base64

async def get_ratings_data():
    data = get_ratings()
    time = list(data.keys())[0]
    img = await daily_ratings_img(time,data[time])
    img2 = await ten_ratings_img(data)
    img = img.convert('RGB')
    buf = BytesIO()
    img.save(buf, format='JPEG')
    base64_str = f'base64://{base64.b64encode(buf.getvalue()).decode()}'
    msg = f'[CQ:image,file={base64_str}]'
    img2 = img2.convert('RGB')
    buf2 = BytesIO()
    img2.save(buf2, format='JPEG')
    base64_str2 = f'base64://{base64.b64encode(buf2.getvalue()).decode()}'
    msg2 = f'[CQ:image,file={base64_str2}]'
    return msg,msg2