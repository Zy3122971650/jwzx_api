import hashlib
from common import *
import re


class Login():
    def __init__(self) -> None:
        super().__init__()

        self.LOGIN_URL = 'http://202.199.224.119:8080/eams/loginExt.action'
        self.HOME_URL = 'http://202.199.224.119:8080/eams/homeExt.action'

    def login(self, username, passwd) -> None:
        html = get_context(self.LOGIN_URL)
        salt = self.__parse_key_slat(html)
        salt_password = salt+passwd

        password = self.__sha1_password(salt_password)
        post_data = {
            'username': username,
            'password': password,
            'session_locale': 'zh_CN'
        }
        post_context(self.LOGIN_URL, post_data)
        get_context(self.HOME_URL)

    def keep_login(self):
        get_context(self.HOME_URL)

    def __parse_key_slat(self, html) -> str:
        rex = "CryptoJS.SHA1\('(\S*)'"
        salt = re.compile(rex).search(html).group(1)
        return salt

    def __sha1_password(self, password: str):
        """[summary]

        Args:
            password (str): [description]

        Returns:
            [type]: [description]
        """
        m = hashlib.sha1()
        m.update(password.encode())
        return m.hexdigest()
