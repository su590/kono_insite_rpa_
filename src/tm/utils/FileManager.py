#!/usr/bin/env python
# -*- coding: utf-8 -*-  
"""
@Date     : 2024-06-05
@Author   : xwq
@Desc     : 文件管理器

"""
import dataclasses
import json
import os
from datetime import datetime, timedelta


def getFilepath(folder: str, name: str, suffix: str) -> str:
    filepath = os.path.join(folder, f'{name}.{suffix}')
    if not os.path.exists(filepath):
        return filepath
    order: int = 1
    while os.path.exists(filepath):
        filepath = os.path.join(folder, f'{name}_{order}.{suffix}')
        order += 1
    return filepath


@dataclasses.dataclass
class FileManager:
    folder: str = 'D:/reptile/download/konotm'

    def __post_init__(self):
        if not (os.path.exists(self.folder) and os.path.isdir(self.folder)):
            os.makedirs(self.folder)
        self.format: str = '%Y%m%d%H'
        # 各保存项的文件名前缀
        self.realtime: str = '实时时段'
        self.midnight: str = '实时时段2355'
        self.yesterday: str = '昨日数据推送'

    def saveJson(self, data: dict, filename: str, dt: datetime = None) -> None:
        """
        保存爬虫结果
        :param data:
        :param filename: 保存文件名前缀
        :param dt: 保存位置，有效值为 年月日时
        :return:
        """
        # 默认值
        dt = dt or datetime.now()

        # 保存
        ymdh: str = dt.strftime(self.format)
        folder = os.path.join(self.folder, ymdh)
        if not (os.path.exists(folder) and os.path.isdir(folder)):
            os.makedirs(folder)
        filepath = getFilepath(folder, filename, 'json')
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4, default=str)

    def saveRealtimeData(self, data: dict, _filename: str = None) -> None:
        """
        保存实时时段的结果
        :param data:
        :param _filename: 保存文件名，调试/内部用
        :return:
        """
        self.saveJson(data, filename=_filename or self.realtime)

    def saveMidnightData(self, data: dict, _filename: str = None):
        """
        保存午夜23:55的额外时段结果
        :param data:
        :param _filename: 保存文件名，调试/内部用
        :return:
        """
        return self.saveJson(data, _filename or self.midnight)

    def saveYesterdayData(self, data: dict, _filename: str = None):
        """
        保存 昨日数据推送的结果
        :param data:
        :param _filename:
        :return:
        """
        return self.saveJson(data, _filename or self.yesterday)

    def getJson(self, dt: datetime, fileprefix: str) -> dict[str, str] | None:
        """
        获取已保存的时段结果，多个时取后缀最大者，即 实时时段_1 > 实时时段
        :param dt: 有效值为 年月日时
        :param fileprefix: 文件名前缀
        :return:
        """
        # 获取可能的文件名
        folder: str = os.path.join(self.folder, dt.strftime(self.format))
        if not os.path.isdir(folder):
            return None
        filenames: list[str] = [filename for filename in os.listdir(folder) if filename.startswith(fileprefix)]
        if not filenames:
            return None

        # 获取最大的文件名
        dstFilename: str = ''
        order: int = -1
        for filename in filenames:
            if not filename.split('.')[:-1]:
                continue
            infix: str = filename.split('.')[-2]
            thisOrder: int = int(infix[-1]) if infix[-1].isdigit() else 0
            if thisOrder > order:
                order = thisOrder
                dstFilename = filename

        # 读取
        dstFilepath: str = os.path.join(folder, dstFilename)
        with open(dstFilepath, 'r', encoding='utf-8') as f:
            data: dict[str, str] = json.load(f)

        return data

    def getRealtimeData(self, dt: datetime, _fileprefix: str = None) -> dict[str, str] | None:
        """
        获取已保存的时段结果，多个时取后缀最大者，即 实时时段_1 > 实时时段
        :param dt: 有效值为 年月日时
        :param _fileprefix: 时段结果的文件名前缀，调试/内部用
        :return:
        """
        return self.getJson(dt, _fileprefix or self.realtime)

    def getLastHourRealtimeData(self) -> dict[str, str] | None:
        """
        获取上个时段的时段结果
        :return:
        """
        lastHour: datetime = datetime.now() - timedelta(hours=1)
        return self.getRealtimeData(lastHour)

    def getLastMidnightRealtimeData(self) -> dict[str, str] | None:
        """
        获取昨晚23:55的时段结果
        :return:
        """
        lastMidnight: datetime = datetime.now() - timedelta(days=1)
        lastMidnight = lastMidnight.replace(hour=23, minute=55, second=55, microsecond=0)
        return self.getRealtimeData(lastMidnight, self.midnight)

    def getYesterdayData(self, dt: datetime, _fileprefix: str = None) -> dict[str, str] | None:
        """
        获取指定日期下的"昨日数据推送"结果
        :param dt:
        :param _fileprefix:
        :return:
        """
        return self.getRealtimeData(dt or datetime.now(), _fileprefix or self.yesterday)
