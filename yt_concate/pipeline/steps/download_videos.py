from yt_dlp import YoutubeDL

from .step import Step
from yt_concate.settings import VIDEOS_DIR


class DownloadVideos(Step):
    def process(self, data, inputs, utils):
        yt_set = set([found.yt for found in data])
        print('videos to download=', len(yt_set))

        for yt in yt_set:
            url = yt.url
            if utils.video_file_exists(yt):
                print(f'found existing video file for {url}, skipping')
                continue

            print('downloading', url)

            ydl_opts = {
                "format": "best",  # 可以換成 'best' 選最好的畫質
                "outtmpl": f"{VIDEOS_DIR}/{yt.id}.%(ext)s",  # 指定輸出路徑與檔名
                "quiet": False
            }

            try:
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
            except Exception as e:
                print("Error downloading", url, ":", e)
                continue

        return data
