# Signal Embed Bot

A Python bot that uses the `signalbot` library to listen for incoming Signal messages containing web video links. When such a message is received, the bot downloads the video using `yt-dlp` and sends it as a file attachment.

Currently supported:
- TikTok

## Prerequisites

- Python 3.13+
- `uv` package manager
- `docker` or `podman`

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd signal-video-bot
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

## Configuration

Create a `.env` file in the project root with your Signal service details and optional filters:

```bash
# Replace with your phone number that is registered to Signal.
PHONE_NUMBER=+1234567890

# If you are not using Docker Compose, set SIGNAL_SERVICE to the address of signal-cli-rest-api
# SIGNAL_SERVICE=http://127.0.0.1:8080

# Optional filters:
# A comma-separated list of groups where TikTok downloading is enabled.
# Leave empty to disable group restrictions.
# TIKTOK_GROUPS=Friends,Work

# Set to true to monitor all groups regardless of TIKTOK_GROUPS.
# MONITOR_ALL_GROUPS=true

# Allow all private contacts to use the TikTok command.
# ALLOW_PRIVATE_CONTACTS=true
```

If running with Docker Compose, the `SIGNAL_SERVICE` is automatically set to `http://signal-api:8080`. If not, then you will need to set it to where signal-cli-rest-api is running. See https://signalbot-org.github.io/signalbot/latest/getting_started/ for more info.

## First Time Setup

Before running the bot, you need to link your Signal account with the Signal CLI REST API. Follow these steps:

1. **Run the Signal CLI REST API in normal mode** to link your account:
   ```bash
   docker run -p 8080:8080 \
       -v $(pwd)/signal-cli-config:/home/.local/share/signal-cli \
       -e 'MODE=normal' bbernhard/signal-cli-rest-api:latest
   ```

2. **Link your Signal account**:
   Open [http://localhost:8080/v1/qrcodelink?device_name=SignalEmbedBot](http://127.0.0.1:8080/v1/qrcodelink?device_name=SignalEmbedBot) in your browser to generate a QR code.

3. **Scan the QR code**:
   In your Signal app, go to Settings > Linked Devices > Link New Device, and scan the QR code displayed in the browser. The server can now receive and send messages. The access key will be stored in the `signal-cli-config` directory.

4. **Stop the container** (Ctrl+C)

Once linked, you can proceed to run the full stack with Docker Compose.

## Running with Docker

1. Ensure you have Docker and Docker Compose installed.

2. Run the services:
   ```bash
   docker compose up -d
   ```

## Testing

The bot is configured to always respond to the user in the "Note to Self" channel in Signal regardless of other configuration options. Send this channel a `Ping` message and you should receive `Pong` in return.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
