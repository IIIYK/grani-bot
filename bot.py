# Telegram Bot для graniclub.ticketscloud.org
import os
from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.constants import ParseMode

load_dotenv()

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))

user_consents = {}

EVENT_DATA = {
    "title": "Сила внутри тебя",
    "subtitle": "Выбирай себя!",
    "description": """Сосредоточимся на балансе, освободимся от лишнего. Найдем источник силы.

Камерный интенсив. Мастера, практики, трансформация.

Все желающие поучаствуют в Новогодней фотосессии!""",
    "date": "20 декабря 2025, суббота",
    "time": "13:00 - 20:00",
    "location": "Москва, м. Алексеевская",
    "age": "18+",
    "ticket_price": "2300 ₽",
    "ticket_type": "VIP - свободное посещение двух залов мероприятия по программе",
    "site_url": "https://graniclub.ticketscloud.org",
    "telegram_contact": "https://t.me/Multyashaa"
}

CONSENT_TEXT = """🔒 <b>Согласие на обработку персональных данных</b>

Я даю согласие на обработку моих персональных данных в соответствии с Федеральным законом №152-ФЗ «О защите персональных данных» в целях:
• Предоставления информации о событиях
• Связи и уведомлений о новостях
• Улучшения сервиса

Мои данные не будут переданы третьим лицам без согласия.

<a href="https://graniclub.ticketscloud.org">Политика конфиденциальности</a>"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name or "Гость"
    
    await context.bot.send_message(ADMIN_ID, f"🆕 Новый пользователь: {user_name} (ID: {user_id})")
    
    if user_id in user_consents:
        await show_event(update, context)
        return
    
    keyboard = [[InlineKeyboardButton("✅ Согласен", callback_data="consent_accept"), InlineKeyboardButton("❌ Не согласен", callback_data="consent_reject")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(CONSENT_TEXT, reply_markup=reply_markup, parse_mode=ParseMode.HTML, disable_web_page_preview=True)

async def consent_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    
    if query.data == "consent_accept":
        user_consents[user_id] = True
        await query.edit_message_text("✅ Спасибо! Ваше согласие принято.\n\nЗагружаю информацию о событии...")
        await show_event(update, context)
    else:
        await query.edit_message_text("❌ Вы отказались от обработки данных.\n\nБез согласия мы не можем предоставить информацию о событиях.\n\nЕсли передумаете, напишите /start")

async def show_event(update: Update, context: ContextTypes.DEFAULT_TYPE):
    event_text = f"""<b>{EVENT_DATA['title']}</b>

<i>{EVENT_DATA['subtitle']}</i>

{EVENT_DATA['description']}

━━━━━━━━━━━━━━━━━━━━━━━
📅 <b>Дата:</b> {EVENT_DATA['date']}
🕐 <b>Время:</b> {EVENT_DATA['time']}
📍 <b>Место:</b> {EVENT_DATA['location']}
⭐ <b>Возраст:</b> {EVENT_DATA['age']}

💰 <b>VIP билет:</b> {EVENT_DATA['ticket_price']}
✨ {EVENT_DATA['ticket_type']}"""
    
    keyboard = [[InlineKeyboardButton("🎫 Купить билеты", url=EVENT_DATA['site_url'])], [InlineKeyboardButton("ℹ️ Подробнее", url=EVENT_DATA['telegram_contact'])]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if update.message:
        await update.message.reply_text(event_text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)
    else:
        await update.callback_query.edit_message_text(event_text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    help_text = """
<b>Доступные команды:</b>
/start - Начать (показать событие)
/help - Справка
/contact - Контакты организаторов
"""
    await update.message.reply_text(help_text, parse_mode=ParseMode.HTML)

async def contact_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact_text = """
<b>📞 Контакты</b>

Напишите организаторам в Telegram:
👤 <b>@Multyashaa</b>

Или посетите сайт:
🌐 https://graniclub.ticketscloud.org
"""
    keyboard = [[InlineKeyboardButton("💬 Написать в Telegram", url=EVENT_DATA['telegram_contact'])], [InlineKeyboardButton("🌐 Перейти на сайт", url=EVENT_DATA['site_url'])]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(contact_text, reply_markup=reply_markup, parse_mode=ParseMode.HTML)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("contact", contact_command))
    
    app.add_handler(CallbackQueryHandler(consent_callback, pattern="^consent_"))
    
    print("🤖 Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
