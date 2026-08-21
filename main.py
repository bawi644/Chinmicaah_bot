import os
import logging
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import yt_dlp

logging.basicConfig(level=logging.INFO)

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is live!")

def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), SimpleHTTPRequestHandler)
    server.serve_forever()

threading.Thread(target=run_web_server, daemon=True).start()

def start(update: Update, context: CallbackContext):
    update.message.reply_text("မင်္ဂလာပါ။ Facebook သို့မဟုတ် TikTok ဗီဒီယို Link ကို ပို့ပေးပါ။")

def download_video(update: Update, context: CallbackContext):
    url = update.message.text
    if "facebook.com" in url or "fb.watch" in url or "tiktok.com" in url:
        msg = update.message.reply_text("ဗီဒီယိုကို ဒေါင်းလုဒ်ရယူနေပါသည်...")
        ydl_opts = {
            'outtmpl': 'video.mp4',
            'format': 'best',
            'max_filesize': 50000000,
        }
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            with open('video.mp4', 'rb') as video_file:
                update.message.reply_video(video_file)
            msg.delete()
            if os.path.exists('video.mp4'):
                os.remove('video.mp4')
        except Exception as e:
            msg.edit_text(f"ဒေါင်းလုဒ်ဆွဲရတာ မအောင်မြင်ပါ: {e}")
    else:
        update.message.reply_text("ကျေးဇူးပြု၍ မှန်ကန်သော Facebook သို့မဟုတ် TikTok Link ကို ပေးပို့ပါ။")

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
      
