# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os
import re
import sys
import json
import time
import asyncio
import requests
import subprocess  # Ensure subprocess is imported

import core as helper
from utils import progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN
from aiohttp import ClientSession
from pyromod import listen
from subprocess import getstatusoutput

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from pyrogram.errors.exceptions.bad_request_400 import StickerEmojiInvalid
from pyrogram.types.messages_and_media import message
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN)


def reencode_video(input_file, output_file):
    """
    Re-encodes a video file using FFmpeg to fix issues like missing moov atom.

    Parameters:
        input_file (str): Path to the input video file.
        output_file (str): Path where the re-encoded video will be saved.
    """
    try:
        # FFmpeg command to re-encode the video
        command = [
            'ffmpeg', '-i', input_file, '-c:v', 'copy', '-c:a', 'copy', output_file
        ]

        # Execute the command
        subprocess.run(command, check=True)
        print(f"Successfully re-encoded the video to {output_file}")

    except subprocess.CalledProcessError as e:
        print(f"Error occurred during re-encoding: {e}")


@bot.on_message(filters.command(["start"]))
async def start(bot: Client, m: Message):
    await m.reply_text(f"<b>Hello {m.from_user.mention} 👋\n\n I Am A Bot For Download Links From Your **.TXT** File And Then Upload That File On Telegram So Basically If You Want To Use Me First Send Me /upload Command And Then Follow Few Steps..\n\nUse /stop to stop any ongoing task.</b>")


@bot.on_message(filters.command("stop"))
async def restart_handler(_, m):
    await m.reply_text("**Stopped**🚦", True)
    os.execl(sys.executable, sys.executable, *sys.argv)


@bot.on_message(filters.command(["upload"]))
async def upload(bot: Client, m: Message):
    editable = await m.reply_text('⏳ Please upload your .TXT file containing download links...')
    input: Message = await bot.listen(editable.chat.id)
    x = await input.download()
    await input.delete(True)

    path = f"./downloads/{m.chat.id}"

    try:
        with open(x, "r") as f:
            content = f.read()
        content = content.split("\n")
        links = []
        for i in content:
            links.append(i.split("://", 1))
        os.remove(x)
    except:
        await m.reply_text("**Invalid file input.**")
        os.remove(x)
        return

    await editable.edit(f"**Successfully received {len(links)} links!**")

    # Here we will process the links and download the videos
    for link in links:
        # Assuming the link is in the correct format, you will need to handle the downloading
        # For demonstration, let's say you have a function download_video that uses yt-dlp
        url = link[1]  # Extracting the URL from the link
        name = url.split('/')[-1]  # Getting a filename from the URL

        # Example path for the video
        video_file_path = f"./downloads/{name}.mp4"
        fixed_video_path = f"./downloads/fixed_{name}.mp4"

        # Attempt to download the video using your existing logic.
        try:
            # Here you would replace this with the actual download logic
            # For example: download_video(url, video_file_path)
            pass  # Placeholder for download logic

            # Check if the downloaded video file has issues
            if not os.path.exists(video_file_path):
                await m.reply_text(f"**Failed to download video from {url}**")
                continue

            # Re-encode the video if necessary
            reencode_video(video_file_path, fixed_video_path)

            # Now you can send the re-encoded video if needed
            await bot.send_document(chat_id=m.chat.id, document=fixed_video_path)

        except Exception as e:
            await m.reply_text(f"**Error processing {url}:** {str(e)}")

    await m.reply_text("**All files processed!**")

bot.run()
