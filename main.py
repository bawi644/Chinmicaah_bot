import os
import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import yt_dlp

logging.basicConfig(level=logging.INFO)

def start(update: Update, context: CallbackContext):
    update.message.reply_text("မင်္ဂလာပါ။ Facebook သို့မဟုတ် TikTok Video Link ပို့ပေးပါ။")

def download_video(update: Update, context: CallbackContext):
    url = update.message.text
    if "facebook.com" in url or "fb.watch" in url or "tiktok.com" in url:
        msg = update.message.reply_text("ဗီဒီယို ဒေါင်းလုဒ်ဆွဲနေပါသည်၊ ခဏစောင့်ပါ။...")
        
        ydl_opts = {
            'outtmpl': 'video.mp4',
            'format': 'best',
            'max_filesize': 50000000,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            with open('video.mp4', 'rb') as video:
                update.message.reply_video(video=video, caption="Downloaded successfully!")
            
            msg.delete()
            os.remove('video.mp4')
        except Exception as e:
            msg.edit_text("ဒေါင်းလုဒ်ဆွဲရတာ မအောင်မြင်ပါ။ Link ကို ပြန်စစ်ပေးပါ။")
    else:
        update.message.reply_text("ကျေးဇူးပြု၍ မှန်ကန်သော Facebook သို့မဟုတ် TikTok Link ပို့ပေးပါ။")

def main():
    token = os.environ.get("BOT_TOKEN")
    updater = Updater(token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, download_video))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
      
