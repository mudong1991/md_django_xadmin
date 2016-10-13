/**
 * Created by mudong on 2016/4/28.
 */
//应用开发模块定义，module 方法的第一个参数为模块的名称，第二个参数为它的依赖模块列表
var vdpAppControllers = angular.module('vdpAppControllers', ['ngCookies', 'angularFileUpload']);

var HOST = window.location.protocol + '//' + window.location.host + '/vdp';
var save_admin_url = HOST + '/api/admin/';
var get_admin_url = HOST + '/api/admin/';
var edit_admin_url = HOST + '/api/admin/';
var delete_admin_url = HOST + '/api/admin/';
var get_system_logs_url = HOST + '/gslbdis/';
var clear_systemlogs_url = HOST + '/slcdis/';
var export_systemlogs_url = HOST + '/sledis/';
var download_systemlogs_url = HOST + '/slddis/?filename=';
var get_userlogs_url = HOST + '/gulbdis/';
var clear_userlogs_url = HOST + '/ulcdis/';
var export_userlogs_url = HOST + '/uledis/';
var export_warninglogs_url = HOST + '/ulwdis/';
var download_userlogs_url = HOST + '/ulddis/?filename=';
var import_userlogs_url = HOST + '/ulidis/';

// 密码复杂程度检查
function checkpwd(pwd){
    var patrn=/^(?![0-9a-z]+$)(?![0-9A-Z]+$)(?![0-9\W]+$)(?![a-z\W]+$)(?![a-zA-Z]+$)(?![A-Z\W]+$)[a-zA-Z0-9\W_]+$/;
    if(patrn.exec(pwd)!= null){
        return true;
    }
    return false;
}

//错误信息解析
function transform_error_message(data) {
    var message = '';
     if (data.hasOwnProperty("detail")){
         data_str = data.detail;
         data_str = data_str.replace("u\'", "\'");
         message =  eval("("+data_str+")").msg;
         if (angular.isArray(message)){
            message = message.join("<br/>");
         }
         return message
     }
    return message
}

var _key = CryptoJS.enc.Utf8.parse('!@#$%^&*()_+|%^&');
var _iv = CryptoJS.enc.Utf8.parse('!@#$%^&*()_+|%^&');

//http请求解密
function dataFileter(data){
    var decrypted_data = CryptoJS.AES.decrypt(data, _key, {
        iv: _iv,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    });
    var uft8_data = decrypted_data.toString(CryptoJS.enc.Utf8);
    //还原转义字符
    edcod_data = uft8_data.replace(/&gt;/g, ">").replace(/&lt;/g, "<").replace(/&quot;/g, '"').replace(/&amp;/g, "&");
    var json_data = eval('(' + edcod_data + ')');
    return json_data;   // 返回处理后的数据
}

/*
 获取请求url中的地址参数
 */
function getQueryStringKeyItem(key, query_string) {
    if (query_string.substr(0, 1) === "?") {
        query_string = query_string.substr(1)
    }
    var reg = new RegExp("(^|&)" + key + "=([^&]*)(&|$)", "i");
    var r = query_string.match(reg);
    if (r != null)
        return decodeURI(r[2]);
    return null;
}


//时间过滤过滤
function formatDate(now) {
    var year=now.getFullYear();
    var month=now.getMonth()+1;
    var date=now.getDate();
    var hour=now.getHours();
    var minute=now.getMinutes();
    var second=now.getSeconds();
    return year+"-"+month+"-"+date+" "+hour+":"+minute+":"+second;
}


