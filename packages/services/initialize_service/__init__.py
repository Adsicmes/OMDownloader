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

    initI18n()
    initAppFont()
