from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, CallbackContext
import re
import json
import os
from datetime import datetime, timedelta

# Dein Bot-Token (füge dein Token hier ein)
BOT_TOKEN = "7744671210:AAHxB1PpgbNydK3GviWuvj9GXH9y1niWxk4"

# Admin-ID
ADMIN_ID = 6617702798

# Gutscheincode-Backup-Datei
BACKUP_FILE = "gutscheincodes.json"

# Countdown-Timer für Angebote (in Stunden)
OFFER_EXPIRY_HOURS = 48

# Gutscheincodes laden oder erstellen
def load_gutscheincodes():
    if os.path.exists(BACKUP_FILE):
        with open(BACKUP_FILE, "r") as file:
            return json.load(file)
    return {}

def save_gutscheincodes(codes):
    with open(BACKUP_FILE, "w") as file:
        json.dump(codes, file)

GUTSCHEINCODES = load_gutscheincodes()

# Hauptmenü anzeigen
def main_menu():
    keyboard = [
        [InlineKeyboardButton("Pakete anzeigen 🛍️", callback_data="show_packages")],
        [InlineKeyboardButton("Zahlungsoptionen 💳", callback_data="payment_options")],
        [InlineKeyboardButton("FAQ ❓", callback_data="faq")],
    ]
    return InlineKeyboardMarkup(keyboard)

# Begrüßung (/start)
async def start(update: Update, context: CallbackContext):
    user_name = update.message.from_user.first_name
    welcome_text = (
        f"Hey {user_name}! 🥰 Schön, dass du hier bist! Ich habe für dich exklusive Inhalte vorbereitet, die du sonst nirgends finden wirst. 😘\n"
        "Schreib einfach auf die Buttons unten, um mehr zu erfahren. Lass uns gemeinsam etwas Besonderes erleben! 💖"
    )
    await update.message.reply_text(welcome_text, reply_markup=main_menu())

