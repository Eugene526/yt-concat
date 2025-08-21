import urllib.request
import json
import logging

from yt_concate.pipeline.steps.step import Step, StepException
from yt_concate.settings import API_KEY


class Helper(Step):
    def process(self, data, inputs, utils, logger):
        api_key = API_KEY
        channel_id = inputs['channel_id']
        channel_url = 'https://www.googleapis.com/youtube/v3/channels?key={}&id={}&part=contentDetails'.format(api_key, channel_id)

        with urllib.request.urlopen(channel_url) as inp:
            resp = json.load(inp)

        if "items" not in resp or len(resp["items"]) == 0:
            raise StepException(f"No channel found for id {channel_id}")

        uploads_playlist_id = resp['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        return uploads_playlist_id
