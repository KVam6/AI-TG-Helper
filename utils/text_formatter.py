import telegramify_markdown

async def format_for_telegram(markdown_text: str) -> str:
    """Базовая конвертация Markdown -> Telegram MarkdownV2"""
    return telegramify_markdown.markdownify(markdown_text)