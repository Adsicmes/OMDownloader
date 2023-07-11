from packages.model.osu_web.user import UserModel


class LoggedUser:
    userInfo: UserModel
    lastUpdate: float
    isLogged: bool = False


loggedUser = LoggedUser()
