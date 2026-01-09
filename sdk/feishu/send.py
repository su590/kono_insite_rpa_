import enum
import json

import requests

from sdk.feishu.auth import getTenantAcessToken


class ReceiveType(enum.Enum):
    OPEN_ID = 'open_id'
    USER_ID = 'user_id'
    UNION_ID = 'union_id'
    EMAIL_ID = 'email'
    CHAT_ID = 'chat_id'


def sendContents(
        receive_id: str,
        contents: list,
        title: str = "",
        receive_id_type: ReceiveType = ReceiveType.OPEN_ID
) -> requests.Response:
    """
    发送富文本
    :param receive_id:
    :param contents:
    :param title:
    :param receive_id_type:
    :return:
    """
    return requests.post(
        url=f"https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type={receive_id_type.value}",
        headers={
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + getTenantAcessToken()
        },
        data=json.dumps({
            "receive_id": receive_id,
            "msg_type": "post",
            "content": json.dumps({"zh_cn": {"title": title, "content": contents}})
        })
    )
