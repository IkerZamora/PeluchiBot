
class Config():
    TELEGRAM_TOKEN = 'your_telegram_secret_token'

class Webhook(Config):
    PORT = 8443
    URL = 'https://<appname>.herokuapp.com/'