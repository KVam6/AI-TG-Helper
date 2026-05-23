from bot.bot import main
from utils.logger import logger

if __name__ == '__main__':
    try:
        logger.info("Starting the bot...")
        import asyncio
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot is stopped by user")
    except Exception as e:
        logger.error(f"Critical error: {e}")