from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
#from linebot.models import TemplateSendMessage, ButtonsTemplate, PostbackTemplateAction, MessageTemplateAction, URITemplateAction

import song_crawler

app = Flask(__name__)

line_bot_api = LineBotApi('dzMHXFwU0FbiK7Ct+zLK80AgIt3wHV7trwSdsh+EjSKNW8vTir0fhCP6qRsqLWjl/UxiiqECfBK6AfHe0htI/Ksqz0DQLAGBoZZnsLG7lgXlHSvG7gd6yW2LT7K5qbXl4fQ4f3X+YCWlfXPv/vptTwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('18305b046cb7b77b860f4381569cafd3')

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text =="貼圖":
        print("貼圖")
        line_bot_api.reply_message(event.reply_token,StickerSendMessage(package_id=1, sticker_id=10))
    elif event.message.text == "歌曲排行":
        buttons_template_message = TemplateSendMessage(
            alt_text='Buttons template',
            template=ButtonsTemplate(
                thumbnail_image_url='https://example.com/image.jpg',
                title='歌曲排行',
                text='請選擇',
                actions=[
                    MessageAction(
                        label='中文歌曲排行',
                        text='中文歌曲排行'                        
                    ),
                    MessageAction(
                        label='西洋歌曲排行',
                        text='西洋歌曲排行'
                    ),
                    MessageAction(
                        label='日亞歌曲排行',
                        text='日亞歌曲排行'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
    elif event.message.text == "中文歌曲排行":
        rank=song_crawler.ranking()
        rankCh='\n'.join(rank[:11])
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=rankCh))
    elif event.message.text == "西洋歌曲排行":
        rank=song_crawler.ranking()
        rankwestern='\n'.join(rank[11:22])
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=rankwestern))
    elif event.message.text == "日亞歌曲排行":
        rank=song_crawler.ranking()
        rankNEA='\n'.join(rank[-11:])
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=rankNEA))
    else:
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run(port=9000,debug =True)
