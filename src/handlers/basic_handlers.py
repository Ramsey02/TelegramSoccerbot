from telegram import Update
from telegram.ext import ContextTypes
from models import Player, storage
import random
import datetime

'''
dont add or remove urself twice
check the list command , also it should print names
do a split randomly command
backup the data
'''


'''
The idea:
so every groupchat has its own single active game, every groupchat has to setup and add themselves ones.
and after that they can create games and cancel them.
'''
######################## helper functions ##################################
async def cleanup_command(update: Update):
    """Delete a command message if possible"""
    try:
        await update.message.delete()
        return True
    except Exception as e:
        await update.context.bot.send_message(
                    chat_id=update.effective_chat.id,
                    text="An error occurred while trying to delete the command message.")
        pass

async def is_admin(update: Update):
    """Check if the sender is an admin in the group"""
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    
    try:
        # Get chat administrators
        chat_admins  = await update.effective_chat.get_administrators()
        # admin_ids = [admin.user.id for admin in admins]
        if update.effective_user.id in (admin.user.id for admin in chat_admins):
            return True
    except Exception as e:
        return False

def is_player_registered(update: Update):
    """Check if the sender is registered in the group"""
    user_id = update.effective_user.id
    chat_id = update.effective_chat.id
    if storage.get_player(user_id, chat_id) is None:
        return False
    return True

def is_there_game(update: Update):
    """Check if the group has an active game"""
    chat_id = update.effective_chat.id
    if storage.get_game(chat_id) is None:
        return False
    return True

def is_group_setup(update: Update):
    """Check if the group is set up for football coordination"""
    chat_id = update.effective_chat.id
    if storage.is_group_registered(chat_id):
        return True
    return False
    
def is_private_chat(update: Update):
    """Check if the chat is a private chat"""
    return update.effective_chat.type == 'private'

def is_group_chat(update: Update):
    """Check if the chat is a group chat"""
    return update.effective_chat.type in ['group', 'supergroup']

############################################################################
""" dont use reply text, instead use send message:
 send message context.bot.send_message(chat_id=update.effective_chat.id,text=)
    """

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """check if its a group or not, returns false if its a private chat"""
    if await is_private_chat(update):
        await context.bot.send_message(chat_id=update.effective_chat.id,text="This bot is meant to be used in group chats only.")
        return
    await context.bot.send_message(chat_id=update.effective_user.id,text="Hello! I'm the football coordination bot. Use /help to see available commands.")
    await cleanup_command(update)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /help command"""
    help_text = """
Available commands:
/start - Start the bot
/help - Show this help message
/register - Register for the game
/remove - Remove yourself from the player list
/list - Show the current teams and waiting list
/setup_football - Set up this group for football coordination (admin only)
    """
    
    # Check if message is from a group chat
    if is_group_chat(update):
        # Send help message privately
        await context.bot.send_message(
            chat_id=update.effective_user.id,
            text=help_text
        )
        # Delete the command message from the group
        await cleanup_command(update)
    else:
        # Direct message - reply normally
        await update.message.reply_text(help_text)


async def helpOutBro_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /help command"""
    help_text = """
dont worry about it got you, i got you, just enter in the chat "/help"
    """
    
    # Check if message is from a group chat
    if await is_group_chat(update):
        # Send message privately
        await context.bot.send_message(
            chat_id=update.effective_user.id,
            text=help_text
        )
        # Delete the command message from the group
        await cleanup_command(update)
    else:
        # Direct message - reply normally
        await update.message.reply_text(help_text)


async def notACommand_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle messages that are not commands"""
    message_text = "I'm sorry, I only understand commands. use /help to see available commands."
    
    # Check if message is from a group chat
    if await is_group_chat(update):
        # Send message privately
        await context.bot.send_message(
            chat_id=update.effective_user.id,
            text=message_text
        )
        # Delete the original message from the group
        await cleanup_command(update)
    else:
        # Direct message - reply normally
        await update.message.reply_text(message_text)


async def invalid_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle invalid commands"""
    message_text = "Invalid command. Use /help to see available commands."
    
    # Check if message is from a group chat
    if await is_group_chat(update):
        # Send message privately
        await context.bot.send_message(
            chat_id=update.effective_user.id,
            text=message_text
        )
        # Delete the command message from the group
        await cleanup_command(update)
    else:
        # Direct message - reply normally
        await update.message.reply_text(message_text)

############################################################################


