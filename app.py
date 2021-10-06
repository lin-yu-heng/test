from flask import Flask, request, abort
from __future__ import print_function
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
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
    list1 = ['Uef0961ac3e279db333cbd9f168ed3cd3','U9cc0d9e3383c477dd19dceb3deaaddc8','333']
    list2 = ['z1','z2','z3']
    text=event.message.text
    user = event.source.user_id
    try:
        name=list1.index(user)
    except InvalidSignatureError:
        name="not find"
    if (text=="getId"):
        text=user
    elif (text=="1"):
        text=list2[name]+"今日工項"
    elif (text=="2"):
        text=list2[name]+"進度回報"
    else:
        text=docs()
    message = TextSendMessage(text)
    line_bot_api.reply_message(event.reply_token, message)
    
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/documents.readonly']

# The ID of a sample document.
DOCUMENT_ID = 'AIzaSyAuhYmNvewPz1LY2pszNMpxTjyMxI1KUik'

def docs():
    """Shows basic usage of the Docs API.
    Prints the title of a sample document.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('docs', 'v1', credentials=creds)

    # Retrieve the documents contents from the Docs service.
    document = service.documents().get(documentId=DOCUMENT_ID).execute()

    return('The title of the document is: {}'.format(document.get('title')))


import os.path
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
