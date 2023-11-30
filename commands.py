import telegram.ext
import time
from pynput.keyboard import Controller
import webbrowser


class CommandManager:
    token = None
    updater = None
    disp = None
    group_id = None

    def __init__(self, name, func):
        self.name = name
        self.disp.add_handler(telegram.ext.CommandHandler(
            self.name, func))

    @classmethod
    def setup(cls, token, group_id, bot_name, time_to_wait, updater):
        cls.token = token
        cls.group_id = group_id
        cls.bot_name = bot_name
        cls.time_to_wait = time_to_wait
        cls.updater = updater
        cls.disp = cls.updater.dispatcher

    @classmethod
    def set_timer(cls, sec):
        cls.time_to_wait = int(sec)

    @classmethod
    def timer(cls, update):
        update.message.reply_text(
            f"Il comando verrà eseguito fra {str(cls.time_to_wait)} secondi ⏳!")
        time.sleep(cls.time_to_wait)


# Command.setup('token', 24234325, 3)
# command = command('name', 'url')


class UrlCommand(CommandManager):
    def __init__(self, name, url):
        super().__init__(name, self.exe_command)
        self.url = url

    @classmethod
    def play(cls, url, update):
        cls.timer(update)
        webbrowser.open(url)

    def exe_command(self, update, context):
        if update.message.chat_id == self.group_id:
            self.play(self.url, update)
            update.message.reply_text(f"Comando {self.name} eseguito ✅.")
        else:
            update.message.reply_text(
                f"Ciao 👋 sono {self.bot_name} per interagire con me utilizza il gruppo dedicato.")
