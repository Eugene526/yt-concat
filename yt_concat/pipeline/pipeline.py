import logging

from .steps.step import StepException


class Pipeline:
    def __init__(self, steps, logger):
        self.steps = steps
        self.logger = logger

    def run(self, inputs, utils):
        data = None
        for step in self.steps:
            try:
                data = step.process(data, inputs, utils, self.logger)
            except StepException as e:
                self.logger.error(f"Exception happened: {e}")
                break
