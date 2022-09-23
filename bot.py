import os
try:
    import telebot
    from telebot import types
    from pySmartDL import SmartDL
except:
    os.system("pip install pyTelegramBotAPI pySmartDL")

from apkmody import Mody
from config import token

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_photo(message.chat.id, caption='Hi, I am apkmody Bot. \nI can search for apps on apkmody.io and download them for you. \nJust send me the name of the app you want to download ☕.', photo='https://apkmody.io/wp-content/uploads/2021/06/xapks-installer-cover-1440x480.jpg')



@bot.message_handler(func=lambda message: True)
def searching_mod(message):
    wait = bot.send_message(message.chat.id, 'Searching...')
    search = message.text
    if Mody.search(search) == None:
        bot.delete_message(message.chat.id, wait.message_id)
        bot.send_message(message.chat.id, 'No results found')
    else:
        data = Mody.search(search)
        bot.delete_message(message.chat.id, wait.message_id)
        for i in data:
            markup = types.InlineKeyboardMarkup()
            btn_docs= types.InlineKeyboardButton(text='Link 🌍', url=i['link'])
            markup.add(types.InlineKeyboardButton('⚡', callback_data='download'), btn_docs)
            bot.send_photo(message.chat.id, i['image'], caption=f'''
            *{i['title']}*\n*Version:* {i['version']}\n*Mod:* {i['mod']}\n*Size:* {i['size']}'''
            , parse_mode='Markdown', reply_markup=markup)



@bot.callback_query_handler(func=lambda call: call.data == 'download')
def choose_mod(call):
    url = call.message.reply_markup.keyboard[0][1].url
    data = Mody.items(url)
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)        
    for i in data:
        markup = types.InlineKeyboardMarkup()
        btn_docs= types.InlineKeyboardButton(text='Link 🌍', url=i['link'])
        markup.add(types.InlineKeyboardButton('Download 🌠', callback_data='mod'), btn_docs)
        bot.reply_to(call.message, f'''*{i['name']}* 📥''', parse_mode='Markdown', reply_markup=markup) 


@bot.callback_query_handler(func=lambda call: call.data == 'mod')
def download_mod(call):
    c_url = call.message.reply_markup.keyboard[0][1].url
    if c_url.count('//') == 2:
        url = c_url.split('//')
        url = url[0]+'//'+url[2]
    elif c_url.count('//') == 1:
        url = c_url
    dlurl = Mody.dlurl(url)
    filename = call.message.text.replace(' ','_').replace(' 📥','')
    filename = f'{filename}_{call.message.message_id}.apk'
    bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=None)
    downloading = bot.reply_to(call.message, 'Downloading...')
    obj = SmartDL(dlurl, dest=f'./{filename}', progress_bar=True)
    obj.start()
    if obj.isSuccessful() == True:
        bot.delete_message(call.message.chat.id, downloading.message_id)
        uplding = bot.reply_to(call.message, 'Uploading...')
        try:
            bot.send_document(call.message.chat.id, open(f'./{filename}', 'rb'))
            bot.delete_message(call.message.chat.id, uplding.message_id)
            os.remove(f'./{filename}')
        except Exception as e:
            bot.delete_message(call.message.chat.id, uplding.message_id)
            bot.send_message(call.message.chat.id, f'Coudn\'t upload file, it\'s too big. Try to download it from link below\n{dlurl}')
            os.remove(f'./{filename}')
        bot.delete_message(call.message.chat.id, uplding.message_id)
    


bot.infinity_polling()
