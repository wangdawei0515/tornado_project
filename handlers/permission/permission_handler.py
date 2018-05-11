#!/usr/bin/env python
#coding=utf-8
# Name:        auto
# Created:
# __author__ = "wangdw"
# Email: wangdawei_@outlook.com
#------------------------------

from handlers.base.base_handler import BaseHandler
from libs.permission import permission_libs
from libs.permission.permission_auth.permission_interface_libs import handler_permission




class ManageHandler(BaseHandler):
    """01权限管理页面函数"""
    def get(self):
        roles, permissions, menus, handlers, users = permission_libs.permission_manager_list_lib(self)
        kw = {
            'roles': roles,
            'permissions': permissions,
            'menus': menus,
            'handlers': handlers,
            'users': users,
            'dev_users': [],

        }
        return self.render('permission/permission_list.html', **kw)


class AddRoleHandler(BaseHandler):
    """02添加角色函数"""
    @handler_permission('AddRoleHandler','handler')
    def post(self):
        name = self.get_argument('name', '')
        permission_libs.add_role_lib(self, name)
        self.redirect('/permission/manage_list')


class DelRoleHandler(BaseHandler):
    """03删除角色"""
    @handler_permission('DelRoleHandler', 'handler')  #这里的DelRoleHandler名称要和浏览器中为试图添加权限中的试图名称要一致
    def get(self):
        roleid = self.get_argument('id', '')
        permission_libs.del_role_lib(self, roleid)
        self.redirect('/permission/manage_list')


class AddPermissionHandler(BaseHandler):
    """04添加权限"""
    @handler_permission('AddPermissionHandler', 'handler')
    def post(self):
        name = self.get_argument('name', '')
        strcode = self.get_argument('strcode', '')
        permission_libs.add_permission_lib(self, name, strcode)
        self.redirect('/permission/manage_list')

class DelPermissionHandler(BaseHandler):
    """05删除权限函数"""
    @handler_permission('DelPermissionHandler', 'handler')
    def get(self):
        perid = self.get_argument('id', '')
        permission_libs.del_permission_lib(self, perid)
        self.redirect('/permission/manage_list')



class AddMenuHandler(BaseHandler):
    """06为菜单添加权限函数"""
    @handler_permission('AddMenuHandler', 'handler')
    def post(self):
        name = self.get_argument('name', '')
        permissionid = self.get_argument('permissionid', '')
        permission_libs.add_menu_lib(self, name, permissionid)
        self.redirect('/permission/manage_list')


class DelMenuHandler(BaseHandler):
    """07删除菜单"""
    @handler_permission('DelMenuHandler', 'handler')
    def get(self):
        menuid = self.get_argument('menuid', '')
        permission_libs.del_menu_lib(self, menuid)
        self.redirect('/permission/manage_list')


class AddHandlerHandler(BaseHandler):
    """08为视图添加权限函数"""
    @handler_permission('AddHandler', 'handler')
    def post(self):
        name = self.get_argument('name', '')
        permissionid = self.get_argument('permissionid', '')
        permission_libs.add_handler_lib(self, name, permissionid)
        self.redirect('/permission/manage_list')


class DelHandlerHandler(BaseHandler):
    """09删除视图函数"""
    @handler_permission('DelHandler', 'handler')
    def get(self):
        handlerid = self.get_argument('handlerid', '')
        permission_libs.del_handler_lib(self, handlerid)
        self.redirect('/permission/manage_list')



class AddUserRoleHandler(BaseHandler):
    """10为用户添加角色"""
    # @handler_permission('UserRoleHandler', 'handler')
    def post(self):
        userid = self.get_argument('userid', '')
        roleid = self.get_argument('roleid', '')
        permission_libs.add_user_role_lib(self, userid, roleid)
        self.redirect('/permission/manage_list')



class AddRolePermissionHandler(BaseHandler):
    """11为角色添加权限"""
    @handler_permission('RolePermissionHandler', 'handler')
    def post(self):
        permissionid = self.get_argument('permissionid', '')
        roleid = self.get_argument('roleid', '')
        permission_libs.add_role_permission_lib(self, permissionid, roleid)
        self.redirect('/permission/manage_list')




class DelUserRoleHandler(BaseHandler):
    """12删除用户的角色"""
    @handler_permission('DelUserRoleHandler', 'handler')
    def get(self):
        userid = self.get_argument('userid', '')
        roleid = self.get_argument('roleid', '')
        permission_libs.del_user_role_lib(self, userid, roleid)
        self.redirect('/permission/manage_list')



class DelUserAllRoleHandler(BaseHandler):
    """13删除用户的所有角色"""
    @handler_permission('DelAllUserRoleHandler', 'handler')
    def get(self):
        userid = self.get_argument('userid', '')
        permission_libs.del_user_allrole_lib(self, userid)
        self.redirect('/permission/manage_list')

