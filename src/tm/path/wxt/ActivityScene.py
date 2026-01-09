# -*- encoding: utf-8 -*-
"""
2024-04-24 by xwq
@DESC: 活动场景

"""
import datetime
import decimal
import json
import os

import requests

from src.tm.path.wxt._CommonRequest import _commonRequest


def getActivityScene(
		session: requests.Session,
		csrfId: str,
		date: datetime.date,
) -> dict[str, decimal.Decimal]:
	"""
	按日期获取 活动场景 数据
	:param session:
	:param csrfId:
	:param date:
	:return:
	"""
	dirname: str = os.path.dirname(os.path.abspath(__file__))
	with open(os.path.join(dirname, 'params', 'ActivityScene.json'), 'r', encoding='utf-8') as f:
		params: dict[str, str] = json.load(f)
	with open(os.path.join(dirname, 'headers', 'ActivityScene.json'), 'r', encoding='utf-8') as f:
		headers: dict[str, str] = json.load(f)
	with open(os.path.join(dirname, 'payload', 'ActivityScene.json'), 'r', encoding='utf-8') as f:
		payload: dict[str, str] = json.load(f)

	return _commonRequest(
		session=session,
		csrfId=csrfId,
		url='https://one.alimama.com/report/query.json',
		params=params,
		headers=headers,
		payload=payload,
		date=date,
	)
