import os
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler,
    filters, ContextTypes, ConversationHandler
)

BOT_TOKEN = os.environ["BOT_TOKEN"]
OWNER_ID = int(os.environ["OWNER_ID"])

ASK_NAME = 1

RUN_INFO = (
    "\n📍 Место сбора: Кофейня AMO, Мичуринский проспект, 56"
    "\n🕖 Сбор в 19:00, старт в 19:30"
    "\n📏 Маршрут: Парк 50-летия Октября, ~5 км"
    "\n💰 Бесплатно"
    "\n\nБудем рады тебя видеть! 🏃"
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Как тебя зовут?")
    return ASK_NAME


async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text
    user = update.message.from_user

    await update.message.reply_text(
        f"{name}, ты зарегистрирован(а) на пробежку в SKY RUNNERS CLUB ✅\n"
        + RUN_INFO
    )

    username = f"@{user.username}" if user.username else "—"
    await context.bot.send_message(
        chat_id=OWNER_ID,
        text=f"🆕 Новая регистрация!\nИмя: {name}\nTelegram: {username}\nID: {user.id}"
    )

    return ConversationHandler.END


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)]},
        fallbacks=[],
    )
    app.add_handler(conv)
    app.run_polling()


if __name__ == "__main__":
    main()
