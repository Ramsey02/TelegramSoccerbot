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
# Option 1: Modify individual handlers
# Here's how you'd update your register_handler:

async def register_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /register command"""
    player = Player.from_update(update)
    storage.add_player(player)
    
    # Reply to the user
    await update.message.reply_text(f"You have been registered {player.full_name}")
    
    # Delete the original command message
    try:
        await update.message.delete()
    except Exception as e:
        # This might fail if the bot doesn't have delete permissions
        logger.warning(f"Could not delete message: {e}")


# Option 2: Create a decorator to handle message deletion
# This is a more elegant solution that keeps your code DRY

import functools
import logging

logger = logging.getLogger(__name__)

def delete_command_after(handler_func):
    """Decorator that deletes the command message after handler execution"""
    @functools.wraps(handler_func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE):
        # Execute the original handler
        result = await handler_func(update, context)
        
        # Delete the original message
        try:
            await update.message.delete()
        except Exception as e:
            logger.warning(f"Could not delete message: {e}")
            
        return result
    return wrapper


# Then you can apply it to your handlers like this:
@delete_command_after
async def register_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /register command"""
    player = Player.from_update(update)
    storage.add_player(player)
    await update.message.reply_text(f"You have been registered {player.full_name}")


# Option 3: Create a utility function for message cleanup
# This gives you more flexibility for different handlers

async def cleanup_command(message):
    """Delete a command message if possible"""
    try:
        await message.delete()
        return True
    except Exception as e:
        logger.warning(f"Could not delete message: {e}")
        return False

async def find_shared_groups(bot, user_id):
    """Find football groups shared between the bot and user"""
    try:
        # Get common chats directly from Telegram API
        common_chats = await bot.get_common_chats(user_id)
        
        # Extract all group IDs
        all_shared_groups = [
            chat.id for chat in common_chats.chats 
            if chat.type in ['group', 'supergroup']
        ]
        
        # Filter for only football groups
        football_groups = [
            group_id for group_id in all_shared_groups
            if storage.is_football_group(group_id)
        ]
        
        return football_groups
        
    except Exception as e:
        logger.error(f"Error finding shared chats: {e}")
        return []

async def setup_football_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Register a group as a football coordination group"""
    # Only process in group chats
    if update.effective_chat.type not in ['group', 'supergroup']:
        await update.message.reply_text("This command can only be used in group chats.")
        return
    
    # Check if sender is an admin
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    
    try:
        # Get chat administrators
        admins = await context.bot.get_chat_administrators(chat_id)
        admin_ids = [admin.user.id for admin in admins]
        
        if user_id in admin_ids:
            # Register the group
            group_name = update.effective_chat.title
            result = storage.register_football_group(chat_id, group_name)
            
            if result:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text=f"This group has been registered for football coordination! ⚽"
                )
            else:
                await context.bot.send_message(
                    chat_id=chat_id,
                    text="There was an error registering this group. Please try again."
                )
        else:
            # Inform that only admins can use this command
            await context.bot.send_message(
                chat_id=chat_id,
                text="Only group administrators can register this group for football coordination."
            )
            
        # Try to delete the command message
        try:
            await update.message.delete()
        except:
            pass
            
    except Exception as e:
        logging.error(f"Error in setup_football_group: {e}")
        await update.message.reply_text("An error occurred. Please try again later.")
        
async def register_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /register command with context awareness"""
    chat_type = update.effective_chat.type
    user = update.effective_user
    
    if chat_type == 'private':
        # Handle private registration
        player = Player.from_update(update)
        result = storage.add_player(player)
        
        if result == 'added':
            # New registration
            await update.message.reply_text(
                f"You have been registered successfully, {player.full_name}!"
            )
            status_text = f"{player.full_name} has registered."
            
        elif result == 'updated':
            # Existing player updated
            await update.message.reply_text(
                f"Your registration has been updated, {player.full_name}!"
            )
            status_text = f"{player.full_name} has updated their registration."
            
        else:
            # Registration failed
            await update.message.reply_text(
                "Registration failed. Please try again later."
            )
            return
            
        # Find and notify shared football groups
        shared_football_groups = await find_shared_groups(context.bot, user.id)
        for group_id in shared_football_groups:
            await context.bot.send_message(
                chat_id=group_id,
                text=f"Playing list has changed! {status_text}"
            )
            
    else:
        # In group chat - delete command silently
        try:
            await update.message.delete()
        except:
            pass  # Silently fail if deletion isn't possible
    """Handle the /register command"""
    chat_type = update.effective_chat.type
    user = update.effective_user
    
    if chat_type == 'private':
        # Register the user
        player = Player.from_update(update)
        storage.add_player(player)
        
        # Confirm registration to the user
        await update.message.reply_text(f"You have been registered successfully, {player.full_name}!")
        
        # Find shared groups using Telegram's API
        shared_groups = await find_shared_groups(context.bot, user.id)
        
        # Notify all relevant football groups
        for group_id in shared_groups:
            # You might want to check if this is actually a football group
            # This could be done by checking against your database of football groups
            if storage.is_football_group(group_id):
                await context.bot.send_message(
                    chat_id=group_id,
                    text=f"Playing list has changed! {player.full_name} has registered."
                )
    else:
        # In group chat - just delete the command
        try:
            await update.message.delete()
        except Exception as e:
            logger.warning(f"Could not delete message: {e}")