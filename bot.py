# -*- coding: utf-8 -*-

from datetime import datetime
from events import Event, Events
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove,
    InlineKeyboardButton, InlineKeyboardMarkup)
from telegram.ext import (Filters, CommandHandler, MessageHandler,
    RegexHandler, Updater)

import argparse
import logging
import os
import sys

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_NAME = None
BOT_ADMINS = []
COMMANDS = {
    # command description used in the 'ayuda' command, keep these up to date
    'ayuda': 'Obtener información acerca de los comandos',
    'hype': 'Tiempo restante para la próxima EE, AE ó GE.' \
        + ' Uso: /hype [EE | AE | GE]',
    'lalala': 'Canto para ti \u2665'
}

EVENTS = Events()

def greetings(bot, update):
    chat_id = update.message.chat.id
    new_members = update.message.new_chat_members
    left_member = update.message.left_chat_member
    if new_members:
        for new_member in new_members:
            # Bot was added to a group chat
            if new_member.username == BOT_NAME:
                bot.send_message(
                    chat_id=chat_id,
                    text='Hola a todos soy {} y os daré muchos mimitos!'
                        .format(BOT_NAME)
                )
            # Another user joined the chat
            else:
                bot.send_message(
                    chat_id=chat_id,
                    text='Bienvenido al grupo {}. ¿Eres tu mi peluchito?'
                        .format(new_member.name)
                )
    elif left_member:
        if left_member.username != BOT_NAME:
            bot.send_sticker(
                chat_id=chat_id,
                sticker=open('./assets/apastar.webp', 'rb')
            )
            if not left_member.is_bot:
                bot.send_sticker(
                    chat_id=left_member.id,
                    sticker=open('./assets/apastar.webp', 'rb')
                )

def apastar_resumen(bot, update):
    update.message.reply_sticker(sticker=open('./assets/apastar.webp', 'rb'))

def lalala_command(bot, update):
    bot.send_audio(
        chat_id=update.message.chat_id,
        audio=open('./assets/snufi_schnuffel_mi_peluchito.mp3', 'rb')
    )

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
    args = update.message.text.split() # Array of string '/hype' + [parameter]
    using_args = len(args) > 1
    if using_args:
        event = EVENTS.get_event(args[1].lower())
    else:
        event = EVENTS.next_event()
    if event:
        now = datetime.now()
        if event.date > now:
            days, hours, minutes, seconds = event.time_left()
            text = 'Tiempo restante para la %s%d ' % (
            event.acronym, event.edition)
            text += '(%d-%d-%d):\n' % (
                event.date.year, event.date.month, event.date.day)
            text += ' %d días, %d horas, %d minutos y %d segundos' % (
                days, hours, minutes, seconds)
            bot.send_message(chat_id=chat_id, text=text)
        else:
            EVENTS.set_event(event.acronym, event.update_date())
            text = ('Aún no se ha anunciado la fecha para la {}{}. '
                .format(event.acronym, event.edition + 1)
                + 'Relaja esos pezones.'
            )
            bot.send_message(chat_id=chat_id, text=text)
    else:
        if using_args:
            bot.send_message(
                chat_id, 'Ese evento no existe. Uso: /hype [EE | GE | AE]'
            )
        else:
            bot.send_message(
                chat_id,
                'Aún no se ha anunciado la fecha de ningún evento. '
                + 'Relaja esos pezones.'
            )

def main(argv):
    parser = argparse.ArgumentParser('bot.py')
    parser.add_argument('--webhooks', action='store_true',
        help='enables webhooks instead of pooling')
    args = parser.parse_args(argv)

    try:
        token = os.environ['TELEGRAM_TOKEN']
    except KeyError:
        logger.exception('Please set the TELEGRAM_TOKEN environment variable')
        sys.exit(2)
    try:
        BOT_NAME = os.environ['BOT_NAME']
    except KeyError:
        logger.exception('Please set the BOT_NAME environment variable')
        sys.exit(2)
    try:
        BOT_ADMINS.append(os.environ['ADMIN'])
    except KeyError:
        logger.exception('Please set the ADMIN environment variable')
        sys.exit(2)

    updater = Updater(token)
    job_queue = updater.job_queue
    if args.webhooks:
        updater.start_webhook(listen='0.0.0.0', url_path=token,
            port=int(os.environ.get('PORT', '8443')))
        try:
            updater.bot.set_webhook(os.path.join(os.environ['URL'], token))
        except KeyError:
            logger.exception('Please set the environment variable URL')
            sys.exit(2)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(MessageHandler(Filters.status_update, greetings))
    dispatcher.add_handler(CommandHandler('ayuda', help_command))
    dispatcher.add_handler(CommandHandler('hype', hype_command))
    dispatcher.add_handler(CommandHandler('lalala', lalala_command))
    dispatcher.add_handler(CommandHandler('resumen', apastar_resumen))
    dispatcher.add_handler(RegexHandler(r'^(resumen\?)$', apastar_resumen))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main(sys.argv[1:])