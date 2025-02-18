from telegram import Update
from telegram.ext import ContextTypes
from models import Player, storage, Game, GameStatus



async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /start command"""
    await update.message.reply_text(
        "Welcome! I'm your new Telegram bot. Use /help to see available commands."
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /help command"""
    help_text = """
Available commands:
/start - Start the bot
/help - Show this help message
    """
    await update.message.reply_text(help_text)

async def helpOutBro_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /help command"""
    help_text = """
dont worry about it got you, i got you, just enter in the chat "/help"
    """
    await update.message.reply_text(help_text)

async def notACommand_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle messages that are not commands"""
    await update.message.reply_text("I'm sorry, I only understand commands. use /help to see available commands.")

async def invalid_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle invalid commands"""
    await update.message.reply_text("Invalid command. Use /help to see available commands.")

############################################################################
async def register_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /register command"""
    player = Player.from_update(update)
    storage.add_player(player)
    # await update.message.reply_text("You have been registered " + args[0])
    await update.message.reply_text("You have been registered " + player.full_name)