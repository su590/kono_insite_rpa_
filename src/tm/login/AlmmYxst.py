# -*- coding: utf-8 -*-  
"""
@Date     : 2024-06-27
@Author   : xwq
@Desc     : <None>

"""
import time

from DrissionPage._configs.chromium_options import ChromiumOptions
from DrissionPage._pages.chromium_page import ChromiumPage

from sdk.drission_page.common.page import get_chromium_page
from sdk.drission_page.support.actions import typewrite
from src import logger
from src.tm.utils.Accounts import Account


def login(account: Account):
    """
    阿里妈妈/营销生态平台 登录入口
    :param account:
    :return:
    """
    # 浏览器
    logger.info(f'阿里妈妈/营销生态 > 账密: {account.user} | {account.pwd}')
    if account.port:
        logger.info(f'阿里妈妈/营销生态 > 指定端口: {account.port}')
        page: ChromiumPage = get_chromium_page(account.port)
    else:
        logger.info('阿里妈妈/营销生态 > 随机端口')
        co: ChromiumOptions = ChromiumOptions()
        co.auto_port()
        co.set_argument('--start-maximized')
        # co.headless()
        page: ChromiumPage = ChromiumPage(co)

    # 登录 阿里妈妈营销生态平台
    url: str = 'https://sem.taobao.com/agentCustomManage'
    page.get(url)

    # "客户信息查询"，存在即已登录
    if page.wait.ele_displayed('c:.mux-card-title-body', timeout=3):
        return page

    page.set.cookies.clear()
    page.get(url)
    page.wait.doc_loaded()
    e_username_input = 'c:[name="fm-login-id"]'
    page.ele(e_username_input)
    typewrite(page, e_username_input, account.user)
    time.sleep(.2)
    typewrite(page, 'c:[name="fm-login-password"]', account.pwd)
    login_button: str = 'c:.password-login'
    page.ele(login_button).click()
    slot: str = 'c:[id="nocaptcha"]'
    if page.ele(slot):
        width: float = page.ele(slot).rect.size[0]
        # height: float = page.ele(slot).rect.size[1]
        location: tuple[float, float] = page.ele(slot).rect.location
        hold_point: tuple[int, int] = (int(location[0] + 5), int(location[1] + 5))
        action = page.actions.move_to(hold_point).hold()
        action.move_to((hold_point[0] + width // 2, hold_point[1] + 5))
        action.move_to((hold_point[0] + width // 3, hold_point[1] - 3))
        action.move_to((hold_point[0] + int(width), hold_point[1]))
        page.ele(login_button).click()
        time.sleep(.5)
    time.sleep(.5)
    ENTRY: str = 'x://button[text()="进入工作台"]'
    if page.wait.ele_displayed(ENTRY):
        page.ele(ENTRY).click()
    page.wait.ele_displayed('c:.f14')
    time.sleep(.5)

    return page


if __name__ == '__main__':
    login(Account('19902276604', 'FDKONO123456', 9229))
    pass
