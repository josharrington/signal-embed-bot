import os
import logging
from signalbot import SignalBot, Config
from signalbot import enable_console_logging
from dotenv import load_dotenv
from commands.UploadTikTokCommand import UploadTikTokCommand
from commands.UploadInstagramCommand import UploadInstagramCommand
from commands.PingCommand import PingCommand

load_dotenv()
enable_console_logging(logging.INFO)

config = Config(
    signal_service=os.getenv("SIGNAL_SERVICE", ""),
    phone_number=os.getenv("PHONE_NUMBER", ""),
)

bot = SignalBot(config)

# Allow specifying which Signal groups the TikTok downloader should run in.
# Provide a comma-separated list in the TIKTOK_GROUPS env var (e.g. "Friends,Work").
# Set MONITOR_ALL_GROUPS=true to monitor all groups instead.
monitor_all_groups = os.getenv("MONITOR_ALL_GROUPS", "false").strip().lower() in (
    "1",
    "true",
    "yes",
    "on",
)
group_list = [g.strip() for g in os.getenv("TIKTOK_GROUPS", "").split(",") if g.strip()]

# Allow all private contacts to use the TikTok command when enabled.
# Set ALLOW_PRIVATE_CONTACTS=true to enable.
allow_private = os.getenv("ALLOW_PRIVATE_CONTACTS", "false").strip().lower() in (
    "1",
    "true",
    "yes",
    "on",
)

commands = [
    UploadTikTokCommand,
    UploadInstagramCommand,
]

for c in commands:
    bot.register(
        c(),
        groups=True if monitor_all_groups else group_list,
        contacts=True if allow_private else [config.phone_number],
    )

# Ping Command will only be available to the user running the bot.
bot.register(PingCommand(), groups=[], contacts=[config.phone_number])

if __name__ == "__main__":
    print("Starting bot...")
    bot.start()
