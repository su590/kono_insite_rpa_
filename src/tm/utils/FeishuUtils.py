# -*- coding: utf-8 -*-  
"""
@Date     : 2024-09-07
@Author   : xwq
@Desc     : <None>

"""
from sdk.feishu.CustomRobotSend import send_text, read_wps_data
from sdk.feishu.send import sendContents, ReceiveType
from sdk.feishu.sms import Sms


def sendTextToNotificationGroup(
        content: str,
):
    """
    发送文本消息到飞书通知群
    Args:
        content:

    Returns:

    """
    # 短信填充
    sms: Sms = Sms()
    for line in content.split('\n'):
        sms.newLine().addText(line)
    contents = sms.contents
    # sendContents('ou_2577711c6941029757e59e566b1bd1f1', contents, receive_id_type=ReceiveType.OPEN_ID)
    # sendContents('oc_2d433fc16ca568cd24f531bf0e1ec9d1', contents, receive_id_type=ReceiveType.CHAT_ID)
    # print(contents)

    send_text(contents)
    # read_wps_data(contents)
