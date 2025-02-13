import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.filters import Command
from dotenv import load_dotenv

# Load bot token from .env file
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Store user data (temporary, use a database for real use)
user_data = {}

# Command: /start
@dp.message(Command("start"))
async def start_command(message: Message):
    user_id = message.from_user.id
    if user_id not in user_data:
        user_data[user_id] = {"balance": 0, "rank": "Beginner"}

    keyboard = [
        [InlineKeyboardButton("💰 Earn ST Coin", callback_data='earn')],
        [InlineKeyboardButton("🎁 Daily Bonus", callback_data='bonus')],
        [InlineKeyboardButton("📊 Leaderboard", callback_data='leaderboard')],
        [InlineKeyboardButton("👤 Profile", callback_data='profile')]
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=keyboard)

    await message.answer("🎮 Welcome to SOUNDTRUMP!\nChoose an option below:", reply_markup=markup)

# Command: /help
@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer("Commands available:\n/start - Start the bot\n/help - Get help")

# Handle all other messages
@dp.message()
async def echo_message(message: Message):
    await message.answer(f"You said: {message.text}")

# Main function to run the bot
async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

# Run the bot
if __name__ == "__main__":
    asyncio.run(main())
