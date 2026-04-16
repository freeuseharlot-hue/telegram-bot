from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

import os

TOKEN = os.getenv("8659050992:AAFVWRTCYoeswGgngfDikWbsw-f_jPyWN5w
")
ADMIN_LINK = "https://t.me/NMLVOID"
ADMIN_CHAT_ID = int(os.getenv("8346171986")) if os.getenv("8346171986") else None
async def notify_admin(context: ContextTypes.DEFAULT_TYPE, text: str):
    if ADMIN_CHAT_ID is not None:
        try:
            await context.bot.send_message(chat_id=ADMIN_CHAT_ID, text=text)
        except Exception:
            pass


def build_admin_summary(user_data: dict) -> str:
    name = user_data.get("name", "-")
    username = user_data.get("username", "-")
    experience = user_data.get("experience", "-")
    goal = user_data.get("goal", "-")
    interest = user_data.get("interest", "-")
    score = user_data.get("score", 0)

    if score >= 3:
        level = "PANAS"
    elif score >= 2:
        level = "HANGAT"
    else:
        level = "DINGIN"

    return (
        "Lead masuk\n"
        f"Nama: {name}\n"
        f"Username: @{username}\n"
        f"Experience: {experience}\n"
        f"Goal: {goal}\n"
        f"Interest: {interest}\n"
        f"Skor: {score}\n"
        f"Level: {level}"
    )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    context.user_data.clear()
    context.user_data["name"] = user.first_name or "-"
    context.user_data["username"] = user.username or "-"
    context.user_data["experience"] = "-"
    context.user_data["goal"] = "-"
    context.user_data["interest"] = "-"
    context.user_data["score"] = 0

    keyboard = [
        [InlineKeyboardButton("Sudah pernah", callback_data="exp_yes")],
        [InlineKeyboardButton("Masih baru", callback_data="exp_no")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        "Halo pak, selamat datang di OR Gaming.\n\n"
        "Kami bantu partner membangun sistem sendiri dengan model white label, "
        "lebih profesional, lebih siap digunakan, dan lebih mudah untuk scale.\n\n"
        "Sebelum lanjut, bapak sudah pernah jalan di bidang ini?"
    )

    await update.message.reply_text(text, reply_markup=reply_markup)
    await notify_admin(context, "Lead baru memulai bot\n" + build_admin_summary(context.user_data))


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # STEP 1 - experience
    if data == "exp_no":
        context.user_data["experience"] = "Masih baru"
        context.user_data["score"] += 1

        keyboard = [
            [InlineKeyboardButton("Ingin cepat jalan", callback_data="goal_fast")],
            [InlineKeyboardButton("Ingin tahu sistem", callback_data="goal_system")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text(
            "Siap pak.\n\n"
            "Biasanya yang baru mulai butuh sistem siap pakai agar tidak buang waktu trial error.\n\n"
            "Saat ini bapak lebih ingin langsung jalan atau memahami sistemnya dulu?",
            reply_markup=reply_markup
        )

    elif data == "exp_yes":
        context.user_data["experience"] = "Sudah pernah"
        context.user_data["score"] += 2

        keyboard = [
            [InlineKeyboardButton("Kendala di sistem", callback_data="goal_system")],
            [InlineKeyboardButton("Ingin scale", callback_data="goal_scale")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text(
            "Berarti bapak sudah punya dasar.\n\n"
            "Biasanya kendala ada di sistem atau masih tergantung platform.\n\n"
            "Saat ini bapak lebih fokus perbaiki sistem atau ingin scale?",
            reply_markup=reply_markup
        )

    # STEP 2 - goal
    elif data == "goal_fast":
        context.user_data["goal"] = "Ingin cepat jalan"
        context.user_data["score"] += 1

        keyboard = [
            [InlineKeyboardButton("Lihat manfaat utama", callback_data="benefit")],
            [InlineKeyboardButton("Masih lihat dulu", callback_data="soft_view")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text(
            "Bagus pak.\n\n"
            "Kalau targetnya cepat jalan, yang paling penting adalah pakai sistem yang lebih siap "
            "dan tidak memakan banyak trial error.\n\n"
            "Saya bisa tunjukkan manfaat utamanya dulu.",
            reply_markup=reply_markup
        )

    elif data == "goal_system":
        context.user_data["goal"] = "Fokus ke sistem"
        context.user_data["score"] += 1

        keyboard = [
            [InlineKeyboardButton("Lihat manfaat utama", callback_data="benefit")],
            [InlineKeyboardButton("Masih lihat dulu", callback_data="soft_view")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text(
            "Siap pak.\n\n"
            "Kalau fokusnya di sistem, berarti bapak sudah ada arah yang lebih jelas.\n\n"
            "Di OR Gaming, bapak bisa punya sistem sendiri dengan model white label, "
            "jadi lebih rapi dan lebih siap dipakai.\n\n"
            "Saya tunjukkan manfaat utamanya ya.",
            reply_markup=reply_markup
        )

    elif data == "goal_scale":
        context.user_data["goal"] = "Ingin scale"
        context.user_data["score"] += 2

        keyboard = [
            [InlineKeyboardButton("Lihat manfaat utama", callback_data="benefit")],
            [InlineKeyboardButton("Langsung ke admin", callback_data="admin")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text(
            "Sip pak.\n\n"
            "Kalau targetnya scale, maka kontrol sistem dan kesiapan struktur jadi jauh lebih penting.\n\n"
            "OR Gaming cocok untuk partner yang ingin lebih siap berkembang tanpa terlalu bergantung penuh pada sistem pihak lain.",
            reply_markup=reply_markup
        )

    # STEP 3 - benefit
    elif data == "benefit":
        keyboard = [
            [InlineKeyboardButton("Saya tertarik", callback_data="interested")],
            [InlineKeyboardButton("Masih lihat dulu", callback_data="soft_view")],
            [InlineKeyboardButton("Chat admin sekarang", callback_data="admin")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text(
            "Benefit utama:\n\n"
            "1. Lebih cepat jalan\n"
            "2. Tampilan lebih profesional\n"
            "3. Sistem lebih siap dipakai\n"
            "4. Lebih mudah diarahkan ke traffic dan closing\n"
            "5. Lebih nyaman untuk partner yang ingin punya kontrol lebih besar\n\n"
            "Kalau bapak merasa arahnya cocok, kita bisa lanjut ke tahap berikutnya.",
            reply_markup=reply_markup
        )

    # STEP 4 - soft / interested / admin
    elif data == "soft_view":
        context.user_data["interest"] = "Masih lihat dulu"

        keyboard = [
            [InlineKeyboardButton("Lanjut ke admin", callback_data="admin")],
            [InlineKeyboardButton("Saya tertarik", callback_data="interested")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text(
            "Tidak masalah pak.\n\n"
            "Biasanya yang masih lihat dulu memang ingin memastikan kecocokan sistemnya.\n\n"
            "Kalau bapak mau, saya bisa arahkan ke admin untuk penjelasan singkat dan langsung ke poin penting.",
            reply_markup=reply_markup
        )

        await notify_admin(
            context,
            "Lead masih observasi\n" + build_admin_summary(context.user_data)
        )

    elif data == "interested":
        context.user_data["interest"] = "Tertarik"
        context.user_data["score"] += 2

        keyboard = [
            [InlineKeyboardButton("Chat Admin Sekarang", url=ADMIN_LINK)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text(
            "Siap pak.\n\n"
            "Saat ini kita fokus ke partner yang memang siap jalan dan ingin lihat alur lebih jelas.\n\n"
            "Klik tombol di bawah untuk lanjut langsung ke admin.",
            reply_markup=reply_markup
        )

        await notify_admin(
            context,
            "Lead tertarik\n" + build_admin_summary(context.user_data)
        )

    elif data == "admin":
        keyboard = [
            [InlineKeyboardButton("Chat Admin Sekarang", url=ADMIN_LINK)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_text(
            "Baik pak.\n\n"
            "Klik tombol di bawah untuk lanjut langsung ke admin dan lihat penjelasan step berikutnya.",
            reply_markup=reply_markup
        )

        await notify_admin(
            context,
            "Lead minta admin\n" + build_admin_summary(context.user_data)
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Gunakan /start untuk mulai ulang alur bot.")


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot V4 jalan...")
    app.run_polling()


if __name__ == "__main__":
    main()
