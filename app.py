from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os
import texthandlers
import logging

app = Flask(__name__)

app.logger.setLevel(logging.DEBUG)# using logging to solve the problem of no debugging messages

logging_handeler = logging.StreamHandler()
logging_handeler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
logging_handeler.setFormatter(formatter)

app.logger.addHandler(logging_handeler)

line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']#是用來驗證請求的有效性
    body = request.get_data(as_text=True)#獲取 HTTP 請求的資料主體（body） 以文字格式解析 後續處理方便
    app.logger.info("Request body: " + body)#請求的資料主體寫入 Flask 應用程式的日誌，方便後續查看
    print("Request body: " + body)
    try:
        handler.handle(body, signature)#資料主體和簽名傳handler處理 handler是WebhookHandler 物件 處理 LINE Bot 收到的事件。
    except InvalidSignatureError:#簽名驗證異常
        abort(400)
    return 'OK'

@app.route("/wake", methods=['POST'])
def i_alive():
    app.logger.info("waker fetching")
    my_variable = '<h1>I alive</h1>'
    return my_variable

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        if event.message.text.startswith("簽到 "):#簽到 座號 名字 課程ID 是否會遲到(0/1) 備註(選填)
            reply = texthandlers.dealer(app,"roll_call",event.message.text[3:]);
            app.logger.info("handler-簽到")
            #message = ImageSendMessage(original_content_url=reply, preview_image_url=reply)
            send_message(event,reply['status'],reply['content'])
        if event.message.text.startswith("開始簽到 "):#開始簽到 課程名稱
            reply = texthandlers.dealer(app,"start_roll_call",event.message.text[5:]);
            app.logger.info("handler-開始簽到")
            #message = ImageSendMessage(original_content_url=reply, preview_image_url=reply)
            send_message(event,reply['status'],reply['content'])
        if event.message.text.startswith("檢視簽到 "):#檢視簽到 ID
            reply = texthandlers.dealer(app,"view_roll_call",event.message.text[5:]);
            app.logger.info("")
            #message = ImageSendMessage(original_content_url=reply, preview_image_url=reply)
            send_message(event,reply['status'],reply['content'])
        if event.message.text.startswith("報分數 "):#報分數 名子 座號\n一項\n第一項成績  (過了"V"，沒過用"X")
            reply = texthandlers.dealer(app,"score_register",event.message.text[4:]);
            app.logger.info("")
            #message = ImageSendMessage(original_content_url=reply, preview_image_url=reply)
            send_message(event,reply['status'],reply['content'])
        if event.message.text.startswith("開始報成績\n"):#開始報成績/n項目一/n項目二
            reply = texthandlers.dealer(app,"start_score_register",event.message.text[6:]);
            app.logger.info("")
            #message = ImageSendMessage(original_content_url=reply, preview_image_url=reply)
            send_message(event,reply['status'],reply['content'])
        if event.message.text.startswith("檢視成績 "):#開始報成績/n項目一/n項目二
            reply = texthandlers.dealer(app,"view_score_register",event.message.text[5:]);
            app.logger.info("")
            #message = ImageSendMessage(original_content_url=reply, preview_image_url=reply)
            send_message(event,reply['status'],reply['content'])
        if event.message.text == "學生" or event.message.text == "老師":
            app.logger.info("user_is_ascking_for_command")
        else:
            reply = "你說得對，\n但是梵蒂岡的常住人口有800人，\n同時，僅澳大利亞就有4700萬隻袋鼠。\n如果袋鼠決定入侵梵蒂岡，\n那麼每一個梵蒂岡人要打58750只袋鼠，\n你不知道，你不在乎，你只關心你自己。"
            app.logger.info("else")
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=reply))
    except Exception as e:
        # app.logger.error("An exception occurred:", e)
        # app.logger.error("Arguments:", e.args)
        app.logger.error("String representation:", str(e))
        # 如果你想得到更技术性的输出，可以使用 repr(e)
        app.logger.error("Technical representation:", repr(e))
        reply = "出了一些問題，請稍後再試"
        message = TextSendMessage(text=reply)
        line_bot_api.reply_message(event.reply_token, message)
def send_message(event,status,content):
    if(status!=1):
        app.logger.error(content)
    message = TextSendMessage(text=content)
    line_bot_api.reply_message(event.reply_token, message)


import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
