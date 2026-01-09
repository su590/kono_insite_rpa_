# -*- encoding: utf-8 -*-
"""
2024-04-23 by xwq
@DESC: 

"""
import datetime
import decimal
import json
import os

import requests

from src.tm.path.wxt._CommonRequest import _commonRequest


def getKwAds(
		session: requests.Session,
		csrfId: str,
		date: datetime.date,
) -> dict[str, decimal.Decimal]:
	dirname: str = os.path.dirname(os.path.abspath(__file__))
	with open(os.path.join(dirname, 'params', 'KwAds.json'), 'r', encoding='utf-8') as f:
		params: dict[str, str] = json.load(f)
	with open(os.path.join(dirname, 'headers', 'KwAds.json'), 'r', encoding='utf-8') as f:
		headers: dict[str, str] = json.load(f)
	with open(os.path.join(dirname, 'payload', 'KwAds.json'), 'r', encoding='utf-8') as f:
		payload: dict[str, str] = json.load(f)

	return _commonRequest(
		session=session,
		csrfId=csrfId,
		url='https://one.alimama.com/report/query.json',
		params=params,
		headers=headers,
		payload=payload,
		date=date
	)
