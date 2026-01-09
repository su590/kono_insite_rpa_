# -*- encoding: utf-8 -*-
"""
2024-04-24 by xwq
@DESC: 

"""
import datetime
import decimal
import json

import requests


def _charge(jsn: dict) -> decimal.Decimal:
	"""
	花费
	:param jsn:
	"""
	try:
		return decimal.Decimal(jsn['data']['list'][0]['charge'])
	except (KeyError, IndexError):
		return decimal.Decimal(0)


def _alipayInshopAmt(jsn: dict) -> decimal.Decimal:
	"""
	总成交金额
	:param jsn:
	"""
	try:
		return decimal.Decimal(str(jsn['data']['list'][0]['alipayInshopAmt']))
	except (KeyError, IndexError):
		return decimal.Decimal(0)


def _alipayDirAmt(jsn: dict) -> decimal.Decimal:
	"""
	直接成交金额
	:param jsn:
	"""
	try:
		return decimal.Decimal(jsn['data']['list'][0]['alipayDirAmt'])
	except (KeyError, IndexError):
		return decimal.Decimal(0)


def _roi(jsn: dict) -> decimal.Decimal:
	"""
	roi
	:param jsn:
	"""
	try:
		return decimal.Decimal(jsn['data']['list'][0]['roi'])
	except (KeyError, IndexError):
		return decimal.Decimal(0)


def _commonRequest(
		session: requests.Session,
		csrfId: str,
		url: str,
		params: dict,
		headers: dict,
		payload: dict,
		date: datetime.date,
) -> dict[str, decimal.Decimal]:
	"""
	{花费: x, 总成交金额: y, 直接成交金额: z, }
	"""
	params['csrfId'] = csrfId
	payload['csrfId'] = csrfId
	payload['startTime'] = date.strftime('%Y-%m-%d')
	payload['endTime'] = date.strftime('%Y-%m-%d')
	if date == datetime.date.today():
		payload['fromRealTime'] = True
	else:
		payload['fromRealTime'] = False
	query: requests.Response = session.post(
		url=url,
		params=params,
		headers=headers,
		data=json.dumps(payload)
	)
	data: dict = query.json()
	result: dict[str, decimal.Decimal] = {
		'花费': _charge(data),
		'总成交金额': _alipayInshopAmt(data),
		'直接成交金额': _alipayDirAmt(data),
		'ROI': _roi(data)
	}
	return result
