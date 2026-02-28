# lifeos/src/integrations/telegram/bot.py
from __future__ import annotations

import structlog
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from src.agents.chief_of_staff import ChiefOfStaff
from src.core.context import ConversationContext

logger = structlog.get_logger()


class LifeOSTelegramBot:
    """Telegram interface for LifeOS."""

    def __init__(self, token: str, owner_chat_id: str, chief: ChiefOfStaff):
        self.token = token
        self.owner_chat_id = int(owner_chat_id)
        self.chief = chief

        self.app = ApplicationBuilder().token(token).build()
        self.app.add_handler(CommandHandler("start", self.cmd_start))
        self.app.add_handler(CommandHandler("status", self.cmd_status))
        self.app.add_handler(CommandHandler("note", self.cmd_note))
        self.app.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message)
        )

    def _is_owner(self, update: Update) -> bool:
        """Only respond to the configured owner."""
        return update.effective_chat is not None and update.effective_chat.id == self.owner_chat_id

    async def cmd_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self._is_owner(update):
            return
        await update.message.reply_text(  # type: ignore[union-attr]
            "🤖 LifeOS Chief of Staff ready.\n\n"
            "Just send me a message and I'll route it to the right advisor.\n\n"
            "Commands:\n"
            "/status — System status\n"
            "/note <text> — Quick note to inbox"
        )

    async def cmd_status(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self._is_owner(update):
            return
        stats = self.chief.get_stats()
        text = (
            "📊 *LifeOS Status*\n\n"
            f"Advisors: {stats['advisors_loaded']}\n"
            f"Loaded: {', '.join(stats['advisor_names'])}"
        )
        await update.message.reply_text(text, parse_mode="Markdown")  # type: ignore[union-attr]

    async def cmd_note(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self._is_owner(update):
            return
        text = " ".join(context.args) if context.args else ""
        if not text:
            await update.message.reply_text("Usage: /note <your note text>")  # type: ignore[union-attr]
            return

        from datetime import date
        from pathlib import Path

        today = date.today().isoformat()
        inbox = Path("knowledge/inbox")
        inbox.mkdir(parents=True, exist_ok=True)
        filepath = inbox / f"{today}-telegram.md"

        if filepath.exists():
            with open(filepath, "a") as f:
                f.write(f"\n\n- {text}")
        else:
            filepath.write_text(
                f"---\ntype: note\ndate: {today}\ntags: [telegram, inbox]\n"
                f"advisor:\nconfidentiality: normal\n---\n\n"
                f"# Telegram Notes — {today}\n\n- {text}\n"
            )
        await update.message.reply_text("📝 Saved to inbox")  # type: ignore[union-attr]

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        if not self._is_owner(update):
            return

        query = update.message.text  # type: ignore[union-attr]
        if not query:
            return

        conv_context = ConversationContext(
            session_id=f"telegram-{update.effective_chat.id}",  # type: ignore[union-attr]
            channel="telegram",
        )

        response = await self.chief.process(query, conv_context)
        rendered = response.render_for("telegram")

        # Telegram has a 4096 char limit
        if len(rendered) > 4000:
            rendered = rendered[:4000] + "\n\n_(truncated)_"

        await update.message.reply_text(rendered, parse_mode="Markdown")  # type: ignore[union-attr]

    async def send_notification(self, message: str) -> None:
        """Send a proactive notification to the owner."""
        bot = self.app.bot
        await bot.send_message(
            chat_id=self.owner_chat_id,
            text=message,
            parse_mode="Markdown",
        )

    def run(self) -> None:
        """Start the bot (blocking)."""
        logger.info("telegram.starting")
        self.app.run_polling()
