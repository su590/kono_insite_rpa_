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
    url: str = 'https://login.taobao.com/member/login.jhtml?redirectURL=https%3A%2F%2Fad.alimama.com%2Findex.htm%3Fforward%3Dhttps%253A%252F%252Fad.alimama.com%252Fportal%252Fv2%252Freport%252FpromotionDataPage.htm&style=mini&full_redirect=true&newMini2=true&enup=0&qrlogin=1&keyLogin=true&sub=true&css_style=hudongcheng&disableQuickLogin=true'
    page.get(url)

    # todo 这边应该有一个相应的判断 判断已登录
    # # "客户信息查询"，存在即已登录
    # if page.wait.ele_displayed('c:.login-error-msg', timeout=3):
    #     # 原本的是get上面的url，测试一下获取下面的url 测试失败 2025/9/22 hcq
    #     page.get('https://ad.alimama.com/portal/v2/report/promotionDataPage.htm')
    #     # page.get('https://ad.alimama.com/portal/v2/report/item/list.htm')
    #     time.sleep(10)
    #     return page

    page.set.cookies.clear()
    page.get(url)
    page.wait.doc_loaded()
    e_username_input = 'c:[id="fm-login-id"]'
    page.wait.ele_displayed(e_username_input)
    typewrite(page, e_username_input, account.user)
    time.sleep(.2)
    typewrite(page, 'c:[id="fm-login-password"]', account.pwd)
    login_button: str = 'c:.password-login'
    page.ele(login_button).click()
    slot: str = 'c:[id="nocaptcha"]'
    if page.ele(slot):
        time.sleep(3)
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
    page.wait.ele_displayed('c:[id="widget-account"]')
    return page


if __name__ == '__main__':
    login(Account('kono洗护旗舰店:机器人实时汇报数据', 'Kono123456', 9288))
