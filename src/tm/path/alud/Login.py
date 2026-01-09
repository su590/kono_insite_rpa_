import time

from DrissionPage import ChromiumPage

from src.tm.login.Alud import login
from src.tm.utils.Accounts import Account


def getCookies(account: Account) -> dict[str, str]:
    page: ChromiumPage = login(account=account)
    effect: str = 'x://div[contains(@id, "toggle_mx")]//span[text()="效果投放"]'
    if page.ele(effect):
        page(effect).click()
        page('c:[title="进入效果首页"]').click()
    page('c:a[href="#!/report2/index?menu=brand&directMediaId="]').click()
    page('c:[title="项目报表"]').click()
    page('x://div[contains(text(), "今日")]').click()
    time.sleep(1)
    cookies: dict[str, str] = {
        d['name']: d['value']
        for d in page.cookies()
    }
    page.close()
    return cookies
