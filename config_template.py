"""
Vzoel Music Bot - Configuration Template
Copy this to main.py and replace the CONFIG section
"""

# Configuration - EDIT THESE VALUES
CONFIG = {
    "BOT_TOKEN": "YOUR_BOT_TOKEN_HERE",  # Get from @BotFather
    "API_ID": 12345678,                   # Get from my.telegram.org
    "API_HASH": "your_api_hash_here",     # Get from my.telegram.org
    "SUDO_USERS": [123456789, 987654321], # Admin user IDs - SEPARATE WITH COMMAS
    "LOG_GROUP_ID": -1001234567890,       # Optional: Log group ID
    "DATABASE_PATH": "vzl_music.db"       # Database file name
}

# CORRECT EXAMPLES:
# Single admin:     "SUDO_USERS": [123456789],
# Multiple admins:  "SUDO_USERS": [123456789, 987654321, 555444333],
#
# WRONG FORMAT:     "SUDO_USERS": [123456789], [987654321]  # This causes error!
# CORRECT FORMAT:   "SUDO_USERS": [123456789, 987654321],  # This works!