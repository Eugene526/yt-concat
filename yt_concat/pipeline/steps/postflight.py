from .step import Step


class Postflight(Step):
    def process(self, data, inputs, utils, logger):
        logger.info('in Postflight')