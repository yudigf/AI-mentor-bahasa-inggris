import telegramify_markdown


def to_telegram_markdown(text: str | None) -> str: 
    """Ubah markdown standard (output dari LLM) mejadi Telegram MarkdownV2 yang valid."""
    if not text:
        return ""
    return telegramify_markdown.markdownify(text)

