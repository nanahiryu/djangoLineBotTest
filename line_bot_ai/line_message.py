from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import urllib.request
import json

with open('line.json') as line:
  line_json = json.load(line)
ACCESSTOKEN = line_json["ACCESSTOKEN"]

# エンドポイントに関してはhttps://developers.line.biz/ja/reference/messaging-api/#messagesにあります
REPLY_ENDPOINT_URL = "https://api.line.me/v2/bot/message/reply"

HEADER = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + ACCESSTOKEN
}

class LineMessage():
    def __init__(self, res_image):
        # res_imageが入ってくる
        self.messages = res_image

    def reply(self, reply_token):
        body = {
            'replyToken': reply_token,
            'messages': self.messages,
        }
        print(body)
        req = urllib.request.Request(REPLY_ENDPOINT_URL, json.dumps(body).encode(), HEADER)
        print(urllib.request.urlopen(req))
        try:
            with urllib.request.urlopen(req) as res:
                print(res)
                body = res.read()
        except urllib.error.HTTPError as err:
            print(err)
        except urllib.error.URLError as err:
            print(err.reason)