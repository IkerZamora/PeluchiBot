# -*- coding: utf-8 -*-
import datetime
import os
import sys
import telebot

token = os.environ['TELEGRAM_TOKEN']

bot = telebot.TeleBot(token)

commands = {
# command description used in the 'ayuda' command, keep these up to date
    'ayuda': 'Obtener información acerca de los comandos',
    'fotopizza': 'Fotopizza de los pizzeros (Próximamente)',
    'hype': 'Tiempo restante para la próxima EE ó AE ó GE ó Gamergy (Próximamente)'
}

# Help command. Returns all the commands with their help text
@bot.message_handler(commands=['ayuda'])
def command_help(m):
    cid = m.chat.id
    help_text = "Lista de comandos disponibles: \n"
    for key in sorted(commands):
        # generate help text out of the commands dictionary defined at the top
        help_text += "/" + key + ": "
        help_text += commands[key] + "\n"
    bot.send_message(cid, help_text)  # send the generated help page

# TODO
# Returns the fotopizza of the user requested
@bot.message_handler(commands=['fotopizza'])
def command_fotopizza(m):
    cid = m.chat.id
    bot.send_message(cid, 'Comando en desarrollo')

# TODO
# Returns the remaining time for the event requested
@bot.message_handler(commands=['hype'])
def command_hype(m):
    cid = m.chat.id
    bot.send_message(cid, 'Comando en desarrollo')

bot.polling()
