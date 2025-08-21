from yt_dlp import YoutubeDL
import logging

from .step import Step
from yt_concate.settings import VIDEOS_DIR


class DownloadVideos(Step):
    def process(self, data, inputs, utils, logger):
        yt_set = set([found.yt for found in data])
        logger.debug('videos to download=', len(yt_set))

        for yt in yt_set:
            url = yt.url
            if utils.video_file_exists(yt):
                logger.debug(f'found existing video file for {url}, skipping')
                continue

            logger.info('downloading', url)

            ydl_opts = {
                "format": "mp4",  # 可以換成 'best' 選最好的畫質
                "outtmpl": f"{VIDEOS_DIR}/{yt.id}.%(ext)s",  # 指定輸出路徑與檔名
                "quiet": False
            }

            try:
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
            except Exception as e:
                logger.warning("Error downloading", url, ":", e)
                continue

        return data
