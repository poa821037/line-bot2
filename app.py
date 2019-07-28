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

line_bot_api = LineBotApi('j3CSW20Uqto5xMUxx6Msjfa523womtrsuTG5+lwwpNF9P+NLHgrU3rTleoBsi8HPM2PXYGrdwoMakA/8GMAqHXm8Q7qDWoMDncOICChM2W8+84PaO2FMd8nQE841jjPySVlTiDJWrJIuUCIE3ovgZwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('75e34be58268b12b037c6c36007d9027')


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