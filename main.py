# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os
import re
import sys
import time
import subprocess
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait

# Replace with your actual API ID and HASH
API_ID = "your_api_id"
API_HASH = "your_api_hash"
BOT_TOKEN = "your_bot_token"

bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN)

# Ensure the downloads directory exists
if not os.path.exists("./downloads"):
    os.makedirs("./downloads")

def reencode_video(input_file, output_file):
    """
    Re-encodes a video file using FFmpeg to fix issues like missing moov atom.
    """
    try:
        command = [
            'ffmpeg', '-i', input_file, '-c:v', 'copy', '-c:a', 'copy', output_file
        ]
        subprocess.run(command, check=True)
        print(f"Successfully re-encoded the video to {output_file}")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during re-encoding: {e}")

@bot.on_message(filters.command(["start"]))
async def start(bot: Client, m: Message):
    await m.reply_text(f"<b>Hello {m.from_user.mention} 👋\n\nI Am A Bot For Download Links From Your **.TXT** File. Use /upload to start.</b>")

@bot.on_message(filters.command("stop"))
async def stop(bot: Client, m: Message):
    await m.reply_text("**Stopped**🚦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.on_message(filters.command(["upload"]))
async def upload(bot: Client, m: Message):
    editable = await m.reply_text('⏳ Please upload your .TXT file containing download links...')
    input: Message = await bot.listen(editable.chat.id)
    
    # Download the uploaded file
    file_path = await input.download()
    await input.delete(True)

    try:
        with open(file_path, "r") as f:
            content = f.read().strip().split("\n")
        
        os.remove(file_path)  # Remove the original uploaded file
        links = [line for line in content if line]

        await editable.edit(f"**Successfully received {len(links)} links!**")

        for link in links:
            name = link.split('/')[-1].split('.')[0]  # Get a base name from the URL
            video_file_path = f"./downloads/{name}.mp4"
            fixed_video_path = f"./downloads/fixed_{name}.mp4"

            try:
                # Here you should replace this with your actual download logic
                # Example download logic (just a placeholder):
                print(f"Downloading video from {link} to {video_file_path}")
                # Assume you have a function called download_video(link, video_file_path)
                # download_video(link, video_file_path)
                
                # For demonstration, we're just creating an empty file
                with open(video_file_path, 'wb') as f:
                    f.write(b'')  # Placeholder for actual video data

                # Check if the video file exists after the download
                if not os.path.exists(video_file_path):
                    await m.reply_text(f"**Failed to download video from {link}**")
                    continue

                # Attempt to re-encode the video
                reencode_video(video_file_path, fixed_video_path)

                # Send the re-encoded video back to the user
                await bot.send_document(chat_id=m.chat.id, document=fixed_video_path)

            except Exception as e:
                await m.reply_text(f"**Error processing {link}: {str(e)}**")

        await m.reply_text("**All files processed!**")

    except Exception as e:
        await m.reply_text(f"**Error reading the file: {str(e)}**")

bot.run()
