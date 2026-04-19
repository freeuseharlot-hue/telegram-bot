import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Ambil dari Railway Variables
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_LINK = "https://t.me/ORGaming1"
admin_id = os.getenv("ADMIN_CHAT_ID")
ADMIN_CHAT_ID = int(admin_id) if admin_id and admin_id.isdigit() else None

# Ganti kalau webhook n8n kamu berubah
WEBHOOK_URL = "https://kaynzed.app.n8n.cloud/webhook/lead"


async def notify_admin(context: ContextTypes.DEFAULT_TYPE, text: str):
    if ADMIN_CHAT_ID:
        try:
            await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=text)
        except Exception:
            pass


def send_to_n8n(data: dict):
    try:
        requests.post(WEBHOOK_URL, json=data, timeout=10)
    except Exception:
        pass


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    context.user_data["name"] = user.first_name
    context.user_data["username"] = user.username or "-"
    context.user_data["score"] = 0

    keyboard = [
        [InlineKeyboardButton("Sudah pernah", callback_data="yes")],
        [InlineKeyboardButton("Masih baru", callback_data="no")]
    ]

    await update.message.reply_text(
        "Halo pak, selamat datang di OR Gaming.\n\n"
        "Kami bantu partner membangun sistem white label yang siap pakai dan siap scale.\n\n"
        "Bapak sudah pernah jalan di bidang ini?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "no":
        context.user_data["score"] += 1

        keyboard = [
            [InlineKeyboardButton("Ingin cepat jalan", callback_data="fast")],
            [InlineKeyboardButton("Ingin tahu sistem", callback_data="system")]
        ]

        await query.message.reply_text(
            "Siap pak.\n\nBiasanya yang baru mulai butuh sistem siap pakai.\n\n"
            "Bapak ingin langsung jalan atau pelajari sistem dulu?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "yes":
        context.user_data["score"] += 2

        keyboard = [
            [InlineKeyboardButton("Kendala sistem", callback_data="system")],
            [InlineKeyboardButton("Ingin scale", callback_data="scale")]
        ]

        await query.message.reply_text(
            "Berarti bapak sudah punya dasar.\n\n"
            "Biasanya kendala di sistem atau ingin scale.\n\n"
            "Fokus bapak sekarang?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data in ["fast", "system", "scale"]:
        context.user_data["score"] += 1

        keyboard = [
            [InlineKeyboardButton("Lihat manfaat", callback_data="benefit")],
            [InlineKeyboardButton("Langsung admin", callback_data="admin")]
        ]

        await query.message.reply_text(
            "Di OR Gaming, bapak bisa punya sistem sendiri (white label).\n\n"
            "- Brand sendiri\n"
            "- Lebih profesional\n"
            "- Siap scale\n\n"
            "Saya tunjukkan manfaatnya?",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "benefit":
        keyboard = [
            [InlineKeyboardButton("Saya tertarik", callback_data="hot")],
            [InlineKeyboardButton("Masih lihat", callback_data="cold")]
        ]

        await query.message.reply_text(
            "Benefit utama:\n\n"
            "1. Lebih cepat jalan\n"
            "2. Tampilan profesional\n"
            "3. Sistem siap pakai\n\n"
            "Kalau cocok, kita lanjut.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "hot":
        context.user_data["score"] += 2

        keyboard = [
            [InlineKeyboardButton("Chat Admin", url=ADMIN_LINK)]
        ]

        await query.message.reply_text(
            "Siap pak.\n\nKlik tombol di bawah untuk lanjut ke admin.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        payload = {
            "nama": context.user_data.get("name"),
            "username": context.user_data.get("username"),
            "score": context.user_data.get("score"),
            "level": "panas"
        }
        send_to_n8n(payload)

        await notify_admin(
            context,
            f"🔥 LEAD PANAS\nNama: {context.user_data.get('name')}\nUsername: @{context.user_data.get('username')}\nScore: {context.user_data.get('score')}"
        )

    elif query.data == "cold":
        payload = {
            "nama": context.user_data.get("name"),
            "username": context.user_data.get("username"),
            "score": context.user_data.get("score"),
            "level": "dingin"
        }
        send_to_n8n(payload)

        await notify_admin(
            context,
            f"⚠️ LEAD DINGIN\nNama: {context.user_data.get('name')}\nUsername: @{context.user_data.get('username')}"
        )

        await query.message.reply_text(
            "Tidak masalah pak.\n\nKalau ingin lanjut nanti, kami siap bantu."
        )

    elif query.data == "admin":
        keyboard = [
            [InlineKeyboardButton("Chat Admin", url=ADMIN_LINK)]
        ]

        await query.message.reply_text(
            "Silakan lanjut ke admin.",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

        payload = {
            "nama": context.user_data.get("name"),
            "username": context.user_data.get("username"),
            "score": context.user_data.get("score"),
            "level": "admin"
        }
        send_to_n8n(payload)

        await notify_admin(
            context,
            f"📩 LEAD MASUK ADMIN\nNama: {context.user_data.get('name')}\nUsername: @{context.user_data.get('username')}"
        )


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))

    print("Bot Railway jalan...")
    app.run_polling()


if __name__ == "__main__":
    main()
