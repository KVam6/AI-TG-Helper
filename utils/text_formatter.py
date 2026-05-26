import re
import telegramify_markdown


def _strip_md_in_tables(text: str) -> str:
    """
    Telegram показывает таблицы как code block,
    поэтому markdown внутри них надо убрать.
    """
    pattern = re.compile(r"((?:^\|.*\|\n?)+)", re.MULTILINE)

    def repl(match: re.Match) -> str:
        block = match.group(1)

        # bold / italic / inline code -> plain text
        block = re.sub(r"\*\*\*(.+?)\*\*\*", r"\1", block)
        block = re.sub(r"\*\*(.+?)\*\*", r"\1", block)
        block = re.sub(r"\*(.+?)\*", r"\1", block)
        block = re.sub(r"`(.+?)`", r"\1", block)

        return block

    return pattern.sub(repl, text)


async def format_for_telegram(markdown_text: str) -> str:
    text = _strip_md_in_tables(markdown_text)
    return telegramify_markdown.markdownify(text)