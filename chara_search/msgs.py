import base64,json
from io import BytesIO
from PIL import Image
from uuid import uuid4
from ..image_host import upload_img

data1 = {
    "markdown":{
        "custom_template_id": "102021217_1708318285",
        "params":[
            {
                "key":"text_1",
                "values":[f"有不认识的角色吗？交给我就好啦  \r选择下方按钮+图片搜索角色  \r"]
            },
            {
                "key":"text_2",
                "values":[f"tips:新版qq长按输入框，选择-全屏输入-就可以在消息中添加图片啦"]
            },
            {
                "key":"img_dec",
                "values":["img#570px #384px"]
            },
            {
                "key":"img_url",
                "values":["https://img2.imgtp.com/2024/05/15/Dra6Z6YZ.jpg"]
            }
        ]
    },        
    "keyboard": {
        "content" :{
            "rows": [
                {
                    "buttons": [
                        {
                            "id": "1",
                            "render_data": {
                                "label": "动画角色",
                                "visited_label": "动画角色"
                            },
                            "action": {
                                "type": 2,
                                "permission": {
                                    "type": 2,
                                },
                                "unsupport_tips": "兼容文本",
                                "data": "动漫角色搜索"
                            }
                        },
                        {
                            "id": "1",
                            "render_data": {
                                "label": "gal角色",
                                "visited_label": "gal角色"
                            },
                            "action": {
                                "type": 2,
                                "permission": {
                                    "type": 2,
                                },
                                "unsupport_tips": "兼容文本",
                                "data": "gal角色搜索"
                            }
                        }
                    ]
                }
            ]
        }
    }
}
data2 = {
    "markdown":{
        "custom_template_id": "102021217_1708318285",
        "params":[
            {
                "key":"text_1",
                "values":[f"图片呢？图片哪去了？  \r"]
            },
            {
                "key":"text_2",
                "values":[f"tips:新版qq长按输入框，选择 -全屏输入-就可以在消息中添加图片啦"]
            },
            {
                "key":"img_dec",
                "values":["img#548px #304px"]
            },
            {
                "key":"img_url",
                "values":["https://img2.imgtp.com/2024/05/15/bG649JUr.jpg"]
            }
        ]
    },        
    "keyboard": {
        "content" :{
            "rows": [
                {
                    "buttons": [
                        {
                            "id": "1",
                            "render_data": {
                                "label": "动画角色",
                                "visited_label": "动画角色"
                            },
                            "action": {
                                "type": 2,
                                "permission": {
                                    "type": 2,
                                },
                                "unsupport_tips": "兼容文本",
                                "data": "动漫角色搜索"
                            }
                        },
                        {
                            "id": "1",
                            "render_data": {
                                "label": "gal角色",
                                "visited_label": "gal角色"
                            },
                            "action": {
                                "type": 2,
                                "permission": {
                                    "type": 2,
                                },
                                "unsupport_tips": "兼容文本",
                                "data": "gal角色搜索"
                            }
                        }
                    ]
                }
            ]
        }
    }
}
raw_csh_msg = base64.b64encode(str(json.dumps(data1,ensure_ascii=False).replace("\\r","\r")).encode("unicode_escape")).decode("utf-8")
raw_bakaga_omae = base64.b64encode(str(json.dumps(data2,ensure_ascii=False).replace("\\r","\r")).encode("unicode_escape")).decode("utf-8")
csh_msg = f'[CQ:markdown,data=base64://{raw_csh_msg}]'
bakaga_omae = f'[CQ:markdown,data=base64://{raw_bakaga_omae}]'

async def MD_gen(name,aname,prob,x,y,url):
    data1 = {
    "markdown":{
        "custom_template_id": "102021217_1708318285",
        "params":[
            {
                "key":"text_1",
                "values":[f"{name}  \r"]
            },
            {
                "key":"text_2",
                "values":[f"来自：{aname}  \r置信度：{prob}"]
            },
            {
                "key":"img_dec",
                "values":[f"img#{x}px #{y}px"]
            },
            {
                "key":"img_url",
                "values":[url]
            }
        ]
    },        
    "keyboard": {
        "content" :{
            "rows": [
                {
                    "buttons": [
                        {
                            "id": "1",
                            "render_data": {
                                "label": "搜动画",
                                "visited_label": "搜动画"
                            },
                            "action": {
                                "type": 2,
                                "permission": {
                                    "type": 2,
                                },
                                "unsupport_tips": "兼容文本",
                                "data": "动漫角色搜索"
                            }
                        },
                        {
                            "id": "1",
                            "render_data": {
                                "label": "搜gal",
                                "visited_label": "搜gal"
                            },
                            "action": {
                                "type": 2,
                                "permission": {
                                    "type": 2,
                                },
                                "unsupport_tips": "兼容文本",
                                "data": "gal角色搜索"
                            }
                        }
                    ]
                }
            ]
        }
    }
}
    return

async def img_upload(pic,box):
    img = Image.open(pic)
    x,y = img.size()
    box1 = [int(box[0]*x),int(box[1]*y),int(box[2]*x),int(box[3]*y)]
    img = img.crop(box)
    img.convert("RGB")
    x1,y1 = img.size()
    buf = BytesIO()
    img.save(buf,"JPEG")
    url = await upload_img(uuid4().hex,buf)
    return url,x1,y1

async def result_msg(data,pic,ev,bot):
    if len(data) == 1:
        if data[0]["data"]:
            for i in data[0]["data"]:
                name = i["name"]
                aname = i["cartoonname"]
                prob = round(i["acc_percent"],3)
                img_url,x,y = await img_upload(pic,i["box"])
                msg = MD_gen(name,aname,prob,x,y,img_url)
                await bot.send(ev,msg)
        else:await bot.send(ev,"未检出图中任何角色")
    else:
        if data[0]["data"]:
            for i in range(0,len(data[0]["data"])):
                m = 0
                if data[0]["data"][i]["acc_percent"] < data[1]["data"][i]["acc_percent"]:
                    m = 1
                name = data[m]["data"][i]["name"]
                aname = data[m]["data"][i]["cartoonname"]
                prob = round(data[m]["data"][i]["acc_percent"],3)
                img_url,x,y = await img_upload(pic,data[m]["data"][i]["box"])
                msg = MD_gen(name,aname,prob,x,y,img_url)
                await bot.send(ev,msg)
        else:await bot.send(ev,"未检出图中任何角色")                
    return