'''
check :
- setup is ready (when you set up once, or twice)
- register is ready (register once, twice, and when the list is full, and empty)
- remove is ready
- backup of data
'''
async def setup_football_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Register a group as a football coordination group"""
    # Only process in group chats
    if not is_group_chat(update):
        await context.bot.send_message(chat_id=update.effective_chat.id,text="This bot is meant to be used in group chats only.")
        return
    # Check if sender is an admin
    chat_id = update.effective_chat.id

    try:
        # Get chat administrators
        if not await is_admin(update):
            await context.bot.send_message(chat_id=chat_id,text="Only group administrators can set up this group for football coordination.")
            return
        # Register the group
        result = storage.register_football_group(chat_id)
        
        if result:
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"This group has been registered for football coordination! ⚽"
            )
        else:
            await context.bot.send_message(
                chat_id=chat_id,
                text="This group is already registered for football coordination."
            )
        # Try to delete the command message
    except Exception as e:
        await context.bot.send_message(
                chat_id=chat_id,
                text="An error occurred while setup! Please try again.")
        pass
    await cleanup_command(update)     

async def create_game(update: Update, context : ContextTypes.DEFAULT_TYPE):
    """Create a new game"""
    chat_id = update.effective_chat.id
    if not is_group_chat(update):
        await context.bot.send_message(chat_id=chat_id,text="This bot is meant to be used in group chats only.")
        return
    if not is_group_setup(update):
        await context.bot.send_message(chat_id=chat_id,text="This group is not set up for football coordination yet. Ask an admin to set it up first.")
        return
    if not await is_admin(update):
        await context.bot.send_message(chat_id=chat_id,text="Only group administrators can create a new game.")
        return
    if is_there_game(update):
        await context.bot.send_message(chat_id=chat_id,text="This group already has an active game.")
        return
    ''' args in this order (if there are any): max_players, date, location'''
    '''checking args with a helper function, args can be 0 or 1 or 2 or 3'''
    result = await aux_create_game_by_diff_num_args(update, context, chat_id)
    await cleanup_command(update)

async def aux_create_game_by_diff_num_args(update, context, chat_id) -> bool:
    sorted_args = sorted(context.args)
    creator_name = update.effective_user.full_name
    if len(sorted_args) > 3:
        await context.bot.send_message(chat_id=chat_id, text="Too many arguments. Use /help to see how to use this command.")
        return False
    if len(sorted_args) == 1:
        '''first one might be either max_players or just a string for location'''
        first_arg = sorted_args[0]
        if isinstance(first_arg, str):
            game = storage.create_game(chat_id, update.effective_user.id, location=first_arg)
            await context.bot.send_message(chat_id=chat_id, text=f"⭐⭐ A new game has been created by {creator_name} at {first_arg}! Use /register to join the game.⭐⭐")
        elif isinstance(first_arg, int):
            game = storage.create_game(chat_id, update.effective_user.id, max_players=first_arg)
            await context.bot.send_message(chat_id=chat_id, text=f"⭐⭐ A new game has been created by {creator_name} with a maximum of {first_arg} players! Use /register to join the game.⭐⭐")
        else:
            await context.bot.send_message(chat_id=chat_id, text="Invalid argument. Use /help to see how to use this command.")
            return False
    elif len(sorted_args) == 2:
        max_players, date = sorted_args
        if not isinstance(max_players, int) or not isinstance(date, datetime.datetime):
            await context.bot.send_message(chat_id=chat_id, text="Invalid max players or date. Use /help to see how to use this command.")
            return False
        game = storage.create_game(chat_id, update.effective_user.id, max_players=max_players, date=date)
        await context.bot.send_message(chat_id=chat_id, text=f"⭐⭐ A new game has been created by {creator_name} for {date} with a maximum of {max_players} players! Use /register to join the game.⭐⭐")
    elif len(sorted_args) == 3:
        max_players, date, location = sorted_args
        if not isinstance(max_players, int) or not isinstance(date, datetime.datetime) or not isinstance(location, str):
            await context.bot.send_message(chat_id=chat_id, text="Invalid max players, date, or location. Use /help to see how to use this command.")
            return False
        game = storage.create_game(chat_id, update.effective_user.id, max_players=max_players, date=date, location=location)
        await context.bot.send_message(chat_id=chat_id, text=f"⭐⭐ A new game has been created by {creator_name} for {date} at {location} with a maximum of {max_players} players! Use /register to join the game.⭐⭐")
    else:
        game = storage.create_game(chat_id, update.effective_user.id)
        await context.bot.send_message(chat_id=chat_id, text=f"⭐⭐ A new game has been created by {creator_name}! Use /register to join the game.⭐⭐")
    return True

async def cancel_game(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the current game"""
    chat_id = update.effective_chat.id
    if not is_group_chat(update):
        await context.bot.send_message(chat_id=chat_id,text="This bot is meant to be used in group chats only.")
        return
    if not is_group_setup(update):
        await context.bot.send_message(chat_id=chat_id,text="This group is not set up for football coordination yet. Ask an admin to set it up first.")
        return
    if not await is_admin(update):
        await context.bot.send_message(chat_id=chat_id,text="Only group administrators can cancel the current game.")
        return
    if not is_there_game(update):
        await context.bot.send_message(chat_id=chat_id,text="This group has no active game.")
        return
    result = storage.delete_game(chat_id)
    if result:
        await context.bot.send_message(chat_id=chat_id,text="The current game has been canceled.")
    else:
        await context.bot.send_message(chat_id=chat_id,text="An error occurred while trying to cancel the current game.")

    await cleanup_command(update)

