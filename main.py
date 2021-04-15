from telebot.types import Message
import telebot
import requests
import re

TG_TOKEN = " " #add new create telegram-bot token 
TG_URL = "https://api.telegram.org/bot"

bot = telebot.TeleBot(TG_TOKEN)


class Example:
    variable = []

class Messages:
    tasks = []

@bot.message_handler(func=lambda message: True)
def reply(message: Message):
    chat_id = message.chat.id
    var = Messages.tasks
    if message.chat.type == 'group':
        username = message.from_user.username
        bot_message = message.text
        usr = ''
        array_text = bot_message.split()
        for x in array_text:
            if re.search('@[a-zA-Z]', x):
                usr = x
                break
        temporary = Example.variable

        if len(temporary):
            for use in temporary:
                if '@' + use['name'] == usr:

                    send_text_to = 'https://api.telegram.org/bot' + str(TG_TOKEN) + '/sendMessage?chat_id=' + str(
                        use['id']) + '&text=' + 'From: @'+ username + '\n' + bot_message
                    mes = {
                        'id': use['id'],
                        'task': bot_message
                    }
                    var.append(mes)
                    Messages.tasks = var

                    response = requests.get(send_text_to)
                    response.json()
                    break

    else:
        if message.text == 'start' or message.text == '/start':
            bot.reply_to(message, "Добро пожаловать в Tasks Bot")
            dict = {
                'name': message.chat.username,
                'id': message.chat.id
            }
            my_id = dict['id']
            temp = Example.variable

            if temp == []:
                temp.append(dict)
                Example.variable = temp
            else:
                for id in temp:
                    if (my_id != id['id']):
                        temp.append(dict)
                        Example.variable = temp

        if message.text == 'tasks' or message.text == '/tasks':
            if Messages.tasks == []:
                bot.send_message(chat_id, 'No tasks yet!')
            else:
                i=1
                for task in Messages.tasks:
                    bot.send_message(chat_id, str(i) + '-task: ' + task)
                    i=i+1

        if message.text != 'start' and message.text != 'tasks':

            var.append(message.text)
            Messages.tasks = var
            bot.reply_to(message, 'Saved in tasks list')
            print(Messages.tasks)



bot.polling()
