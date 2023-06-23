import os
import logging

basedir = os.path.abspath(os.path.dirname(__file__))

# https://api.telegram.org/bot{my_bot_token}/setWebhook?url={url_to_send_updates_to}
# insert your bot token
TOKEN = "<INSERT TOKEN>"

# logger settings
logging.basicConfig(filename="logs.txt",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.INFO)
