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
            elif message == '選択肢':
                # 選択肢と送られるとボタンのテンプレートが出せます
                # labelがユーザーから見えている文字列, dataがそのボタンが押されたときにサーバーに返ってくる文字列になります
                actions = [
                    {
                        "type": "postback",
                        "label": "山",
                        "data": "event=journey&action=mountain"
                    },
                    {
                        "type": "postback",
                        "label": "海",
                        "data": "event=journey&action=ocean"
                    },
                ]
                res_context = TemplateSendMessage(
                    alt_text='buttons template',
                    template=ButtonsTemplate(text='旅行にいくならどっちがいい...？', actions=actions)
                    )
            else:
                res_context = TextSendMessage(text="それには答えられないわ...")
                
        # buttonのresponse.dataのjsonには'postback'というkeyが含まれます
        # そのためbuttonへの返答には以下の文が動きます
        if 'postback' in data.keys():
            query = {}
            temp_list = data['postback']['data'].split('&')
            for temp in temp_list:
                key, item = temp.split('=')
                query[key] = item
            if data['postback']['data'] == 'event=journey&action=mountain':
                res_context = TextSendMessage(text=f'山楽しいよね event: {query["event"]} action: {query["action"]}')
            if data['postback']['data'] == 'event=journey&action=ocean':
                res_context = TextSendMessage(text=f'海楽しいよね event: {query["event"]} action: {query["action"]}')

        try:
            line_bot_api.reply_message(reply_token, res_context)
        except LineBotApiError as e:
            print(e)

        return HttpResponse("ok")

