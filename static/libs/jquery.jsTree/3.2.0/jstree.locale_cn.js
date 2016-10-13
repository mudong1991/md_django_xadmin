; (function ($) {
    /**
     * jsTree Chinese Translation
     * Benjamin
     * Dual licensed under the MIT and GPL licenses:
     * http://www.opensource.org/licenses/mit-license.php
     * http://www.gnu.org/licenses/gpl.html
    **/
    //  汉化
    $.jstree = $.jstree || {};

    $.jstree.defaults.contextmenu.show_contextmenu_at_disabled_node = false;

    $.jstree.defaults.contextmenu.items = function (o, cb) { // Could be an object directly
        // 禁用状态的节点不显示右键菜单.
        if (o) {
            if (o.state.disabled) {
                if (!$.jstree.defaults.contextmenu.show_contextmenu_at_disabled_node) {
                    return null;
                }
                return {
                    "create": {
                        "separator_before": false,
                        "separator_after": true,
                        "_disabled": false, //(this.check("create_node", data.reference, {}, "last")),
                        "label": "新建",
                        "action": function (data) {
                            var inst = $.jstree.reference(data.reference),
                                obj = inst.get_node(data.reference);
                            inst.create_node(obj, {}, "last", function (new_node) {
                                setTimeout(function () { inst.edit(new_node); }, 0);
                            });
                        }
                    }
                };
            }
        }

        // 正常情况下返回的中文菜单
        return {
            "create": {
                "separator_before": false,
                "separator_after": false,
                "_disabled": false, //(this.check("create_node", data.reference, {}, "last")),
                "label": "新建",
                "action": function (data) {
                    var inst = $.jstree.reference(data.reference),
                        obj = inst.get_node(data.reference);
                    inst.create_node(obj, {}, "last", function (new_node) {
                        setTimeout(function () { inst.edit(new_node); }, 0);
                    });
                }
            },
            "rename": {
                "separator_before": false,
                "separator_after": false,
                "_disabled": false, //(this.check("rename_node", data.reference, this.get_parent(data.reference), "")),
                "label": "编辑",
                /*
                "shortcut"			: 113,
                "shortcut_label"	: 'F2',
                "icon"				: "glyphicon glyphicon-leaf",
                */
                "action": function (data) {
                    var inst = $.jstree.reference(data.reference),
                        obj = inst.get_node(data.reference);
                    if (obj) {
                        if (!obj.state.disabled) {
                            inst.edit(obj);
                        }
                    }
                }
            },
            "remove": {
                "separator_before": false,
                "icon": false,
                "separator_after": false,
                "_disabled": false, //(this.check("delete_node", data.reference, this.get_parent(data.reference), "")),
                "label": "删除",
                "action": function (data) {
                    window.top.layer.confirm("确定要删除所选节点（含子节点）？", function (index) {
                        window.top.layer.close(index);
                        var inst = $.jstree.reference(data.reference),
                            obj = inst.get_node(data.reference);
                        if (obj) {
                            if (!obj.state.disabled) {
                                if (inst.is_selected(obj)) {
                                    inst.delete_node(inst.get_selected());
                                } else {
                                    inst.delete_node(obj);
                                }
                            }
                        }
                    }, function () {

                    });
                }
            }
        };
    };
})(jQuery);