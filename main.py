import os
import logging
import sys
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import asyncio

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(name)

# Get token from environment variable
TOKEN = os.environ.get('BOT_TOKEN')

if not TOKEN:
    logger.error("No BOT_TOKEN found in environment variables!")
    logger.error("Please set the BOT_TOKEN environment variable and restart.")
    sys.exit(1)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message when the command /start is issued."""
    user = update.effective_user
    
    # Create inline keyboard
    keyboard = [
        [InlineKeyboardButton("📢 About", callback_data='about'),
         InlineKeyboardButton("🆘 Help", callback_data='help')],
        [InlineKeyboardButton("🔗 GitHub", url='https://github.com/yourusername/yourrepo')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        f"👋 Hello {user.first_name}!\n\n"
        f"🤖 I'm your test bot running on cloud hosting!\n"
        f"✅ If you see this message, the deployment is working!\n\n"
        f"Try sending me any message or use the buttons below:",
        reply_markup=reply_markup
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    help_text = (
        "🆘 Available Commands:\n"
        "/start - Welcome message\n"
        "/help - This help menu\n"
        "/status - Check bot status\n"
        "/echo <text> - Echo your message\n"
        "/info - Get your user info\n"
        "/test - Run a connectivity test\n\n"
        "💡 Features:\n"
        "• Button support\n"
        "• Message echoing\n"
        "• User info display\n"
        "• Environment variable test"
    )
    await update.message.reply_text(help_text, parse_mode='Markdown')

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Check bot status and environment."""
    try:
        import psutil
        memory = psutil.virtual_memory()
        memory_info = f"{memory.percent}% used"
    except ImportError:
        memory_info = "psutil not installed"
    
    status_text = (
        f"📊 Bot Status\n"
        f"✅ Bot is running\n"
        f"🆔 Bot Token: {TOKEN[:8]}... (hidden)\n"
        f"🌐 Webhook: Not configured\n"
        f"🔄 Polling: Active\n\n"
        f"Environment Info:\n"
        f"• Python Version: {sys.version.split()[0]}\n"
        f"• Platform: {os.environ.get('DYNO', 'Unknown')}\n"
        f"• Working Directory: {os.getcwd()}\n"
        f"• Memory: {memory_info}"
    )
    await update.message.reply_text(status_text, parse_mode='Markdown')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo the user message."""
    if context.args:
        text = ' '.join(context.args)
        await update.message.reply_text(f"🔊 Echo: {text}")
    else:
        await update.message.reply_text("Please provide text to echo. Example: /echo Hello World!")

async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Get user information."""
    user = update.effective_user
    info_text = (
        f"📋 Your Information\n"
        f"• User ID: {user.id}\n"
        f"• First Name: {user.first_name}\n"
        f"• Last Name: {user.last_name or 'Not set'}\n"
        f"• Username: @{user.username or 'Not set'}\n"
        f"• Language: {user.language_code or 'Unknown'}\n"
        f"• Bot: {'Yes' if user.is_bot else 'No'}"
    )
    await update.message.reply_text(info_text, parse_mode='Markdown')

async def test(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Run connectivity tests."""
    await update.message.reply_text("🧪 Running tests...")
    
    # Test 1: Environment variables
    token_test = "✅ PASS" if TOKEN else "❌ FAIL"
    
    # Test 2: Write permission
    try:
        with open('test.txt', 'w') as f:
            f.write('test')
        os.remove('test.txt')
        write_test = "✅ PASS"
    except:
        write_test = "❌ FAIL"
    
    # Test 3: Import test
    try:
        import psutil
        import_test = "✅ PASS"
        memory = psutil.virtual_memory()
        memory_info = f"{memory.percent}% used"
    except ImportError:
        import_test = "❌ FAIL (psutil not installed)"
        memory_info = "Unknown"
    
    test_results = (
        f"🔬 Test Results\n"
        f"• Token Check: {token_test}\n"
        f"• File Write: {write_test}\n"
        f"• Imports: {import_test}\n"
        f"• Memory: {memory_info}\n"
        f"• Python: Working\n"
        f"• Bot Framework: Working"
    )
    await update.message.reply_text(test_results, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle regular messages."""
    message_text = update.message.text
    user = update.effective_user
    
    response = f"📨 You said: '{message_text}'\n\n"
    response += f"I'm a test bot running on cloud hosting!\n"
    response += f"Try using /help to see what I can do."
    
    await update.message.reply_text(response)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle button presses."""
    query = update.callback_query
    await query.answer()
    
    if query.data == 'about':
        await query.edit_message_text(
            text="🤖 About This Bot\n\n"
                 "This is a test Telegram bot designed to verify "
                 "cloud hosting deployments. It demonstrates:\n"
                 "• Basic command handling\n"
                 "• Inline keyboards\n"
                 "• Environment variable usage\n"
                 "• Message processing\n\n"
                 "Created for testing purposes.",
            parse_mode='Markdown'
        )
    elif query.data == 'help':
        await query.edit_message_text(
            text="🆘 Quick Help\n\n"
                 "Commands: /start, /help, /status, /info, /test\n"
                 "Features: Buttons, echo, user info",
            parse_mode='Markdown'
        )

def main():
    """Start the bot."""
    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("echo", echo))
    application.add_handler(CommandHandler("info", info))
    application.add_handler(CommandHandler("test", test))
    
    # Register message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Register callback handler for buttons
    application.add_handler(CallbackQueryHandler(button_callback))

    # Start the bot
    logger.info(f"Starting bot with token: {TOKEN[:8]}...")
    logger.info("Bot is polling for updates...")
    
    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if name == 'main':
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)
