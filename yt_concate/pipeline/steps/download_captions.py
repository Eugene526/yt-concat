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
            # 先用不帶副檔名的 outtmpl
            "outtmpl": {"default": utils.get_caption_filepath("%(id)s").replace(".txt", "")},
            "quiet": False,
        }

        for url in data:
            print("downloading caption for", url)

            if utils.caption_file_exist(url):
                print("Found existing caption file")
                continue

            try:
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                # 下載下來的會是 "<base>.en.srt"
                base_path = utils.get_caption_filepath(url).replace(".txt", "")
                srt_path = base_path + ".en.srt"
                txt_path = base_path + ".txt"

                if os.path.exists(srt_path):
                    with open(srt_path, "r", encoding="utf-8") as srt_file:
                        content = srt_file.read()

                    with open(txt_path, "w", encoding="utf-8") as txt_file:
                        txt_file.write(content)

                    os.remove(srt_path)  # 刪掉原始 srt 檔

            except Exception as e:
                print("Error:", e)
                continue

        end = time.time()
        print("took", end - start)
