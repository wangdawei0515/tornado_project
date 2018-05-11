#!/usr/bin/env python
#coding=utf-8
# Name:        auto
# Created:
# __author__ = "wangdw"
# Email: wangdawei_@outlook.com
#------------------------------


from models.permission.permission_model import Role, Permission, Menu, Handler
from models.account.account_user_model import User
from libs.flash.flash_lib import flash

def permission_manager_list_lib(self):
    """01权限管理页面函数"""
    roles = Role.all()
    permissions = Permission.all()
    menus = Menu.all()
    handlers = Handler.all()
    users = User.all()

    return roles, permissions, menus, handlers, users

def add_role_lib(self, name):
    """02添加角色函数"""
    role= Role.by_name(name)
    if role is not None:
        flash(self, "角色已经存在，添加失败", "error")
        return
    role = Role()
    role.name = name
    self.db.add(role)
    self.db.commit()
    flash(self, "角色添加成功", "success")

def del_role_lib(self, roleid):
    """03删除角色"""
    role= Role.by_id(roleid)
    if role is None:
        flash(self, "角色删除失败", "error")
        return
    self.db.delete(role)
    self.db.commit()
    flash(self, "角色删除成功", "success")

def add_permission_lib(self, name, strcode):
    """04添加权限"""
    permission= Permission.by_name(name)
    if permission is not None:
        flash(self, "权限已存在，添加失败", "error")
        return
    permission = Permission()
    permission.name = name
    permission.strcode = strcode
    self.db.add(permission)
    self.db.commit()
    flash(self, "权限添加成功", "success")

def del_permission_lib(self,perid):
    """05删除权限函数"""
    per = Permission.by_id(perid)
    if per is None:
        flash(self, "此权限不存在，删除失败", "error")
        return
    self.db.delete(per)
    self.db.commit()
    flash(self, "权限删除成功", "success")

def add_menu_lib(self, name, permissionid):
    """06为菜单添加权限函数"""
    permission = Permission.by_id(permissionid)
    if name == "" or permissionid == "":
        flash(self, "菜单名称或权限ID为空了，所以添加失败", "error")
        return
    menu = Menu.by_name(name)#注意
    if menu is not None:
        flash(self, "菜单名称已存在，添加失败", "error")
        return
    menu = Menu()
    menu.name = name
    menu.permission = permission #问题 可不可以
    #menu.p_id = permissionid    ##这句话和上面这句效果一摸一样的，所以上面的写了这里就注释掉
    self.db.add(menu)
    self.db.commit()
    flash(self, "菜单权限，添加成功", "success")

def del_menu_lib(self, menuid):
    """07删除菜单"""
    menu = Menu.by_id(menuid)
    if menu is None:
        flash(self, "菜单权限，删除失败", "error")
        return
    self.db.delete(menu)
    self.db.commit()
    flash(self, "菜单权限，删除成功", "success")

def add_handler_lib(self, name, permissionid):
    """08为视图添加权限函数"""
    permission = Permission.by_id(permissionid)
    if permission is None:
        flash(self, "处理器权限，添加失败", "error")
        return
    hanlder = Handler.by_name(name)  # 注意
    if hanlder is None:
        hanlder = Handler()
    hanlder.name = name
    hanlder.permission = permission
    self.db.add(hanlder)
    self.db.commit()
    flash(self, "处理器权限，添加成功", "success")

def del_handler_lib(self,handlerid):
    """09删除视图函数"""
    handler = Handler.by_id(handlerid)
    if handler is None:
        flash(self, "处理器权限，删除失败", "error")
        return
    self.db.delete(handler)
    self.db.commit()
    flash(self, "处理器权限，删除成功", "success")

def add_user_role_lib(self, userid, roleid):
    """10为用户添加角色"""
    user = User.by_id(userid)
    role = Role.by_id(roleid)
    if user is None or role is None:
        flash(self, "为用户添加角色失败", "error")
        return
    user.roles.append(role) #这行的意思是：往多对多关系表中插入数据
    #role.users.append(user)
    self.db.add(user)
    self.db.commit()
    flash(self, "为用户添加角色成功", "success")

def add_role_permission_lib(self, permissionid, roleid):
    """11为角色添加权限"""
    permission = Permission.by_id(permissionid)
    role = Role.by_id(roleid)
    if permission is None or role is None:
        flash(self, "为角色添加权限失败", "error")
        return
    permission.roles.append(role) #多对多关系添加
    self.db.add(permission)
    self.db.commit()
    flash(self, "为角色添加权限成功", "success")

def del_user_role_lib(self, userid,roleid):
    """12删除用户的角色"""
    user = User.by_id(userid)
    role = Role.by_id(roleid)
    user.roles.remove(role)
    self.db.add(user)
    self.db.commit()
    flash(self, '用户角色删除成功', 'success')


def del_user_allrole_lib(self, userid):
    """13删除用户的所有角色"""
    user = User.by_id(userid)
    user.roles = []
    self.db.add(user)
    self.db.commit()
    flash(self, '用户角色删除成功', 'success')
