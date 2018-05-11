#coding=utf-8
from random import randint
from datetime import datetime
from utils.captcha.captcha import create_captcha
from models.account.account_user_model import User
from libs.yun_tong_xun.yun_tong_xun_lib import sendTemplateSMS

def create_captcha_img(self, pre_code, code): #code是时间戳
    """01生成验证码，保存到redis"""
    if pre_code:
        self.conn.delete("captcha:%s" % pre_code)
    text, img = create_captcha()
    self.conn.setex("captcha:%s" % code, text.lower(), 60)  #三个参数分别表示：键，值，过期时间
    return img

def auth_captche(self,captcha_code,code):
    """02-1校验验证码"""
    if captcha_code == '':
        return {'status': False, 'msg': '请输入图形验证码'}
    elif self.conn.get("captcha:%s" %code) != captcha_code.lower():  #在redis中取值与输入框的验证码进行比较验证都转成小写
        return {'status': False, 'msg': '输入的图形验证码不正确'}
    return {"status":True, 'msg':'正确'}

def login(self, name,password):
    """02登录函数"""
    if name == '' or password == '':
        return {'status': False, 'msg': '请输入用户名或密码'}
    user = User.by_name(name)
    if user and user.auth_password(password):
        user.last_login = datetime.now()
        user.loginnum += 1    #修改了信息就要add然后commit
        self.db.add(user)
        self.db.commit()
        self.session.set('user_name',user.name)
        return {"status": True, 'msg': '登录成功'}
    return {'status': False, 'msg': '用户名或密码错误'}

def get_mobile_code_lib(self, mobile):
    """03发送手机短信"""
    if isinstance(mobile, unicode):
        mobile = mobile.encode('utf-8')
    mobile_code = randint(1000,9999)
    print '手机短信验证码是：', mobile_code
    self.conn.setex("mobile_code:%s" % mobile, mobile_code, 2000 )
    #这里测试时最好注释掉否则很快就把云通讯上的钱玩完了，就算把下面注释后也可以在Linux的后台也能看到的
    #sendTemplateSMS(mobile, [mobile_code, 30], 1)
    return {'status': True, 'msg': '验证码已经发送到%s, 请查收'%mobile}

def regist(self, name, mobile, mobile_captcha,
                        password1, password2, captcha, code,agree):
    """04注册函数
    一个是类型，一个边界值
    """
    if agree == "":
        return {'status':False, 'msg':"您没有点击同意条款"}
    if self.conn.get("captcha:%s" % code) != captcha.lower():
        return {'status': False, 'msg': '图形验证码不正确'}
    if self.conn.get("mobile_code:%s" % mobile) != mobile_captcha:
        return {'status': False, 'msg': '短信验证码不正确'}
    if password1 != password2:
        return {'status': False, 'msg': '两次密码不一致'}
    #存入数据库
    user = User.by_name(name)
    if user is not None:
        return {'status': False, 'msg': '用户已经存在'}
    user = User()
    user.name = name
    user.password = password2
    user.mobile = mobile
    self.db.add(user)
    self.db.commit()
    return {'status': True, 'msg': "注册成功"}




