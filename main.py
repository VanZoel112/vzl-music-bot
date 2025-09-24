#!/usr/bin/env python3
"""
Vzoel Music Bot - Realistic Telegram Music Bot Implementation
Founder: Vzoel Fox's Lutpan
ID Founder: @VZLfxs
Features: YouTube, Spotify, SoundCloud streaming dengan PyTgCalls
NO PREMIUM EMOJIS - Using standard emojis only (realistic approach)
"""

import asyncio
import os
import re
import logging
import importlib
from typing import Dict, List, Optional
import json
import sqlite3
from datetime import datetime

# Telegram libraries
from pyrogram import Client, filters, types
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import ChatAdminRequired, UserNotParticipant

# PyTgCalls for voice streaming
from pytgcalls import PyTgCalls

# PyTgCalls keeps moving AudioPiped between releases. Try the newest import
# path first (v4.x), then fall back to the legacy locations so the bot keeps
# working regardless of the installed version.
# Resolve AudioPiped import location across PyTgCalls releases.
_audio_piped = None
for _module_path, _attr in (
    ("pytgcalls.types.stream", "AudioPiped"),  # PyTgCalls >= 4.0
    ("pytgcalls.types", "AudioPiped"),          # PyTgCalls 3.x
    ("pytgcalls.types.input_stream", "AudioPiped"),  # PyTgCalls <= 2.x
):
    try:
        _module = importlib.import_module(_module_path)
        _audio_piped = getattr(_module, _attr)
        break
    except (ImportError, AttributeError):
        continue

if _audio_piped is None:
    raise ImportError(
        "Unable to import AudioPiped from pytgcalls. Please ensure a compatible "
        "version of PyTgCalls is installed."
    )

AudioPiped = _audio_piped
    
    except ImportError:
    try:  # PyTgCalls 3.x
        from pytgcalls.types import AudioPiped
    except ImportError:  # PyTgCalls <= 2.x
from pytgcalls.exceptions import GroupCallNotFound

# Audio/Video processing
import yt_dlp
from mutagen import File as MutagenFile

# Configuration
CONFIG = {
    "BOT_TOKEN": "8314911312:AAEZTrlru95_QNycAt4TlYH_k-7q2f_PQ9c",
    "API_ID": 26576546,
    "API_HASH": "d1948cd4d196a991366f762189c4ff3d",
    "SUDO_USERS": [8024282347, 7768763441],  # Admin user IDs
    "LOG_GROUP_ID": -1003098574590,  # Optional: Log group
    "DATABASE_PATH": "vzl_music.db"
}

# Initialize bot
app = Client(
    "vzl_music_bot",
    api_id=CONFIG["API_ID"],
    api_hash=CONFIG["API_HASH"],
    bot_token=CONFIG["BOT_TOKEN"]
)

# Initialize PyTgCalls
pytgcalls = PyTgCalls(app)

# Global variables
active_chats: Dict[int, dict] = {}
queue_manager: Dict[int, list] = {}

