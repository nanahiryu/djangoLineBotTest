# djangoLineBotTest

## ローカルに開発環境を作る
1. 作業したいディレクトリで`git clone https://github.com/nanahiryu/djangoLineBotTest.git`
2. `cd `

## ローカルサーバーの立て方
1. プロジェクトディレクトリ(`manage.py`がある階層です)で`python manage.py runserver`
2. プロジェクトディレクトリで`ngrok http 8000`
3. line developerで作成したチャネルを開き、MessagingAPI設定のWebhookURLを書き換える([参考URL](https://qiita.com/njn0te/items/d717840dc2addeae6439))
