from .directory import *
from .i18n import *
from .logger import *
from .resource import *
from .view import *


def initAll():
    initLogger()
    initResources()

    initLanguageConfiguration()
    initThemeConfiguration()
    initThemeColorConfiguration()

    initDir()

    initI18n()
    initAppFont()
