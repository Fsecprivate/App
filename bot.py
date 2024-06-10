import os
import pandas as pd
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from mega import Mega
from dotenv import load_dotenv

load_dotenv()

# Telegram Bot token
TELEGRAM_TOKEN = os.getenv('6945433492:AAHPvr6R1tqKiyyzAtZ2N2kcOy6AncEe5QY')

# MEGA login credentials
MEGA_EMAIL = os.getenv('Followerhub100@gmail.com')
MEGA_PASSWORD = os.getenv('12345@tutun')

# Initialize MEGA instance and login
mega = Mega()
m = mega.login(MEGA_EMAIL, MEGA_PASSWORD)

def download_files_from_mega():
    # Download all XLSX files from MEGA
    files = m.get_files()
    for file_id, file_info in files.items():
        if file_info['name'].endswith('.xlsx'):
            m.download(file_info, dest_path='.')

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! Use /search <mobile_number> to find details.')

def search(update: Update, context: CallbackContext) -> None:
    number = context.args[0]
    download_files_from_mega()
    
    results = []
    for file_name in os.listdir('.'):
        if file_name.endswith('.xlsx'):
            df = pd.read_excel(file_name)
            matches = df[df.apply(lambda row: row.astype(str).str.contains(number).any(), axis=1)]
            if not matches.empty:
                results.append(matches)
    
    if results:
        reply = ""
        for result in results:
            reply += result.to_string(index=False) + "\n\n"
        update.message.reply_text(reply)
    else:
        update.message.reply_text('No details found for this number.')

def main():
    updater = Updater(TELEGRAM_TOKEN)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CommandHandler('search', search))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
  
