import os
from time import sleep
import telebot
from telebot import types
from confige import token
from apkmody import Mody

bot = telebot.TeleBot(token)

@bot.message_handler(func=lambda message: True)
def searching_mod(message):
    if message.text.lower() == 'stop':
        bot.send_message(message.chat.id, 'Bye')
        bot.stop_bot()
    else:
        search = message.text
        wait = bot.send_message(message.chat.id, 'Searching...')
        wait
        data = Mody.search(search)
        bot.delete_message(message.chat.id, wait.message_id)
        for i in data:
            markup = types.InlineKeyboardMarkup()
            btn_docs= types.InlineKeyboardButton(text='Link 🌍', url=i['link'])
            markup.add(types.InlineKeyboardButton('Download ⚡', callback_data='download'), btn_docs)
            bot.send_photo(message.chat.id, i['image'], caption=f'''*{i['title']}*
*Version:* {i['version']}
*Mod:* {i['mod']}
''', parse_mode='Markdown', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'download')
def choose_mod(call):
    print(call)





bot.infinity_polling()