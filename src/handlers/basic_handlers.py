from telegram import Update
from telegram.ext import ContextTypes
from models import Player, storage, Game



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
async def cleanup_command(message):
    """Delete a command message if possible"""
    await message.delete()
    return True
    # try:
    # except Exception as e:
    #     logger.warning(f"Could not delete message: {e}")
    #     return False

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
            result = storage.register_football_group(chat_id,user_id)
            
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
        await update.message.reply_text("An error occurred while setup! Please try again.")

# async def find_shared_groups(bot, user_id):
#     """Find football groups shared between the bot and user"""

"""
since i cannot use get_common_chats() to check the common groupchats between the bot and the player,
then there are two options here:
1) the player must specify by himself which is the groupchat he wants to register in, and admin can check if
he is indeed a member and register him
2) the player sends commands in the groupchat, which is easier but not as clean imo as the first option
"""
async def register_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /register command in group chats"""
    chat_type = update.effective_chat.type
    user = update.effective_user
    player = Player.from_update(update)

    if chat_type == 'group' or chat_type == 'supergroup':
        # Get the actual group ID directly from the update
        group_id = update.effective_chat.id
        
        # Register the player with this group
        result = storage.add_player(player, group_id)
        
        # First delete the original command
        try:
            await update.message.delete()
        except Exception as e:
            logger.warning(f"Could not delete command message: {e}")
        
        # Then send a standalone announcement (not a reply)
        try:
            await context.bot.send_message(
                chat_id=group_id,
                text=f"{player.full_name} has been registered successfully!"
            )
        except Exception as e:
            pass
'''
if chat_type == 'private':
    # Handle private registration
    player = Player.from_update(update)
    common_groups = await find_shared_groups(context.bot, user.id)
    if common_groups is []:
        await update.message.reply_text(
            "You need to be in a football coordination group to register."
        )
        return
    # we need to check if args is empty, if it is empty we need to ask the user to input the group name in case there are more than one common group
    elif len(common_groups) > 1:
        await update.message.reply_text(
            """You are in multiple football coordination groups. Please use the command again and specify the group name. 
            for example: /register <group_name>"""
        )
    else:
        # Register player in the only groupchat he is in
        result = storage.add_player(player, common_groups[0])
        await update.message.reply_text(
            f"You have been registered successfully, {player.full_name}!"
        )            
    # Find and notify shared football groups
    '''