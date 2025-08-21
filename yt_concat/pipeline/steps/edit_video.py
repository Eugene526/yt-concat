from moviepy import VideoFileClip, concatenate_videoclips
import logging

from .step import Step


class EditVideo(Step):
    def process(self, data, inputs, utils, logger):
        clips = []
        for found in data:
            logger.debug(f"Caption time: {found.time}")
            start, end = self.parse_caption_time(found.time)
            clip = VideoFileClip(found.yt.video_filepath)
            duration = clip.duration
            if start < duration:
                safe_end = min(end, duration - 0.05)
                if safe_end > start:
                    logger.debug(f"Cut clip: {start} to {safe_end}")
                    video = clip.subclipped(start, safe_end)
                    clips.append(video)
                else:
                    logger.debug(f"Skip invalid range, {start} {safe_end}")
            else:
                logger.warning(f"Skip, start >= duration {duration}")

            if len(clips) >= inputs['limit']:
                break

        if clips:
            final_clip = concatenate_videoclips(clips, method="compose")
            output_filepath = utils.get_output_filepath(inputs['channel_id'], inputs['search_word'])
            logger.info(f"Exporting video to {output_filepath}")
            final_clip.write_videofile(output_filepath, audio=True)
        else:
            logger.warning("No valid clips found")

    def parse_caption_time(self, caption_time):
        start, end = caption_time.split(' --> ')
        return self.parse_time_str(start), self.parse_time_str(end)

    def parse_time_str(self, time_str):
        h, m, s = time_str.split(':')
        s, ms = s.split(',')
        return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000
