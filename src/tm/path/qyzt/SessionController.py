# -*- coding: utf-8 -*-  
"""
@date : 2024/6/1
@author: 许伟淇
@describe: 

"""
import json
import os

import requests


def getSession() -> requests.Session:
    with open(os.path.join(os.path.dirname(__file__), 'resource', 'Cookies.json'), 'r', encoding='utf-8') as f:
        cookies: dict = json.load(f)
    session: requests.Session = requests.session()
    session.cookies.update(cookies)
    return session
