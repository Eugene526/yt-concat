import urllib.request
import json

from yt_concate.pipeline.steps.step import Step
from yt_concate.settings import API_KEY
from yt_concate.pipeline.steps.helpers import Helper


class GetVideoList(Step):
    def process(self, data, inputs, utils):
        channel_id = inputs['channel_id']
        api_key = API_KEY

        if utils.video_list_file_exists(channel_id):
            print('Found existing video list file for channel id')
            return self.read_file(utils.get_video_list_filepath(channel_id))

        base_video_url = 'https://www.youtube.com/watch?v='
        base_playlist_items_url = 'https://www.googleapis.com/youtube/v3/playlistItems?'

        uploads_playlist_id = Helper().process(data, inputs, utils)

        current_api_url = base_playlist_items_url + \
            'key={}&playlistId={}&part=snippet,contentDetails&maxResults=50'.format(
                api_key, uploads_playlist_id)

        video_links = []
        page_count = 0

        while True:
            page_count += 1

            with urllib.request.urlopen(current_api_url) as inp:
                resp = json.load(inp)

            if 'error' in resp:
                error_message = resp['error'].get('message', 'Unknown API Error')
                raise Exception(
                    f"API Error: {error_message} (Code: {resp['error'].get('code', 'N/A')})")

            for item in resp['items']:
                video_id = item['contentDetails']['videoId']
                video_links.append(base_video_url + video_id)

            next_page_token = resp.get('nextPageToken')

            if next_page_token:
                current_api_url = base_playlist_items_url + \
                    'key={}&playlistId={}&part=snippet,contentDetails&maxResults=50&pageToken={}'.format(
                        api_key, uploads_playlist_id, next_page_token)
            else:
                break

        print(video_links)
        self.write_to_file(video_links, utils.get_video_list_filepath(channel_id))
        return video_links

    def write_to_file(self, video_links, filepath):
        with open(filepath, 'w') as f:
            for url in video_links:
                f.write(url + '\n')

    def read_file(self, filepath):
        video_links = []
        with open(filepath, 'r') as f:
            for url in f:
                video_links.append(url.strip())
        return video_links
