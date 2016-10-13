/**
 * Created by Administrator on 2016/4/28.
 */
var vdpAppServices = angular.module("vdpAppServices", ["ngResource"])

// jqGrid相关的服务
vdpAppServices.service("$grid", function () {
    return {
        // 获取表格对象
        "instance": function (grid_selector) {
            return $(grid_selector);
        },
        // 初始化表格
        "init": function (grid_selector, pager_selector, data_url, col_models, extra_params) {
            var int_params = {
                url: data_url,
                datatype: "json",
                height: '100%',
                colModel: col_models,
                autowidth: true,
                multiselect: true,
                pager: pager_selector,
                viewrecords: true,
                rowNum: 10,
                rowList: [10, 15, 20, 30],
                loadtext: "加载中...",
                rownumbers: true
            };
            if (extra_params) {
                $.extend(int_params, extra_params)
            }
            $(grid_selector).jqGrid(int_params).navGrid(pager_selector, {
                edit : false,
                add : false,
                del : false,
                search: false,
                refresh:true,
            });
        },
        // 获取选中的行的数据中的ID属性
        "getSelectedRowIDs": function (grid_selector) {
            return $(grid_selector).jqGrid("getGridParam", "selarrrow");
        },
        // 根据数据ID来获取整行的数据。
        "getRowDataByID": function (grid_selector, row_id) {
            return $(grid_selector).jqGrid("getRowData", row_id);
        },
        //获取所有行数据
        "getAllRowIds": function (grid_selector){
            return $(grid_selector).jqGrid("getDataIDs");
        },
        "checkRowSelected": function (grid_selector, multiple) {
            var ids = this.getSelectedRowIDs(grid_selector);
            if (ids && ids.length > 0) {
                if (!multiple) {
                    if (ids.length > 1) {
                        layer.alert("只能选择一行");
                        return false;
                    }
                } else {
                    layer.alert("您未选择任何内容");
                    return false;
                }
            }
            return true;
        },
        "reloadGrid": function (grid_selector) {
            $(grid_selector).trigger("reloadGrid")
        },
        // 加载指定的页码
        "loadPrePage": function (grid_selector) {
            // jqGrid在删除了整页数据后重新加载当前页会出错，所以需要额外处理，直接显示第一页。
                var current_page = $(grid_selector).jqGrid("getGridParam", "total");
                if (current_page > 1) {
                    current_page = parseInt(current_page) - 1
                } else {
                    current_page = 1
                }
                $(grid_selector).jqGrid("setGridParam", {"page": current_page});
                setTimeout(function () {
                    $(grid_selector).trigger("reloadGrid")
                }, 1000);
        }

    }
});