import logging

from .step import Step


class Preflight(Step):
    def process(self, data, inputs, utils, logger):
        logger.info('in Preflight')
        utils.create_dirs()