from email.mime import image
from django.shortcuts import render
from django.http import HttpResponse
import json
from django.views.decorators.csrf import csrf_exempt

from linebot import LineBotApi
from linebot.models import ImageSendMessage
from linebot.exceptions import LineBotApiError

import json

with open('line.json') as line:
  line_json = json.load(line)
ACCESSTOKEN = line_json["ACCESSTOKEN"]

line_bot_api = LineBotApi(ACCESSTOKEN)

@csrf_exempt
def index(request):
    if request.method == 'POST':
        request = json.loads(request.body.decode('utf-8'))
        data = request['events'][0]
        message = data['message']
        reply_token = data['replyToken']
        if message == 'random':
            res_image = ImageSendMessage(original_content_url="https://unsplash.it/630/400", preview_image_url="https://unsplash.it/630/400")
        else:
            res_image = ImageSendMessage(original_content_url="https://i.pximg.net/c/600x600/img-master/img/2017/06/30/21/10/14/63636005_p0_master1200.jpg", preview_image_url="https://i.pximg.net/c/600x600/img-master/img/2017/06/30/21/10/14/63636005_p0_master1200.jpg")

        try:
            line_bot_api.reply_message(reply_token, res_image)
        except LineBotApiError as e:
            print(e)

        return HttpResponse("ok")