# Database setup
def init_database():
    """Initialize SQLite database for music bot data"""
    conn = sqlite3.connect(CONFIG["DATABASE_PATH"])
    cursor = conn.cursor()

    # Create tables
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS music_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER,
            user_id INTEGER,
            title TEXT,
            url TEXT,
            platform TEXT,
            played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_stats (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            total_requests INTEGER DEFAULT 0,
            last_request TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

# YouTube-DL configuration
YDL_OPTIONS = {
    'format': 'bestaudio[ext=webm]/bestaudio[ext=m4a]/bestaudio',
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'extractflat': False,
    'outtmpl': 'downloads/%(title)s.%(ext)s',
    'quiet': True
}

class MusicBot:
    """VZL Music Bot - Core functionality"""

    def __init__(self):
        self.current_song: Dict[int, dict] = {}
        self.is_paused: Dict[int, bool] = {}

    async def extract_info(self, query: str) -> Optional[dict]:
        """Extract audio info from various sources"""
        try:
            with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                # Check if it's a URL or search query
                if re.match(r'https?://', query):
                    info = ydl.extract_info(query, download=False)
                else:
                    # Search on YouTube
                    info = ydl.extract_info(f"ytsearch1:{query}", download=False)
                    if info.get('entries'):
                        info = info['entries'][0]

                return {
                    'title': info.get('title', 'Unknown'),
                    'url': info.get('url', ''),
                    'duration': info.get('duration', 0),
                    'thumbnail': info.get('thumbnail', ''),
                    'uploader': info.get('uploader', 'Unknown'),
                    'webpage_url': info.get('webpage_url', ''),
                    'platform': 'YouTube'
                }
        except Exception as e:
            logging.error(f"Error extracting info: {e}")
            return None

    async def play_music(self, chat_id: int, track_info: dict):
        """Play music in voice chat"""
        try:
            # Create AudioPiped for audio-only playback
            stream = AudioPiped(track_info['url'])

            # Play in voice chat
            await pytgcalls.play(chat_id, stream)

            # Update current song
            self.current_song[chat_id] = track_info
            self.is_paused[chat_id] = False

            return True
        except Exception as e:
            logging.error(f"Error playing music: {e}")
            return False

    async def add_to_queue(self, chat_id: int, track_info: dict):
        """Add track to queue"""
        if chat_id not in queue_manager:
            queue_manager[chat_id] = []

        queue_manager[chat_id].append(track_info)

    async def get_queue(self, chat_id: int) -> List[dict]:
        """Get current queue"""
        return queue_manager.get(chat_id, [])

    async def skip_current(self, chat_id: int) -> bool:
        """Skip current track and play next"""
        try:
            queue = await self.get_queue(chat_id)
            if queue:
                next_track = queue.pop(0)
                await self.play_music(chat_id, next_track)
                return True
            else:
                await pytgcalls.stop(chat_id)
                return False
        except Exception as e:
            logging.error(f"Error skipping: {e}")
            return False

# Initialize music bot
music_bot = MusicBot()

# Bot commands
@app.on_message(filters.command(["start", "help"]))
async def start_command(client, message: Message):
    """Start command with bot info"""
    start_text = f"""🎵 **Vzoel Music Bot**

🎧 **Fitur:**
🔸 YouTube streaming
🔸 Spotify track info
🔸 SoundCloud support
🔸 Queue management
🔸 Voice chat streaming

🎮 **Commands:**
/play <query> - Play music
/queue - Show current queue
/skip - Skip current track
/stop - Stop music
/pause - Pause playback
/resume - Resume playback
/current - Now playing info

👨‍💻 **Founder:** Vzoel Fox's Lutpan
🆔 **ID Founder:** @VZLfxs
⚡ **Powered by:** PyTgCalls v2.2+"""

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎵 Join Voice Chat", callback_data="join_vc")],
        [InlineKeyboardButton("📊 Bot Stats", callback_data="bot_stats")]
    ])

    await message.reply_text(start_text, reply_markup=keyboard)

@app.on_message(filters.command("play"))
async def play_command(client, message: Message):
    """Play music command"""
    if len(message.command) < 2:
        await message.reply("🎵 **Usage:** `/play <song name or URL>`")
        return

    query = " ".join(message.command[1:])
    chat_id = message.chat.id

    # Processing message
    process_msg = await message.reply("🔍 **Searching for:** `{}`".format(query))

    try:
        # Extract track info
        track_info = await music_bot.extract_info(query)
        if not track_info:
            await process_msg.edit("❌ **Error:** Could not find track!")
            return

        await process_msg.edit("🎧 **Loading track...**")

        # Check if something is already playing
        if chat_id in music_bot.current_song:
            # Add to queue
            await music_bot.add_to_queue(chat_id, track_info)

            queue_pos = len(await music_bot.get_queue(chat_id))
            await process_msg.edit(
                f"📝 **Added to Queue** (Position: {queue_pos})\n\n"
                f"🎵 **Title:** {track_info['title']}\n"
                f"👤 **Uploader:** {track_info['uploader']}\n"
                f"⏱️ **Duration:** {track_info.get('duration', 'Unknown')} seconds"
            )
        else:
            # Play immediately
            success = await music_bot.play_music(chat_id, track_info)

            if success:
                keyboard = InlineKeyboardMarkup([
                    [InlineKeyboardButton("⏸️ Pause", callback_data=f"pause_{chat_id}"),
                     InlineKeyboardButton("⏭️ Skip", callback_data=f"skip_{chat_id}")],
                    [InlineKeyboardButton("📋 Queue", callback_data=f"queue_{chat_id}"),
                     InlineKeyboardButton("⏹️ Stop", callback_data=f"stop_{chat_id}")]
                ])

                await process_msg.edit(
                    f"▶️ **Now Playing:**\n\n"
                    f"🎵 **Title:** {track_info['title']}\n"
                    f"👤 **Uploader:** {track_info['uploader']}\n"
                    f"⏱️ **Duration:** {track_info.get('duration', 'Unknown')} seconds\n"
                    f"🔗 **Platform:** {track_info['platform']}",
                    reply_markup=keyboard
                )
            else:
                await process_msg.edit("❌ **Error:** Failed to play track!")

    except Exception as e:
        await process_msg.edit(f"❌ **Error:** {str(e)}")

