import re
from PIL import Image
from io import BytesIO
from hoshino import aiorequests
from pyzbar.pyzbar import decode
from ..info import hashToID

async def get_pic(ev) -> list:
    """
    下载消息中的图片
    """
    pic = []
    match = re.findall(r'(\[CQ:image,file=.*?,url=.*?\])', str(ev.message))
    if not match:
        return pic
    for cq in match:
        url = re.search(r"\[CQ:image,file=(.*),url=(.*)\]", cq).group(2)
        resp = await aiorequests.get(url)
        resp_cont = await resp.content
        pic.append(Image.open(BytesIO(resp_cont)).convert("RGBA"))
    return pic

async def check_QR(pic:list)->list:
    """
    查找所有符合条件的二维码,返回卡组
    [{'clan':int,'deck':list}]
    """
    decks = []
    for img in pic:
        decode_list = decode(img)
        if not decode_list:
            continue
        for decoded in decode_list:
            data = decoded.data
            if data.startswith(b'https://shadowverse-portal.com/deck/1.'):
                data = data.replace(b'https://shadowverse-portal.com/deck/1.', b'').split('?')[0]
            else:
                continue
            cardlist_hash = data.decode('utf-8').split(".")
            if len(cardlist_hash) != 41:
                continue
            cardlist = [hashToID(hash) for hash in cardlist_hash[1:]]
            decks.append({'clan':int(cardlist_hash[0]),'deck':cardlist})
    return decks