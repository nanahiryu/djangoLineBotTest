from email.mime import image
from re import template
from django.shortcuts import render
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi
from linebot.models import ImageSendMessage, TextSendMessage, TemplateSendMessage, ButtonsTemplate
from linebot.exceptions import LineBotApiError

import environ

env = environ.Env()

ACCESSTOKEN = env("ACCESSTOKEN")

line_bot_api = LineBotApi(ACCESSTOKEN)

@csrf_exempt
def index(request):
    if request.method == 'POST':
        request = json.loads(request.body.decode('utf-8'))
        data = request['events'][0]
        print(data)
        reply_token = data['replyToken']
        if 'message' in data.keys():
            message = data['message']['text']
            if message == '画像':
                res_context = ImageSendMessage(original_content_url=r"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTGwjQL1IJHjHO4p3Z16VSdNsVRzrTvIcbNW4FVLJgnoe7ZiACh&s", preview_image_url=r"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTGwjQL1IJHjHO4p3Z16VSdNsVRzrTvIcbNW4FVLJgnoe7ZiACh&s")
            
            elif message == 'シナリオ':
                actions = [
                    {
                        "type": "postback",
                        "label": "電気が流れる道筋（電気回路）",
                        "data": "init=0&scenario=1"
                    },
                    {
                        "type": "postback",
                        "label": "電流",
                        "data": "init=0&scenario=2"
                    },
                    {
                        "type": "postback",
                        "label": "電流",
                        "data": "init=0&scenario=3"
                    },
                    {
                        "type": "postback",
                        "label": "電圧",
                        "data": "init=0&scenario=4"
                    },
                ]
                res_context = TemplateSendMessage(
                    alt_text='buttons template',
                    template=ButtonsTemplate(text='どのシナリオが見たいかな？', actions=actions)
                    )
            else:
                res_context = TextSendMessage(text="それには答えられないわ...")
                
        # buttonのresponse.dataのjsonには'postback'というkeyが含まれます
        # そのためbuttonへの返答には以下の文が動きます
        if 'postback' in data.keys():
            # postbackに含まれるdataをqueryという辞書に入れていく処理
            # 例：data: "one=first&two=second" -> {one: first, two: second}
            query = {}
            temp_list = data['postback']['data'].split('&')
            for temp in temp_list:
                key, item = temp.split('=')
                query[key] = item
            # 辞書に入れる処理ここまで

            # シナリオを返します
            if 'init' in query.keys():
                if query['scenario'] == "1":
                    actions = [
                    {
                        "type": "postback",
                        "label": "うん",
                        "data": "scenario=1&state=0&next=1"
                    },
                ]
                    res_context = TemplateSendMessage(
                        alt_text='buttons template',
                        template=ButtonsTemplate(text='電化製品って電気がないと動かないって習ったよね？', actions=actions)
                        )
                else:
                    res_context = TextSendMessage(text=f'準備中です...')
                    
            if 'state' in query.keys():
                if query['scenario'] == "1":
                    if query['next'] == "1":
                        actions = [
                            {
                                "type": "postback",
                                "label": "電流",
                                "data": "scenario=1&state=1&next=2"
                            },
                            {
                                "type": "postback",
                                "label": "電圧",
                                "data": "scenario=1&state=1&next=3"
                            },
                        ]
                        res_context = TemplateSendMessage(
                            alt_text='buttons template',
                            template=ButtonsTemplate(text='「電気の流れ」のことって何て言うんだっけ？', actions=actions)
                            )
                    if query['next'] == '2':
                        res_context = TextSendMessage(text=f'電流ね！「電気」の「流れ」だから「電流」なんだろうね。ちょっとウケる')
                        try:
                            line_bot_api.reply_message(reply_token, res_context)
                        except LineBotApiError as e:
                            print(e)
                        actions = [
                            {
                                "type": "postback",
                                "label": "回路",
                                "data": "scenario=1&state=5&next=6"
                            },
                            {
                                "type": "postback",
                                "label": "回路図",
                                "data": "scenario=1&state=5&next=7"
                            },
                        ]
                        res_context = TemplateSendMessage(
                            alt_text='buttons template',
                            template=ButtonsTemplate(text='電流が流れるための道筋って...なんて呼ぶんだっけ？', actions=actions)
                            )
                    if query['next'] == '3':
                        actions = [
                            {
                                "type": "postback",
                                "label": "電流？",
                                "data": "scenario=1&state=3&next=4"
                            },
                        ]
                        res_context = TemplateSendMessage(
                            alt_text='buttons template',
                            template=ButtonsTemplate(text='あれ、電流だっけ？「電気」の「流れ」だから」...', actions=actions)
                            )
                    if query['next'] == '4':
                        res_context = TextSendMessage(text=f'電流だと思う！「電気」の「流れ」だから「電流」！')
                        try:
                            line_bot_api.reply_message(reply_token, res_context)
                        except LineBotApiError as e:
                            print(e)
                        actions = [
                            {
                                "type": "postback",
                                "label": "回路",
                                "data": "scenario=1&state=5&next=6"
                            },
                            {
                                "type": "postback",
                                "label": "回路図",
                                "data": "scenario=1&state=5&next=7"
                            },
                        ]
                        res_context = TemplateSendMessage(
                            alt_text='buttons template',
                            template=ButtonsTemplate(text='電流が流れるための道筋って...なんて呼ぶんだっけ？', actions=actions)
                            )
                    if query['next'] == '6' | '7':
                        res_context = TextSendMessage(text=f'準備中です...')
        try:
            line_bot_api.reply_message(reply_token, res_context)
        except LineBotApiError as e:
            print(e)

        return HttpResponse("ok")

