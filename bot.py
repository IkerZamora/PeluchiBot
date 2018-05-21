# -*- coding: utf-8 -*-

from config import Config, Webhook
from events import Event, Events
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove,
    InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Updater, CommandHandler)

import argparse
import datetime
import os
import sys

ENVIRONMETNS = ['development','production']

COMMANDS = {
    # command description used in the 'ayuda' command, keep these up to date
    'ayuda': 'Obtener información acerca de los comandos',
    'hype': 'Tiempo restante para la próxima EE ó AE ó GE.' \
        + ' Uso: /hype (EE | AE | GE)'
}

# Help command. Returns all the commands with their help text
def help_command(bot, update):
    help_text = 'Lista de comandos disponibles: \n'
    for key in sorted(COMMANDS):
        # generate help text out of the commands dictionary defined at the top
        help_text += '/' + key + ': '
        help_text += COMMANDS[key] + '\n'
    # send the generated help page
    bot.send_message(chat_id=update.message.chat_id, text=help_text)

# Hype command. Returns the remaining time for the event requested
def hype_command(bot, update):
    chat_id = update.message.chat_id
    param = ''
    try:
        param = update.message.text.split()[1].lower()
    except IndexError:
        bot.send_message(
            chat_id, 'Se necesita un atributo. Uso: /hype (EE | GE | AE)')
        return
    events = Events()
    event = events.get_event(param)
    if event == 0:
        bot.send_message(
            chat_id, 'Ese evento no existe. Uso: /hype (EE | GE | AE)')
        return
    days, hours, minutes, seconds = event.time_left()
    text = 'Tiempo restante para la %s%d ' % (
    event.acronym, event.edition)
    text += '(%d-%d-%d):\n' % (
        event.date.year, event.date.month, event.date.day)
    text += ' %d días, %d horas, %d minutos y %d segundos' % (
        days, hours, minutes, seconds)
    bot.send_message(chat_id=chat_id, text=text)

def main(argv):

    parser = argparse.ArgumentParser('bot.py')
    parser.add_argument('--environment', dest='env', required=True,
        choices=ENVIRONMETNS, help='sets bot\'s deployment environment')
    args = parser.parse_args(argv)

    if args.env not in ENVIRONMETNS:
        parser.print_help()
        sys.exit(1)

    if args.env == 'development':
        configuration = Config
        updater = Updater(configuration.TELEGRAM_TOKEN)

    elif args.env == 'production':
        configuration = Webhook
        updater = Updater(configuration.TELEGRAM_TOKEN)
        updater.start_webhook(listen='0.0.0.0', port=configuration.PORT,
            url_path=configuration.TELEGRAM_TOKEN)
        updater.bot.set_webhook(configuration.URL \
            + configuration.TELEGRAM_TOKEN)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('ayuda', help_command))
    dispatcher.add_handler(CommandHandler('hype', hype_command))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main(sys.argv[1:])