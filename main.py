import os
import logging
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

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
      
