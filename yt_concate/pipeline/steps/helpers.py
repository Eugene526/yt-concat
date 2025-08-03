import urllib.request
import json

from yt_concate.pipeline.steps.step import Step
from yt_concate.settings import API_KEY


class Helper(Step):
    def process(self, data, inputs):
        api_key = API_KEY
        channel_id = inputs['channel_id']
        channel_url = 'https://www.googleapis.com/youtube/v3/channels?key={}&id={}&part=contentDetails'.format(api_key,
                                                                                                               channel_id)

        with urllib.request.urlopen(channel_url) as inp:
            resp = json.load(inp)

        uploads_playlist_id = resp['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        return uploads_playlist_id
