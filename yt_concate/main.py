import urllib.request
import json
from yt_concate.settings import API_KEY

CHANNEL_ID = 'UCKSVUHI9rbbkXhvAXK-2uxA'

def get_uploads_playlist_id(channel_id, api_key):
    channel_url = 'https://www.googleapis.com/youtube/v3/channels?key={}&id={}&part=contentDetails'.format(api_key,channel_id)

    try:
        with urllib.request.urlopen(channel_url) as inp:
            resp = json.load(inp)

        if 'error' in resp:
            error_message = resp['error'].get('message', 'Unknown API Error')
            raise Exception(f"API Error: {error_message} (Code: {resp['error'].get('code', 'N/A')})")

        uploads_playlist_id = resp['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        return uploads_playlist_id
    except urllib.error.URLError as e:
        raise
    except KeyError:
        raise
    except IndexError:
        raise
    except Exception as e:
        raise


def get_all_video_in_channel(channel_id):
    api_key = API_KEY

    base_video_url = 'https://www.youtube.com/watch?v='
    base_playlist_items_url = 'https://www.googleapis.com/youtube/v3/playlistItems?'

    uploads_playlist_id = get_uploads_playlist_id(channel_id, api_key)

    current_api_url = base_playlist_items_url + 'key={}&playlistId={}&part=snippet,contentDetails&maxResults=50'.format(
        api_key, uploads_playlist_id)

    video_links = []
    page_count = 0

    while True:
        page_count += 1
        try:
            with urllib.request.urlopen(current_api_url) as inp:
                resp = json.load(inp)

            if 'error' in resp:
                error_message = resp['error'].get('message', 'Unknown API Error')
                raise Exception(f"API Error: {error_message} (Code: {resp['error'].get('code', 'N/A')})")

            for item in resp['items']:
                video_id = item['contentDetails']['videoId']
                video_links.append(base_video_url + video_id)

            next_page_token = resp.get('nextPageToken')

            if next_page_token:
                current_api_url = base_playlist_items_url + 'key={}&playlistId={}&part=snippet,contentDetails&maxResults=50&pageToken={}'.format(
                    api_key, uploads_playlist_id, next_page_token)
            else:
                break

        except urllib.error.URLError as e:
            break
        except Exception as e:
            break

    return video_links


if __name__ == "__main__":
    try:
        video_list = get_all_video_in_channel(CHANNEL_ID)
        print(len(video_list))
    except Exception as e:
        pass