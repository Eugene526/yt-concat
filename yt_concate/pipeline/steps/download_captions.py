from yt_dlp import YoutubeDL
import os
import time
import logging

from .step import Step, StepException


class DownloadCaptions(Step):
    def process(self, data, inputs, utils, logger):
        start = time.time()
        for yt in data:
            if utils.caption_file_exist(yt):
                logger.debug(f"Found existing caption file for {yt.id}")
                continue

            logger.debug(f"Downloading caption for {yt.id}")

            ydl_opts = {
                "skip_download": True,
                "writesubtitles": True,
                "writeautomaticsub": True,
                "subtitleslangs": ["en"],
                "subtitlesformat": "srt",
                "outtmpl": {"default": yt.get_caption_filepath().replace(".txt", "")},
                "quiet": True,
                "no_warnings": True
            }

            try:
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([yt.url])

                base_path = yt.get_caption_filepath().replace(".txt", "")
                srt_path = base_path + ".en.srt"
                txt_path = base_path + ".txt"

                if os.path.exists(srt_path):
                    with open(srt_path, "r", encoding="utf-8") as srt_file:
                        content = srt_file.read()

                    with open(txt_path, "w", encoding="utf-8") as txt_file:
                        txt_file.write(content)

                    os.remove(srt_path)

            except Exception as e:
                logger.warning(f"Error downloading {yt.id}: {e}")
                continue

        end = time.time()
        logger.info(f"Took {end - start:.2f} seconds to download captions")
        return data
