import os
import telebot
import subprocess

# Securely retrieve the bot token and RTMP URL
BOT_TOKEN = os.getenv("7313917094:AAGqqvjgwBHaAAQJSxRR6oCp3s25BilWQdQ")  # Add your token here
RTMP_URL = os.getenv("rtmps://dc5-1.rtmp.t.me/s/1529495932:a-yqHTaa-uW6Tx0r2wpa2w")  # Full RTMP URL with the key (e.g., rtmp://dc3-1.rtmp.t.me/live/<key>)

bot = telebot.TeleBot(BOT_TOKEN)
stream_process = None

@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(message, "Hello! Use /startstream to begin streaming and /stopstream to stop.")

@bot.message_handler(commands=["startstream"])
def start_stream(message):
    global stream_process
    if stream_process:
        bot.reply_to(message, "Stream is already running!")
        return

    m3u8_url = "https://livecdn.thepapare.com/out/v1/f08df06f4d95476a90bd2f868dcb524a/index.m3u8"  # Replace with your M3U8 stream URL

    bot.reply_to(message, "Starting the stream...")
    try:
        # FFmpeg command to stream to Telegram
        stream_process = subprocess.Popen([
            "ffmpeg",
            "-i", m3u8_url,
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-maxrate", "3000k",
            "-bufsize", "6000k",
            "-f", "flv",
            RTMP_URL
        ])
        bot.reply_to(message, "Stream started successfully!")
    except Exception as e:
        bot.reply_to(message, f"Error starting stream: {e}")

@bot.message_handler(commands=["stopstream"])
def stop_stream(message):
    global stream_process
    if not stream_process:
        bot.reply_to(message, "No stream is running!")
        return

    stream_process.terminate()
    stream_process = None
    bot.reply_to(message, "Stream stopped successfully!")

bot.polling()
