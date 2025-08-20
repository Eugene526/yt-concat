import sys, getopt

from yt_concate.pipeline.steps.preflight import Preflight
from yt_concate.pipeline.steps.helpers import Helper
from yt_concate.pipeline.steps.get_video_list import GetVideoList
from yt_concate.pipeline.steps.initialize_yt import InitializeYT
from yt_concate.pipeline.steps.download_captions import DownloadCaptions
from yt_concate.pipeline.steps.read_caption import ReadCaption
from yt_concate.pipeline.steps.search import Search
from yt_concate.pipeline.steps.download_videos import DownloadVideos
from yt_concate.pipeline.steps.edit_video import EditVideo
from yt_concate.pipeline.steps.cleanup import CleanUp
from yt_concate.pipeline.steps.postflight import Postflight
from yt_concate.pipeline.steps.step import StepException
from yt_concate.pipeline.pipeline import Pipeline
from yt_concate.utils import Utils

CHANNEL_ID = 'UCKSVUHI9rbbkXhvAXK-2uxA'


def main():
    inputs = {
        'channel_id': CHANNEL_ID,
        'search_word': 'incredible',
        'limit': 20,
        'cleanup': False,
    }

    def print_usage():
        print('python3 test2.py OPTIONS')
        print('OPTIONS:')
        print('{:>6} {:<12}{}'.format('-c', '--channel', 'Channel id of the Youtube channel to download.'))
        print('{:>6} {:<12}{}'.format('', '--cleanup', 'Remove captions and videos downloaded during run.'))
        print('{:>6} {:<12}{}'.format('-s', '--searchword',
                                      'Search keyword used to find matching segments in subtitles.'))
        print('{:>6} {:<12}{}'.format('-l', '--limit', 'The maximum number of fragments extracted based on keywords.'))

    short_opts = 'c:s:l:h'
    long_opts = 'channel= cleanup searchword= limit= help'.split()

    try:
        opts, args = getopt.getopt(sys.argv[1:], short_opts, long_opts)
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print_usage()
            sys.exit(0)
        elif opt in ("-c", "--channel"):
            inputs['channel_id'] = arg
            username = arg
        elif opt in ("-s", "--searchword"):
            inputs['search_word'] = arg
        elif opt in ("-l", "--limit"):
            inputs['limit'] = arg
        elif '--cleanup' in opt:
            inputs['cleanup'] = True

    steps = [
        Preflight(),
        Helper(),
        GetVideoList(),
        InitializeYT(),
        # DownloadCaptions(),
        ReadCaption(),
        Search(),
        DownloadVideos(),
        EditVideo(),
        CleanUp(),
        Postflight(),
    ]

    utils = Utils()
    p = Pipeline(steps)
    p.run(inputs, utils)


if __name__ == '__main__':
    main()
