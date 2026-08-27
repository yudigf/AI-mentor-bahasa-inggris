import src.core.env as env

import os
import random

from zoneinfo import ZoneInfo  # WIB - Asia/Jakarta

from telegram import Update
from telegram.error import BadRequest
from telegram.ext import (
    ContextTypes,
    Application,
    CommandHandler,  # /start /report
    MessageHandler,  # text atau suara (voice note)
    Defaults,
    filters,
)

from telegram.constants import ParseMode  # MarkdownV2
from telegram.request import HTTPXRequest
from loguru import logger
from datetime import time, date, timedelta  # generate - per 1 minggu / 7 hari

from src.agents.lead import LeadAgent
from src.repository.chat_repository import ChatRepository
from src.core.format import to_telegram_markdown
from src.core.artifacts import Artifact

timezone = ZoneInfo("Asia/Jakarta")

chat_repository = ChatRepository()
lead_agent = LeadAgent()

# python-telegram-bot config
bot_config = Defaults(parse_mode=ParseMode.MARKDOWN_V2, tzinfo=timezone)


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.effective_message:
        return

    user = update.effective_user
    user_id = user.id
    username = user.username or user.first_name or f"User_{user_id}"
    chat_id = update.effective_chat.id

    chat_repository.save_user(user_id=user_id, username=username, chat_id=chat_id)

    safe_text = to_telegram_markdown(
        f"Halo!, Selamat datang {username} di Mentor Bahasa Inggris Virtual.\n"
        "Aku siap bantu kamu untuk belajar bahasa inggris! \n"
        "Kamu bisa langsung coba ketik pesan seperti ini: \n"
        "- *buatkan soal reading*\n"
        "- *periksa: I goes to school*\n"
        "- *kasih tips belajar*\n"
        "atau ngobrol bebas untuk melatih *speaking atau writing* kamu!\n"
        "- Ketik /start untuk mendaftarkan akun dan mulai belajar\n"
        "- Ketik /report untuk membuat laporan belajar\n",
    )

    await update.effective_message.reply_text(safe_text)


async def report_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.effective_message:
        return

    await update.effective_message.reply_text(
        to_telegram_markdown("laporan sedang kami buat, mohon tunggu...")
    )

    user = update.effective_user
    user_id = user.id
    username = user.username or user.first_name or f"User_{user_id}"

    end_date = date.today()
    start_date = end_date - timedelta(days=7)

    report_file_path = lead_agent.handle_report(
        user_id=user_id, username=username, start_date=start_date, end_date=end_date
    )

    with open(str(report_file_path), "rb") as report_pdf:
        await update.effective_message.reply_document(
            document=report_pdf,
            caption=to_telegram_markdown(
                f"Laporan belajar bahasa inggris dari tanggal {start_date.isoformat()} - {end_date.isoformat()}"
            ),
        )

    try:
        if os.path.exists(str(report_file_path)):
            os.remove(str(report_file_path))
    except Exception as e:
        logger.warning(f"gagal menghapus report {report_file_path}: {e}")



async def _send_artifact(update: Update, artifact: Artifact):
    if not update.effective_message:
        return

    artifact_path = artifact.get("path")
    kind = artifact.get("kind")
    caption = artifact.get("caption")

    safe_caption_text = to_telegram_markdown(caption) if caption else None

    if not artifact_path or not os.path.exists(str(artifact_path)):
        logger.warning(f"artifact tidak ditemukan: {artifact_path}")
        return

    with open(str(artifact_path), "rb") as artifact_file:
        if kind == "audio":
            await update.effective_message.reply_audio(
                audio=artifact_file, caption=safe_caption_text
            )
        elif kind == "video":
            await update.effective_message.reply_video(
                video=artifact_file, caption=safe_caption_text
            )
        else:
            await update.effective_message.reply_document(
                document=artifact_file, caption=safe_caption_text
            )

    try:
        os.remove(str(artifact_path))
        logger.info(f"success remove file {artifact_path}")
    except Exception as e:
        logger.warning(f"gagal menghapus file {artifact_path}: {e}")


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.effective_message or not update.effective_message.text:
        return

    reply_text = await update.effective_message.reply_text(
        to_telegram_markdown("mentor sedang menyiapkan jawaban...")
    )

    user_id = update.effective_user.id
    user_message = update.effective_message.text

    response = lead_agent.handle_send_message(
        user_id=user_id, message_text=user_message
    )

    safe_text = to_telegram_markdown(response["text"])

    await reply_text.edit_text(safe_text)

    if response.get("artifacts"):
        for item in response["artifacts"]:
            logger.debug(f"artifacts: {item}")
            await _send_artifact(update, item)


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.effective_user or not update.effective_message or not update.effective_message.voice:
        return

    reply_text = await update.effective_message.reply_text(
        to_telegram_markdown("suara sedang kami proses, mohon tunggu...")
    )

    user_id = update.effective_user.id

    # download file audio dari telegram
    env.TEMP.mkdir(parents=True, exist_ok=True)
    voice_file = await context.bot.get_file(update.effective_message.voice.file_id)
    voice_file_path = env.TEMP / f"{update.effective_message.voice.file_id}.ogg"
    await voice_file.download_to_drive(str(voice_file_path))

    evaluation_speaking_result = lead_agent.handle_send_voice(
        user_id=user_id, voice_file_path=voice_file_path
    )

    safe_text = to_telegram_markdown(evaluation_speaking_result)

    await reply_text.edit_text(safe_text)

    if os.path.exists(str(voice_file_path)):
        os.remove(str(voice_file_path))



async def task_reminder(context: ContextTypes.DEFAULT_TYPE):
    logger.info("[app.py][task_reminder]")
    users = chat_repository.get_users()
    skill_types = ["reading", "writing", "listening", "speaking"]

    for user in (users.data or []):
        try:
            user_id = user["user_id"]
            message = f"Pagi! ☀️ Yuk, luangkan 5 menit untuk latihan {random.choice(skill_types)} hari ini."
            chat_repository.save_message(
                user_id=user_id, role="model", message_text=message
            )
            safe_text = to_telegram_markdown(message)
            await context.bot.send_message(chat_id=user_id, text=safe_text)
        except Exception as e:
            logger.warning(f"Gagal mengirim reminder ke {user.get('user_id')}: {e}")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Error: {context.error}")

    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text(f"Terjadi error: {context.error}")


def run():
    request = HTTPXRequest(connect_timeout=20.0, read_timeout=30.0)
    app = (
        Application.builder()
        .token(env.TELEGRAM_BOT_TOKEN)
        .request(request)
        .defaults(bot_config)
        .build()
    )

    # register route handler
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("report", report_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))

    # scheduler
    target_time = time(hour=10, minute=3, second=0, tzinfo=timezone)
    app.job_queue.run_daily(
        callback=task_reminder, time=target_time, name="task_reminder"
    )
    # app.job_queue.run_repeating(callback=task_reminder, interval=5, first=0)

    app.add_error_handler(error_handler)

    print("Mentor Bahasa Inggris Virtual berhasil di jalankan...")
    app.run_polling(allowed_updates=Update.ALL_TYPES, timeout=30)