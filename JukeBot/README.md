#JukeBot #

This is a bot to control a media player running on your pc.

Work-in-progress bot from BQ Innovation Labs.

## Requisites ##
This requires the [twx-bot API](https://github.com/datamachine/twx.botapi). To install the stable version:

    $ sudo pip install twx.botapi

## Configuration ##
For the bot to work properly, the configuration file provided has to be modified with your bot's token and user
id.

To get a token check out the Official Telegram Bot API [documentation](https://core.telegram.org/bots/api).

To get the user id, open a chat with JukeBot and issue the command /start . After that, your id will appear on the
bot stdout.

## Usage ##
Just run the python script:

    $ python JukeBot.py