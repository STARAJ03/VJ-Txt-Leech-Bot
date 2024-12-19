# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel For Amazing Bot https://youtube.com/@Tech_VJ
# Ask Doubt on telegram @KingVJ01

import os
import time
import datetime
import aiohttp
import aiofiles
import asyncio
import logging
import requests
import tgcrypto
import subprocess
import concurrent.futures

from utils import progress_bar
from pyrogram import Client, filters
from pyrogram.types import Message

def duration(filename):
    try:
        # Run ffprobe command to get the duration of the video
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', filename],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        # Check for errors in stderr
        if result.stderr:
            raise ValueError(result.stderr.decode().strip())
        
        # Convert the output to float
        return float(result.stdout.strip())
    
    except ValueError as e:
        print(f"Error: {e}")
        return None  # or handle it in a way that fits your application's needs

def exec(cmd):
    # Executes a shell command and returns its output.
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.stdout.decode().strip(), result.stderr.decode().strip()

def pull_run(work, cmds):
    # Executes a list of shell commands concurrently using a thread pool.
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = {executor.submit(exec, cmd): cmd for cmd in cmds}
        for future in concurrent.futures.as_completed(futures):
            cmd = futures[future]
            try:
                output, error = future.result()
                if output:
                    print(f"Output of {cmd}: {output}")
                if error:
                    print(f"Error in {cmd}: {error}")
            except Exception as e:
                print(f"Command {cmd} generated an exception: {e}")

async def aio(url, name):
    # Asynchronously download a file from a URL and save it as a PDF.
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                async with aiofiles.open(name, 'wb') as f:
                    await f.write(await response.read())

def download(url, name):
    # Synchronously download a file in chunks from a URL.
    response = requests.get(url, stream=True)
    with open(name, 'wb') as f:
        for chunk in response.iter_content(chunk_size=10240):
            f.write(chunk)

def parse_vid_info(info):
    # Parses video information and extracts relevant details excluding resolutions and audio formats.
    # Implementation goes here...
    pass

def vid_info(info):
    # Similar to parse_vid_info, but returns a dictionary mapping format identifiers to other details.
    # Implementation goes here...
    pass

def run(cmd):
    # Asynchronously runs a shell command and captures its output.
    # Implementation goes here...
    pass

def old_download(url, file_name, chunk_size=10240):
    # Synchronously downloads a file in chunks from a URL.
    # Implementation goes here...
    pass

def human_readable_size(size, decimal_places=2):
    # Converts a size in bytes to a human-readable format (KB, MB, GB, etc.).
    # Implementation goes here...
    pass

def time_name():
    # Generates a timestamped filename based on the current date and time.
    return datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

def download_video(url, cmd, name):
    # Downloads a video using a specific command with aria2c, retries if the download fails.
    # Implementation goes here...
    pass

async def send_doc(bot, m, cc, ka, cc1, prog, count, name):
    # Asynchronously sends a document to a Telegram chat.
    # Implementation goes here...
    pass

async def send_vid(bot, m, cc, filename, thumb, name, prog):
# Additional code and implementation details would go here...
    
    subprocess.run(f'ffmpeg -i "{filename}" -ss 00:00:12 -vframes 1 "{filename}.jpg"', shell=True)
    await prog.delete (True)
    reply = await m.reply_text(f"**Uploading ...** - `{name}`")
    try:
        if thumb == "no":
            thumbnail = f"{filename}.jpg"
        else:
            thumbnail = thumb
    except Exception as e:
        await m.reply_text(str(e))

    dur = int(duration(filename))

    start_time = time.time()

    try:
        await m.reply_video(filename,caption=cc, supports_streaming=True,height=720,width=1280,thumb=thumbnail,duration=dur, progress=progress_bar,progress_args=(reply,start_time))
    except Exception:
        await m.reply_document(filename,caption=cc, progress=progress_bar,progress_args=(reply,start_time))

    
    os.remove(filename)

    os.remove(f"{filename}.jpg")
    await reply.delete (True)
    
