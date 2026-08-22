import logging
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)
import yt_dlp

# Logging သတ်မှတ်ခြင်း
logging.basicConfig(level=logging.INFO)


# UptimeRobot Ping ခေါ်ဆိုမှုကို တုံ့ပြန်ရန် Web Server
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

  def do_GET(self):
    self.send_response(200)
    self.end_headers()
    self.wfile.write(b"Bot is live!")

  def do_HEAD(self):
    self.send_response(200)
    self.end_headers()


def run_web_server():
  port = int(os.environ.get("PORT", 8080))
  server = HTTPServer(("0.0.0.0", port), SimpleHTTPRequestHandler)
  server.serve_forever()


# Web Server ကို Background တွင် စတင်မောင်းနှင်ခြင်း
threading.Thread(target=run_web_server, daemon=True).start()


# Telegram Bot Command များနှင့် လုပ်ဆောင်ချက်များ
def start(update: Update, context: CallbackContext):
  update.message.reply_text(
      "မင်္ဂလာပါ။ Facebook သို့မဟုတ် TikTok ဗီဒီယို Link ကို ပို့ပေးပါ။"
  )


def download_video(update: Update, context: CallbackContext):
  url = update.message.text
  if (
      "facebook.com" in url
      or "fb.watch" in url
      or "tiktok.com" in url
      or "vt.tiktok.com" in url
  ):
    msg = update.message.reply_text(
        "ဗီဒီယိုကို ဒေါင်းလုဒ်ရယူနေပါသည်... ခဏစောင့်ပေးပါ။"
    )

    ydl_opts = {
        "format": "best",
        "outtmpl": "downloaded_video.%(ext)s",
        "quiet": True,
    }

    try:
      with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)

      msg.edit_text("ဗီဒီယိုကို Telegram သို့ ပို့ပေးနေပါသည်...")

      with open(filename, "rb") as video:
        update.message.reply_video(video)

      msg.delete()
      if os.path.exists(filename):
        os.remove(filename)

    except Exception as e:
      logging.error(e)
      msg.edit_text("ဒေါင်းလုဒ်ဆွဲရာတွင် အမှားအယွင်း ရှိနေပါသည်။")


def main():
  token = os.environ.get("BOT_TOKEN")
  if not token:
    print("BOT_TOKEN မရှိပါ")
    return

  updater = Updater(token, use_context=True)
  dp = updater.dispatcher

  dp.add_handler(CommandHandler("start", start))
  dp.add_handler(
      MessageHandler(Filters.text & ~Filters.command, download_video)
  )

  updater.start_polling()
  updater.idle()


if __name__ == "__main__":
  main()
