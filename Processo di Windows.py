import telegram.ext
import requests
import os
import time
import pyautogui
import subprocess
import psutil
import sys
import json
import ctypes
from commands import CommandManager, UrlCommand
from math import fabs


def restart_programm(update):
    update.message.reply_text(
        "Il bot si riavvierà a momenti...")
    time.sleep(1)
    python = sys.executable
    os.execl(python, python, * sys.argv)


def format_string(args):
    return ' '.join(args)


def checkIfProcessRunning(process_name):
    for proc in psutil.process_iter():
        try:
            if process_name.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


def check_group(func):
    def wrapper(update, context):
        if update.message.chat_id == GROUP_ID:
            return func(update, context)
        else:
            update.message.reply_text(
                f"Ciao 👋 sono {BOT_NAME} per interagire con me utilizza il gruppo dedicato.")
    return wrapper


@check_group
def start(update, context):
    update.message.reply_text(
        f"Ciao 👋 sono {BOT_NAME}. Usa /menu per vedere i comandi disponibili.")


@check_group
def menu(update, context):

    url_commands_menu = ''
    tab = '        '
    if len(URL_COMMANDS):
        for command in URL_COMMANDS:
            url_commands_menu = url_commands_menu + '/' + \
                command['name'] + ' -> ' + command['desc'] + '\n' + tab
    else:
        url_commands_menu = 'Aggiungi un comando con /crea \n'

    update.message.reply_text(f"""
        COMANDI 📑:
        /menu -> Mostra questo menu 📑
        /status -> Controlla se il pc è acceso 💡
        /spegni -> Spegnere il computer 🛑
        /riavvia -> Riavvia il computer 🔃
        /logout -> Torna alla schermata di login 🔐
        /volume -> Modifica il volume 🔊        
        /cerca -> Cerca su Google 🌐
        /link -> Cerca con un link 🔗
        /chiudi -> Chiudi Chrome ✖
        /wallpaper -> Cambia sfondo del pc 🖼
                              
COMANDI URL 🔗:
        {url_commands_menu}                    
COMANDI APOCALITTICI ⚠:
        /nuke -> prompts nuke ☣
                                  
COMANDI AMMINISTRAZIONE 🔧:
        /settimer -> Imposta il timer dei comandi ⌛
        /comandi -> Lista comandi personalizzati 📑
        /crea -> Crea un comando 🚀
        /elimina -> Elimina un comando 🗑
        """
                              )


@check_group
def status(update, context):
    update.message.reply_text("Il computer è acceso 💡!")


@check_group
def spegni(update, context):
    update.message.reply_text("Spegnimento del computer...")
    CommandManager.timer(update)
    os.system(f"shutdown /s /t 1")
    update.message.reply_text("Computer spento 🛑!")


@check_group
def riavvia(update, context):
    update.message.reply_text("Riavvio del computer...")
    CommandManager.timer(update)
    os.system(f"shutdown /r /t 1")
    update.message.reply_text("Computer riavviato 🔃!")


@check_group
def logout(update, context):
    update.message.reply_text("Logout in corso...")
    CommandManager.timer(update)
    os.system("shutdown -l")
    update.message.reply_text("Logout effettuato🚪!")


