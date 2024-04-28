from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *
import os
import texthandlers

app = Flask(__name__)

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
    my_variable = '<h1>I alive</h1>'
    return my_variable

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    try:
        if event.message.text.startswith("簽到 "):#簽到 名字 課程ID 是否會遲到(0/1) 備註(選填)
            reply = texthandlers.roll_call(event.message.text[4:]);
            app.logger.info("")
            #message = ImageSendMessage(original_content_url=reply, preview_image_url=reply)
            if(reply.status == 1):
                massage = TextSendMessage(text=reply.content)
                line_bot_api.reply_message(event.reply_token, message)
        if event.message.text.startswith("開始簽到 "):#開始簽到 課程名稱
            reply = texthandlers.start_roll_call(event.message.text[6:]);
            app.logger.info("")
            #message = ImageSendMessage(original_content_url=reply, preview_image_url=reply)
            if(reply.status == 1):
                massage = TextSendMessage(text=reply.content)
                line_bot_api.reply_message(event.reply_token, message)
        if event.message.text.startswith("檢視簽到 "):#檢視簽到 ID
            reply = texthandlers.view_roll_call(event.message.text[4:]);
            app.logger.info("")
            #message = ImageSendMessage(original_content_url=reply, preview_image_url=reply)
            if(reply.status == 1):
                massage = TextSendMessage(text=reply.content)
                line_bot_api.reply_message(event.reply_token, message)
        if event.message.text.startswith("報分數 "):#報分數 名子 座號\n一項\n第一項成績  (過了"V"，沒過用"X")
            reply = texthandlers.score_register(event.message.text[5:]);
            app.logger.info("")
            #message = ImageSendMessage(original_content_url=reply, preview_image_url=reply)
            if(reply.status == 1):
                massage = TextSendMessage(text=reply.content)
            line_bot_api.reply_message(event.reply_token, message)
        if event.message.text.startswith("開始報成績 "):#開始報成績/n項目一/n項目二
            reply = texthandlers.start_score_register(event.message.text[7:]);
            app.logger.info("")
            #message = ImageSendMessage(original_content_url=reply, preview_image_url=reply)
            if(reply.status == 1):
                massage = TextSendMessage(text=reply.content)
                line_bot_api.reply_message(event.reply_token, message)
        if event.message.text.startswith("檢視成績 "):#開始報成績/n項目一/n項目二
            reply = texthandlers.view_score_register(event.message.text[6:]);
            app.logger.info("")
            #message = ImageSendMessage(original_content_url=reply, preview_image_url=reply)
            if(reply.status == 1):
                massage = TextSendMessage(text=reply.content)
                line_bot_api.reply_message(event.reply_token, message)
        else:
            reply = "你說得對，\n但是梵蒂岡的常住人口有800人，\n同時，僅澳大利亞就有4700萬隻袋鼠。\n如果袋鼠決定入侵梵蒂岡，\n那麼每一個梵蒂岡人要打58750只袋鼠，\n你不知道，你不在乎，你只關心你自己。"
        '''
        # if event.message.text=="請支援收銀":
        #     reply="我是支援收銀機。\n我會負責支援收銀 和 輸贏\n\n使用方式如下:\n→梗圖支援 梗圖關鍵字\n他會幫你找到最符合關鍵字的梗圖並傳回來\n\n→歌曲支援 歌曲關鍵字\n他會幫你找到最符合關鍵字的歌曲並傳回來 可以直接打歌詞\n\n→請支援收銀\n他會告訴你有什麼可以用的指令\n\n-文字\n他會跟你講ㄧ樣的話\n\n+文字\n他會說 對嘛對嘛\n\n\n如果不是特定的關鍵字的話我是不會回覆的"
        #     app.logger.info("我支援了收銀") 
        #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))

        # if event.message.text.startswith("-"):
        #     app.logger.info("附和")
        #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text=event.message.text[1:]))
        # if event.message.text.startswith("+"):
        #     app.logger.info("對嘛對嘛")
        #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text="對嘛對嘛"))
        # if event.message.text.startswith("歌曲支援 "):
            
        #     reply= request_4.find_video(event.message.text[4:])
        #     app.logger.info("Song is :"+str(reply))

        #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply))
        # if request_4.check_keywords(event.message.text):
        #     app.logger.info(":(")
        #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text="不好欸"))
        # if event.message.text=="歌曲支援" or event.message.text=="梗圖支援":
        #     app.logger.info("missing keyword")
        #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請輸入關鍵字"))
'''

    except Exception as e:
        app.logger.error("An error occurred: " + str(e))
        reply = "出了一些問題，請稍後再試"
        message = TextSendMessage(text=reply)
        line_bot_api.reply_message(event.reply_token, message)
    

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)