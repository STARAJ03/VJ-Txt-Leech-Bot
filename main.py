import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from vars import API_ID, API_HASH, BOT_TOKEN

bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@bot.on_message(filters.command(["start"]))
async def start(bot: Client, m: Message):
    await m.reply_text(
        f"<b>Hello {m.from_user.mention} 👋\n\nI can download videos in multiple formats! Send me a .TXT file containing your links using /upload command.</b>"
    )

@bot.on_message(filters.command("upload"))
async def upload_command(bot: Client, m: Message):
    await m.reply_text('Please send your .TXT file containing video links ⚡️')

@bot.on_message(filters.document & filters.user(bot.me.id))
async def handle_document(bot: Client, m: Message):
    if m.document and m.document.file_name.endswith('.txt'):
        editable = await m.reply_text('Processing your file...')
        
        # Download the file
        x = await m.download()
        await m.delete()  # Delete the original message

        try:
            with open(x, "r") as f:
                content = f.read().strip().split("\n")
            links = [line.strip() for line in content if line]
            os.remove(x)
        except Exception as e:
            await editable.edit(f"**Error reading file:** {str(e)}")
            return

        await editable.edit(f"**Total links found: {len(links)}**\n\n**Send the starting index (1) for downloads**")
        input0: Message = await bot.listen(editable.chat.id)
        count = int(input0.text)
        await input0.delete(True)

        await editable.edit("**Please enter desired video format (mp4, mkv, etc.)**")
        input1: Message = await bot.listen(editable.chat.id)
        video_format = input1.text.strip()
        await input1.delete(True)

        await editable.edit("**Enter a caption for the uploaded file**")
        input2: Message = await bot.listen(editable.chat.id)
        caption = input2.text.strip()
        await input2.delete(True)

        try:
            for i in range(count - 1, len(links)):
                url = links[i]
                name = f"video_{str(i + 1).zfill(3)}.{video_format}"

                cmd = f'yt-dlp -o "{name}" "{url}" --format "{video_format}"'
                await editable.edit(f"**Downloading:** `{name}` from `{url}`")

                try:
                    os.system(cmd)
                    await bot.send_document(chat_id=m.chat.id, document=name, caption=caption)
                    os.remove(name)  # Clean up the file after sending
                except Exception as e:
                    await m.reply_text(f"**Error downloading:** `{url}`\n{str(e)}")

        except Exception as e:
            await m.reply_text(f"**An error occurred:** {str(e)}")

        await m.reply_text("**All downloads completed!**")
    else:
        await m.reply_text("**Please send a valid .TXT file!**")

bot.run()
