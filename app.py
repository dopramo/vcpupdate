import os
import telebot
import subprocess

# Replace with your actual token and RTMP URL
BOT_TOKEN = "7313917094:AAGqqvjgwBHaAAQJSxRR6oCp3s25BilWQdQ"
RTMP_URL = "rtmps://dc5-1.rtmp.t.me/s/1529495932:a-yqHTaa-uW6Tx0r2wpa2w"  # Replace with your actual RTMP URL
bot = telebot.TeleBot(BOT_TOKEN)

stream_process = None  # To track the streaming process

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hello! Use /startstream to begin streaming and /stopstream to stop.")

@bot.message_handler(commands=['startstream'])
def start_stream(message):
    global stream_process
    if stream_process:
        bot.reply_to(message, "Stream is already running!")
        return

    m3u8_url = "https://livecdn.thepapare.com/out/v1/f08df06f4d95476a90bd2f868dcb524a/index.m3u8"  # Replace with your actual M3U8 link
    bot.reply_to(message, "Starting the stream...")

    try:
        # Run FFmpeg to stream to Telegram with added compatibility settings
        stream_process = subprocess.Popen([
            "ffmpeg",
            "-i", m3u8_url,  # Input M3U8 stream
            "-c:v", "libx264",  # Video codec
            "-preset", "veryfast",  # Encoding speed
            "-b:v", "1500k",  # Video bitrate
            "-r", "25",  # Frame rate
            "-g", "50",  # Keyframe interval (important for RTMP)
            "-f", "flv",  # Output format
            RTMP_URL  # RTMP URL
        ])
        bot.reply_to(message, "Stream started successfully!")
    except Exception as e:
        bot.reply_to(message, f"Error starting stream: {e}")

@bot.message_handler(commands=['stopstream'])
def stop_stream(message):
    global stream_process
    if not stream_process:
        bot.reply_to(message, "No stream is running!")
        return

    stream_process.terminate()  # Stop the FFmpeg process
    stream_process = None
    bot.reply_to(message, "Stream stopped successfully!")

bot.polling()