//第一个参数是controller的名称，第二个数组是所要注入的依赖服务列表
//管理员信息列表控制器
vdpAppControllers.controller("adminController", ["$scope","$http" ,"$window","$cookies", "$grid",
    function ($scope, $http, $window, $cookies, $grid){
        var data_url = "/api/admin/";
        var grid_selector = "#jqGrid_AdminUser";
        var pager_selector = "#jqGrid_AdminPager";
        var extra_param = {
            multiselect: true,
            sortname: 'id',
            sortorder: 'desc',
            loadui:"disable",
            postData: {
                "user__username": function () {
                    return $scope.searchinfo.user__username ? $scope.searchinfo.user__username : ""
                },
            },
            "loadError": function (data) {
                // jqGrid在删除了整页数据后重新加载当前页会出错，所以需要额外处理。
                $grid.loadPrePage(grid_selector);
            },
        };
        var col_models = [
            {label: 'ID', name: 'id', index: 'id', width: 30, hidden: true},
            {label: '真实姓名', name: 'user_showname', align: 'center', width: 30, sortable: true},
            {label: '用户名', name: 'user__username', align: 'center', width: 45, sortable: true},
            {
                label: '登陆认证方式', name: 'user_type', align: 'center', width: 45, sortable: true,
                formatter: function (cellValue, options, rowObject) {
                    if (cellValue == "key") {
                        return "UKEY";
                    }
                    else {
                        return "用户名密码";
                    }
                }
            },
            {
                label: '角色', name: 'role_id', align: 'center', width: 45, sortable: true,
                formatter: function (cellValue, options, rowObject) {
                    if (cellValue == 1) {
                        return "系统管理员";
                    }
                    else if (cellValue == 2) {
                        return "安全管理员";
                    } else{
                        return "审计管理员";
                    }
                }
            },
            {label: '单位', name: 'unit', align: 'center', width: 45, sortable: true},
            {label: '登陆次数', name: 'login_times', align: 'center', width: 45, sortable: true},
            {label: '最近一次登陆时间', name: 'lastlogintime', align: 'center', width: 55, sortable: true},
            {
                label: '在线状态', name: 'isonline', align: 'center', width: 35, sortable: true,
                formatter: function (cellValue, options, rowObject) {
                    if (cellValue == "0") {
                        return "离线";
                    }
                    else {
                        return "在线";
                    }
                }
            },
            {
                label: '状态', name: 'user__is_active', align: 'center', width: 35, sortable: true,
                formatter: function (cellValue, options, rowObject) {
                    if (cellValue == 'False') {
                        return "锁定";
                    }
                    else {
                        return "启用";
                    }
                }
            }
        ];

        $scope.searchinfo = {'user__username': ''};

        $grid.init(grid_selector, pager_selector, data_url, col_models, extra_param);

        function bindPageData() {
            $(grid_selector).trigger('reloadGrid');
        }

        // 增加管理员
        $scope.addadmin = function (){
            layer.open({
                type:2,
                title: "添加系统用户",
                content: '/vdp/aat',
                border: [10, 1, 'white'],
                area :["320px", "400px"],
                closeBtn: 1,
                shade:0.2,
                fadeIn:500,
                moveOut:false,
                shadeClose: true,
                shift:1,
                end : function (){
                    $grid.reloadGrid(grid_selector);
                }
            })
        };

        $scope.input_search = function(event){
            if (event.keyCode == 13){
                $grid.reloadGrid(grid_selector);
            }
        };
        //查找管理员
        $scope.search = function () {
            $grid.reloadGrid(grid_selector);
        };
        //修改管理员
        $scope.editadmin = function (){
            var ids = $grid.getSelectedRowIDs(grid_selector);

            if (ids.length == 0){
                $window.layer.alert("请选择一个需要编辑的用户!");
                return;
            }else if(ids.length > 1){
                $window.layer.alert("一次仅能编辑一个用户,请选择需要编辑的用户!");
                return;
            }
            var selectUser = $grid.getRowDataByID(grid_selector, ids[0]);

            $window.layer.open({
                type:2,
                title: "修改信息",
                content: '/vdp/eat/?user_id='+selectUser.id,
                border: [10, 1, 'white'],
                area :["320px", "400px"],
                closeBtn: 1,
                shade:0.2,
                fadeIn:500,
                moveOut:false,
                shadeClose: true,
                shift:1,
                end : function (){
                    $grid.reloadGrid(grid_selector);
                }
            });
        };
        //删除管理员
        $scope.deleteadmin = function (){
            var ids = $grid.getSelectedRowIDs(grid_selector);

            if (ids.length == 0){
                $window.layer.alert("请选择需要删除的用户!");
                return;
            }
            //数据监测，判断用户是否可以被删除？
            var error_msg = ''
            for (var i in ids){
                var row_data = $grid.getRowDataByID(grid_selector, ids[i]);
                if (row_data.user__username=="manager" || row_data.user__username=='admin'){
                    error_msg += "用户"+row_data.user__username+"不能被删除\n";
                    $window.layer.alert(error_msg, 3);
                    return;
                }
            }

            $window.layer.confirm("确定要删除所选管理员?",{icon: 3, title:'提示'}, function () {
                var ajax_settings = [];
                $.each(ids, function(){
                    var row_data = $grid.getRowDataByID(grid_selector, this);
                    if(row_data){
                        var cur_url = delete_admin_url + this + '/';
                        var setting = {
                            url:cur_url,
                            type: 'delete',
                            headers:{'X-CSRFToken': $cookies.csrftoken}
                        };
                        ajax_settings.push(setting);
                    }
                });

                var queue = ajax_make_queue("处理管理员删除中...", "删除管理员", ajax_settings, bindPageData, bindPageData);
                queue.start_queue();
            })
        };
        //锁定管理员
        $scope.lockadmin = function (){
            var ids = $grid.getSelectedRowIDs(grid_selector);

            if (ids.length == 0){
                $window.layer.alert("请选择需要锁定的用户!");
                return;
            };
            //数据监测，判断用户是否可以被锁定？
            var error_msg = ''
            for (var i in ids){
                var row_data = $grid.getRowDataByID(grid_selector, ids[i]);
                if (row_data.user__username=="manager" || row_data.user__username=='mudong'){
                    error_msg += "用户"+row_data.user__username+"不能被锁定\n";
                    $window.layer.alert(error_msg, 3);
                    return;
                }
            }

            $window.layer.confirm("确定要锁定所选管理员?", {icon: 3, title:'提示'}, function (){
                var ajax_settings = []
                $.each(ids, function(){
                    var row_data = $grid.getRowDataByID(grid_selector, this)
                    if(row_data){
                        var cur_url = get_admin_url + this + '/lock/';
                        var setting = {
                            url:cur_url,
                            type: 'POST',
                            headers:{'X-CSRFToken': $cookies.csrftoken}
                        };
                        ajax_settings.push(setting);
                    }
                });
                var queue = ajax_make_queue("处理管理员锁定中...", "锁定管理员", ajax_settings, bindPageData, bindPageData);
                queue.start_queue();
            })
        };
        //解锁管理员
        $scope.unlockadmin = function (){
            var ids = $grid.getSelectedRowIDs(grid_selector);

            if (ids.length == 0){
                $window.layer.alert("请选择需要解锁的用户!");
                return;
            };

            $window.layer.confirm("确定要解锁所选管理员?", {icon: 3, title:'提示'}, function (){
                var ajax_settings = []
                $.each(ids, function(){
                    var row_data = $grid.getRowDataByID(grid_selector, this)
                    if(row_data){
                        var cur_url = get_admin_url + this + '/unlock/';
                        var setting = {
                            url:cur_url,
                            type: 'POST',
                            headers:{'X-CSRFToken': $cookies.csrftoken}
                        };
                        ajax_settings.push(setting);
                    }
                });
                var queue = ajax_make_queue("处理管理员解锁中...", "解锁管理员", ajax_settings, bindPageData, bindPageData);
                queue.start_queue();
            })
        };
    }
]);

