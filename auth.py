# coding=utf-8


class Auth:

    logon_user = ''

    @classmethod
    def set_logon_user(cls, user_id):
        cls.logon_user = user_id
        return cls.logon_user

    @classmethod
    def get_logon_user(cls):
        return cls.logon_user
