# 🎵 VZL Music Bot

**Realistic Telegram Music Bot dengan PyTgCalls Integration**

Created by: **VanZoel112**
Enhanced by: **Vzoel Fox's Ltpn**

---

## 🚀 Features

- 🎧 **YouTube Streaming** - Direct audio streaming dari YouTube
- 🎵 **Multi-Platform Support** - YouTube, Spotify info, SoundCloud
- 📋 **Queue Management** - Antrian musik dengan skip/pause controls
- 🎙️ **Voice Chat Integration** - PyTgCalls untuk streaming langsung
- 💾 **Database Tracking** - SQLite untuk history dan stats
- 🤖 **Inline Controls** - Button controls untuk pause/skip/stop
- 🔍 **Smart Search** - URL atau search query support

---

## ⚡ Quick Start

### 1️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 2️⃣ Configuration

Edit configuration di `main.py`:

```python
CONFIG = {
    "BOT_TOKEN": "YOUR_BOT_TOKEN_HERE",
    "API_ID": 12345678,
    "API_HASH": "your_api_hash_here",
    "SUDO_USERS": [123456789],  # Admin user IDs
    "LOG_GROUP_ID": -1001234567890,  # Optional: Log group
    "DATABASE_PATH": "vzl_music.db"
}
```

### 3️⃣ Run Bot

```bash
python main.py
```

---

## 🎮 Commands

### Basic Commands

- `/start` - Bot information dan help
- `/play <query>` - Play musik (URL atau search)
- `/queue` - Lihat antrian musik
- `/current` - Info lagu yang sedang diputar
- `/skip` - Skip lagu saat ini
- `/stop` - Stop musik dan clear queue
- `/pause` - Pause musik
- `/resume` - Resume musik

### Inline Controls

Setiap lagu yang diputar akan memiliki button controls:
- ⏸️ **Pause** - Pause/Resume musik
- ⏭️ **Skip** - Skip ke lagu berikutnya
- 📋 **Queue** - Lihat antrian
- ⏹️ **Stop** - Stop musik

---

## 🛠️ Technical Details

### Dependencies

- **PyTgCalls 3.0+** - Voice chat streaming
- **Pyrogram 2.2+** - Telegram MTProto client
- **yt-dlp** - YouTube audio extraction
- **Mutagen** - Audio metadata handling
- **SQLite3** - Database storage

### Audio Quality

- Format: `bestaudio[ext=webm]/bestaudio[ext=m4a]/bestaudio`
- Quality: Best available audio quality
- Codec: WebM/M4A optimization

### Performance

- **Async/await** - Non-blocking operations
- **Queue system** - Multiple tracks management
- **Memory efficient** - Stream langsung tanpa download
- **Error handling** - Robust fallback system

---

## 🎯 Use Cases

### Group Voice Chat
- Stream musik untuk group voice chat
- Multiple users bisa request lagu
- Queue management untuk fair play

### Personal Music
- Private music streaming
- Personal playlist management
- Audio quality priority

### Event Streaming
- Live event background music
- Scheduled music streaming
- Community music sessions

---

## ⚠️ Limitations

### Standard Emojis Only
Bot menggunakan standard emoji karena:
- Premium emoji memerlukan Fragment username (cost 1000+ TON ≈ $2000+)
- Realistic approach untuk personal use
- Compatibility dengan semua devices

### Audio Sources
- **YouTube**: Full streaming support ✅
- **Spotify**: Metadata only (Track info) ⚠️
- **SoundCloud**: Limited support ⚠️
- **Local Files**: Not supported ❌

---

## 🔧 Troubleshooting

### PyTgCalls Errors
```bash
# Update PyTgCalls
pip install --upgrade pytgcalls

# Check version
python -c "import pytgcalls; print(pytgcalls.__version__)"
```

### YouTube-DL Errors
```bash
# Update yt-dlp
pip install --upgrade yt-dlp

# Clear cache
yt-dlp --rm-cache-dir
```

### Database Issues
```bash
# Reset database
rm vzl_music.db
# Bot will recreate on next run
```

---

## 📁 Project Structure

```
vzl_music_bot/
├── main.py              # Main bot file
├── requirements.txt     # Dependencies
├── README.md           # This file
├── vzl_music.db        # SQLite database (auto-generated)
└── downloads/          # Temp download folder (auto-created)
```

---

## 🔐 Security Notes

### Important
1. **Bot Token**: Keep your bot token secure
2. **API Credentials**: Never share API_ID/API_HASH
3. **Admin Users**: Only add trusted users to SUDO_USERS
4. **Log Group**: Optional but recommended for monitoring

### Best Practices
- Use environment variables for sensitive data
- Regular database backups
- Monitor bot usage and logs
- Update dependencies regularly

---

## 📜 License

This project is created for educational and personal use.

**© 2024 VanZoel112 - VZL Music Bot**

---

## 🎵 Enjoy Your Music!

*Bot musik realistis untuk streaming Telegram yang sesungguhnya! 🎧*

---

**Support & Updates**
- Repository: [VZL Music Bot](https://github.com/VanZoel112/vzl-music-bot)
- Creator: VanZoel112
- Enhanced by: Vzoel Fox's Ltpn