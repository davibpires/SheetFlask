class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = "z6Ct_d2Wy0ZcZZVUYD3beI5ZCSsFrR6-f3ZDyn_MW00"
    AUTHORIZED_USERS = ["lucas@sheetgo.com", "mauricio@sheetgo.com", "rafael@sheetgo.com"]


class TestConfig(BaseConfig):
    DEBUG = True
    TESTING = True
    WTF_CSRF_ENABLED = False
