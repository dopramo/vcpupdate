import subprocess
import logging
import os
import telebot

BOT_TOKEN = os.environ.get('BOT_TOKEN')
RTMP_URL = os.environ.get('RTMP_URL')
M3U8_URL = os.environ.get('M3U8_URL')

bot = telebot.TeleBot(BOT_TOKEN)

# Set logging for debugging purposes
logging.basicConfig(level=logging.DEBUG)

# Global process to handle FFmpeg
stream_process = None

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Bot is working!")

@bot.message_handler(commands=['startstream'])
def start_stream(message):
    global stream_process
    if stream_process:
        bot.reply_to(message, "Stream is already running!")
        return

    bot.reply_to(message, "Starting the stream...")

    try:
        # Start streaming using FFmpeg
        stream_process = subprocess.Popen([
            "ffmpeg",
            "-i", M3U8_URL,
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-b:v", "1500k",
            "-r", "25",
            "-g", "50",
            "-f", "flv",
            RTMP_URL
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        stdout, stderr = stream_process.communicate()

        # Log FFmpeg output
        logging.debug(stdout.decode())
        logging.debug(stderr.decode())

        bot.reply_to(message, "Stream started successfully!")

    except Exception as e:
        logging.error(f"Error starting stream: {str(e)}")
        bot.reply_to(message, f"Error starting stream: {str(e)}")

@bot.message_handler(commands=['stopstream'])
def stop_stream(message):
    global stream_process
    if not stream_process:
        bot.reply_to(message, "No stream is running!")
        return

    # Stop the stream process
    stream_process.terminate()
    stream_process = None
    bot.reply_to(message, "Stream stopped successfully!")

# Start polling
bot.polling()
