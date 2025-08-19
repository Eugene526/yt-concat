from moviepy.editor import VideoFileClip, concatenate_videoclips

from .step import Step


class EditVideo(Step):
    def process(self, data, inputs, utils):
        clips = []
        for found in data:
            print("Caption time:", found.time)
            start, end = self.parse_caption_time(found.time)
            clip = VideoFileClip(found.yt.video_filepath)
            duration = clip.duration
            if start < duration:
                safe_end = min(end, duration - 0.05)
                if safe_end > start:
                    print("Cut clip:", start, "to", safe_end)
                    video = clip.subclip(start, safe_end)
                    clips.append(video)
                else:
                    print("Skip invalid range", start, safe_end)
            else:
                print("Skip, start >= duration", duration)

            if len(clips) >= inputs['limit']:
                break

        if clips:
            final_clip = concatenate_videoclips(clips, method="compose")
            output_filepath = utils.get_output_filepath(inputs['channel_id'], inputs['search_word'])
            print("Exporting video to", output_filepath)
            final_clip.write_videofile(output_filepath, audio=True)
        else:
            print("No valid clips found")

    def parse_caption_time(self, caption_time):
        start, end = caption_time.split(' --> ')
        return self.parse_time_str(start), self.parse_time_str(end)

    def parse_time_str(self, time_str):
        h, m, s = time_str.split(':')
        s, ms = s.split(',')
        return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000
