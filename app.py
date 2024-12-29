import os
import telebot
import subprocess

# Read from environment variables
BOT_TOKEN = os.environ.get('BOT_TOKEN')
RTMP_URL = os.environ.get('RTMP_URL')
m3u8_url = os.environ.get('M3U8_URL')  # If you store the M3U8 URL in Heroku

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
