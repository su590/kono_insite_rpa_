import requests

from sdk.decrypt import aes
from sdk.feishu import APP_ID, APP_SECRET


def getTenantAcessToken() -> str:
    return requests.post(
        url="https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
        data={'app_id': aes(APP_ID), 'app_secret': aes(APP_SECRET)},
    ).json()['tenant_access_token']
