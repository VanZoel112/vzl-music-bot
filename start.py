#!/usr/bin/env python3
"""
VZL Music Bot - Easy Launcher
Quick start script untuk VZL Music Bot
"""

import os
import sys
import subprocess

def check_requirements():
    """Check if all requirements are installed"""
    try:
        import pyrogram
        import pytgcalls
        import yt_dlp
        import mutagen
        print("✅ All requirements are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def install_requirements():
    """Install requirements automatically"""
    print("🔧 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        return False

def check_config():
    """Check if configuration is properly set"""
    try:
        # Read main.py to check config
        with open("main.py", "r") as f:
            content = f.read()

        if "YOUR_BOT_TOKEN_HERE" in content:
            print("⚠️  Bot token belum diset!")
            print("Edit main.py dan isi:")
            print("- BOT_TOKEN")
            print("- API_ID")
            print("- API_HASH")
            print("- SUDO_USERS")
            return False

        print("✅ Configuration looks good")
        return True
    except FileNotFoundError:
        print("❌ main.py not found!")
        return False

def main():
    """Main launcher function"""
    print("🎵 VZL Music Bot - Easy Launcher")
    print("=" * 40)

    # Check if main.py exists
    if not os.path.exists("main.py"):
        print("❌ main.py tidak ditemukan!")
        return

    # Check requirements
    if not check_requirements():
        print("🔧 Installing missing requirements...")
        if not install_requirements():
            return

    # Check config
    if not check_config():
        return

    # Create downloads directory
    os.makedirs("downloads", exist_ok=True)
    print("📁 Downloads directory ready")

    # Start bot
    print("🚀 Starting VZL Music Bot...")
    print("=" * 40)

    try:
        subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\n⏹️  Bot stopped by user")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")

if __name__ == "__main__":
    main()