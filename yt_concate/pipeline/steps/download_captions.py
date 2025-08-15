from yt_dlp import YoutubeDL
import os
import time

from .step import Step, StepException


class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        start = time.time()

        ydl_opts = {
            "skip_download": True,
            "writesubtitles": True,
            "writeautomaticsub": True,
            "subtitleslangs": ["en"],
            "subtitlesformat": "srt",
            "outtmpl": {"default": utils.get_caption_filepath("%(id)s.srt")},
            "quiet": False,
        }

        for url in data:
            print('downloading caption for', url)

            if utils.caption_file_exist(url):
                print('Found existing caption file')
                continue

            try:
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                # 下載完後將 SRT 轉 TXT
                srt_path = utils.get_caption_filepath(url).replace(".txt", ".srt")
                if os.path.exists(srt_path):
                    with open(srt_path, "r", encoding="utf-8") as srt_file:
                        content = srt_file.read()

                    with open(utils.get_caption_filepath(url), "w", encoding="utf-8") as txt_file:
                        txt_file.write(content)

                    os.remove(srt_path)

            except Exception as e:
                print('Error:', e)
                continue

        end = time.time()
        print('took', end - start)
