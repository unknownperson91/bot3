from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters
import logging
from datetime import datetime

# Replace with your own API token
TOKEN = '7550763981:AAEoMs8CMRBZlQKv5XV3WTusZwzDVdqeAUk'

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Create user message tracking for spam detection
user_messages = {}

# Long start message
def start_message(first_name: str):
    return f"""
👋🏻 **Welcome {first_name}!**

I am Group Help, your personal assistant for managing Telegram groups with ease and safety! 

Here's how I can assist you:

- **Supergroup Management**: Add me to your Supergroup and make me an admin to start managing your group smoothly.
- **Spam Protection**: I can help detect spammy messages and warn users automatically.
- **File Handling**: I can process images, documents, videos, and other file types with ease.
- **User Interaction**: Feel free to interact with me using commands or by sending me messages and media.

❓ **Commands you can use**:
- **/start**: Welcome message and bot introduction.
- **/help**: Show all commands and how to use them.
- **/info**: Information about the bot and its capabilities.
- **/contact**: Get contact details or reach out for support.

📚 **Privacy Policy**: [Insert privacy policy link here]

💬 I'm always here to help! Just send me a message or command, and I'll respond instantly.
"""

# Command Handlers
async def start(update: Update, context: CallbackContext):
    first_name = update.message.from_user.first_name
    await update.message.reply_text(start_message(first_name))

async def help(update: Update, context: CallbackContext):
    help_message = """
Here are the available commands you can use:

- **/start**: Get a warm welcome and introduction to the bot.
- **/help**: Shows this list of commands.
- **/info**: Get more info about the bot and its features.
- **/contact**: Get the contact information for support or questions.

If you have any questions, feel free to ask me! 😊
"""
    await update.message.reply_text(help_message)

async def info(update: Update, context: CallbackContext):
    info_message = """
**About Group Help Bot**:

I am a Telegram bot designed to assist group admins with managing their groups. Some of the key features I provide are:

1. **Group Management**: Add me to your Supergroup and promote me as an admin to let me handle user interaction and content moderation.
2. **Spam Protection**: I can detect rapid, repeated messages (spam) and issue warnings to prevent spamming.
3. **File Handling**: Whether it's an image, document, video, or any other file, I can process it and let you know I’ve received it.

Feel free to experiment with me! You can send messages, files, and media, and I'll respond accordingly.
"""
    await update.message.reply_text(info_message)

async def contact(update: Update, context: CallbackContext):
    contact_message = """
**Contact Information**:

If you need any support or have any questions, you can reach out to the developer here:

📧 Email: [Insert email here]
📱 Telegram: [Insert Telegram username or contact info here]

I'll do my best to respond to your queries! 😊
"""
    await update.message.reply_text(contact_message)

# Detect spammy messages
async def detect_spam(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    message_text = update.message.text.lower() if update.message.text else ""
    now = datetime.now().timestamp()

    # Initialize user message count if not already set
    if user_id not in user_messages:
        user_messages[user_id] = {'count': 0, 'last_message': now}

    if now - user_messages[user_id]['last_message'] < 5:
        user_messages[user_id]['count'] += 1
    else:
        user_messages[user_id]['count'] = 1

    # Store last message timestamp
    user_messages[user_id]['last_message'] = now

    # Spam detection threshold
    if user_messages[user_id]['count'] > 5:
        await update.message.reply_text("⚠️ You're sending messages too quickly. Please slow down!")

async def handle_media(update: Update, context: CallbackContext):
    user_first_name = update.message.from_user.first_name
    await update.message.reply_text(start_message(user_first_name))

async def new_member(update: Update, context: CallbackContext):
    new_member = update.message.new_chat_members[0]
    await update.message.reply_text(f"👋🏻 Welcome to the group, {new_member.first_name}! Feel free to ask me anything.")

async def left_member(update: Update, context: CallbackContext):
    left_member = update.message.left_chat_member
    await update.message.reply_text(f"❌ {left_member.first_name} left the group.")

# Main function to start the bot
def main():
    # Create Application and pass it your bot's token
    application = Application.builder().token(TOKEN).build()

    # Command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("contact", contact))

    # Message handler to detect spam and media
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, detect_spam))
    application.add_handler(MessageHandler(filters.PHOTO | filters.DOCUMENT | filters.AUDIO | filters.VIDEO, handle_media))

    # New and left member handlers
    application.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member))
    application.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, left_member))

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
