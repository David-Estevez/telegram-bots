#########################################################################
##
## OuijaBot - Talk with the spirits!
##
#########################################################################

import ConfigParser
import os
import re, string
from twx.botapi import *

from OuijaController import OuijaController

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

    port = config.get('ouija', 'port')
    baudrate = config.get('ouija', 'baudrate')
    magnet1_pin = int(config.get('ouija', 'magnet1'))
    magnet2_pin = int(config.get('ouija', 'magnet2'))

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

    # Create OuijaController
    print '[+] Creating OuijaController...'
    ouija = OuijaController(port, baudrate, magnet1_pin, magnet2_pin)
    ouija.connect()

    while True:
        try:
            updates = bot.get_updates(offset=last_id).wait()

            for update in updates:
                id = update.message.message_id
                update_id = update.update_id
                user = update.message.sender

                chat_id = update.message.chat.id
                text = update.message.text

                if text and int(update_id) > last_id:
                    last_id = update_id
                    save_last_id(last_id)
                    save_log(id, update_id, chat_id, text)

                    #text = regex.sub('', text)
                    print '[+] Received: ' + text
                    words = text.split()

                    for i, word in enumerate(words):
                        # Process commands:
                        if word == '/start':
                            print "New user started the app: " + str(user)
                        elif user.id == int(user_id) and (word == '/say' or word == '/say@'+bot.username):
                            print 'Bot said: \"' + ' '.join(words[i+1:]) + '\"'
                            ouija.say(' '.join(words[i+1:]).lower())
                            break
                        elif user.id == int(user_id) and (word == '/yes' or word == '/yes@'+bot.username):
                            print 'Bot said "yes"'
                            ouija.go_to('yes')
                            break
                        elif user.id == int(user_id) and (word == '/no' or word == '/no@'+bot_name):
                            print 'Bot said "no"'
                            ouija.go_to('no')
                            break


        except (KeyboardInterrupt, SystemExit):
            print '\nkeyboardinterrupt caught (again)'
            print '\n...Program Stopped Manually!'
            raise

if __name__  == '__main__':
    main()
