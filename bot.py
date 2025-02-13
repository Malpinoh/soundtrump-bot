import logging
import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from aiogram.filters import Command
from dotenv import load_dotenv
from aiohttp import web
from aiogram.types import Update


# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Set this in Railway environment variables

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Store user data (temporary, use a database for real use)
user_data = {}

# /start command
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

# /help command
@dp.message(Command("help"))
async def help_command(message: Message):
    await message.answer("Commands available:\n/start - Start the bot\n/help - Get help")

# Handle button clicks
@dp.callback_query()
async def handle_buttons(callback: CallbackQuery):
    if callback.data == "earn":
        await callback.message.answer("💰 You clicked 'Earn ST Coin'!")
    elif callback.data == "bonus":
        await callback.message.answer("🎁 Daily Bonus coming soon!")
    elif callback.data == "leaderboard":
        await callback.message.answer("📊 Leaderboard is being updated.")
    elif callback.data == "profile":
        await callback.message.answer("👤 Your profile is under construction.")
    
    await callback.answer()  # Acknowledge callback

# Webhook setup
async def on_startup(_):
    await bot.set_webhook(WEBHOOK_URL)

async def on_shutdown(_):
    await bot.delete_webhook()

# Create web server for webhook
app = web.Application()
async def handle_webhook(request):
    update = await request.json()
    from aiogram.types import Update

async def handle_webhook(request):
    body = await request.json()
    update = Update.model_validate(body)  # Aiogram v3 uses `model_validate` instead of `parse_raw`
    await dp.update.update(update)
    return web.Response()
    return web.Response()

app.router.add_post("/webhook", handle_webhook)

# Run the bot with webhook
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    web.run_app(app, host="0.0.0.0", port=8000)
