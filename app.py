from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('o8hhFkgDyBJBIEWz21FASf4rDBirYtQM6Y35w32/H6ZRuUQfjReh0qlR2DjgSPiuAMDHUn4fi4VaAze1uMAIRML5FojHtWLQndVkXwEEuaWb7BhKHc2Gba3rQk1pwlZMJq7mSpeNu+y1Ac7YoaEzHQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('070ff662b2e2a008f07868bea5506d9f')


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
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
