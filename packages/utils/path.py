import os
import re


def isValidLocalPath(path):
    """ check if path is valid and is a local path """

    if not isinstance(path, str):
        return False

    if not path:
        return False

    if os.path.exists(path) and (os.path.isdir(path) or os.path.isfile(path)):
        return True

    return False


def convertToValidFilename(string):
    invalid_chars = r'[\\/:\*\?"<>\|]'

    return re.sub(invalid_chars, '_', string)
