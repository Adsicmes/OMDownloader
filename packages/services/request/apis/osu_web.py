import re
from enum import Enum
from queue import Queue
from typing import Tuple, List

import httpx
import ujson
from lxml import etree

from packages.config import config
from packages.model.osu_web.beatmap import BeatmapParamsOfficial


class OsuWebApi:
    BASE_URL = "https://osu.ppy.sh"
    API_URL = BASE_URL + "/api/v2"

    def __init__(self, client: httpx.Client = None, timeout: int = int(config['ConnectionTimeout.ppy_sh'])):
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

    def searchBeatmaps(self, params: BeatmapParamsOfficial) -> httpx.Response:
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

        return self.client.get(self.BASE_URL + "/beatmapsets/search", params=search_params)

    def getUser(self, userId: int) -> Tuple[dict, httpx.Response]:
        url = self.BASE_URL + f"/users/{userId}"
        resp = self.client.get(url)

        if resp.status_code != 200:
            return {}, resp

        html = etree.HTML(resp.text)
        xpath_filter = "//div[contains(@class, 'js-react--profile-page') and contains(@class, 'osu-layout') and contains(@class, 'osu-layout--full')]"
        user_info: etree._Element = html.xpath(xpath_filter)[0]

        return ujson.loads(user_info.get("data-initial-data")), resp

    def downloadBeatmapset(self, sid: int, fp: str, nv: bool = False, q: Queue = None):
        """
        Download beatmapset

        "q" is a queue that transfer download status.
        The first int is total size, and many int follow it is the chunk that already downloaded.
        Finally, it will return True that indicates the download is done.
        """
        url = f'https://osu.ppy.sh/beatmapsets/{sid}/download'
        url = url + '?noVideo=1' if nv else url
        headers = {'referer': f'https://osu.ppy.sh/beatmapsets/{sid}/'}

        resp = self.client.get(url, follow_redirects=False, headers=headers)
        redirect_download_url = resp.headers['location']

        with self.client.stream("GET", redirect_download_url, headers=headers) as resp:
            resp.raise_for_status()

            q.put(int(resp.headers.get("content-length", 0))) if q is not None else None
            downloaded_size = 0

            with open(fp, "wb") as file:
                for chunk in resp.iter_raw():
                    file.write(chunk)
                    downloaded_size += len(chunk)

                    q.put(downloaded_size) if q is not None else None

                q.put(True) if q is not None else None
