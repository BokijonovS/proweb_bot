from pprint import pprint
import os
from flask import Flask
from threading import Thread

import telebot
import requests
import re

from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton

# Replace with your Telegram bot token and Freepik API key
BOT_TOKEN = "7642750809:AAGia4vhE-SE_024OcrbVBi6EKPA4yvcFU8"
API_KEY = "FPSXaa11b9ac63744a619f3ab20df2157ea9"

bot = telebot.TeleBot(BOT_TOKEN)

# Flask setup
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

def run_flask():
    port = int(os.getenv("PORT", 5000))  # Use the PORT environment variable or default to 5000
    app.run(host="0.0.0.0", port=port)

# Telegram bot handlers
@bot.message_handler(commands=['start'])
def start_command(message):
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    icon_button = KeyboardButton("Icon")  # You can use any emoji as the icon
    other_button = KeyboardButton("Video")  # You can use any emoji as the icon
    other_button1 = KeyboardButton("Photo")  # You can use any emoji as the icon
    markup.add(icon_button, other_button, other_button1)
    bot.reply_to(message, "Welcome to the Freepik Downloader Bot! Please choose one of the options below!",
                 reply_markup=markup)

@bot.message_handler(func=lambda message: "Icon" in message.text)
def handle_message(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, "Icon id sini kiriting")
    bot.register_next_step_handler(msg, give_icon)

def give_icon(message: Message):
    chat_id = message.chat.id
    resource_id = message.text
    print(resource_id)

    # Freepik API endpoint for resource details
    download_url = f"https://api.freepik.com/v1/icons/{resource_id}/download"

    # Headers for authentication
    headers = {
        "x-freepik-api-key": API_KEY
    }

    response = requests.get(download_url, headers=headers)
    pprint(response)
    if response.status_code == 200:
        download_data = response.json()
        pprint(download_data)
        file_url = download_data['data']['url']
        print(file_url)
        bot.send_message(chat_id, f'<a href="{file_url}">Bu yerdan yuklab olishingiz mumkin</a>.', parse_mode='HTML')
    else:
        bot.send_message(chat_id, f"Failed to fetch resource: {response.status_code} - {response.text}")

@bot.message_handler(func=lambda message: "Video" in message.text or "Photo" in message.text)
def handle_message(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, "Resurs id sini kiriting")
    bot.register_next_step_handler(msg, give_resource)

def give_resource(message: Message):
    chat_id = message.chat.id
    resource_id = message.text
    print(resource_id)

    # Freepik API endpoint for resource details
    download_url = f"https://api.freepik.com/v1/resources/{resource_id}/download"

    # Headers for authentication
    headers = {
        "x-freepik-api-key": API_KEY
    }

    response = requests.get(download_url, headers=headers)
    pprint(response)
    if response.status_code == 200:
        download_data = response.json()
        pprint(download_data)
        file_url = download_data['data']['url']
        print(file_url)
        bot.send_message(chat_id, f'<a href="{file_url}">Bu yerdan yuklab olishingiz mumkin</a>.', parse_mode='HTML')
    else:
        bot.send_message(chat_id, f"Failed to fetch resource: {response.status_code} - {response.text}")

# Main entry point
if __name__ == "__main__":
    print("Bot is running...")
    # Start Flask server in a separate thread
    Thread(target=run_flask).start()
    # Start the bot
    bot.polling()
