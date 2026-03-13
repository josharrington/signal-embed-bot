import base64
import tempfile
import os
import re
from pathlib import Path
from signalbot import Command, regex_triggered, Context
import yt_dlp


class UploadInstagramCommand(Command):
    """
    Triggers on any message containing 'www.instagram.com'.
    Downloads the Instagram video and sends it as a file attachment.
    """

    def extract_instagram_url(self, text: str) -> str | None:
        """Extract the first Instagram URL from the text."""
        match = re.search(r"(?:www\.)?instagram\.com/\S+", text)
        return match.group(0) if match else None

    @regex_triggered(r"www\.instagram\.com")
    async def handle(self, ctx: Context) -> None:
        original_text = ctx.message.text
        instagram_url = self.extract_instagram_url(original_text)

        if not instagram_url:
            return

        # Download the video using yt-dlp
        with tempfile.TemporaryDirectory() as temp_dir:
            ydl_opts = {
                "outtmpl": os.path.join(temp_dir, "%(title)s.%(ext)s"),
                "format": "best",
                "quiet": True,
                "no_warnings": True,
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # type: ignore
                    info = ydl.extract_info(instagram_url, download=True)
                    filename = ydl.prepare_filename(info)

                # Read the downloaded file and encode as base64
                with open(filename, "rb") as f:
                    file_content = f.read()
                    base64_data = base64.b64encode(file_content).decode("utf-8")

                # Send the video as an attachment
                video_filename = Path(filename).name
                await ctx.send(
                    f"[BOT] Attached Instagram Video: {video_filename}",
                    base64_attachments=[base64_data],
                )

            except Exception as e:
                await ctx.send(f"Failed to download video: {str(e)}")
            finally:
                try:
                    os.remove(filename)
                except:
                    pass
