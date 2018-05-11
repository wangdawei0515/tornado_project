#coding=utf-8
#放处理器
from handlers.base.base_handler import BaseHandler
from libs.account import account_libs

class ProfileHandler(BaseHandler):
    """00用户信息函数"""
    def get(self):
        self.render('account/account_profile.html', message=None)


class ProfileEditHandler(BaseHandler):
    """01编辑用户信息"""
    def get(self):
        self.render('account/account_edit.html')

    def post(self):
        name = self.get_argument('name', '')
        password = self.get_argument('password', '')
        print name, password
        result = account_libs.edit_profile(self, name, password)
        if result['status'] is False:
            return self.render('account/account_profile.html', message=result['msg'])
        return self.render('account/account_profile.html', message=result['msg'])


class ProfileModifyEmailHandler(BaseHandler):
    """02修改邮箱"""
    def get(self):
        self.render('account/account_send_email.html')

    def post(self):
        email = self.get_argument('email', '')#获取需要验证的邮箱号
        print u'验证码已发送到邮箱:%s，请在5分钟内完成验证'%email
        result = account_libs.send_email_libs(self, email)
        if result['status'] is True:
            return self.write(result['msg'])
        return self.write(result['msg'])


class ProfileAuthEmailHandler(BaseHandler):
    """03验证邮箱验证码"""
    def get(self):
        email_code = self.get_argument('code', '')
        email = self.get_argument('email', '')
        u = self.get_argument('user_id', '')
        result = account_libs.auth_email_libs(self, email_code, email, u)
        if result['status'] is True:
            return self.redirect('/account/user_edit')
        return self.write(result['msg'])


class ProfileAddAvaterHandler(BaseHandler):
    """04验证邮箱验证码"""
    def post(self):
        avatar_data = self.request.files.get('user_avatar', '')
        #[{'body': 'abcdefg', 'content_type': u'text/plain', 'filename': u'111.txt'}]
        result = account_libs.add_avatar_lib(self, avatar_data[0]['body'])
        if result['status'] is True:
            return self.redirect('/account/user_edit')
        return self.write(result['msg'])







