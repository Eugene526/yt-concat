import os
import shutil
import logging

from .step import Step

class CleanUp(Step):
    def process(self, data, inputs, utils, logger):
        captions = '../downloads/captions'
        videos = '../downloads/videos'

        if inputs.get('cleanup', False):
            logger.info("Cleaning up downloaded files...")

            for folder in [captions, videos]:
                if os.path.exists(folder):
                    for filename in os.listdir(folder):
                        file_path = os.path.join(folder, filename)
                        if os.path.isfile(file_path) or os.path.islink(file_path):
                            os.remove(file_path)
                            logger.info(f"Deleted file: {file_path}")
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                            logger.info(f"Deleted folder: {file_path}")

        return data