# Pakete anzeigen
async def show_packages(update: Update, context: CallbackContext):
    query = update.callback_query
    if query:
        await query.answer()

    expiry_time = datetime.now() + timedelta(hours=OFFER_EXPIRY_HOURS)
    countdown = expiry_time.strftime("%d.%m.%Y %H:%M:%S")

    packages = (
        f"Hier sind meine exklusiven Pakete (Angebot gültig bis {countdown}):\n\n"
        "1️⃣ Sweet Starter (20 €): Ein kleiner Einstieg.\n"
        "2️⃣ Classy Collection (30 €): Für alle, die mehr wollen.\n"
        "3️⃣ Bold Bundle (50 €): Premium-Inhalte in großer Menge.\n"
        "4️⃣ Luxury Lounge (75 €): VIP-Zugang zu exklusiven Inhalten.\n"
        "5️⃣ Royal Fantasy (100 €): Das ultimative Erlebnis."
    )

    keyboard = [
        [InlineKeyboardButton("Sweet Starter 🧁", callback_data="package_1")],
        [InlineKeyboardButton("Classy Collection ✨", callback_data="package_2")],
        [InlineKeyboardButton("Bold Bundle 💪", callback_data="package_3")],
        [InlineKeyboardButton("Luxury Lounge 🌟", callback_data="package_4")],
        [InlineKeyboardButton("Royal Fantasy 👑", callback_data="package_5")],
        [InlineKeyboardButton("Zurück zum Hauptmenü 🔙", callback_data="back_to_main_menu")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    if query:
        await query.edit_message_text(packages, reply_markup=reply_markup)
    else:
        await update.message.reply_text(packages, reply_markup=reply_markup)

# Zahlungsoptionen
async def payment_options(update: Update, context: CallbackContext):
    query = update.callback_query
    if query:
        await query.answer()

    payment_text = (
        "Die Bezahlung ist ganz einfach! 😘 Du hast zwei Möglichkeiten:\n\n"
        "1️⃣ Zahl über PayPal: [PayPal.me/larii7](https://www.paypal.me/larii7)\n"
        "2️⃣ Schick mir einen Amazon-Gutschein direkt hier im Chat. Ich überprüfe ihn sofort und schalte dir dein Paket frei.\n\n"
        "Nachdem du mit PayPal bezahlt hast, sende mir bitte einen Screenshot der Zahlung, damit ich die Zahlung bestätigen kann. 💖"
    )

    keyboard = [
        [InlineKeyboardButton("PayPal bezahlen 💳", callback_data="paypal_payment")],
        [InlineKeyboardButton("Amazon-Gutschein senden 🎁", callback_data="amazon_gutschein_payment")],
        [InlineKeyboardButton("Zurück zum Hauptmenü 🔙", callback_data="back_to_main_menu")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    if query:
        await query.edit_message_text(payment_text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.message.reply_text(payment_text, reply_markup=reply_markup, parse_mode="Markdown")

# FAQ anzeigen
async def faq(update: Update, context: CallbackContext):
    query = update.callback_query
    if query:
        await query.answer()

    faq_text = (
        "Häufige Fragen:\n\n"
        "❓ *Wie lange dauert die Freischaltung?*\n"
        "Antwort: In der Regel innerhalb kurzer Zeit – meistens sofort! 😘\n\n"
        "❓ *Kann ich ein Paket upgraden?*\n"
        "Antwort: Natürlich! Schreib mir einfach, welches Paket du möchtest.\n\n"
        "❓ *Welche Zahlungsmethoden gibt es?*\n"
        "Antwort: Du kannst per PayPal oder mit einem Amazon-Gutschein zahlen."
    )

    keyboard = [
        [InlineKeyboardButton("Zurück zum Hauptmenü 🔙", callback_data="back_to_main_menu")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    if query:
        await query.edit_message_text(faq_text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.message.reply_text(faq_text, reply_markup=reply_markup, parse_mode="Markdown")

# Paket-Auswahl
async def package_selected(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    package_map = {
        "package_1": "Sweet Starter (20 €)",
        "package_2": "Classy Collection (30 €)",
        "package_3": "Bold Bundle (50 €)",
        "package_4": "Luxury Lounge (75 €)",
        "package_5": "Royal Fantasy (100 €)",
    }

    package_name = package_map.get(query.data, "Unbekanntes Paket")
    await query.edit_message_text(
        f"Du hast das Paket '{package_name}' ausgewählt. Bitte schließe die Zahlung ab, um Zugang zu erhalten. 💖",
        reply_markup=InlineKeyboardMarkup([ 
            [InlineKeyboardButton("Zur Zahlung gehen 💳", callback_data="payment_options")],
            [InlineKeyboardButton("Zurück zu den Paketen 🔙", callback_data="show_packages")],
            [InlineKeyboardButton("Zurück zum Hauptmenü 🔙", callback_data="back_to_main_menu")],
        ])
    )

# Zurück zum Hauptmenü
async def back_to_main_menu(update: Update, context: CallbackContext):
    query = update.callback_query
    if query:
        await query.answer()
        await query.edit_message_text("Zurück zum Hauptmenü!", reply_markup=main_menu())

# PayPal-Zahlung bestätigen (Screenshot)
async def handle_paypal_payment(update: Update, context: CallbackContext):
    if update.message:
        await update.message.reply_text(
            "Du hast PayPal als Zahlungsmethode gewählt. Bitte sende mir einen Screenshot der Zahlung, damit ich sie bestätigen kann. 💖",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Zurück zu den Zahlungsoptionen 💳", callback_data="payment_options")],
                [InlineKeyboardButton("Zurück zum Hauptmenü 🔙", callback_data="back_to_main_menu")]
            ])
        )
    else:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            "Du hast PayPal als Zahlungsmethode gewählt. Bitte sende mir einen Screenshot der Zahlung, damit ich sie bestätigen kann. 💖",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Zurück zu den Zahlungsoptionen 💳", callback_data="payment_options")],
                [InlineKeyboardButton("Zurück zum Hauptmenü 🔙", callback_data="back_to_main_menu")]
            ])
        )
    
    user_name = update.message.from_user.first_name if update.message else update.callback_query.from_user.first_name
    chat_id = update.message.chat_id if update.message else update.callback_query.message.chat.id
    forward_text = f"💌 {user_name} (ID: {chat_id}) hat PayPal als Zahlungsmethode gewählt und wartet auf den Screenshot."
    await context.bot.send_message(chat_id=ADMIN_ID, text=forward_text)

# Amazon-Gutschein bestätigen
async def handle_amazon_gutschein_payment(update: Update, context: CallbackContext):
    if update.message:
        await update.message.reply_text(
            "Du hast den Amazon-Gutschein als Zahlungsmethode gewählt. Bitte sende mir den Code des Gutscheins, damit ich ihn überprüfen kann. 💖",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Zurück zu den Zahlungsoptionen 💳", callback_data="payment_options")],
                [InlineKeyboardButton("Zurück zum Hauptmenü 🔙", callback_data="back_to_main_menu")]
            ])
        )
    else:
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(
            "Du hast den Amazon-Gutschein als Zahlungsmethode gewählt. Bitte sende mir den Code des Gutscheins, damit ich ihn überprüfen kann. 💖",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("Zurück zu den Zahlungsoptionen 💳", callback_data="payment_options")],
                [InlineKeyboardButton("Zurück zum Hauptmenü 🔙", callback_data="back_to_main_menu")]
            ])
        )
    
    user_name = update.message.from_user.first_name if update.message else update.callback_query.from_user.first_name
    chat_id = update.message.chat_id if update.message else update.callback_query.message.chat.id
    forward_text = f"💌 {user_name} (ID: {chat_id}) hat einen Amazon-Gutschein als Zahlungsmethode gewählt und wartet auf den Code."
    await context.bot.send_message(chat_id=ADMIN_ID, text=forward_text)

