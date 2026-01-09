# -*- coding: utf-8 -*-  
"""
@date : 2024/6/1
@author: 许伟淇
@describe: 

"""
import dataclasses
import json
import os

import requests


def getSession() -> requests.Session:
    with open(os.path.join(os.path.dirname(__file__), 'Cookies.json'), 'r', encoding='utf-8') as f:
        cookies: dict = json.load(f)
    session: requests.Session = requests.session()
    session.cookies.update(cookies)
    return session


@dataclasses.dataclass
class SessionController:

    def __post_init__(self):
        self.session: requests.Session = getSession()

    def saveCookies(self):
        with open(os.path.join(os.path.dirname(__file__), 'Cookies.json'), 'w', encoding='utf-8') as f:
            json.dump(self.session.cookies.get_dict(), f, ensure_ascii=False, indent=4)

    @property
    def cookies(self) -> dict[str, str]:
        return self.session.cookies.get_dict()