//新增管理员控制器
vdpAppControllers.controller("addadminController", ["$scope","$http" ,"$window","$cookies",
    function ($scope, $http, $window, $cookies){
        $scope.user = {user_type: "pwd", user__username:"", ukeydn:"", unit:"", user_showname:"", role_id:1, user__password:"", pwd:"", user__is_active: 1, isonline: 0, lastlogintime: "", login_times: 0, user_id:1};

        // 提交保存用户信息
        $scope.save = function (){
            if($scope.user.role_id == undefined || $scope.user.role_id == ''){
                $window.layer.alert("未选择角色");
                return;
            }else if ($scope.user.user_type == undefined || $scope.user.user_type == '') {
                $window.layer.alert('未选择登录认证方式！');
                return;
            }

            if($scope.user.user_type == "pwd"){
                if ($scope.user.user__username == undefined || $scope.user.user__username == '') {
                    $window.layer.alert('用户名不能为空！');
                }else if ($scope.user.pwd != $scope.user.user__password) {
                    $window.layer.alert('两次密码输入不一致！');
                } else if(!checkpwd($scope.user.pwd)) {
                    $window.layer.alert("密码请包括大写字母、小写字母、数字、特殊字符中至少三种进行组合！");
                }else {
                    var sendAddPro_status =  $scope.sendAddPro($scope.user);
                    if (sendAddPro_status){
                        $scope.user.user__password = CryptoJS.MD5(user.user__password).toString();
                        $scope.user.pwd = CryptoJS.MD5(user.user__password).toString();
                    }
                }
            }

            else if($scope.user.user_type == "key") {
                if ($scope.user.user__username == undefined || $scope.user.user__username == ''){
                    $window.layer.alert('用户名不能为空！');
                    return;
                }
                if ($scope.user.ukeydn == undefined || $scope.user.ukeydn == ''){
                    $window.layer.alert('用户DN不能为空！');
                    return;
                }
                var user = $scope.user;
                user.user__password = "123456";
                $scope.sendAddPro(user);
            }
        };

        $scope.show_save_btn = function (){
            if ($scope.user.user_type != 'pwd'){
                $("#layer_confirm").removeAttr("disabled");
            }else {
                $("#layer_confirm").attr("disabled", "");
            }
        };

        $scope.sendAddPro = function (user){
            $http({
                method: 'post',
                url: save_admin_url,
                data: JSON.stringify(user),
                headers:{'X-CSRFToken': $cookies.csrftoken},
                contentType: "application/json"
            }).success(function(data, status, headers, config) {
                layer.alert('创建成功!', 3, function () {
                    var index = parent.layer.getFrameIndex(window.name); //先得到当前iframe层的索引
                    parent.layer.close(index); //再执行关闭
                    return true;
                })
            }).error(function(data, status, headers, config) {
                if(status == 500){
                    layer.alert("服务器错误,请检查!", 3);
                }
                var message = transform_error_message(data);

                layer.alert(message, 3);
                return false;
            });
        }
    }
]);

