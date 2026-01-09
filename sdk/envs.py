import winreg


def get_chrome_path() -> str:
    with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe") as key:
        chrome_path: str = winreg.QueryValue(key, None)
    return chrome_path
