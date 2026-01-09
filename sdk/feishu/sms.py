import dataclasses
from typing import Self

from sdk.feishu.image import getImgKey


@dataclasses.dataclass
class Sms:
    """
    飞书文本消息
    """
    contents: list = dataclasses.field(default_factory=list)
    row: int = -1
    col: int = -1

    def newLine(self) -> Self:
        """
        新增一行
        :return:
        """
        self.contents.append([])
        self.row += 1
        self.col = -1
        return self

    def setStyle(self, style: list[str], row: int = None, col: int = None) -> Self:
        """
        设置格式，默认当前行列
        :param col:
        :param row:
        :param style:
        :return:
        """
        if row is None:
            row = self.row
        if col is None:
            col = self.col
        self.contents[row][col]['style'] = style
        return self

    def addText(self, text: str, style: list[str] = None):
        """
        新增文本
        :param text:
        :param style:
        :return:
        """
        self.contents[self.row].append({"tag": "text", "text": text})
        self.col += 1
        if style:
            self.setStyle(style)
        return self

    # 添加超链接
    def addHref(self, href, text: str = None, style: list[str] = None) -> Self:
        """
        新增超链接
        :param href:
        :param text:
        :param style:
        :return:
        """
        self.contents[self.row].append({"tag": "a", "href": href, "text": href if text is None else text})
        self.col += 1
        if style:
            self.setStyle(style)
        return self

    def addAt(self, userId: str, userName: str = None, style: list[str] = None) -> Self:
        """
        新增 @
        :param userId:
        :param userName:
        :param style:
        :return:
        """
        userName = "xxx" if userName is None else userName
        self.contents[self.row].append({"tag": "at", "user_id": userId, "user_name": userName})
        self.col += 1
        if style:
            self.setStyle(style)
        return self

    def addImg(self, *, imgKey: str = None, imgPath: str = None) -> Self:
        """
        新增图片
        :param imgPath:
        :param imgKey:
        :return:
        """
        if (imgKey and imgPath) or (imgKey is None and imgPath is None):
            raise ValueError('imgKey和imgPath不能同时存在/不存在')
        if imgPath:
            imgKey: str = getImgKey(imgPath)
        self.contents[self.row].append({"tag": "img", "image_key": imgKey})
        self.col += 1
        return self

    def addMedia(self, fileKey: str, imageKey: str = None):
        """
        新增视频文件
        :param fileKey:
        :param imageKey:
        :return:
        """
        self.contents[self.row].append({"tag": "media", "file_key": fileKey})
        self.col += 1
        if imageKey:
            self.contents[self.row][self.col]['image_key'] = imageKey
        return self

    def addEmotion(self, emojiType: str):
        """
        新增表情
        :param emojiType:
        :return:
        """
        self.contents[self.row].append({"tag": "emotion", "emoji_type": emojiType})
        self.col += 1
        return self
