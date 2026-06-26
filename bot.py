import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from moviepy.editor import VideoFileClip

BOT_TOKEN = "8126946610:AAEDssLPgK7OblaG2fpRs6BDmP3fTy7iKR0"
CHANNEL_ID = "-1004417937513"

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    video = update.message.video or update.message.document

    if not video:
        await update.message.reply_text("لطفاً یک ویدیو بفرستید.")
        return

    await update.message.reply_text("در حال پردازش ویدیو... ⏳")

    try:
        file = await context.bot.get_file(video.file_id)
        input_path = "input.mp4"
        output_path = "output.mp4"

        await file.download_to_drive(input_path)

        clip = VideoFileClip(input_path)
        size = min(clip.w, clip.h)
        clip = clip.crop(x_center=clip.w/2, y_center=clip.h/2, width=size, height=size)
        clip.write_videofile(output_path, codec="libx264")

        await context.bot.send_video_note(
            chat_id=CHANNEL_ID,
            video_note=open(output_path, "rb")
        )

        await update.message.reply_text("ویدیو با موفقیت در کانال منتشر شد! ✅")

        os.remove(input_path)
        os.remove(output_path)

    except Exception as e:
        await update.message.reply_text(f"خطا: {str(e)}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.VIDEO | filters.Document.ALL, handle_video))
    print("ربات روشن شد... 🚀")
    app.run_polling()

if __name__ == "__main__":
    main()
