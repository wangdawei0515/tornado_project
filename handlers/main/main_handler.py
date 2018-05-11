#coding=utf-8

from handlers.base.base_handler import BaseHandler


class MainHandler(BaseHandler):
    def get(self):
        self.redirect('/auth/user_login')


