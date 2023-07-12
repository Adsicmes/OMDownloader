import re
from enum import Enum
from typing import Tuple, List

import httpx

from packages.config import config
from packages.model.osu_web.beatmap import BeatmapParamsOfficial


class OsuWebApi:
    BASE_URL = "https://osu.ppy.sh"

    def __init__(self, client: httpx.Client = None, timeout: int = config['connectionTimeout']['ppy_sh']):
        if client is None:
            self.externalClient = False
            self.client = httpx.Client(timeout=timeout)
        else:
            self.externalClient = True
            self.client = client

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.externalClient:
            self.closeClient()

    def closeClient(self):
        self.client.close()

    def _pageCSRFToken(self) -> Tuple[str, httpx.Response]:
        resp = self.client.get(self.BASE_URL + "/home")
        csrfToken = re.compile(r".*?csrf-token.*?content=\"(.*?)\">", re.DOTALL).match(resp.text).group(1)
        return csrfToken, resp

    def login(self, username: str, password: str) -> httpx.Response:
        headers = {"referer": self.BASE_URL + "/home"}
        return self.client.post(self.BASE_URL + "/session", headers=headers, data={
            "username": username,
            "password": password,
            "_token": self._pageCSRFToken()[0]
        })

    def logout(self) -> httpx.Response:
        csrfToken, _ = self._pageCSRFToken()
        headers = {"referer": self.BASE_URL + "/home", "X-CSRF-TOKEN": csrfToken}
        cookies = {"X-CSRF-TOKEN": csrfToken}
        return self.client.delete(self.BASE_URL + "/session", headers=headers, cookies=cookies)

    def searchBeatmaps(self, params: BeatmapParamsOfficial):
        search_params = {}
        for k, v in params.items():
            if v is None:
                continue
            if isinstance(v, str):
                search_params[k] = v
            elif isinstance(v, Enum):
                search_params[k] = v.value
            elif isinstance(v, List):
                search_params[k] = [x.value for x in v]

        return self.client.get(self.BASE_URL + "/beatmaps/search", params=search_params)
