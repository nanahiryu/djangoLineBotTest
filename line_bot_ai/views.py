from email.mime import image
from django.shortcuts import render
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi
from linebot.models import ImageSendMessage
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
        message = data['message']['text']
        reply_token = data['replyToken']
        if message == '正解':
            res_image = ImageSendMessage(original_content_url=r"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTGwjQL1IJHjHO4p3Z16VSdNsVRzrTvIcbNW4FVLJgnoe7ZiACh&s", preview_image_url=r"https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTGwjQL1IJHjHO4p3Z16VSdNsVRzrTvIcbNW4FVLJgnoe7ZiACh&s")
        else:
            res_image = ImageSendMessage(original_content_url=r"https://2.bp.blogspot.com/-b8RGYZ3IXX4/Vf-aJng1qzI/AAAAAAAAyDo/pTdU_3xTK0w/s400/dame_man.png", preview_image_url=r"https://2.bp.blogspot.com/-b8RGYZ3IXX4/Vf-aJng1qzI/AAAAAAAAyDo/pTdU_3xTK0w/s400/dame_man.png")

        try:
            line_bot_api.reply_message(reply_token, res_image)
            print(message)
            print(res_image)
        except LineBotApiError as e:
            print(e)

        return HttpResponse("ok")

