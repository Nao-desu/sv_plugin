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
    [{'clan':list,'deck':list}]
    """
    decks = []
    for img in pic:
        decode_list = decode(img)
        if not decode_list:
            continue
        for decoded in decode_list:
            deck = {'clan':[],'deck':[]}
            data = decoded.data
            if data.startswith(b'https://shadowverse-portal.com/'):
                #data = data.replace(b'https://shadowverse-portal.com/deck/1.', b'').split(b'?')[0]
                data = data.split(b'/')[-1].split(b'?')[0]
            else:
                continue
            cardlist_hash = data.decode('utf-8').split(".")[1:]
            for i in cardlist_hash:
                if len(i)==5:
                    break
                deck['clan'].append(int(i))
            deck['deck'] = [hashToID(hash) for hash in cardlist_hash[len(deck['clan']):]]
            # if len(cardlist_hash) != 41:
            #     continue
            #cardlist = [hashToID(hash) for hash in cardlist_hash[1:]]
            decks.append(deck)
    return decks