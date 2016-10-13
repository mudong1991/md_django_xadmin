# -*- coding: UTF-8 -*-
__author__ = 'MD'
import psutil
import os
import datetime, time
import platform, socket
from firstapp import models
from rest_framework.decorators import api_view, APIView
from rest_framework.response import Response
from firstapp import util
from firstapp import cust_exceptions
from rest_framework import viewsets
from firstapp import serializers
from pagination import CustomPagination
from rest_framework import filters
from rest_framework import permissions
from firstapp import custom_filters


# 自定义Grid排序
class GridOrderingFilter(filters.OrderingFilter):
    ordering_param = 'sidx'
    ordering_type_param = 'sord'
    ordering_fields = '__all__'

    def get_ordering(self, request, queryset, view):
        """
        Ordering is set by a comma delimited ?ordering=... query parameter.
        The `ordering` query parameter can be overridden by setting
        the `ordering_param` value on the OrderingFilter or by
        specifying an `ORDERING_PARAM` value in the API settings.
        """
        params = request.query_params.get(self.ordering_param)
        ordering_type = request.query_params.get(self.ordering_type_param)
        order_type_str = ''
        if ordering_type == 'desc':
            order_type_str = '-'
        if params:
            fileds = [order_type_str + param.strip() for param in params.split(',')]
            return fileds
        return self.get_default_ordering(view)


# 系统状态api
@api_view(['GET'])
def systeminfo(request):
    """
    获取系统状态视图函数
    """
    system_info = {"warning_info": {}, "basic_info": [], "resource_info": {}, "interface_status": {}}
    # 告警信息
    system_info["warning_info"]["warning_total_count"] = models.WarningLogs.objects.all().count()
    system_info["warning_info"]["warning_unread_count"] = models.WarningLogs.objects.filter(read_flag=0).count()
    system_info["warning_info"]["last_update_time"] = '2016-5-11 15:12:34'

    # 基本信息(电脑的基本信息)
    system_info['basic_info'] = [
        {u"item_name": u"主机名称", u"item_value": socket.gethostname()},
        {u"item_name": u"主机系统类型", u"item_value": platform.system()},
        {u"item_name": u"主机系统位数", u"item_value": platform.architecture()[0]},
        {u"item_name": u"主机系统启动时间",
         u"item_value": u"%s" % datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")},
        {u"item_name": u"硬盘大小", u"item_value": str((psutil.disk_usage('C:/').total
                                                    + psutil.disk_usage('D:/').total + psutil.disk_usage(
            'E:/').total + psutil.disk_usage('F:/').total
                                                    ) / 1000 / 1000 / 1000) + 'M' if platform.system() == 'Windows' else psutil.disk_usage(
            '/').total
         },
        {
            u"item_name": u"分区信息",
            u"item_value": u"设备名:" + str([disk_part.device for disk_part in psutil.disk_partitions()]) + \
                           u" 挂载点:" + str([disk_part.mountpoint for disk_part in psutil.disk_partitions()]) + \
                           u" 类型:" + str([disk_part.fstype for disk_part in psutil.disk_partitions()])
        },
        {u"item_name": u"内存大小", u"item_value": str(psutil.virtual_memory().total / 1000 / 1000 / 1000) + 'G'},
        {u"item_name": u"物理CPU个数", u"item_value": u"%s" % psutil.cpu_count(logical=False)},

        {u"item_name": u"设备软件版本", u"item_value":
            "v" + models.SystemStatus.objects.first().cur_system_version
            if models.SystemStatus.objects.first() else "v0.0.1.0"},

    ]

    # 硬件状态
    system_info['resource_info']['cpu_percent'] = psutil.cpu_percent()
    system_info['resource_info']['memory_percent'] = psutil.virtual_memory().percent
    system_info['resource_info']['disk_part'] = []

    def bgcolor_set(percent):
        if 0 <= percent < 25:
            return "#74C374"
        elif 25 <= percent < 50:
            return "#5BC0DE"
        elif 50 <= percent < 75:
            return "#F2B968"
        else:
            return "#DE6B68"

    for dp in psutil.disk_partitions():
        system_info['resource_info']['disk_part'].append({'disk_part_name': dp.device.replace(':\\', ''),
                                                          'disk_part_percent': psutil.disk_usage(dp.device).percent,
                                                          'percent_bgcolor': bgcolor_set(
                                                              psutil.disk_usage(dp.device).percent)
                                                          })

    # 网络状态
    system_info['interface_status'] = {'rows': []}
    network = psutil.net_io_counters(pernic=True)

    for net_name in network:
        net_info = network[net_name]

        s2 = net_info.bytes_sent
        r2 = net_info.bytes_recv

        bytes_sent = '{0:.2f}'.format(s2 / 1024)
        bytes_recv = '{0:.2f}'.format(r2 / 1024)
        err_out_in = net_info.errout + net_info.errin
        drop_out_in = net_info.dropin + net_info.dropout

        system_info['interface_status']['rows'].append(
            {'int_name': net_name.decode('gbk'), 'link_status': '1', 'up_rate': bytes_sent, 'down_rate': bytes_recv,
             'discard_num': drop_out_in, 'error_num': err_out_in}
        )

    return Response(system_info)


# 系统时间设置
class SystemTimeSet(APIView):

    def post(self, request):
        time_to_sync = str(request.data.get('time_to_sync', False))
        time_to_set = str(request.data.get('time_to_set', None)).strip()

        if time_to_sync == 'True':
            struct_time_to_set = util.get_web_time()
        else:
            from datetime import datetime
            time_max = datetime.strptime('2036-01-01 00:00:00', "%Y-%m-%d %H:%M:%S")
            time_min = datetime.strptime('1981-01-01 00:00:00', "%Y-%m-%d %H:%M:%S")

            # 时间验证
            try:
                time_set = datetime.strptime(time_to_set, "%Y-%m-%d %H:%M:%S")
            except:
                raise cust_exceptions.VdpOperationFailed(detail="您设置的时间格式不是有效的格式，有效格式如：xxxx-xx-xx xx:xx:xx")
            else:
                if (time_set - time_max).days >= 0 or (time_set - time_min).days <= 0:
                    raise cust_exceptions.VdpOperationFailed(detail="设置的时间必须是1981到2035年范围内的有效时间！")
            # 转换成时间struct_time
            struct_time_to_set = time.strptime(time_to_set, "%Y-%m-%d %H:%M:%S")

        # 设置时间
        print struct_time_to_set
        util.set_system_time(struct_time_to_set)

        return Response({'msg': 'ok'})


class GetSystemTime(APIView):
    def post(self, request):
        cur_time = models.SystemStatus().get_cur_system_time()
        print cur_time
        return Response({'cur_time': cur_time})


# 图书借出信息视图集合
class BookBorrowInfoSet(viewsets.ModelViewSet):
    queryset = models.BookBorrowInfo.objects.all()
    serializer_class = serializers.BookBorrowInfoSerializer
    filter_class = custom_filters.BookBorrowInfoFilter
    pagination_class = CustomPagination
    filter_backends = (filters.SearchFilter, filters.DjangoFilterBackend, GridOrderingFilter)
    permission_classes = (permissions.DjangoModelPermissions,)