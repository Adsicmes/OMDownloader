import os

import i18n
from PySide6.QtCore import QFile
from loguru import logger

from packages.config import config
from packages.view import error_message


class JsonLoader(i18n.loaders.json_loader.JsonLoader):  # noqa
    def __init__(self):
        super(JsonLoader, self).__init__()

    @staticmethod
    def load_file(fp):
        try:
            file = QFile(fp)
            file.open(QFile.ReadOnly)
            content = file.readAll().toStdString()
            file.close()
            return content
        except IOError as e:
            raise i18n.I18nFileLoadError("error loading file {0}: {1}".format(fp, e.strerror)) from e

    def load_resource(self, filename, root_data, remember_content):
        if filename in self.loaded_files:
            data = self.loaded_files[filename]
            if not data:
                # cache is missing or exhausted
                return {}
        else:
            file_content = self.load_file(filename)
            data = self.parse_file(file_content)
        if not self.check_data(data, root_data):
            raise i18n.I18nFileLoadError("error getting data from {0}: {1} not defined".format(filename, root_data))
        enable_memoization = i18n.config.get('enable_memoization')
        if enable_memoization:
            if remember_content:
                self.loaded_files[filename] = data
            else:
                self.loaded_files[filename] = None
        return self.get_data(data, root_data)


def load_translation_file(filename, fp, locale=None):
    if locale is None:
        locale = i18n.config.get("locale")
    skip_locale_root_data = i18n.config.get('skip_locale_root_data')
    root_data = None if skip_locale_root_data else locale
    # if the file isn't dedicated to one locale and may contain other `root_data`s
    remember_content = "{locale}" not in i18n.config.get("filename_format") and root_data
    translations_dic = i18n.resource_loader.load_resource(fp, root_data, remember_content)
    namespace = i18n.resource_loader.get_namespace_from_filepath(filename)
    i18n.resource_loader.load_translation_dic(translations_dic, namespace, locale)


def load_external_translation_file():
    external_language_dir = r"lang"
    for f in os.listdir(external_language_dir):
        f_l = f.split(".")
        if len(f_l) != 3 or f_l[1] == "zh_CN" or f_l[1] == "en_US":
            logger.info(f"Skip load external translation file: {f}")
            continue
        load_translation_file(f, os.path.join(external_language_dir, f), f_l[1])
        logger.info(f"Successfully load external translation file: {f}")


def on_missing_translation(key, locale, **kwargs):
    logger.error(f"Missing translation for '{key}' in '{locale}'.")


def on_load_error(error, **kwargs):
    if isinstance(error, i18n.I18nFileLoadError):
        error_message("Error", "Translation file could not be loaded.\n"
                               "Maybe it doesn't exist? Or its format is wrong?\n"
                               "You can try to check the translation file.")

    exit()


@logger.catch(onerror=on_load_error)
def initI18n():
    logger.info("Initializing i18n...")

    i18n.register_loader(JsonLoader, ["json"])

    load_translation_file("app.en_US.json", ":/res/raw/lang/app.en_US.json", "en_US")
    load_translation_file("app.zh_CN.json", ":/res/raw/lang/app.zh_CN.json", "zh_CN")
    logger.info("Successfully load built-in translation files. (en_US, zh_CN)")

    load_external_translation_file()
    logger.info("Successfully load external translation files.")

    i18n.set("locale", config["View.i18nLanguage"])
    i18n.set("fallback", "en_US")
    i18n.set("file_format", "json")
    i18n.set("enable_memoization", True)
    i18n.set("on_missing_translation", on_missing_translation)
    logger.info("Successfully set i18n configs.")

    logger.info("Successfully initialized i18n.")
