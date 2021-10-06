from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('o8hhFkgDyBJBIEWz21FASf4rDBirYtQM6Y35w32/H6ZRuUQfjReh0qlR2DjgSPiuAMDHUn4fi4VaAze1uMAIRML5FojHtWLQndVkXwEEuaWb7BhKHc2Gba3rQk1pwlZMJq7mSpeNu+y1Ac7YoaEzHQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('070ff662b2e2a008f07868bea5506d9f')

# 監聽所有來自 /callback 的 Post Request
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

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
#     profile = line_bot_api.get_profile()
    text=event.message.text
    if (text=="111"):
        message = TextSendMessage(event.user_id.text)
    else:
        message = TextSendMessage(text)
    line_bot_api.reply_message(event.reply_token, message)
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
