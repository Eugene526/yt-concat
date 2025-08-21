import sys
import getopt
import logging
import os
from datetime import datetime

from yt_concat.pipeline.steps.preflight import Preflight
from yt_concat.pipeline.steps.helpers import Helper
from yt_concat.pipeline.steps.get_video_list import GetVideoList
from yt_concat.pipeline.steps.initialize_yt import InitializeYT
from yt_concat.pipeline.steps.download_captions import DownloadCaptions
from yt_concat.pipeline.steps.read_caption import ReadCaption
from yt_concat.pipeline.steps.search import Search
from yt_concat.pipeline.steps.download_videos import DownloadVideos
from yt_concat.pipeline.steps.edit_video import EditVideo
from yt_concat.pipeline.steps.cleanup import CleanUp
from yt_concat.pipeline.steps.postflight import Postflight
from yt_concat.pipeline.steps.step import StepException
from yt_concat.pipeline.pipeline import Pipeline
from yt_concat.utils import Utils

CHANNEL_ID = ''


def config_logger():
    log_dir = 'logs'
    os.makedirs(log_dir, exist_ok=True)  # 如果不存在就創建

    # 檔名使用當前時間
    log_filename = datetime.now().strftime('%Y-%m-%d %H-%M-%S') + '.log'
    log_path = os.path.join(log_dir, log_filename)

    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(filename)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler = logging.FileHandler(log_path)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger


def main():
    inputs = {
        'channel_id': CHANNEL_ID,
        'search_word': '',
        'limit': 20,
        'cleanup': False,
    }

    def print_usage():
        print('python3 test2.py OPTIONS')
        print('OPTIONS:')
        print('{:>6} {:<12}{}'.format('-c', '--channel', 'Channel id of the Youtube channel to download.'))
        print('{:>6} {:<12}{}'.format('', '--cleanup', 'Remove captions and videos downloaded during run.'))
        print('{:>6} {:<12}{}'.format(
            '-s', '--searchword', 'Search keyword used to find matching segments in subtitles.'))
        print('{:>6} {:<12}{}'.format(
            '-l', '--limit', 'The maximum number of fragments extracted based on keywords.'))

    short_opts = 'c:s:l:h'
    long_opts = 'channel= cleanup searchword= limit= help'.split()

    try:
        opts, _ = getopt.getopt(sys.argv[1:], short_opts, long_opts)
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print_usage()
            sys.exit(0)
        elif opt in ('-c', '--channel'):
            inputs['channel_id'] = arg
        elif opt in ('-s', '--searchword'):
            inputs['search_word'] = arg
        elif opt in ('-l', '--limit'):
            inputs['limit'] = arg
        elif '--cleanup' in opt:
            inputs['cleanup'] = True

    if not inputs['channel_id']:
        print_usage()
        sys.exit(2)

    steps = [
        Preflight(),
        Helper(),
        GetVideoList(),
        InitializeYT(),
        DownloadCaptions(),
        ReadCaption(),
        Search(),
        DownloadVideos(),
        EditVideo(),
        CleanUp(),
        Postflight(),
    ]

    logger = config_logger()
    utils = Utils()
    pipeline = Pipeline(steps, logger)
    pipeline.run(inputs, utils)


if __name__ == '__main__':
    main()
