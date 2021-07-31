import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, ConversationHandler
from telegram import ParseMode, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, replymarkup
import requests, random

def start(update, context):
    first_name = update.effective_user.first_name 
    keyboard = [
        [
            KeyboardButton("Share Your Phone", request_contact=True),
            KeyboardButton("Share Your Location", request_location=True),
        ],
        [
            KeyboardButton("Button Click"),
            
        ]
    ]
    
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    
    update.message.reply_text(f"Welcome {first_name}\n share your contact or location by clicking the button\n\nSend /random", reply_markup=reply_markup)
    


def get_contact(update, context):
    phone = update.message.contact.phone_number
    update.message.reply_text(f"Your phone number is {phone}\n\nSend /help")


def get_location(update, context):
    location = update.message.location
    update.message.reply_text(f"Your location is {location.latitude} {location.longitude}\n\nSend /help")
    
def echo(u, c):
    u.message.reply_text("This is a message text")
    return 

def get_random(update, context, local=False):
    keyboard = [
        [
            InlineKeyboardButton("Cat", callback_data='cats'),
            InlineKeyboardButton("Dogs", callback_data='dogs'),
        ],
        [
            InlineKeyboardButton("Human", callback_data='human'),
            InlineKeyboardButton("Any Picture", callback_data='any'),
            
        ],
        [
            InlineKeyboardButton("Quote", callback_data='quote'),
            InlineKeyboardButton("Jokes", callback_data='joke'),
            
        ],
        [
            
            InlineKeyboardButton("Join Group", url='https://t.me/CSEC_ASTU'),
        ]
    ]
    
    context.bot.send_message(chat_id=update.effective_user.id,text=f"Choose a random ", reply_markup=InlineKeyboardMarkup(keyboard))

def send_cat_photo(update, context):
    query = update.callback_query
    query.delete_message()
    url = 'http://thecatapi.com/api/images/get?format=src'
    bot = context.bot
    cat = requests.get(url)
    # print(cat.text) 
    # cat = cat.json()[0]['url']
    bot.send_photo(chat_id=update.effective_user.id, photo=url)
    get_random(update, context, local=True)

def send_dog_photo(update, context):
    query = update.callback_query
    query.delete_message() 
    url = 'https://dog.ceo/api/breeds/image/random'
    bot = context.bot
    bot.send_photo(chat_id=update.effective_user.id, photo=requests.get(url).json()['message'])
    get_random(update, context, local=True)
    
    
def send_any_photo(update, context):
    url = "https://picsum.photos/200/300"
    query = update.callback_query
    query.delete_message() 
    bot = context.bot
    pic = requests.get(url)
    bot.send_photo(chat_id=update.effective_user.id, photo=pic.content)
    get_random(update, context, local=True)

def send_jokes(update, context):
    query = update.callback_query
    query.delete_message()
    
    url = ['https://yomomma-api.herokuapp.com/jokes', 'https://icanhazdadjoke.com/']
    jurl = random.choice(url)
    joke = requests.get(jurl, headers={"Accept": "application/json"})
    context.bot.send_message(chat_id=update.effective_user.id, 
                                 text="<code>"+ joke.json()['joke'] + "</code>", parse_mode=ParseMode.HTML)
        
    get_random(update, context, local=True)

def send_quote(update, context):
    query = update.callback_query
    query.delete_message()
    
    url = "https://api.quotable.io/random"
    quote = requests.get(url)
    tags = " ".join([ f'#{i.replace("-", "_")}' for i in quote.json()['tags'] ])
    text = f"{tags}\n\n<code>{quote.json()['content']}</code>\n\n<b>{quote.json()['author']}</b>"
    context.bot.send_message(
        chat_id=update.effective_user.id,
        text=text, 
        parse_mode=ParseMode.HTML
    )
    
    get_random(update, context, local=True)
    
    
def main():
    "Use your own token this token already revoked!!!"
    updater = Updater("1797824142:AAGOy7fivv23Orx31USixFla-4iUn_-rayA")
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler('start', start))
    
    dp.add_handler(MessageHandler(
        Filters.contact, get_contact)
    )
    
    dp.add_handler(
        MessageHandler(Filters.location, get_location)
    )
    
    dp.add_handler(CommandHandler('random', get_random))
    
    dp.add_handler(CallbackQueryHandler(
        send_cat_photo, pattern='cats'
    ))
    
    dp.add_handler(CallbackQueryHandler(
        send_any_photo, pattern='any'
    ))
    
    dp.add_handler(CallbackQueryHandler(
        send_jokes, pattern='joke'
    ))
    
    dp.add_handler(
        CallbackQueryHandler(send_dog_photo, pattern='dogs')
    )
    
    dp.add_handler(
        CallbackQueryHandler(send_quote, pattern='quote')
    )
    
    dp.add_handler(MessageHandler(Filters.text, echo))
    
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    

