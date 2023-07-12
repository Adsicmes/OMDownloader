from .directory import *
from .i18n import *
from .logger import *
from .login import *
from .resource import *
from .view import *


def initPreUILoaded():
    initLogger()
    initResources()

    initDir()

    initLanguageConfiguration()
    initThemeConfiguration()
    initThemeColorConfiguration()

    initI18n()
    initAppFont()


def initAfterUILoaded():
    initLogin()