//修改管理员控制器
vdpAppControllers.controller("editadminController", ["$scope", "$http", "$window", "$cookies",
    function ($scope, $http, $window, $cookies){
        //初始化一个user对象,防止页面出错
        $scope.user = {user_type: "pwd", user__username:"", ukeydn:"", unit:"", user_showname:"", role_id:2, user__password:"", pwd:"", user__is_active: 1, isonline: 0, lastlogintime: "", login_times: 0, user_id:1};
        //页面加载时候数据加载
        var user_id = getQueryStringKeyItem('user_id',$window.location.search);

        $window.onload = function (){
            $http({
                method: "GET",
                url: edit_admin_url +user_id+ "/",
                headers:{'X-CSRFToken': $cookies.csrftoken},
                contentType: "application/json"
            }).success(function(data, status, headers, config) {
                $scope.user = data;
                $scope.user.pwd = $scope.user.user__password = '';

                angular.element("#pw_check").hide();
                if ($scope.user.user_type == 'key'){
                    $scope.user.user_type = 'pwd';
                }else {
                    angular.element("#layer_confirm").removeAttr("disabled");
                }
            })
        };

        // 提交保存用户信息
        $scope.save = function (){
            if($scope.user.role_id == undefined || $scope.user.role_id == ''){
                $window.layer.alert("未选择角色");
                return;
            }else if ($scope.user.user_type == undefined || $scope.user.user_type == '') {
                $window.layer.alert('未选择登录认证方式！');
                return;
            }

            if($scope.user.user_type == "pwd"){
                if ($scope.user.user__username == undefined || $scope.user.user__username == '') {
                    $window.layer.alert('用户名不能为空！');
                }else if ($scope.user.pwd != $scope.user.user__password) {
                    $window.layer.alert('两次密码输入不一致！');
                } else if(!checkpwd($scope.user.pwd)) {
                    $window.layer.alert("密码请包括大写字母、小写字母、数字、特殊字符中至少三种进行组合！");
                }else {
                    var user = $scope.user;

                    var sendAAPro_status = $scope.sendEditPro(user);
                    if (sendAAPro_status){
                        user.user__password = CryptoJS.MD5(user.user__password).toString();
                        user.pwd = CryptoJS.MD5(user.user__password).toString();
                    }
                }
            }
        };

        $scope.show_save_btn = function (){
            if ($scope.user.user_type != 'pwd'){
                $("#layer_confirm").removeAttr("disabled");
            }else {
                $("#layer_confirm").attr("disabled", "");
            }
        };

        $scope.sendEditPro = function (user){
            $http({
                method: 'put',
                url: edit_admin_url +user_id+ "/",
                data: JSON.stringify(user),
                headers:{'X-CSRFToken': $cookies.csrftoken},
                contentType: "application/json"
            }).success(function(data, status, headers, config) {
                layer.alert('更新成功!', 3, function () {
                    var index = parent.layer.getFrameIndex(window.name); //先得到当前iframe层的索引
                    parent.layer.close(index); //再执行关闭
                    return true;
                })
            }).error(function(data, status, headers, config) {
                if(status == 500){
                    layer.alert("服务器错误,请检查!", 3);
                }
                var message = transform_error_message(data);
                layer.alert(message, 3);
                return false;
            });
        };
    }
]);

