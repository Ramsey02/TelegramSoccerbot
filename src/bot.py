import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import Config
from handlers.basic_handlers import *
from models import Storage, Player, Game, GameStatus

# Set up logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def error_handler(update, context):
    """Log errors caused by updates."""
    logger.error(f"Update {update} caused error {context.error}")

def main():
    """Start the bot."""
    # Validate configuration
    Config.validate()
    
    # Create application instance
    application = Application.builder().token(Config.BOT_TOKEN).build()

    
    # Add handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("HELPMEBRO", helpOutBro_command))
    application.add_handler(CommandHandler("register", register_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~ filters.COMMAND,notACommand_handler))
    application.add_handler(MessageHandler(filters.COMMAND,invalid_command))

    # Add error handler
    application.add_error_handler(error_handler)

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()
