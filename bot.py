from telegram.ext import (Updater, CommandHandler, 
                        MessageHandler, Filters, CallbackQueryHandler)

from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.message import Message

import requests

def start(update, context):
    first_name = update.effective_user.first_name
    keyboard = [
        [ 
         KeyboardButton("Share Your Contact", request_contact=True),
         KeyboardButton("Share Your Location", request_location=True),
         ],
        [
            KeyboardButton("Click Me")
        ]
    ]
    
    reply_markup = ReplyKeyboardMarkup(keyboard)
    
    update.message.reply_text(f"welcome {first_name}", reply_markup=reply_markup)
    # context.bot.send_message(chat_id=update.effective_user.id, text="Hello {}".format(first_name), reply_markup=reply_markup) 
    
def get_contact(update, context):
    phone_number = update.message.contact.phone_number
    update.message.reply_text(f"Your phone number is {phone_number}")

def get_location(update, context):
    
    update.message.reply_text(f"Your location is {update.message.location.latitude}")

def echo(update, contex):
    update.message.reply_text(update.message.text)


def get_random(update, context):
    keyboard = [
        [
            InlineKeyboardButton(
                "Cat", callback_data="cat"
            ),
            InlineKeyboardButton(
                "Dog", callback_data="dog"
            )
        ],
        [
            InlineKeyboardButton("Join Our Channel", url="https://t.me/csec_astu")
        ]
    ]
    
    reply_markup = InlineKeyboardMarkup(keyboard) 
    context.bot.send_message(chat_id=update.effective_user.id ,text="Choose", reply_markup=reply_markup)

def send_cat_photo(update, context):
    update.callback_query.delete_message()
    url = 'http://thecatapi.com/api/images/get?format=src'
    cat = requests.get(url)
    
    context.bot.send_photo(
        chat_id=update.effective_user.id, 
        photo=cat.content
    )
    get_random(update, context)
    

def main():
    updater = Updater("1797824142:AAGOy7fivv23Orx31USixFla-4iUn_-rayA")
    dp = updater.dispatcher
    
    dp.add_handler(
        CommandHandler("start", start)
    )
    dp.add_handler(
        MessageHandler(
            Filters.contact, get_contact 
        )
    )
    dp.add_handler(
        MessageHandler(
            Filters.location, get_location 
        )
    )
    
    dp.add_handler(
        CommandHandler("random", get_random)
    )
    
    dp.add_handler(
        CallbackQueryHandler(
            send_cat_photo, pattern=r"^cat$"
        )
    )
    
    # unhandle 
    dp.add_handler(
        MessageHandler(
            Filters.text, echo 
        )
    )
    
    updater.start_polling()
    updater.idle()
    
if __name__ == '__main__':
    main()
    