@app.on_message(filters.command("queue"))
async def queue_command(client, message: Message):
    """Show current queue"""
    chat_id = message.chat.id
    queue = await music_bot.get_queue(chat_id)

    if not queue:
        await message.reply("📋 **Queue is empty!**")
        return

    queue_text = "📋 **Current Queue:**\n\n"
    for i, track in enumerate(queue[:10], 1):  # Show max 10 tracks
        queue_text += f"`{i}.` {track['title']}\n"

    if len(queue) > 10:
        queue_text += f"\n... and {len(queue) - 10} more tracks"

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔄 Shuffle", callback_data=f"shuffle_{chat_id}"),
         InlineKeyboardButton("🗑️ Clear", callback_data=f"clear_{chat_id}")]
    ])

    await message.reply_text(queue_text, reply_markup=keyboard)

@app.on_message(filters.command("current"))
async def current_command(client, message: Message):
    """Show currently playing track"""
    chat_id = message.chat.id

    if chat_id not in music_bot.current_song:
        await message.reply("🔇 **No music is currently playing!**")
        return

    track = music_bot.current_song[chat_id]
    status = "⏸️ Paused" if music_bot.is_paused.get(chat_id) else "▶️ Playing"

    current_text = f"""🎵 **Now Playing:**

{status}

**Title:** {track['title']}
**Uploader:** {track['uploader']}
**Platform:** {track['platform']}
**Duration:** {track.get('duration', 'Unknown')} seconds"""

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("⏸️ Pause" if not music_bot.is_paused.get(chat_id) else "▶️ Resume",
                             callback_data=f"toggle_{chat_id}"),
         InlineKeyboardButton("⏭️ Skip", callback_data=f"skip_{chat_id}")]
    ])

    await message.reply_text(current_text, reply_markup=keyboard)

@app.on_message(filters.command(["pause", "resume"]))
async def pause_resume_command(client, message: Message):
    """Pause/Resume music"""
    chat_id = message.chat.id
    command = message.command[0]

    try:
        if command == "pause":
            await pytgcalls.pause(chat_id)
            music_bot.is_paused[chat_id] = True
            await message.reply("⏸️ **Music paused!**")
        else:
            await pytgcalls.resume(chat_id)
            music_bot.is_paused[chat_id] = False
            await message.reply("▶️ **Music resumed!**")
    except Exception as e:
        await message.reply(f"❌ **Error:** {str(e)}")

@app.on_message(filters.command("skip"))
async def skip_command(client, message: Message):
    """Skip current track"""
    chat_id = message.chat.id

    success = await music_bot.skip_current(chat_id)
    if success:
        await message.reply("⏭️ **Track skipped!**")
    else:
        await message.reply("⏹️ **Queue ended. Music stopped.**")

@app.on_message(filters.command("stop"))
async def stop_command(client, message: Message):
    """Stop music and clear queue"""
    chat_id = message.chat.id

    try:
        await pytgcalls.stop(chat_id)

        # Clear data
        if chat_id in music_bot.current_song:
            del music_bot.current_song[chat_id]
        if chat_id in music_bot.is_paused:
            del music_bot.is_paused[chat_id]
        if chat_id in queue_manager:
            queue_manager[chat_id].clear()

        await message.reply("⏹️ **Music stopped and queue cleared!**")
    except Exception as e:
        await message.reply(f"❌ **Error:** {str(e)}")

# Callback handlers
@app.on_callback_query()
async def callback_handler(client, callback_query):
    """Handle inline keyboard callbacks"""
    data = callback_query.data
    chat_id = callback_query.message.chat.id

    if data.startswith("pause_"):
        await pytgcalls.pause(int(data.split("_")[1]))
        await callback_query.answer("⏸️ Paused")

    elif data.startswith("skip_"):
        success = await music_bot.skip_current(int(data.split("_")[1]))
        await callback_query.answer("⏭️ Skipped" if success else "⏹️ Queue ended")

    elif data.startswith("stop_"):
        await pytgcalls.stop(int(data.split("_")[1]))
        await callback_query.answer("⏹️ Stopped")

# PyTgCalls event handlers
@pytgcalls.on_kicked()
async def on_kicked(chat_id: int):
    """Handle when bot is kicked from voice chat"""
    logging.info(f"Kicked from voice chat: {chat_id}")

@pytgcalls.on_closed_voice_chat()
async def on_closed_vc(chat_id: int):
    """Handle when voice chat is closed"""
    logging.info(f"Voice chat closed: {chat_id}")

# Main execution
async def main():
    """Main bot execution"""
    # Initialize database
    init_database()

    # Start PyTgCalls
    await pytgcalls.start()
    print("🎵 VZL Music Bot Started!")
    print("📱 PyTgCalls initialized successfully")

    # Keep bot running
    await app.start()
    print("🤖 Bot client started")

    # Keep alive
    await asyncio.Future()  # Run forever

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Create downloads directory
    os.makedirs("downloads", exist_ok=True)

    # Run bot
    asyncio.run(main())
