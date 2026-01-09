#!/usr/bin/env python
# -*- coding: utf-8 -*-  
"""
@Date     : 2024-06-05
@Author   : xwq
@Desc     : <None>

"""
import json
import os

import requests


def getCsrfId(session: requests.Session) -> str:
    with open(os.path.join(os.path.dirname(__file__), 'payload', 'CheckAccess.json'), 'r', encoding='utf-8') as f:
        payload: dict = json.load(f)
    with open(os.path.join(os.path.dirname(__file__), 'headers', 'CheckAccess.json'), 'r', encoding='utf-8') as f:
        headers: dict = json.load(f)

    checkAccess: requests.Response = session.post(
        url='https://one.alimama.com/member/checkAccess.json?bizCode=universalBP',
        headers=headers,
        data=json.dumps(payload)
    )
    csrfId: str = checkAccess.json()['data']['accessInfo']['csrfId']
    return csrfId
