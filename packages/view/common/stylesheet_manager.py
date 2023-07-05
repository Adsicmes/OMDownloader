from enum import Enum

from qfluentwidgets import StyleSheetBase, Theme, qconfig


class StyleSheet(StyleSheetBase, Enum):
    """ Style sheet """

    TITLEBAR = "titlebar"

    HOME_INTERFACE = "home_interface"
    MAP_DOWNLOAD_INTERFACE = "map_download_interface"

    PARAMETER_FILL_IN_WIDGET = "parameter_fill_in_widget"

    def path(self, theme=Theme.AUTO):
        theme = qconfig.theme if theme == Theme.AUTO else theme
        return f":/res/raw/qss/{theme.value.lower()}/{self.value}.qss"
