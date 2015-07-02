#########################################################################
##
## BotBQ (BBQ) - Telegram bot to have a fake friend
##
#########################################################################

import ConfigParser
import os
import re, string
from twx.botapi import TelegramBot

import random

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

def process_answers(answers_raw):
    # Parse comma-separated answers from config file
    return

def main():
    print '[+] Starting bot...'

    # Read the config file
    print '[+] Reading config file...'
    config = ConfigParser.ConfigParser()
    config.read([os.path.expanduser('./config')])

    # Read data
    bot_name = config.get('bot', 'name')
    bot_token = config.get('bot', 'token')
    cool_answers_raw = config.get('phrases', 'cool_answers')
    cool_answers = [ answer for answer in cool_answers_raw.split('"') if answer and answer!=',']

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
                        if 'http://' in word or 'https://' in word:
                            # Get a random answer phrase:
                            answer = random.choice(cool_answers)
                            bot.send_message(chat_id, answer)

        except (KeyboardInterrupt, SystemExit):
            print '\nkeyboardinterrupt caught (again)'
            print '\n...Program Stopped Manually!'
            raise

if __name__  == '__main__':
    main()
