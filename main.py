import os
import tempfile
import pypandoc
from PIL import Image
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

# === Replace with your own Telegram Bot Token ===
BOT_TOKEN = "8472757590:AAGHTdJSOPeSrY9byxih3Vw8Nv2LngpI40s"

# === Start Command ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome to File Converter Bot!\n\n"
        "Send me any image or document, and I’ll convert it for you.\n\n"
        "Example:\n"
        "- Send a JPG and type `to png`\n"
        "- Send a DOCX and type `to pdf`"
    )

# === Handle Files ===
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    caption = message.caption or ""

    if not ("to " in caption.lower()):
        await message.reply_text("Please specify conversion format (e.g., `to png`, `to pdf`).")
        return

    target_format = caption.lower().split("to ")[-1].strip()

    file = await message.document.get_file() if message.document else await message.photo[-1].get_file()
    input_path = tempfile.mktemp()
    output_path = tempfile.mktemp(suffix=f".{target_format}")

    await file.download_to_drive(input_path)

    try:
        # ==== Image Conversion ====
        if any(input_path.lower().endswith(ext) for ext in [".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tiff"]):
            img = Image.open(input_path)
            img.save(output_path)
            await message.reply_document(document=open(output_path, "rb"), filename=f"converted.{target_format}")

        # ==== Document Conversion ====
        elif any(input_path.lower().endswith(ext) for ext in [".docx", ".txt", ".odt", ".md", ".pdf"]):
            pypandoc.convert_file(input_path, target_format, outputfile=output_path, extra_args=['--standalone'])
            await message.reply_document(document=open(output_path, "rb"), filename=f"converted.{target_format}")

        else:
            await message.reply_text("❌ Unsupported file type for conversion.")
    except Exception as e:
        await message.reply_text(f"⚠️ Conversion failed: {e}")
    finally:
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)

# === Run Bot ===
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Document.ALL | filters.PHOTO, handle_file))

    print("🤖 Bot running...")
    app.run_polling()

if __name__ == "__main__":
    main()
    
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! I'm alive!")

app = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()
app.add_handler(CommandHandler("start", start))
app.run_polling()   # 👈 keeps the container alive