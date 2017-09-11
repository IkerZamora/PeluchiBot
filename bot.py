# -*- coding: utf-8 -*-
#import redis
import os
import telebot
import datetime
import sys

# This will prevent errors with special characters
reload(sys)
sys.setdefaultencoding("utf-8")

# Example of your code beginning
#           Config vars
token = os.environ['TELEGRAM_TOKEN']
#some_api_token = os.environ['SOME_API_TOKEN']
#             ...

# If you use redis, install this add-on https://elements.heroku.com/addons/heroku-redis
#r = redis.from_url(os.environ.get("REDIS_URL"))

#       Your bot code below
# bot = telebot.TeleBot(token)
# some_api = some_api_lib.connect(some_api_token)
#              ...

bot = telebot.TeleBot(token)

commands = {
    # command description used in the 'ayuda' command, keep these up to date
    'apastar': 'Manda a alguien a pastar',
    'ayuda': 'Obtener información acerca de los comandos',
    'ayylmao': 'ayyy lmao',
    'ban': 'Ban hammer!',
    'drama': 'Drama :O',
    'fichas': 'Fichas, fichas!',
    'hype': 'Tiempo restante para la próxima EE ó AE ó GE',
    'kappa': 'Kappa',
    'lag': 'Lag, lag everywhere',
    'rip': 'RIP',
    'spam': 'Spam',
    'thug': 'Thug life'
}

@bot.message_handler(commands=['ayuda'])
def command_help(m):
    cid = m.chat.id
    help_text = "Lista de comandos disponibles: \n"
    for key in sorted(commands):
        # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page

bot.polling()
