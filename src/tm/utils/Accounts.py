#!/usr/bin/env python
# -*- coding: utf-8 -*-  
"""
@Date     : 2024-06-05
@Author   : xwq
@Desc     : 读取账号

"""
import dataclasses
import os.path

import yaml


@dataclasses.dataclass(frozen=True)
class Account:
    user: str
    pwd: str
    port: int | None = None


def getAccount(key: str) -> Account:
    """
    获取目标账号
    用例：getAccount('sej')
    :param key:
    :return:
    """
    parent_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    with open(os.path.join(parent_dir, 'resources', 'Accounts.yml'), 'r', encoding='utf-8') as f:
        accounts: dict = yaml.safe_load(f)
    user: str = accounts[key]['user']
    pwd: str = accounts[key]['pwd']
    if accounts[key].get('port'):
        port: int = int(accounts[key]['port'])
    else:
        port: None = None
    return Account(user=str(user), pwd=str(pwd), port=port)
