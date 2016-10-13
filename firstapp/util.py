# -*- coding: UTF-8 -*-
__author__ = 'MD'
from firstapp.models import User, UserLogs, UserLoginLogs
from XadminDemo.settings import LOCK_TIME, LOGIN_FAILED_TIMES_LIMIT
from firstapp import models
from firstapp import cust_exceptions
from django.shortcuts import render
import logging
import time
import os
import platform
import httplib
from django.utils.translation import ugettext_lazy as _


# 定义日志器
running_log = logging.getLogger("info")
debug_log = logging.getLogger("django.request")

TIME_FORMAT = "%Y-%m-%d %H:%M:%S"  # 格式化时间格式化


# 保证翻译正确与models中的userlogs的选项一致
class operation_type:
    log_in_out = 'loginout'
    domain_control = 'other'


class operation_result:
    login_success = "login successful"
    logout_success = "logout successful"

operation_num = {'loginout': 1, 'other': 2}
operation_str = {'loginout': "login/logout", 'system_manage': "other"}

description_str_format = '{0}|{1}|{2}|{3}'


def save_user_log(request, time, operation_type, description, read=False):
    ip = request.environ.get("REMOTE_ADDR")
    description_str = description_str_format.format(request.user.username, ip, operation_str[operation_type],
                                                    description)
    models.UserLogs(user=request.user, ip=ip, operation_type=operation_num[operation_type], read=read, time=time,
                    description=description_str).save()


def get_current_time():
    """
    :return: 当前的时间字符串
    """
    time_string = time.strftime(TIME_FORMAT, time.localtime(time.time()))
    return time_string


def time_calculator(atime, btime):
    """
    :param atime: 第一个时间
    :param btime: 第二个时间
    :return: 相差的秒数(a-b)
    """
    time_a = time.mktime(time.strptime(atime, TIME_FORMAT))
    time_b = time.mktime(time.strptime(btime, TIME_FORMAT))
    seconds = time_a - time_b
    return seconds


def time_calculator_seconds(atime, seconds):
    """
    :param atime: 第一个时间
    :param seconds: 小于这个时间的秒数
    :return: 相减格式化后的时间
    """
    time_a = time.mktime(time.strptime(atime, TIME_FORMAT))
    time_b = time_a - seconds
    btime = time.strftime(TIME_FORMAT, time.localtime(time_b))
    return btime


class UserLogin(object):
    def __init__(self, request, username=None):
        self.request = request
        self.username = username
        self.ip = request.environ.get("REMOTE_ADDR")  # 获取客户端的ip
        self.status = 0
        self.login_time = ''

    def get_login_failed_times(self):
        check_last_time = time_calculator_seconds(get_current_time(), LOCK_TIME)
        # 300s内用户登录的日志记录
        login_locktime_logs = UserLoginLogs.objects.filter(
            ip=self.ip,
            login_time__lte=get_current_time(),
            login_time__gte=check_last_time,
        ).order_by("-login_time")

        success_index = 0
        failed_times = 0
        # 300s内用户登录的次数
        count = login_locktime_logs.count()

        for index, log in enumerate(login_locktime_logs):
            if log.status == 1:
                success_index = index + 1

        if success_index == 0:
            failed_times = count
        else:
            failed_times = success_index - 1

        return failed_times

    def LOCK_IP(self):
        """
        :return:  返回锁定IP地址，没有锁定就返回为空
        """
        if self.get_login_failed_times() >= LOGIN_FAILED_TIMES_LIMIT:
            return self.ip
        else:
            return None

    def set_logintime(self, login_time):
        self.login_time = login_time

    def set_status(self, status):
        self.status = status

    def get_last_fail_login_time(self):
        last_fail_login_time = UserLoginLogs.objects.filter(ip=self.ip, username=self.username, status=self.status) \
                                   .order_by("-login_time")[:1].values("login_time")
        return last_fail_login_time[0]["login_time"]

    def save_log(self):
        try:
            log = UserLoginLogs(
                ip=self.ip,
                username=self.username,
                login_time=self.login_time,
                status=self.status
            )
            log.save()
        except Exception as e:
            running_log.info("管理员登录日志储存错误！" + str(e))
            print "管理员登录日志储存错误！"

    def del_log(self):
        try:
            log = UserLoginLogs.objects.filter(ip=self.ip, username=self.username, status=self.status,
                                               login_time=self.login_time)
            log.delete()
        except Exception as e:
            running_log.info("管理员登录日志删除错误！" + str(e))
            print "管理员登录日志删除错误！"


