from loguru import logger


def initResources():
    logger.info("Initializing resources...")
    from packages import resources  # noqa # pylint: disable=unused-import
    logger.info("Successfully initialized resources.")