# import configparser
# import os
# from typing import TypedDict, Literal
#
# from packages.utils import getSysUsername
#
# CFG_PATH = f'config.{getSysUsername()}.ini'
# DEFAULT_CFG = """
# [View]
# ; All view-related configurations
# i18nLanguage=auto
# theme=auto
# themeColor=auto
#
# [Queue]
# ; All queue-related configurations
# maxTaskCount=3
#
# [ConnectionTimeout]
# ppy_sh=10
#
# [Retry]
# ppy_sh=3
#
# [Others]
# cacheLocation=cache
# dataLocation=data
# langLocation=lang
# """.strip()
#
# class SectionView(TypedDict):
#     i18nLanguage: str
#     theme: str
#     themeColor: str
#
#
# class Queue(TypedDict):
#     maxTaskCount: int
#
#
# class ConnectionTimeout(TypedDict):
#     ppy_sh: int
#
#
# class Retry(TypedDict):
#     ppy_sh: int
#
#
# class Others(TypedDict):
#     cacheLocation: str
#     dataLocation: str
#     langLocation: str
#
#
# class ConfigItem(TypedDict):
#     view: SectionView
#     queue: Queue
#     connectionTimeout: ConnectionTimeout
#     retry: Retry
#     others: Others
#
#
# class Config:
#     _config: ConfigItem
#
#     _cfg: configparser.ConfigParser
#
#     def __init__(self):
#         self._cfg = self._readCfgFile()
#
#         try:
#             self._config = ConfigItem(
#                 view=SectionView(
#                     i18nLanguage=self._cfg.get("View", "i18nLanguage"),
#                     theme=self._cfg.get("View", "theme"),
#                     themeColor=self._cfg.get("View", "themeColor")
#                 ),
#                 queue=Queue(
#                     maxTaskCount=int(self._cfg.get("Queue", "maxTaskCount"))
#                 ),
#                 connectionTimeout=ConnectionTimeout(
#                     ppy_sh=int(self._cfg.get("ConnectionTimeout", "ppy_sh"))
#                 ),
#                 retry=Retry(
#                     ppy_sh=int(self._cfg.get("Retry", "ppy_sh"))
#                 ),
#                 others=Others(
#                     cacheLocation=self._cfg.get("Others", "cacheLocation"),
#                     dataLocation=self._cfg.get("Others", "dataLocation"),
#                     langLocation=self._cfg.get("Others", "langLocation")
#                 )
#             )
#         except configparser.NoSectionError | configparser.NoOptionError:
#             pass
#
#     def __getitem__(self, item):
#         return self._config[item]
#
#     @staticmethod
#     def _readCfgFile():
#         """
#         try to read config ini, if not found, create a new one
#         and write default config text into it
#         """
#         cfg_file = configparser.ConfigParser()
#
#         if not os.path.exists(CFG_PATH):
#             with open(CFG_PATH, "w") as cfg:
#                 cfg.write(DEFAULT_CFG)
#
#         cfg_file.read(CFG_PATH)
#         return cfg_file
#
#     def setViewI18nLanguage(self, value: str):
#         self._config["view"]["i18nLanguage"] = value
#
#     def setViewTheme(self, theme: Literal["dark", "light", "auto"]):
#         self._config["view"]["theme"] = theme
#
#     def setViewThemeColor(self, color: str):
#         self._config["view"]["themeColor"] = color
#
#     def setItem(self, section: str, item: str, value):
#         self._config[section][item] = value
#         self._cfg.set(section, item, value)
#         self._save()
#
#     def _save(self):
#         self._cfg.write(open(CFG_PATH, "w"))

import configparser
import os
from typing import Dict, Union

from PySide6.QtCore import QObject, Signal

from packages.utils.system import getSysUsername


class ConfigFile(QObject):
    configChanged = Signal()

    def __init__(self) -> None:
        super().__init__()
        self.config: configparser.ConfigParser = configparser.ConfigParser()
        self.configFile: str = f"config.{getSysUsername()}.ini"
        self.defaultConfig: Dict[str, Dict[str, Union[str, int]]] = {
            'View': {
                'i18nLanguage': 'auto',
                'theme': 'auto',
                'themeColor': 'auto'
            },
            'Queue': {
                'maxTaskCount': 3
            },
            'ConnectionTimeout': {
                'ppy_sh': 10
            },
            'Retry': {
                'ppy_sh': 3
            },
            'Others': {
                'osuPath': 'auto',
                'cacheLocation': 'cache',
                'dataLocation': 'data',
                'langLocation': 'lang'
            }
        }
        self.tempConfig: Dict[str, Dict[str, Union[str, int]]] = {}
        self.loadConfig()

    def loadConfig(self) -> None:
        if not os.path.exists(self.configFile):
            self.createConfig()
        self.config.read(self.configFile)

    def createConfig(self) -> None:
        # os.makedirs(os.path.dirname(self.configFile), exist_ok=True)
        self.config.read_dict(self.defaultConfig)
        with open(self.configFile, 'w') as configFile:
            self.config.write(configFile)

    def getValue(self, section: str, key: str) -> str:
        if section in self.tempConfig and key in self.tempConfig[section]:
            return self.tempConfig[section][key] or self.config.get(section, key)
        return self.config.get(section, key)

    def setValue(self, section: str, key: str, value: Union[str, int], saveToFile: bool = True) -> None:
        value = str(value)
        if section in self.tempConfig and key in self.tempConfig[section]:
            self.tempConfig[section][key] = value
        else:
            self.config.set(section, key, str(value))
            if saveToFile:
                os.makedirs(os.path.dirname(self.configFile), exist_ok=True)
                with open(self.configFile, 'w') as configFile:
                    self.config.write(configFile)
        self.configChanged.emit()

    def __getitem__(self, key: str) -> str:
        section, key = key.split('.')
        return self.getValue(section, key)


config = ConfigFile()  # cfg after handle
