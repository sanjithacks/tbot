from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from telegram.ext.callbackcontext import CallbackContext
from telegram import (ChatAction)
from telegram import ParseMode, Update
import requests
import json
import hashlib
import math
from pytz import timezone
import pytz
import time
from datetime import datetime
import datetime as dt
import os

TOKEN = os.environ.get("TOKEN")

LINK = "https://giveaway.betros.xyz/_tgReg.php"

GIVEAWAY = "https://giveaway.betros.xyz/?param="

EVENT = "https://giveaway.betros.xyz/event.json"

tx = dt.datetime.now().timestamp()

utc = pytz.utc
fmt = '%Y-%m-%d %H:%M:%S %Z%z'

utc_dt = utc.localize(datetime.utcfromtimestamp(tx))

kol_tz = timezone('Asia/Kolkata')
kol_dt = utc_dt.astimezone(kol_tz)

kolT = math.floor(kol_dt.timestamp())

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Unique Giveaway Link",
                              callback_data='giveawayLink')],
        [InlineKeyboardButton(
            "About Me", callback_data='me')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_chat_action(
                    chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
    context.bot.send_message(
                    chat_id=update.effective_message.chat_id, text="Hello Sir, How may I help you.", parse_mode="HTML",reply_markup=reply_markup)


def keyboard_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == "giveawayLink":
        respE = requests.post(EVENT)
        if respE.status_code == 200:
            respEJ = json.loads(respE.text)
            if respEJ["startTime"] < kolT:
                query.answer('Giveaway link time over')
                context.bot.send_chat_action(
                    chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
                context.bot.send_message(
                    chat_id=update.effective_message.chat_id, text="Giveaway Link Period over.", parse_mode="HTML", disable_web_page_preview=True)
            else:
                uid = str(update.effective_chat.id)
                fname = update.effective_chat.first_name
                result = hashlib.md5(uid.encode())
                dt = {"uid": uid, "fname": fname, "hash": result.hexdigest()}
                resp = requests.post(LINK, data=dt)
                if resp.status_code == 200:
                    resj = json.loads(resp.text)
                    query.answer('Your unique giveaway link')
                    if resj["status"] == True and resj["exist"]:
                        msg = "Your unique link for giveaway: {}{}".format(
                            GIVEAWAY, result.hexdigest())
                        context.bot.send_chat_action(
                            chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
                        context.bot.send_message(
                            chat_id=update.effective_message.chat_id, text=msg, parse_mode="HTML", disable_web_page_preview=True)
                    else:
                        msg = "Your unique link for giveaway: {}{}".format(
                            GIVEAWAY, result.hexdigest())
                        context.bot.send_chat_action(
                            chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
                        context.bot.send_message(
                            chat_id=update.effective_message.chat_id, text=msg, parse_mode="HTML", disable_web_page_preview=True)

        else:
            query.answer('Something went wrong')
            context.bot.send_chat_action(
                chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
            context.bot.send_message(
                chat_id=update.effective_message.chat_id, text="Something went wrong.", parse_mode="HTML", disable_web_page_preview=True)

    if query.data == "me":
        query.answer('About You')
        msg = "<b>About You</b>\nName: {}\nUID: {}".format(
            update.effective_chat.first_name, update.effective_message.chat_id)
        context.bot.send_chat_action(
            chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        context.bot.send_message(
            chat_id=update.effective_message.chat_id, text=msg, parse_mode="HTML", disable_web_page_preview=True)


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CallbackQueryHandler(keyboard_callback))
    updater.start_polling()
    updater.idle()


# start application with main function
if __name__ == '__main__':
    main()
