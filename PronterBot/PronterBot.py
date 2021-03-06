#########################################################################
##
## PronterBot - Receive updates from pronterface directly to telegram
##
#########################################################################

import ConfigParser
import os
import re, string
from twx.botapi import *

import xmlrpclib


__author__ = 'def'

def load_last_id():
    if not os.path.isfile('id'):
        save_last_id(0)
        return 0

    with open('id', 'r') as f:
        return int(f.readline())

def save_last_id(last_id):
    with open('id', 'w') as f:
        f.write(str(last_id))

def save_log(id, update_id, chat_id, text):
    with open('log.txt', 'a') as f:
        f.write(str((id, update_id, chat_id, text))+'\n')

def send_keyboard(bot, user_id):
    keyboard = [ ['home'], ['start'], ['stop']]
    reply_markup = ReplyKeyboardMarkup.create(keyboard)
    bot.send_message(user_id, 'testing keyboard', reply_markup=reply_markup)

def main():
    print '[+] Starting bot...'

    # Read the config file
    print '[+] Reading config file...'
    config = ConfigParser.ConfigParser()
    config.read([os.path.expanduser('./config')])

    # Read data
    bot_name = config.get('bot', 'name')
    bot_token = config.get('bot', 'token')

    try:
        user_id = config.get('users', 'allowed')
    except ConfigParser.NoOptionError, ConfigParser.NoSectionError:
        print '[-] ATTENTION: No allowed user specified. Send a /start command to the bot and set the corresponding id in the users/allowed key at the config file.'
        user_id = None
    # Last mssg id:
    last_id = int(load_last_id())
    print '[+] Last id: %d' % last_id

    # Configure regex
    regex = re.compile('[%s]' % re.escape(string.punctuation))

    # Create bot
    print '[+] Connecting bot...'
    bot = TelegramBot(bot_token)
    bot.update_bot_info().wait()
    print '\tBot connected! Bot name: %s' % bot.username

    # Connect to pronterface
    rpc = xmlrpclib.ServerProxy('http://localhost:7978')

    # Send custom keyboard
    # if user_id:
    #    send_keyboard(bot, user_id)

    while True:
        try:
            updates = bot.get_updates(offset=last_id).wait()

            for update in updates:
                id = update.message.message_id
                update_id = update.update_id
                user = update.message.sender

                chat_id = update.message.chat.id
                text = update.message.text

                if int(update_id) > last_id:
                    last_id = update_id
                    save_last_id(last_id)
                    save_log(id, update_id, chat_id, text)

                    #text = regex.sub('', text)
                    words = text.split()

                    for word in words:
                        # Process commands:
                        if word == '/start':
                            print "New user started the app: " + str(user)
                        elif word == '/status':
                            status = rpc.status()
                            message = ''
                            if not status['temps']:
                                bot.send_message(user_id, "Printer not connected!")
                                break
                            else:
                                message += 'Temperatures:\n\tBase: %s/%s\n\tExtruder: %s/%s' % (status['temps']['B'][0], status['temps']['B'][1], \
                                                                                            status['temps']['T'][0], status['temps']['T'][1])
                            if status['progress']:
                                message += '\nProgress: %2.1f%%\nZ: %d\nFile: %s' % (status['progress'], status['z'], status['filename'])

                            print message
                            bot.send_message(user_id, message)


        except (KeyboardInterrupt, SystemExit):
            print '\nkeyboardinterrupt caught (again)'
            print '\n...Program Stopped Manually!'
            raise

if __name__  == '__main__':
    main()
