from loguru import logger


def initResources():
    logger.info("Initializing resources...")
    from resources import resources  # noqa # pylint: disable=unused-import
    logger.success("Successfully initialized resources.")