@check_group
def volume(update, context):

    if context.args[0]:
        try:
            value = int(context.args[0])
        except:
            update.message.reply_text(
                "Il valore deve essere un numero (es: /volume 50).")

        if value == 0:
            update.message.reply_text(
                "Scrivi il valore dopo il comando (es: /volume 50).")
        if value > 0:
            click = (value//2)
            pyautogui.press('volumeup', click)
            update.message.reply_text(
                f"Il volume è stato aumentato ⏫ {value}.")

        else:
            value = fabs(value)
            click = int(value//2)
            pyautogui.press('volumedown', click)

            update.message.reply_text(
                f"Il volume è stato diminuito ⏬ di {value}.")
    else:
        update.message.reply_text(
            "Scrivi il valore dopo il comando (es: /volume 50).")


@check_group
def cerca(update, context):
    args = context.args
    if args:
        search = format_string(args)
        UrlCommand.play('https://www.google.com/search?q='+search, update)
        update.message.reply_text("Ricerca eseguita ➡🌐.")
    else:
        update.message.reply_text(
            "Scrivi cosa desideri cercare (es: /cerca panini)")


@check_group
def link(update, context):
    args = context.args
    url = format_string(args)
    if args:
        UrlCommand.play(url, update)
        update.message.reply_text("Link aperto ➡🔗.")
    else:
        update.message.reply_text(
            "Scrivi il link dopo il comando (es: /link www.facebook.it).")


@check_group
def chiudi(update, context):
    if checkIfProcessRunning('chrome'):
        try:
            subprocess.call("TASKKILL /F /IM chrome.exe", shell=True)
            update.message.reply_text("Chrome è stato chiuso 🛑")
        except:
            update.message.reply_text("Chrome è già stato chiuso 🛑")
    else:
        update.message.reply_text("Chrome non è in esecuzione ❌")


def set_wallpaper(url):
    folder_path = BASE_DIR + 'src\images\\'
    if not url:
        image = '\default_image.jpg'
    else:
        n_folder_items = len(os.listdir(folder_path))
        image = 'bg_' + str(n_folder_items)+'.jpg'
        try:
            r = requests.get(url)
            with open(folder_path + image, 'wb') as outfile:
                outfile.write(r.content)
        except:
            raise ValueError('Image not found')

    abs_file_path = ctypes.c_wchar_p(folder_path + image)
    ctypes.windll.user32.SystemParametersInfoW(
        20, 0, abs_file_path, 0)


@check_group
def wallpaper(update, context):
    url = format_string(context.args)
    try:
        set_wallpaper(url)
    except:
        update.message.reply_text(
            f"Immagine non trovata ❌")
        return
    update.message.reply_text(
        f"Sfondo inserito 🖼")


@check_group
def nuke(update, context):
    if TIME_TO_WAIT != 0:
        update.message.reply_text(
            f"Avvio della nuke fra: {TIME_TO_WAIT} secondi 🚀")
        time.sleep(TIME_TO_WAIT)
    else:
        pass
    update.message.reply_text(
        f"☢☢☢ {update.message.from_user.username.upper()} E' UN PAZZO. HA APPENA LANCIATO LA PROMPTS NUKE ☢☢☢")
    context.bot.send_message(
        chat_id=GROUP_ID, text=f"ESPLOSIONE FRA:")
    set_wallpaper(
        'https://i0.wp.com/www.michigandaily.com/wp-content/uploads/2023/09/Nuclear.jpg?fit=1200%2C800&ssl=1')
    for i in range(0, 10):
        time.sleep(1)
        context.bot.send_message(
            chat_id=GROUP_ID, text=f"☢ {10-i} ☢")
    else:
        time.sleep(1)
        context.bot.send_message(
            chat_id=GROUP_ID, text=f"☢ E' STATO BELLO AMICI ☢")
    set_wallpaper('https://images.theconversation.com/files/537993/original/file-20230718-17-19622i.jpeg?ixlib=rb-1.1.0&rect=502%2C1275%2C11227%2C5604&q=45&auto=format&w=1356&h=668&fit=crop')
    subprocess.run([BASE_DIR + "nuke.bat"])


######################################
# ADMIN COMMANDS
@check_group
def settimer(update, context):
    time = context.args[0]

    try:
        time = int(time)
    except:
        update.message.reply_text(
            "Scrivi i secondi dopo il comando (es: /settimer 10 ). [MAX: 15]")
        return

    if time == TIME_TO_WAIT:
        update.message.reply_text(
            f"Il valore è già impostato a {TIME_TO_WAIT}s.")
        return

    if 0 <= time <= 15:

        with open(BASE_DIR + 'data.json') as df:
            data = json.load(df)

        data['settings']['time_to_wait'] = time

        with open(BASE_DIR + 'data.json', 'w') as df:
            df.write(json.dumps(data))

        if time != 0:
            update.message.reply_text(
                f"Ora i comandi verrano eseguiti dopo {time} secondi ⏳.")
        else:
            update.message.reply_text(
                f"Ora i comandi verrano eseguiti all'istante ⚡.")

    else:
        update.message.reply_text(
            "Scrivi i secondi dopo il comando (es: /settimer 10 ). (0-15s)")
    restart_programm(update)


@check_group
def crea(update, context):
    if len(URL_COMMANDS) < 30:
        command_to_add = format_string(context.args)
        if not command_to_add or command_to_add.count('-') < 2:
            update.message.reply_text(
                "Scrivi il comando nel seguente formato: /crea NOMECOMANDO-BREVEDESCRIZIONECOMANDO-LINKDELCOMANDO")
        else:
            sp = []  # splitters index
            for i, c in enumerate(command_to_add):
                if c == '-':
                    sp.append(i)
                if len(sp) == 2:
                    continue

            command_name = command_to_add[0:sp[0]].lower()
            if any(command_name == command['name'] for command in URL_COMMANDS):
                update.message.reply_text(
                    "Esiste già un altro comando con questo nome ❌")
                return
            elif ' ' in command_name:
                update.message.reply_text(
                    "Non puoi inserire spazi nel NOME del comando ❌")
                return
            else:
                pass

            command_desc = command_to_add[sp[0]+1:sp[1]]
            command_url = command_to_add[sp[1] +
                                         1:]

            with open(BASE_DIR + 'data.json') as df:
                data = json.load(df)

            data['url_commands'].append(
                {"name": command_name, "desc": command_desc, "url": command_url, })

            with open(BASE_DIR + 'data.json', 'w') as df:
                df.write(json.dumps(data))

            update.message.reply_text(
                f"Comando {command_name.upper()} aggiunto ✅ (Il programma è stato riavviato 🔃)")
            restart_programm(update)


@check_group
def elimina(update, context):
    command_name = format_string(context.args)
    if command_name != '':
        idx = None
        for i, command in enumerate(URL_COMMANDS):
            if command_name == command['name']:
                idx = i
                break

        if idx != None:
            with open(BASE_DIR + 'data.json') as df:
                data = json.load(df)

            del data['url_commands'][idx]

            with open(BASE_DIR + 'data.json', 'w') as df:
                df.write(json.dumps(data))

            update.message.reply_text("Comando eliminato 🗑")
            restart_programm(update)

        else:
            update.message.reply_text("Comando inesistente ❌")
    else:
        update.message.reply_text(
            "Scrivi il comando nel seguente formato: /elimina nome_comando")


@check_group
def url_commands_list(update, context):
    if len(URL_COMMANDS) == 0:
        menu = 'Non è stato creato ancora alcun comando personalizzato ❌'
    else:
        menu = 'LISTA COMANDI AGGIUNTIVI📑:'
    for command in URL_COMMANDS:
        menu = menu + "\t\t\n" + '/' + \
            command['name'] + ' -> ' + command['desc']
    update.message.reply_text(menu)


#########################################
is_connected = False
while is_connected == False:

    try:
        BASE_DIR = os.path.dirname(os.path.realpath(__file__)) + '\\'

        with open(BASE_DIR + 'data.json', 'r') as df:
            data = json.load(df)
            TOKEN = data['token']
            BOT_NAME = data['bot_name']
            GROUP_ID = data['group_id']
            TIME_TO_WAIT = data['settings']['time_to_wait']
            URL_COMMANDS = data['url_commands']

        updater = telegram.ext.Updater(TOKEN, use_context=True)
        CommandManager.setup(TOKEN, GROUP_ID, BOT_NAME, TIME_TO_WAIT, updater)

        # Default Commands
        CommandManager('start', start)
        CommandManager('menu', menu)
        CommandManager('status', status)
        CommandManager('spegni', spegni)
        CommandManager('riavvia', riavvia)
        CommandManager('logout', logout)
        CommandManager('volume', volume)
        CommandManager('cerca', cerca)
        CommandManager('chiudi', chiudi)
        CommandManager('link', link)
        CommandManager('wallpaper', wallpaper)
        CommandManager('nuke', nuke)

        # Admin Commands
        CommandManager('settimer', settimer)
        CommandManager('crea', crea)
        CommandManager('elimina', elimina)
        CommandManager('comandi', url_commands_list)

        # Url Commands
        for comm in URL_COMMANDS:
            command = UrlCommand(comm['name'], comm['url'])

        # when bot goes online
        updater.start_polling()
        is_connected = True
        print('bot is now connected...')
        updater.dispatcher.bot.sendMessage(
            chat_id=GROUP_ID, text=f'Il bot è online 🤖 !')
        updater.idle()

    except:
        is_connected = False
        time.sleep(3)
        print('reconnection...')
