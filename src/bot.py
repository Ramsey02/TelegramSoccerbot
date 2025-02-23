import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from config import Config
from handlers.basic_handlers import *

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
    # Group setup handlers
    application.add_handler(CommandHandler("setup_football", setup_football_group))
    
    # Basic command handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("HELPMEBRO", helpOutBro_command))
    
    # game management handlers
    application.add_handler(CommandHandler("create", create_game))
    application.add_handler(CommandHandler("create_game", create_game))
    application.add_handler(CommandHandler("cancel_game", cancel_game))
    # Player management handlers
    application.add_handler(CommandHandler("register", register_handler))
    application.add_handler(CommandHandler("remove", remove_player))
    application.add_handler(CommandHandler("list", list_players))
    
    
    # Default handlers for unrecognized messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, notACommand_handler))
    application.add_handler(MessageHandler(filters.COMMAND, invalid_command))

    # Add error handler
    application.add_error_handler(error_handler)

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()