def get_appname():
    """
    获取app的名字，即包的名字
    :return: str
    """
    return __package__


def get_template(name):
    """
    :param name: 网页模板名
    :return: 网页模板(绝对路径)
    """
    return get_appname() + "/" + name + ".html"


def file_write(path, chunks, filename):
    destination_file = os.path.join(path, filename)
    try:
        d_file = open(destination_file, 'wb+')
    except:
        raise Exception(message="目标路径无法打开")
    else:
        for c in chunks:
            d_file.write(c)
        d_file.close()


def get_web_time():
    try:
        conn = httplib.HTTPConnection('www.baidu.com', timeout=5000)
        conn.request("GET", "/")
        response = conn.getresponse()
        if response.status == 200:
            ts = response.getheader('date')
            # 将GMT时间转换成北京时间
            ltime = time.strptime(ts[5:25], "%d %b %Y %H:%M:%S")
            web_shruct_time = time.localtime(time.mktime(ltime) + 8 * 60 * 60)
            return web_shruct_time
        else:
            raise cust_exceptions.VdpOperationFailed(detail="网络请求失败，原因:" + str(response.reason) +
                                                            '相应代码:' + str(response.status))
    except Exception as e:
        raise cust_exceptions.VdpOperationFailed(detail="获取网络地址失败，请检查网络连接！")


def set_system_time(struct_time_to_set):
    if platform.system() == 'Windows':
        import win32api
        if struct_time_to_set:
            win32api.SetLocalTime(struct_time_to_set)
        else:
            raise cust_exceptions.VdpOperationFailed(detail="设置时间为空！")
    else:
        os.system(u"date -s '%s'" % time.strftime("%Y-%m-%d %H:%M:%S", struct_time_to_set))


class AppTemplate(object):
    """
    基于约定加载模板，这样就不需要将app名字嵌入到模板中，约定是以当前app的模板为根目录加载，
    下级目录使用__(双下划线)来代替目录分隔符,给出从app模板根路径到模板路径的位置，不加后缀
    """

    def __getattribute__(self, name):
        name = name.replace("__", "/")
        return get_appname(name)


def trans_menu_to_dict(menu, submenu):
    item = dict()
    item['title'] = menu.name
    item['description'] = menu.description
    item['link'] = menu.url
    item['icon'] = menu.icon
    item['id'] = menu.id
    if submenu:
        item['submenu'] = submenu
    return item


def trans_menus_list(menus):
    level_one_menus = []
    submenus = dict()
    # level_two_menus = []
    for menu in menus:
        # item = trans_menu_to_dict(menu)
        if menu.parent is not None:
            mp = menu.parent
            if not submenus.has_key(mp.id):
                submenus[mp.id] = []
            submenus[mp.id].append(trans_menu_to_dict(menu, None))
        else:
            level_one_menus.append(menu)
    level_one_menus.sort(key=lambda x: x.ordernum)
    return [trans_menu_to_dict(menu, submenus.get(menu.id, None)) for menu in level_one_menus]
    # pass


def flatten(l):
    for el in l:
        yield el
        if el.has_key("submenu"):
            for sub in flatten(el['submenu']):
                yield sub
                # else:


# 构造一个迭代器，用于处理文件，传递给StreaminghttpResponse
def file_iterator(file_name, chunk_size=1024):
    with open(file_name) as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break


def cust_html(template):
    """
    自定义html路径地址
    :return:template.html的形式
    """
    _, ext = os.path.splitext(template)
    if ext and len(ext) > 0:
        return "firstapp/" + str(template)
    else:
        return "firstapp/" + str(template) + ".html"


def cust_img(img_url):
    """
        自定义img路径地址
        :return:静态图片地址的形式
        """
    return "img/" + str(img_url)


def cust_render(template_name, dict, request):
    """
    自定义render函数，为render的dict添加一些常用属性和RequestContext
    """
    dict["app_name"] = get_appname()
    dict["loadtemplate"] = AppTemplate()

    # 获取系统版本号
    system_status = models.SystemStatus.objects.first()
    if system_status:
        dict['current_version'] = system_status.cur_system_version
    else:
        dict['current_version'] = '0.0.1.0'

    if request.user and hasattr(request.user, 'first_name') and request.user.first_name == "key":
        # UKey用户
        dict["is_use_uKey"] = True
    else:
        dict["is_use_uKey"] = False

    return render(request, get_template(template_name), dict)


