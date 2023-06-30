import getpass
import time


def getSysUsername():
    """ get system username """
    return getpass.getuser()


def getNowUnixTimestamp():
    """ get system timestamp """
    return time.time()
