#coding=utf-8
from handlers.base.base_handler import BaseHandler
from libs.account import account_auth_libs


class CaptchaHandler(BaseHandler):
    """01生成验证码"""
    def get(self):
        pre_code = self.get_argument('pre_code', '')
        code  = self.get_argument('code', '')
        img = account_auth_libs.create_captcha_img(self,pre_code, code)
        self.set_header("Content-Type", "image/jpg")
        self.write(img)


class LoginHandler(BaseHandler):
    """02登录函数"""
    def get(self):
        self.render('account/auth_login.html')

    def post(self):
        name = self.get_argument("name","")
        password = self.get_argument("password","")
        code = self.get_argument("code","") #在redis中取数据对比
        captcha_code = self.get_argument("captcha","")
        print name,password,code,captcha_code
        result = account_auth_libs.auth_captche(self,captcha_code,code)
        if result['status'] is False:
            return self.write({'status':400, 'msg':result['msg']})
        result = account_auth_libs.login(self,name,password)
        if result['status'] is True:
            return self.write({'status': 200, 'msg': result['msg']})
            # return self.redirect('/auth/user_login')
        return self.write({'status': 400, 'msg': result['msg']})


class LogoutHandler(BaseHandler):
    """03退出登陆函数"""
    def get(self):
        # self.render('account/auth_login.html')  #打开这个页面
        return self.redirect('/auth/user_login')  #路由跳转到/auth/user_login  ，两种方式都可以


class MobileCodeHandler(BaseHandler):
    """04发送手机短信"""
    def post(self):
        mobile = self.get_argument('mobile', '')
        code = self.get_argument('code', '')
        captcha = self.get_argument('captcha', '')
        print mobile, code, captcha
        result = account_auth_libs.auth_captche(self, captcha, code)
        if result['status'] is False:
            return self.write({'status': 400, 'msg': result['msg']})
        result = account_auth_libs.get_mobile_code_lib(self, mobile)
        if result['status'] is True:
            return self.write({'status': 200, 'msg': result['msg']})
        return self.write({'status': 400, 'msg': result['msg']})


class RegistHandler(BaseHandler):
    """05注册函数"""
    def get(self):
        self.render('account/auth_regist.html',message='注册')

    def post(self): #form表单请求 不是ajax
        mobile = self.get_argument('mobile', '')
        mobile_captcha = self.get_argument('mobile_captcha', '')
        code = self.get_argument('code', '')
        name = self.get_argument('name', '')
        password1 = self.get_argument('password1', '')
        password2 = self.get_argument('password2', '')
        captcha = self.get_argument('captcha', '')
        agree = self.get_argument('agree', '')
        result = account_auth_libs.auth_captche(self, captcha, code)
        if result['status'] is False:
            return self.render('account/auth_regist.html', message = result['msg'])
        #用户注册
        result = account_auth_libs.regist(self, name, mobile,
                                          mobile_captcha, password1, password2, captcha, code,agree)
        if result['status'] is True:
            return self.redirect('/auth/user_login')
        return self.render('account/auth_regist.html', message = result['msg'])