//系统状态控制器
vdpAppControllers.controller("systemController", ["$scope", "$http", "$window", "$cookies", "$grid",
    function ($scope, $http, $window, $cookies, $grid){
        $scope.warning_info = {};
        $scope.basic_info = [];
        $scope.resource_info = {};
        $scope.interface_status = {};


        var status_url = '/api/systeminfo';
        var grid_selector = "#jqGrid_interface";
        var col_model = [
            {label: '名称', name: 'int_name', align: 'center', width: 30},
            {
                label: '连接状态', name: 'link_status', align: 'center', width: 40,
                formatter: function (cellValue, options, rowObject) {
                    if (cellValue == "0" || cellValue == 0) {
                        return "<i class='fa fa-times bigger-140' style='color:red'></i>";
                    }
                    else {
                        return "<i class='fa fa-check bigger-140' style='color:green'></i>";
                    }
                }
            },
            {label: '上行(KB/s)', name: 'up_rate', align: 'center', width: 40},
            {label: '下行(KB/s)', name: 'down_rate', align: 'center', width: 40},
            {label: '丢弃包数', name: 'discard_num', align: 'center', width: 40},
            {label: '错误包数', name: 'error_num', align: 'center', width: 40}
        ];
        var extra_params = {
            multiselect: false,
            rownumbers: false,
            datatype: 'local',
            loadComplete: function (){
                angular.element(grid_selector)[0].addJSONData($scope.interface_status);
            }
        };
        $grid.init(grid_selector, '', '', col_model, extra_params);

        var is_stop_page_refresh = false;
        function set_percent_info (selector, data_value){
            selector = angular.element(selector);
            data_value = parseFloat(data_value);
            selector.css({"width": data_value+"\%"});
            if (0.0<= data_value && data_value < 25.0){
                selector.css({"backgroundColor": '#74C374'});
            }else if(25.0<= data_value && data_value< 50.0){
                selector.css({"backgroundColor": '#5BC0DE'});
            }else if(50.0 <= data_value && data_value < 75.0){
                selector.css({"backgroundColor": '#F2B968'});
            }else{
                selector.css({"backgroundColor": '#DE6B68'});
            }
        };


        var net_flag = 1;
        var per_down = [], ofter_down = [], per_up=[], ofter_up=[];
        function bindPageData() {
            if (!is_stop_page_refresh) {
                $http({
                    method: 'get',
                    url: status_url,
                    headers: {'X-CSRFToken': $cookies.csrftoken},
                    contentType: "application/json"
                }).success(function (data, status, headers, config) {
                    $scope.warning_info = data.warning_info;
                    $scope.basic_info = data.basic_info;
                    $scope.resource_info = data.resource_info;
                    $scope.interface_status = data.interface_status;


                    // 网速计算
                    for (var inter in data.interface_status.rows) {
                        if (net_flag){
                            per_down[inter] = data.interface_status.rows[inter].down_rate;
                            per_up[inter] = data.interface_status.rows[inter].up_rate;
                        }
                        ofter_down[inter] = data.interface_status.rows[inter].down_rate - per_down[inter];
                        per_down[inter] = data.interface_status.rows[inter].down_rate;

                        ofter_up[inter] = data.interface_status.rows[inter].up_rate - per_up[inter];
                        per_up[inter] = data.interface_status.rows[inter].up_rate;
                    }
                    net_flag = 0;
                    // 硬件状态
                    //cpu
                    var cup_percent = $scope.resource_info.cpu_percent;
                    //内存
                    var memory_percent = $scope.resource_info.memory_percent;
                    set_percent_info("#cpu_percent_info", cup_percent);
                    set_percent_info("#memory_percent_info", memory_percent);
                    // 网络状态
                    for (var inter in data.interface_status.rows) {
                        $scope.interface_status.rows[inter].down_rate = (ofter_down[inter]/3).toFixed(2);
                        $scope.interface_status.rows[inter].up_rate = (ofter_up[inter]/3).toFixed(2);
                    }

                    $grid.reloadGrid(grid_selector);

                }).error(function (data, status, headers, config) {
                    //$window.layer.alert("服务器错误,请检查!", 3);
                    return false;
                });
            }

            // 3s后再次获取数据
            setTimeout(bindPageData, 5000);
        }

        bindPageData();

        $scope.show_warning = function (show_all_read){
            $window.layer.open({
                type:2,
                title: ['告警信息'],
                content: '/vdp/wlt/?show_query=false&&show_all_read=' + show_all_read,
                area :["720px", "580px"],
                closeBtn: 1,
                shade:0.2,
                fadeIn:500,
                moveOut:false,
                shadeClose: true,
                shift:1,
                maxmin:true,
            })
        }
    }
]);

