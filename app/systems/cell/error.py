import logging
from utility.display import format_traceback, format_exception_info


logger = logging.getLogger(__name__)


class ErrorHandler:
    def __init__(self, command):
        self.command = command

    def handle(self, error):
        # Log command-level error
        logger.error(f"Command-level error: {str(error)}")
        self._log_error_details(error)

    def _log_error_details(self, error):
        logger.debug("Error traceback:\n%s", "\n".join([item.strip() for item in format_traceback()]))
        logger.debug("Exception info:\n%s", "\n".join([item.strip() for item in format_exception_info()]))