# Gutscheincode prüfen und weiterleiten
async def handle_gutschein_code(update: Update, context: CallbackContext):
    user_message = update.message.text
    user_name = update.message.from_user.first_name
    chat_id = update.message.chat_id

    if re.match(r"^[A-Za-z0-9-]{12,}$", user_message):
        GUTSCHEINCODES[user_message] = {
            "user": user_name,
            "chat_id": chat_id,
            "timestamp": datetime.now().isoformat(),
        }
        save_gutscheincodes(GUTSCHEINCODES)

        forward_text = (
            f"💌 Neue Nachricht von {user_name} (ID: {chat_id}):\n\n"
            f"Gutscheincode: {user_message}"
        )
        await context.bot.send_message(chat_id=ADMIN_ID, text=forward_text)

        await update.message.reply_text(
            "Danke für deinen Gutscheincode! Ich überprüfe ihn und melde mich bei dir. 💖"
        )
    else:
        await update.message.reply_text(
            "Dein Gutscheincode scheint ungültig zu sein. Bitte überprüfe ihn und versuche es erneut. 😕"
        )

# Bildnachricht empfangen (für PayPal Screenshot)
async def handle_screenshot(update: Update, context: CallbackContext):
    if update.message.photo:
        # Das Foto wird an den Admin weitergeleitet
        photo_file_id = update.message.photo[-1].file_id  # Das größte Foto auswählen

        # Senden des Fotos an den Admin
        await context.bot.send_photo(chat_id=ADMIN_ID, photo=photo_file_id)

        # Bestätigung an den Benutzer
        await update.message.reply_text("Danke für den Screenshot! Ich überprüfe die Zahlung und melde mich bei dir. 💖")

        # Weiterleitung der Nachricht an den Admin
        user_name = update.message.from_user.first_name
        chat_id = update.message.chat_id
        forward_text = (
            f"💌 Screenshot von {user_name} (ID: {chat_id}) für die PayPal-Zahlung erhalten."
        )
        await context.bot.send_message(chat_id=ADMIN_ID, text=forward_text)
    else:
        await update.message.reply_text("Bitte sende mir einen Screenshot der PayPal-Zahlung. 💖")

# Hauptfunktion, um den Bot zu starten
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(show_packages, pattern="show_packages"))
    application.add_handler(CallbackQueryHandler(payment_options, pattern="payment_options"))
    application.add_handler(CallbackQueryHandler(faq, pattern="faq"))
    application.add_handler(CallbackQueryHandler(package_selected, pattern="package_"))
    application.add_handler(CallbackQueryHandler(back_to_main_menu, pattern="back_to_main_menu"))
    application.add_handler(CallbackQueryHandler(handle_paypal_payment, pattern="paypal_payment"))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_gutschein_code))  # Korrektur hier
    application.add_handler(CallbackQueryHandler(handle_amazon_gutschein_payment, pattern="amazon_gutschein_payment"))
    application.add_handler(MessageHandler(filters.PHOTO, handle_screenshot))  # Korrektur hier

    application.run_polling()

if __name__ == "__main__":
    main() 