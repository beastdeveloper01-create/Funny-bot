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
    if not TOKEN:
        logger.error("No BOT_TOKEN found in environment variables!")
        return
    
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
    logger.info("Starting bot...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if name == 'main':
    main()
