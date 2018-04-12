# -*- coding: utf-8 -*-
import datetime
import os
import sys
import telebot

from events import Event, Events

try:
    token = os.environ['TELEGRAM_TOKEN']
except KeyError:
    print("Please set the environment variable TELEGRAM_TOKEN")
    sys.exit(1)

bot = telebot.TeleBot(token)

commands = {
# command description used in the 'ayuda' command, keep these up to date
    'ayuda': 'Obtener información acerca de los comandos',
    'hype': 'Tiempo restante para la próxima EE ó AE ó GE. Uso: /hype (EE | AE | GE)'
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

# Returns the remaining time for the event requested
@bot.message_handler(commands=['hype'])
def command_hype(m):
    cid = m.chat.id
    param = ""
    try:
        param = m.text.split()[1].lower()
    except IndexError:
        bot.send_message(
            cid, "Se necesita un atributo. Uso: /hype (EE | GE | AE)")
        return
    events = Events()
    event = events.get_event(param)
    if event == 0:
        bot.send_message(
            cid, "Ese evento no existe. Uso: /hype (EE | GE | AE)")
        return
    days, hours, minutes, seconds = event.time_left()
    text = "Tiempo restante para la %s%d " % (
    event.acronym, event.edition)
    text += "(%d-%d-%d):\n" % (
        event.date.year, event.date.month, event.date.day)
    text += " %d días, %d horas, %d minutos y %d segundos" % (
        days, hours, minutes, seconds)
    bot.send_message(cid, text)

bot.polling()
