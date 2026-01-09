import requests
from requests_toolbelt import MultipartEncoder

from sdk.feishu.auth import getTenantAcessToken


def getImgKey(imgPath: str) -> str:
    form: MultipartEncoder = MultipartEncoder({'image_type': 'message', 'image': (open(imgPath, 'rb'))})
    return requests.post(
        url="https://open.feishu.cn/open-apis/im/v1/images",
        headers={'Content-Type': form.content_type, 'Authorization': f'Bearer {getTenantAcessToken()}'},
        data=form
    ).json()['data']['image_key']
