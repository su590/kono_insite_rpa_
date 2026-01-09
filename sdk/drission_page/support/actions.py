import random
import time
from typing import Union

from DrissionPage import ChromiumPage
from DrissionPage.common import Actions, Keys
from DrissionPage.items import ChromiumFrame, ChromiumTab


def typewrite(
        page: Union[ChromiumPage, ChromiumFrame, ChromiumTab],
        locator: str,
        text: str,
        backspace: int = 20
):
    """
    打字，即缓慢输入
    示例 typewrite(page, '#fm-login-id', account)
    :param page: ChromiumPage, 其实应该是ChromiumBase
    :param locator: str，其实tuple[str, str]/ChromeElement也行
    :param text:
    :param backspace:
    :return:
    """
    page.actions.click(locator).type(Keys.LEFT*backspace)
    page.actions.click(locator).type(Keys.BACKSPACE*backspace)
    actions: Actions = page.actions.click(locator)
    for c in text:
        actions.type(c)
        time.sleep(random.uniform(0.1, 0.2))