//告警日志管理控制器
vdpAppControllers.controller("warningLogController", ["$scope", "$http", "$window", "$cookies", "$grid",
    function ($scope, $http, $window, $cookies, $grid){
        var grid_selector = "#jqGrid_WarningLogs";
        var pager_selector = "#jqGrid_WarningLogsPager";
        $scope.show_query = getQueryStringKeyItem('show_query' ,$window.location.search);
        var show_all_read = getQueryStringKeyItem('show_all_read', $window.location.search);
        var new_unread = getQueryStringKeyItem('new_unread', $window.location.search);
        var new_unread_id = getQueryStringKeyItem('id', $window.location.search);

        var now = new Date();
        var before = new Date((Date.parse(now) - 259200000));
        var new_unread_start_time = formatDate(before);
        var new_unread_end_time = formatDate(now);
        new_unread_id = new_unread_id != null ? new_unread_id:'';
        var new_unread_url = '/api/warninglogs/new_unread/?start_time='+new_unread_start_time+'&&end_time='+new_unread_end_time+'&&id='+new_unread_id;
        var data_url = new_unread == 'true' ? new_unread_url: '/api/warninglogs/';

        $scope.serious_level_options = [{id:1, name:'轻微'}, {id:2, name:'一般'}, {id:3, name:'严重'}];
        $scope.warning_type_options = [{id:1, name:'违规终端'}, {id:2, name:'主机系统异常'}];

        $scope.keyword = '';
        $scope.serious_level = '';
        $scope.warning_type = '';

        $scope.post_data_obj = function (postData) {
            //开始时间处理
            if (angular.element("#happend_time_gte").val()) {
                postData.start_time = angular.element("#happend_time_gte").val();
            } else {
                delete postData.start_time
            }

            //结束时间处理
            if (angular.element("#happend_time_lte").val()) {
                postData.end_time = angular.element("#happend_time_lte").val();
            } else {
                delete postData.end_time
            }

            //严重级别处理
            if ($scope.serious_level) {
                postData.serious_level = $scope.serious_level.id;
            } else {
                delete postData.serious_level
            }

            //告警类型处理
            if ($scope.warning_type) {
                postData.warning_type = $scope.warning_type.id
            } else {
                delete postData.warning_type
            }

            // 搜索关键字处理
            if ($scope.keyword.length > 0) {
                var patt = new RegExp($scope.keyword);
                if (patt.test('违规终端')) {
                    postData.warning_type = 1;
                } else if (patt.test('主机系统异常')) {
                    postData.warning_type = 2;
                } else if (patt.test('轻微')) {
                    postData.serious_level = 1;
                } else if (patt.test('一般')) {
                    postData.serious_level = 2;
                } else if (patt.test('严重')) {
                    postData.serious_level = 3;
                } else if (patt.test('未知类型')) {
                    postData.warning_type = 0;
                } else {
                    postData.search = $scope.keyword ? $scope.keyword : "";
                }
            }else{
                delete postData.search
            }

            return postData;
        }

        var extra_params = {
            multiselect: false,
            sortname: 'id',
            sortorder: 'desc',
            loadui: 'disable',
            serializeGridData: function (postData){
                if ($scope.show_query == 'true'){
                    postData = $scope.post_data_obj(postData);
                }else{
                    if (new_unread != 'true'){
                        postData.read_flag = show_all_read == 'true' ? '': 0;
                    }
                }
                return postData
            },
            loadComplete: function (){
                //
            },
            loadError: function (data) {
                // jqGrid在删除了整页数据后重新加载当前页会出错，所以需要额外处理。
                $grid.loadPrePage(grid_selector);
            },
            //onSelectRow: function (row_id, status){
            //    var row_data = $grid.getRowDataByID(grid_selector, row_id);
            //}
        };

        var formatter_warning_type = function (cellvalue, options, rowObject) {
                switch (cellvalue) {
                    case 1:
                    case '1':
                        return '违规终端';
                    case 2:
                    case '2':
                        return '系统异常';
                    default:
                        return '未知类型';
                }
            };

        var formatter_serious_level = function (cellvalue, options, rowObject) {
            switch (cellvalue) {
                case 2:
                case '2':
                    return '一般';
                case 3:
                case '3':
                    return "<b style='color:red; font-weight: normal;'>严重</b>";
                case 1:
                case '1':
                    return '轻微';
                default:
                    return '未知程度';
            }
        };

        var formatter_read_flag = function (cellvalue, options, rowObject) {
            switch (cellvalue) {
                case 0:
                case '0':
                    return '未读';
                default:
                    return '已读';
            }
        };

        var col_models = [
                {label: 'ID', name: 'id', index: 'id', width: 30, hidden: true},
                {label: '告警时间', name: 'happen_time', align: 'center', width: 45},
                {label: '告警设备IP', name: 'device_ip', align: 'center', width: 30},
                {
                    label: '告警类型',
                    name: 'warning_type',
                    align: 'center',
                    width: 45,
                    formatter: formatter_warning_type
                },
                {
                    label: '严重程度',
                    name: 'serious_level',
                    align: 'center',
                    width: 45,
                    formatter: formatter_serious_level
                },
                {label: '是否已读', name: 'read_flag', width: 30, align: 'center',formatter: formatter_read_flag},
                {label: '描述', name: 'description', width: 80}
            ];

        $grid.init(grid_selector, pager_selector, data_url, col_models, extra_params);


        $scope.input_search = function(event){
            if (event.keyCode == 13){
                $grid.reloadGrid(grid_selector);
            }
        };

        $scope.find_log = function (){
            $grid.reloadGrid(grid_selector);
        };

        $scope.set_all_read = function (){
            //全部设置成已读
            postData = {};
            postData = $scope.post_data_obj(postData);
            $http.post('/api/warninglogs/set_all_read/?'+parseParam(postData)).success(function (data){
                $window.parent.layer.alert('设置成功!', {icon:1});
                $grid.reloadGrid(grid_selector);
            }).error(function (data){
                $window.parent.layer.alert('服务器出错!', {icon: 2});
            });
        }

        $scope.export_log = function (){
            layer.msg('正在导出日志文件......', {icon: 16});
            postData = {};
            postData = $scope.post_data_obj(postData);
            $http.get('/api/warninglogs/export_log/?'+parseParam(postData)).success(function (data) {
                layer.closeAll();
                if(data.resultcode == 0){
                    layer.msg("导出日志文件成功！准备下载日志文件......", {icon:16});
                    $window.parent.location.href = '/api/warninglogs/down_log/?file_name=' + data.file_name;
                    layer.closeAll();
                }else{
                    console.log(data.msg);
                    layer.tips(data.msg, '#export', {
                        tips: [1, '#3595CC'],
                        time: 4000
                    });
                }
            }).error(function (data){
                layer.closeAll();
                layer.alert("发生错误!"+transform_error_message(data));
            });
        }

        $scope.import_log = function () {
            layer.msg('正在导入日志文件......', {icon:16});

        }

    }
]);

