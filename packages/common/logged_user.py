from typing import Optional, Any, Union

from packages.common.qtsignalbus import signalBus
from packages.enums.osu import PlayMode
from packages.model.osu_web.user import LoginUserModel


class LoggedUser:
    userInfo: LoginUserModel
    lastUpdate: float
    isLogged: bool = False
    selectedMode: PlayMode = PlayMode.OSU

    def __getitem__(self, item):
        return getattr(self, item)

    def login(self):
        self.isLogged = True

    def updateUserInfo(self,
                       userInfo: Union[LoginUserModel, dict, None] = None,
                       key: Optional[str] = None,
                       value: Optional[Any] = None
                       ) -> bool:
        if userInfo and key:
            raise ValueError("key and userInfo must have only one at the same time!")

        if userInfo:
            for k, v in userInfo.items():
                if k == "avatar_url" and v != self.userInfo["avatar_url"]:
                    signalBus.avatarUpdate.emit(userInfo["avatar_url"])
                if k == "cover_url" and v != self.userInfo["cover_url"]:
                    signalBus.coverUpdate.emit(userInfo["cover_url"])
                setattr(self.userInfo, k, v)

            self.userInfo = userInfo
            return True

        if key and value:
            if key not in self.userInfo:
                return False

            if key == "avatar_url" and value != self.userInfo["avatar_url"]:
                signalBus.avatarUpdate.emit(value)
            if key == "cover_url" and value != self.userInfo["cover_url"]:
                signalBus.coverUpdate.emit(value)

            setattr(self.userInfo, key, value)


loggedUser = LoggedUser()
