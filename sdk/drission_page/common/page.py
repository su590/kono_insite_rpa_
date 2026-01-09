import configparser
import os.path

from DrissionPage import ChromiumOptions
from DrissionPage import ChromiumPage

from sdk.envs import get_chrome_path


def _get_user_data_path(port: int) -> str:
    """
    取该端口下的浏览器数据存放地址，无则新建
    :param port:
    :return:
    """
    config: configparser.ConfigParser = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resource', 'config.ini'))
    user_data_path: str = os.path.join(config.get('paths', 'ChromeProfile'), f'{port}')
    if not os.path.exists(user_data_path):
        os.makedirs(user_data_path)
    return user_data_path


def _get_download_path() -> str:
    """
    获取浏览器默认下载地址
    :return:
    """
    config: configparser.ConfigParser = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'resource', 'config.ini'))
    return config.get('paths', 'download')


def default_co(
        port: int = 9222,
        ip: str = '127.0.0.1',
) -> ChromiumOptions:
    """
    使用默认配置 + 通过代码化显式配置，方便调控、迁移
    :param ip:
    :param port:
    :return:
    """
    co: ChromiumOptions = ChromiumOptions(read_file=False)

    # ------------------设置浏览器启动时的窗口表现-------------------
    co.set_argument('--start-maximized')  # 窗口最大化
    co.set_argument('--no-default-browser-check')  # 禁用默认浏览器检查
    co.set_argument('--disable-suggestions-ui')  # 禁用地址栏的建议功能
    co.set_argument('--no-first-run')  # 禁用“首次运行”的欢迎页面和配置向导
    co.set_argument('--disable-infobars')  # 禁用浏览器的提示信息栏，如提示用户保存密码
    co.set_argument('--disable-popup-blocking')  # 禁用浏览器的弹窗阻止功能
    co.set_argument('--hide-crash-restore-bubble')  # 隐藏崩溃恢复提示气泡
    co.set_argument(
        '--disable-features=PrivacySandboxSettings4')  # 禁用隐私沙箱（Privacy Sandbox）设置中的某个特定功能，即 "PrivacySandboxSettings4"

    # --------------------设置浏览器的运行表现--------------------
    co.set_paths(
        browser_path=get_chrome_path(),  # 自动查找当前用户下的chrome.exe地址，并设置
        address=f'{ip}:{port}',  # 设置浏览器地址，如 127.0.0.1:9222
        download_path=_get_download_path(),  # 设置默认下载地址，如 D:/reptile/download
        user_data_path=_get_user_data_path(port),  # 设置用户文件夹路径，如 D:/reptile/chromes/9222
    )

    return co


def get_chromium_page(port: int = 9222, *, co: ChromiumOptions = None) -> ChromiumPage:
    """
    返回指定端口的浏览器，
    :param port:
    :param co:
    :return:
    """
    if co is None:
        co = default_co(port)
    page: ChromiumPage = ChromiumPage(addr_or_opts=co)
    return page
