import logging

from utility.display import format_exception_info

logger = logging.getLogger(__name__)


class ErrorHandler:
    def __init__(self, command):
        self.command = command

    def handle(self, error):
        # Log command-level error
        logger.error(f"Command-level error: {str(error)}")
        logger.error("\n".join([item.strip() for item in format_exception_info()]))