//系统日志
vdpAppControllers.controller('systemLogController', ["$scope", "$http", "$window", "$cookies", "$grid", "FileUploader",
    function ($scope, $http, $window, $cookies, $grid, FileUploader){
        var grid_selector = "#jqGrid_SystemLogs";
        var pager_selector = "#jqGrid_SystemLogsPager";
        var data_url = '/api/systemlogs/';
        $scope.username = '';

        $scope.operation_type = '';
        $scope.operation_type_options = [{id:1, name:'登录/退出'}, {id:2, name:'网络域管理'},{id:3, name:'网络配置'},
                                        {id:4, name:'用户管理'},{id:5, name:'设备控制'}];

        $scope.post_data_obj = function (postData) {
            //开始时间处理
            if (angular.element("#happend_time_gte").val()) {
                postData.start_time = angular.element("#happend_time_gte").val();
            } else {
                delete postData.start_time
            }

            //结束时间处理
            if (angular.element("#happend_time_lte").val()) {
                postData.end_time = angular.element("#happend_time_lte").val();
            } else {
                delete postData.end_time
            }

            //告警类型处理
            if ($scope.operation_type) {
                postData.operation_type = $scope.operation_type.id
            } else {
                delete postData.operation_type
            }

            // 用户名搜索
            if ($scope.username) {
                postData.username = $scope.username
            } else {
                delete postData.username
            }


            return postData;
        };

        var extra_params = {
            multiselect: false,
            sortname: 'id',
            sortorder: 'desc',
            loadui: 'disable',
            serializeGridData: function (postData){
                postData = $scope.post_data_obj(postData);
                return postData;
            },
            loadComplete: function (){
                //
            },
            loadError: function (data) {
                // jqGrid在删除了整页数据后重新加载当前页会出错，所以需要额外处理。
                $grid.loadPrePage(grid_selector);
            },
            //onSelectRow: function (row_id, status){
            //    var row_data = $grid.getRowDataByID(grid_selector, row_id);
            //}
        };


        var formatter_operation_type = function (cellvalue, options, rowObject) {
            switch (cellvalue) {
                case 1:
                case '1':
                    return '登录/退出';
                case 2:
                case '2':
                    return "网络域管理";
                case 3:
                case '3':
                    return '网络配置';
                case 4:
                case '4':
                    return '用户管理';
                case 5:
                case '5':
                    return '设备控制';
                default:
                    return '未知程度';
            }
        };

        var col_models = [
            {label: 'ID', name: 'id', index: 'id', width: 30, hidden: true},
            {label: '用户名', name: 'username', align: 'center', width: 45},
            {label: '时间', name: 'time', align: 'center', width: 30},
            {
                label: '日志类型',
                name: 'type',
                align: 'center',
                width: 45,
                formatter: formatter_operation_type
            },
            {label: '描述', name: 'description', align: 'center',width: 100}
        ];

        $grid.init(grid_selector, pager_selector, data_url, col_models, extra_params);


        $scope.username_search = function(event){
            if (event.keyCode == 13){
                $grid.reloadGrid(grid_selector);
            }
        };

        $scope.find_log = function (){
            $grid.reloadGrid(grid_selector);
        };

        $scope.export_log = function (){
            layer.msg('正在导出日志文件......', {icon: 16});
            postData = {};
            postData = $scope.post_data_obj(postData);
            $http.get('/api/systemlogs/export_log/?'+parseParam(postData)).success(function (data) {
                layer.closeAll();
                if(data.resultcode == 0){
                    layer.msg("导出日志文件成功！准备下载日志文件......", {icon:16});
                    $window.parent.location.href = '/api/systemlogs/down_log/?file_name=' + data.file_name;
                    layer.closeAll();
                }else{
                    console.log(data.msg);
                    layer.tips(data.msg, '#export', {
                        tips: [1, '#3595CC'],
                        time: 4000
                    });
                }
            }).error(function (data){
                layer.closeAll();
                layer.alert("发生错误!"+transform_error_message(data));
            });
        };

        //文件上传
        var uploader = $scope.uploader = new FileUploader({
            //url: '/vdp/system_log_import/',
            url: '/api/systemlogs/system_log_import/',
            queueLimit: 1,
            withCredentials: true,
            removeAfterUpload: true,
            headers: {'X-CSRFToken': $cookies.csrftoken}
        });

        uploader.onSuccessItem = function (fileItem, response, status, headers) {
            if (response.resultcode){
                layer.alert(response.msg, {icon: 2});
            }else {
                layer.alert(response.msg, {icon: 1}, function (index) {
                    $grid.reloadGrid(grid_selector);
                    layer.close(index);
                });
            }
        };

    }
]);

