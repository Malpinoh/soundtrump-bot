import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, Update
from aiogram.filters import Command
from dotenv import load_dotenv
from aiohttp import web
import asyncio

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # Ensure this is set in Railway environment variables

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
    
    await callback.answer()  

# Webhook setup functions
async def on_startup(_):
    webhook_url = os.getenv("WEBHOOK_URL")  # Get webhook URL from env
    if webhook_url:
        await bot.set_webhook(webhook_url)
        print(f"✅ Webhook set to: {webhook_url}")
    else:
        print("❌ WEBHOOK_URL is not set!")

async def on_shutdown(_):
    await bot.delete_webhook()

# Webhook request handler
async def handle_webhook(request):
    body = await request.json()
    update = Update.model_validate(body)  # Properly validate update

    await dp.feed_update(bot, update)  # Correct aiogram v3 method
    
    return web.Response()

# Create web server for webhook
app = web.Application()
app.router.add_post("/webhook", handle_webhook)

# Run the bot with webhook
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    web.run_app(app, host="0.0.0.0", port=8000)
