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
    
    # Define handlers
    handlers = [
        # Group setup handlers
        CommandHandler("setup_football", setup_football_group),
        
        # Basic command handlers
        CommandHandler("start", start_command),
        CommandHandler("help", help_command),
        CommandHandler("HELPMEBRO", helpOutBro_command),
        
        # Game management handlers
        CommandHandler("create", create_game),
        CommandHandler("create_game", create_game),
        CommandHandler("cancel_game", cancel_game),
        
        # Player management handlers
        CommandHandler("register", register_handler),
        CommandHandler("remove", remove_player),
        CommandHandler("list", list_players),
        
        # Default handlers for unrecognized messages
        MessageHandler(filters.TEXT & ~filters.COMMAND, notACommand_handler),
        MessageHandler(filters.COMMAND, invalid_command)
    ]
    
    # Add handlers to application
    for handler in handlers:
        application.add_handler(handler)

    # Add error handler
    application.add_error_handler(error_handler)

    # Start the bot
    application.run_polling()

if __name__ == "__main__":
    main()