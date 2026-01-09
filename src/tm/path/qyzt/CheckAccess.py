# -*- coding: utf-8 -*-  
"""
@date : 2024/6/1
@author: 许伟淇
@describe: 

"""
import json
import os
import time

import requests

from src.tm.path.qyzt.SessionController import getSession


def getCsrfId(session: requests.Session = None) -> str:
    if session is None:
        session = getSession()

    with open(os.path.join(os.path.dirname(__file__), 'resource', 'CheckAccessPayload.json'), 'r', encoding='utf-8') as f:
        payload: dict = json.load(f)
    with open(os.path.join(os.path.dirname(__file__), 'resource', 'CheckAccessHeaders.json'), 'r', encoding='utf-8') as f:
        headers: dict = json.load(f)
    payload['timeStr'] = str(int(time.time() * 1000))
    csrfId: str = session.post(
        url='https://ud.alimama.com/member/checkAccess.json',
        headers=headers,
        data=payload
    ).json()['data']['accessInfo']['csrfId']

    return csrfId
