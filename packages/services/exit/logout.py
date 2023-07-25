from loguru import logger

from packages.common.logged_user import loggedUser
from packages.common.request import osuWebApi


def exitLogout():
    if loggedUser.isLogged:
        logger.info("Logging out osu account...")
        osuWebApi.logout()
        loggedUser.isLogged = False
        return
    logger.info("Osu account is not login, dont need to logout.")
