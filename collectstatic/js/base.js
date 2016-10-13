/**
 * Created by mudong on 2016/8/21.
 */
/**
 * Created by mu on 2016/7/26.
 */
(function () {
    root = this;
    v = root.MD = {};
    v.util = {};
    v.util.showMessage = function (msg, type, callback) {
        window.layer.alert(msg, {icon: type}, function () {
            callback();
        });
    }
})();

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

//错误信息解析
function transform_error_message(data) {
    var message = '';
     if (data.hasOwnProperty("detail")){
         data_str = data.detail;
         data_str = data_str.replace("u\'", "\'");
         message =  eval("("+data_str+")").msg;
         if ($.isArray(message)){
            message = message.join("<br/>");
         }
         return message
     }
    else if (data.hasOwnProperty("responseText")){
         var data_str = data.responseText;
         return data_str
     }

    return message
}

/* ***************************************
 * jqGrid 相关控制函数 -->
 * ***************************************/
// 初始化
function jqGrid_InitGrid(grid_selector, pager_selector, data_url, col_models, extra_params) {
    var init_param = {
        url: data_url,
        datatype: 'json',
        height: "100%",
        colModel: col_models,
        autowidth: true,
        multiselect: true,
        pager: pager_selector,
        viewrecords: true,
        rowNum: 15,
        rowList: [10, 15, 20, 30],
        rownumbers: true,
        autoencode: false
    };
    if (extra_params) {
        $.extend(init_param, extra_params);
    }
    $(grid_selector).jqGrid(init_param);
}

//获取选定的行
function jqGrid_GetSelectedRowIds(grid_selector) {
    return $(grid_selector).jqGrid('getGridParam', 'selarrrow');
}

//获取指定行的数据
function jqGrid_GetRowDataById(grid_selector, row_id) {
    return $(grid_selector).jqGrid('getRowData', row_id);
}

// 检查选定的行
function jqGrid_CheckRowSelected(grid_selector, multiple) {
    var ids = jqGrid_GetSelectedRowIds(grid_selector);
    if (ids && ids.length > 0) {
        if (multiple) {

        }
        else {
            // 单行
            if (ids.length > 1) {
                window.top.layer.alert('您只能选择一行！');
                return false;
            }
        }
    }
    else {
        window.top.layer.alert('您未选择任何行！');
        return false;
    }
    return true;
}

//直接获取选定行的数据,前提是已经选择了某一行,多行获取的为最后一个选项的数据,请选使用jqGrid_CheckRowSelected再调用jqGrid_GetSelectRowData
function jqGrid_GetSelectRowData(grid_selector) {
    return $(grid_selector).jqGrid('getRowData', $(grid_selector).jqGrid('getGridParam', 'selrow'));
}
/* ***************************************
 * <-- jqGrid 相关控制函数
 * ***************************************/


/*解密*/
function decToUtf(data) {
    var _key = CryptoJS.enc.Utf8.parse('!@#$%^&*()_+|%^&');
    var _iv = CryptoJS.enc.Utf8.parse('!@#$%^&*()_+|%^&');
    var decrypted_data = CryptoJS.AES.decrypt(data, _key, {
        iv: _iv,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    });
    var uft8_data = decrypted_data.toString(CryptoJS.enc.Utf8);
    return uft8_data;
}

/* 解析后台传给前端的错误信息 */
var parseErrorMessage = function (response) {
    var data = '';
    if (response.hasOwnProperty("responseText")) {
        data = $.parseJSON(response.responseText);
    }
    if (data.hasOwnProperty("msg")){
        return data.msg;
    }
    if (data.hasOwnProperty('detail')){
        return data.detail;
    }
    if (data.hasOwnProperty('message')){
        return data.message;
    }
    return data;
};

var transformErrorMessage = function (message) {
    if ($.isArray(message)) {
        return message.join("<br/>")
    }
    return message
};

var alertErrorMessage = function (data, failOpName, callback) {
    var msg = parseErrorMessage(data);
    msg = transformErrorMessage(msg);
    failOpName = failOpName || "数据提交";
    if (callback && $.isFunction(callback)) {
        window.layer.alert(failOpName + "失败！\n失败原因：<br/>" + msg + "！", 3, "信息", function () {
            window.layer.closeAll();
            callback();
        });
    }
    else {
        window.layer.alert(failOpName + "失败！\n失败原因：<br/>" + msg + "！", 3);
    }
};

/* ***************************************
 * Ajax 辅助方法 -->
 * ***************************************/
// 生成Ajax队列对象,附加start_queue方法,调用该方法将Ajax请求加入队列,启动Ajax请求.
function ajax_make_queue(load_msg, failed_operation, ajax_settings, success_action, after_failed_action, before_failed_action) {
    var allow_queue = new $.qjax({
        timeout: 15000,
        onStart: function () {
            layer.load(load_msg);
        },
        onStop: function () {
            // 处理完成,可能最后一个失败,其他时候失败不会走到onStop
            if (!allow_queue.IsError) {
                layer.closeAll();
                if (success_action && $.isFunction(success_action)) {
                    success_action()
                }
            }
        },
        onError: function (req) {
            allow_queue.IsError = true;
            allow_queue.Clear();
            layer.closeAll();
            if (before_failed_action && $.isFunction(before_failed_action)) {
                before_failed_action(req, this.data || this)
            }
            else {
                alertErrorMessage(req, failed_operation, function () {
                    if (after_failed_action && $.isFunction(after_failed_action)) {
                        after_failed_action()
                    }
                });
            }
        }
    });

    // 启动Ajax队列
    allow_queue.start_queue = function () {
        $.each(ajax_settings, function () {
            allow_queue.Queue(this);
        });
    };

    // 返回队列对象
    return allow_queue;
}
/* ***************************************
 * <-- Ajax 辅助方法
 * ***************************************/
// jquery将obj对象转成url方法

var parseParam=function(param, key){
  var paramStr="";
  if(param instanceof String||param instanceof Number||param instanceof Boolean){
    paramStr+="&"+key+"="+encodeURIComponent(param);
  }else{
    $.each(param,function(i){
      var k=key==null?i:key+(param instanceof Array?"["+i+"]":"."+i);
      paramStr+='&'+parseParam(this, k);
    });
  }
  return paramStr.substr(1);
};