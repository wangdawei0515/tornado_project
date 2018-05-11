#coding=utf-8

from models.account.account_user_model import User
from models.permission import permission_model
from libs.db.dbsession import dbSession


pp = [
    ('添加角色', 'add_role'),
    ('删除角色', 'del_role'),
    ('用户添加角色', 'add_user_role'),
    ('用户删除角色', 'del_user_role'),
    ('角色添加权限', 'add_role_per'),
    ('角色删除权限', 'del_role_per'),
    ('权限管理菜单', 'admin_menu'),
    ('添加权限', 'add_per'),
    ('删除权限', 'del_per'),
    ('添加菜单', 'add_menu'),
    ('删除菜单', 'del_menu'),
    ('添加处理器', 'add_handler'),
    ('删除处理器', 'del_handler'),
]
h = [
    ('AddRoleHandler', '1'),
    ('DelRoleHandler', '2'),
    ('UserRoleHandler', '3'),
    ('DelUserRoleHandler', '4'),
    ('RolePermissionHandler', '5'),
    ('AddPermissionHandler', '8'),
    ('DelPermissionHandler', '9'),
    ('AddMenuHandler', '10'),
    ('DelMenuHandler', '11'),
    ('AddHandler', '12'),
    ('DelHandler', '13'),
]

def init_data():
    """往permission_role表中添加admin这个角色"""
    role = permission_model.Role()
    role.name = 'admin'
    dbSession.add(role)
    dbSession.commit()

    """添加权限"""
    for i in range(13):
        pa = permission_model.Permission()
        pa.name = pp[i][0]
        pa.strcode = pp[i][1]
        dbSession.add(pa)
    dbSession.commit()

    """添加管理员用户"""
    u = [
        ('admin', '111111'),
    ]
    for i in xrange(1):
        user = User()
        user.name = u[i][0]
        user.password = u[i][1]
        dbSession.add(user)
    dbSession.commit()

    """为处理器添加权限"""
    for i in xrange(11):
        user = permission_model.Handler()
        user.name = h[i][0]
        user.p_id = h[i][1]
        dbSession.add(user)
    dbSession.commit()
    p = dbSession.query(permission_model.Permission).all()
    r = dbSession.query(permission_model.Role).filter_by(name='admin').first()
    for i in p:
        r.permissions.append(i)
    dbSession.add(r)
    dbSession.commit()

    """给admin用户赋予角色"""
    u_r = ["1", "1"]
    user_to_role = permission_model.UserToRole()
    user_to_role.u_id = u_r[0]
    user_to_role.r_id = u_r[1]
    dbSession.add(user_to_role)
    dbSession.commit()

    """给admin添加权限管理菜单显示"""
    p_r = ["adminmenu", "7"]
    menu = permission_model.Menu()
    menu.name = p_r[0]
    menu.p_id = p_r[1]
    dbSession.add(menu)
    dbSession.commit()