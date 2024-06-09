import json
import base64

MD_id = '102021217_1716818078'
MD_id1 = '102021217_1710070483'

def MD_gen(param,button):
    data = {
        'markdown':{
            'custom_template_id':MD_id,
            'params':[
                {'key':'name','values':[param[0]]},
                {'key':'img_size','values':[param[1]]},
                {'key':'img_url','values':[param[2]]},
                {'key':'hint_word','values':[param[3]]},
                {'key':'else','values':[param[4]]}
            ]
        },
        'keyboard':{'content':{'rows':button}}
    }
    raw_data = json.dumps(data,ensure_ascii=False).replace("\\r","\r")
    return f'[CQ:markdown,data=base64://{base64.b64encode(str(raw_data).encode("unicode_escape")).decode("utf-8")}]'

def MD_gen1(param,button):
    data = {
        'markdown':{
            'custom_template_id':MD_id,
            'params':[
                {'key':'text_1','values':[param[0]]},
                {'key':'text_2','values':[param[1]]},
                {'key':'text_3','values':[param[2]]},
            ]
        },
        'keyboard':{'content':{'rows':button}}
    }
    raw_data = json.dumps(data,ensure_ascii=False).replace("\\r","\r")
    return f'[CQ:markdown,data=base64://{base64.b64encode(str(raw_data).encode("unicode_escape")).decode("utf-8")}]'

def button_gen(is_enter,lable,data):
    return {"render_data": {"label": lable,"visited_label": lable,"style":1},
            "action": {"type": 2 ,"permission": {"type": 2,},"enter":is_enter,"unsupport_tips":"兼容文本","data": data}}

def link_button(lable,link):
    return {"render_data": {"label": lable,"visited_label": lable},
            "action": {"type": 0 ,"permission": {"type": 2,},"unsupport_tips":"兼容文本","data": link}}