import logging
import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackContext,
    CommandHandler,
    MessageHandler,
    filters,
)
import yt_dlp

logging.basicConfig(level=logging.INFO)


class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):

  def do_GET(self):
    self.send_response(200)
    self.end_headers()
    self.wfile.write(b"Bot is live!")

  def do_HEAD(self):
    self.send_response(200)
    self.end_headers()
      
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


threading.Thread(target=run_web_server, daemon=True).start()


async def start(update: Update, context: CallbackContext):
  await update.message.reply_text(
      "မင်္ဂလာပါ။ Facebook သို့မဟုတ် TikTok ဗီဒီယို Link ကို ပို့ပေးပါ။"
  )


async def download_video(update: Update, context: CallbackContext):
  url = update.message.text
  if (
      "facebook.com" in url
      or "fb.watch" in url
      or "tiktok.com" in url
      or "vt.tiktok.com" in url
  ):
    msg = await update.message.reply_text(
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

      await msg.edit_text("ဗီဒီယိုကို Telegram သို့ ပို့ပေးနေပါသည်...")

      with open(filename, "rb") as video:
        await update.message.reply_video(video)

      await msg.delete()
      if os.path.exists(filename):
        os.remove(filename)

    except Exception as e:
      logging.error(e)
      await msg.edit_text("ဒေါင်းလုဒ်ဆွဲရာတွင် အမှားအယွင်း ရှိနေပါသည်။")


def main():
  token = os.environ.get("BOT_TOKEN")
  if not token:
    print("BOT_TOKEN မရှိပါ")
    return

  app = ApplicationBuilder().token(token).build()
  app.add_handler(CommandHandler("start", start))
  app.add_handler(
      MessageHandler(filters.TEXT & ~filters.COMMAND, download_video)
  )

  app.run_polling()


if __name__ == "__main__":
  main()