//修改密码
vdpAppControllers.controller('changepwdController', ["$scope", "$http", "$window", "$cookies",
    function ($scope, $http, $window, $cookies){
        $scope.pwd_old = null;
        $scope.pwd_new = null;
        $scope.pwd_check = null;

        $scope.change = function (){
            if ($scope.pwd_old == null || $scope.pwd_new == null || $scope.pwd_check == null){
                $window.layer.alert('对不起输入的信息不完整!');
            }else{
                if($scope.pwd_new != $scope.pwd_check){
                    $window.layer.alert('新密码两次输入的不一样！');
                }else if(!checkpwd($scope.pwd_new)){
                    $window.layer.alert("密码请包括大写字母、小写字母、数字、特殊字符中至少三种进行组合！", 3);
                    return;
                }else{
                    var send_pwd_data = {"pwd_old": $scope.pwd_old, "pwd_new":$scope.pwd_new};
                    $scope.pwd_new = CryptoJS.MD5($scope.pwd_new).toString();
                    $scope.pwd_check = CryptoJS.MD5($scope.pwd_new).toString();
                    $.ajax({
                        url: '/changepwd/',
                        method: 'put',
                        data: send_pwd_data,
                        headers: {'X-CSRFToken': $cookies.csrftoken}
                    }).then(function (data, status){
                        if(data.statuscode == 0){
                            $window.layer.alert(data.msg, {icon:1, end: function (){
                                $window.parent.location.href = data.link;
                            }}, function (index){
                                $window.layer.close(index);
                                $window.parent.location.href = data.link;
                            });
                        }else{
                            $window.layer.alert(data.msg, {icon:2});
                        }
                    }, function (data, status){
                        var message = transform_error_message(data);
                        $window.layer.alert(message, {icon:3});
                        return false;
                    })

                }
            }
        }
    }
]);
