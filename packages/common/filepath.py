import os

from packages.config import config
from packages.utils.system import getSysUsername


class DataFilePath:
    basePath = config["Others.dataLocation"]
    userLoginInfo = os.path.join(config["Others.dataLocation"], "userLoginInfo.pk")


class CacheFilePath:
    basePath = config["Others.cacheLocation"]
    avatarPath = os.path.join(config["Others.cacheLocation"], "avatar.jpg")
    coverPath = os.path.join(config["Others.cacheLocation"], "cover.jpg")
    mapDownloadPath = os.path.join(config["Others.cacheLocation"], "mapDownload")


class _OSUPath:
    @property
    def basePath(self):
        return config["Others.osuPath"]

    @property
    def cfgPath(self):
        return os.path.join(self.basePath, f'osu!.{getSysUsername()}.cfg')

    @property
    def songPath(self):
        with open(self.cfgPath, encoding='utf-8', errors='ignore') as f:
            content = f.readlines()

        n = 0
        for i in content:
            if 'BeatmapDirectory' in i:
                break
            else:
                n += 1
        content = content[n].replace("\n", "").split(' = ')

        if ':\\' not in content[1]:
            return os.path.join(self.basePath, content[1])
        else:
            return content[1]

    @property
    def osuDbPath(self):
        return os.path.join(self.basePath, 'osu!.db')


OSUPath = _OSUPath()