"""
since i cannot use get_common_chats() to check the common groupchats between the bot and the player,
then there are two options here:
1) the player must specify by himself which is the groupchat he wants to register in, and admin can check if
he is indeed a member and register him
2) the player sends commands in the groupchat, which is easier but not as clean imo as the first option
"""
async def register_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /register command in group chats"""
    if is_group_chat(update):
        # Get the actual group ID directly from the update
        group_id = update.effective_chat.id
        user_id = update.effective_user.id

        if is_group_setup(update) is None:
            await context.bot.send_message(
                chat_id=user_id,
                text="This group is not set up for football coordination yet ❗ Ask an admin to set it up first. "
            )
            return
        
        if not is_there_game(update):
            await context.bot.send_message(
                chat_id=user_id,
                text="This group has no active game❗ Ask an admin to set it up first. "
            )
            return
        
        if is_player_registered(update):
            await context.bot.send_message(
                chat_id=user_id,
                text="You are already registered for this game.❗❗"
            )
            return
        player = Player.from_update(update)
        # Register the player with this group
        result = storage.add_player(player, group_id)
        if result:
            await context.bot.send_message(
                chat_id=user_id,
                text=f"{player.full_name} has been registered successfully! ✅"
            )
        else:
            await context.bot.send_message(
                chat_id=user_id,
                text="the playing list and waitlist are full. Please try again later."
            )
    else:
        await update.message.reply_text("This command can only be used in group chats.")
    cleanup_command(update)

async def remove_player(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /remove command"""
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    if not is_group_chat(update):
        await context.bot.send_message(chat_id=user_id,text="This bot is meant to be used in group chats only.")
        return
    if not is_group_setup(update):
        await context.bot.send_message(chat_id=user_id,text="This group is not set up for football coordination yet. Ask an admin to set it up first.")
        return
    if not is_player_registered(update):
        await context.bot.send_message(chat_id=user_id,text="You are not registered for this game.")
        return
    result = storage.remove_player(user_id,chat_id)
    if result:
        await context.bot.send_message(chat_id=user_id,text=f"{update.effective_user.full_name} has been removed from the game.")
    else:
        await context.bot.send_message(chat_id=user_id,text="An error occurred while trying to remove the player.")
    await cleanup_command(update)

async def list_players(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /list command"""
    chat_id = update.effective_chat.id
    if not is_group_chat(update):
        await context.bot.send_message(chat_id=chat_id,text="This bot is meant to be used in group chats only.")
        return
    if not is_group_setup(update):
        await context.bot.send_message(chat_id=chat_id,text="This group is not set up for football coordination yet. Ask an admin to set it up first.")
        return
    if not is_there_game(update):
        await context.bot.send_message(chat_id=chat_id,text="This group has no active game.")
        return
    game = storage.get_game(chat_id)
    playing_list = game.playing_list
    waiting_list = game.waiting_list
    playing_list_text = "\n".join([player.full_name for player in playing_list])
    waiting_list_text = "\n".join([player.full_name for player in waiting_list])
    await context.bot.send_message(chat_id=chat_id,text=f"Playing list:\n{playing_list_text}\n\nWaiting list:\n{waiting_list_text}")
    await cleanup_command(update)