from yt_dlp import YoutubeDL
import os
import time

from .step import Step, StepException


class DownloadCaptions(Step):
    def process(self, data, inputs, utils):
        start = time.time()
        for yt in data:
            if utils.caption_file_exist(yt):
                print("Found existing caption file for", yt.id)
                continue

            print("downloading caption for", yt.id)

            ydl_opts = {
                "skip_download": True,
                "writesubtitles": True,
                "writeautomaticsub": True,
                "subtitleslangs": ["en"],
                "subtitlesformat": "srt",
                # 先用不帶副檔名的 outtmpl
                "outtmpl": {"default": yt.get_caption_filepath().replace(".txt", "")},
                "quiet": True,
                "no_warnings": True
            }

            try:
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([yt.url])

                # 下載下來的會是 "<base>.en.srt"
                base_path = yt.get_caption_filepath().replace(".txt", "")
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

        return data
