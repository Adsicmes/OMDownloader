import ctypes
from ctypes import windll

import darkdetect
from PySide6.QtGui import QFontDatabase
from loguru import logger

from packages.config import config


@logger.catch
def initAppFont():
    logger.info("Initializing app font...")
    for font in [
        "TorusNotched-Bold",
        "TorusNotched-Heavy",
        "TorusNotched-Light",
        "TorusNotched-Regular",
        "TorusNotched-SemiBold",
        "TorusNotched-Thin",
        "Aller_Std_Bd",
        "Aller_Std_BdIt",
        "Aller_Std_It",
        "Aller_Std_Lt",
        "Aller_Std_LtIt",
        "Aller_Std_Rg",
        "Segoe Fluent Icons"
    ]:
        QFontDatabase.addApplicationFont(f":/res/raw/fonts/{font}.ttf")
        logger.info(f"Initialized app font: {font}")
    logger.info("Initialized app font.")


@logger.catch
def initLanguageConfiguration():
    # initialize i18n language
    # Language Code Reference Link:
    # https://learn.microsoft.com/zh-cn/previous-versions/system-center/system-center-2012-R2/dn281927%28v=sc.12%29
    lang_code = windll.kernel32.GetSystemDefaultUILanguage()  # return int, but can be directly compared with python hex

    if config["view"]["i18nLanguage"] != "auto":
        return

    if lang_code == 0x804:
        config.setViewI18nLanguage("zh_CN")
    elif lang_code == 0x409:
        config.setViewI18nLanguage("en_US")
    else:
        config.setViewI18nLanguage("en_US")
    logger.info("Successfully detect system language.")


@logger.catch
def initThemeConfiguration():
    if config["view"]["theme"] != "auto":
        return

    if darkdetect.isDark():
        config.setViewTheme("dark")
    else:
        config.setViewTheme("light")
    logger.info("Successfully detect if system in dark mode.")


@logger.catch
def initThemeColorConfiguration():
    if config["view"]["themeColor"] != "auto":
        return

    a = ctypes.c_ulong()
    b = ctypes.c_bool()
    a_p = ctypes.byref(a)
    b_p = ctypes.byref(b)
    windll.dwmapi.DwmGetColorizationColor(a_p, b_p)
    logger.info("Successfully detect system theme color.")
    hexStrValue = hex(a.value)[2:]
    config.setViewThemeColor(hexStrValue)
