import pytest
from telegram import Update, Message, Chat, User
from telegram.ext import ContextTypes
from src.handlers.basic_handlers import start_command, help_command

@pytest.fixture
def mock_update():
    update = Update(1)
    update.message = Message(1, User(1, 'test_user', False), None, Chat(1, 'private'))
    return update

@pytest.fixture
def mock_context():
    return ContextTypes.DEFAULT_TYPE()

@pytest.mark.asyncio
async def test_start_command(mock_update, mock_context):
    await start_command(mock_update, mock_context)
    assert mock_update.message.reply_text.called

@pytest.mark.asyncio
async def test_help_command(mock_update, mock_context):
    await help_command(mock_update, mock_context)
    assert mock_update.message.reply_text.called
