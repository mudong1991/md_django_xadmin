# -*- coding: UTF-8 -*-
__author__ = 'MD'
from xadmin.views import LoginView, LogoutView
from django.template.response import TemplateResponse
from firstapp.util import cust_html
from django.views.decorators.cache import never_cache
from django.utils.translation import ugettext_lazy as _
from django.http.response import HttpResponseRedirect
from django.conf import settings
from firstapp.util_ase import ase_html_data_decrypt
from firstapp.util import running_log, UserLogin
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from firstapp import models
from firstapp import util
from django.contrib.auth.models import AnonymousUser


# 自定义登录页视图设置
class LoginViewSetting(LoginView):
    title = _("Username Login")

    @never_cache
    def get(self, request, *args, **kwargs):
        context = self.get_context()
        context.update({"title": self.title})
        return TemplateResponse(request, cust_html('login'), context=context)

    @never_cache
    def post(self, request, *args, **kwargs):
        context = self.get_context()
        redirect_to = request.get_full_path()
        username = request.POST.get("username", '')
        password = request.POST.get("password", '')

        if settings.DEBUG:
            print 'username：' + username
            print 'password：' + password

        # AES解密
        try:
            username = ase_html_data_decrypt(username)
            password = ase_html_data_decrypt(password)
        except Exception, e:
            # 记录错误信息
            running_log.info(e)

        # 判断是否存在该用户名
        is_exist = User.objects.select_related().exclude(username="SAFE_MANAGER_30").filter(
            username=username).first()
        # 用户登录日志器类实例化
        userloginlog = UserLogin(request, username=username)
        # 登录认证
        user = authenticate(username=username, password=password)

        # 用户不存在
        if not is_exist:
            error_reason = u"用户不存在!"
            context.update({"error": True, "error_reason": error_reason})
            return TemplateResponse(request, cust_html('login'), context=context)
        elif is_exist.is_active is False:
            error_reason = u"用户已经被锁定，请联系管理员!"
            context.update({"error": True, "error_reason": error_reason})
            return TemplateResponse(request, cust_html('login'), context=context)
        else:
            # 第三次密码错误后面该IP继续操作后的处理，即使密码输入成功也要锁定IP锁定禁止登陆
            lock_ip_obj = models.LockIp.objects.filter(ip=request.environ.get("REMOTE_ADDR")).first()
            if lock_ip_obj:
                # userloginlog.set_logintime(util.get_current_time())
                # userloginlog.del_log()  # 删除请求日志
                remain_time = int(settings.LOCK_TIME - util.time_calculator(
                    util.get_current_time(),
                    lock_ip_obj.lock_time
                ))
                if settings.DEBUG:
                    print remain_time
                if remain_time >= 0:
                    error_reason = u"您的IP地址已经被暂时锁定，限制该用户登录操作!"
                    return TemplateResponse(request, cust_html('login'), context=dict(error=True,
                                                                                      error_reason=error_reason,
                                                                                      remain_time=int(remain_time)))
                else:
                    lock_ip_obj.delete()

            # 用户存在，密码正确，成功登陆。
            if user is not None:
                user.backend = 'django.contrib.auth.backends.ModelBackend'  # 指定默认的登录验证方式
                login(request, user)

                # 保存用户操作记录
                print request.session.session_key
                current_user = User.objects.get(id=is_exist.id)
                current_user.last_login = util.get_current_time()
                current_user.isonline = True
                current_user.sessionid = request.session.session_key  # 必须要先login登录完成，才会生成session_key
                current_user.login_times += 1
                current_user.save()

                # 保存用户登陆日志
                userloginlog.set_logintime(util.get_current_time())
                userloginlog.set_status(1)
                userloginlog.save_log()

                # 保存操作日志
                util.save_user_log(request, util.get_current_time(), util.operation_type.log_in_out,
                                   util.operation_result.login_success)

                # 设置session
                request.session['homepage'] = '/'

                return HttpResponseRedirect(redirect_to)
            # 用户存在，密码不不正确，有三次机会，三次都密码错误，ip锁LOCK_TIME时间，限制登陆操作。
            else:
                # 保存用户登陆日志,用于userloginlog.get_login_failed_times（）函数判断限制时间类失败登陆的次数
                userloginlog.set_logintime(util.get_current_time())
                userloginlog.set_status(0)
                userloginlog.save_log()

                # 获取 LOGIN_FAILED_TIMES_LIMIT 时间内登录失败的次数
                failed_times = userloginlog.get_login_failed_times()

                error_reason = u"对不起，密码错误!"
                # 超过三次输入错误，锁定IP
                if failed_times >= settings.LOGIN_FAILED_TIMES_LIMIT:
                    models.LockIp.objects.create(ip=request.environ.get("REMOTE_ADDR"),
                                                 lock_time=util.get_current_time())

                    error_reason += u"连续三次登录失败，您的ip地址已被暂时锁定!"
                    context.update({"error": True, "error_reason": error_reason, "remain_time": int(settings.LOCK_TIME)})
                    return TemplateResponse(request, cust_html('login'), context=context)
                else:
                    error_reason += u"您还有{0}次机会，连续三次失败您的ip地址将会被系统锁定3分钟".format(
                        settings.LOGIN_FAILED_TIMES_LIMIT - failed_times)

                context.update({"error": True, "error_reason": error_reason})
                return TemplateResponse(request, cust_html('login'), context=context)


# 自定义退出视图设置
class LogoutViewSetting(LogoutView):

    # 只有不是匿名用户信息才会被记录
    def get(self, request, *args, **kwargs):
        if request.user and not isinstance(request.user, AnonymousUser):
            user = User.objects.get(id=request.user.id)
            user.isonline = False
            user.save()

            # 记录操作日志
            util.save_user_log(request, util.get_current_time(), util.operation_type.log_in_out,
                               util.operation_result.logout_success)

        return super(LogoutViewSetting, self).get(request, *args, **kwargs)
