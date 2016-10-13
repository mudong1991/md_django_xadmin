/**
 * Created by Administrator on 2016/5/9.
 */

//layer弹窗密码强度检查
function check(value){
    var strongRegex = new RegExp("^(?=.{8,})(?=.*[A-Z])(?=.*[a-z])(?=.*[0-9])(?=.*\W).*$", "g");
    var mediumRegex = new RegExp("^(?=.{7,})(((?=.*[A-Z])(?=.*[a-z]))|((?=.*[A-Z])(?=.*[0-9]))|((?=.*[a-z])(?=.*[0-9]))).*$", "g");
    var enoughRegex = new RegExp("(?=.{6,}).*", "g");

    var pw_check = $("#pw_check");
    var pw_strength_bar = $("#pw_check_bar");
    var pw_strength_text = $("#pw_check_text");
    var enter_btn = $("#layer_confirm");

    if(value.length == 0){
        pw_check.hide();
    }else{
        pw_check.show();
    }

    if (false == enoughRegex.test(value) || value.length == 0)
    {
        pw_strength_bar.css({
            "width":"25%",
            "background-color": "#d9534f"
        });
        enter_btn.attr("disabled","disabled");
        pw_strength_text.html('太短');
    }
    else if (strongRegex.test(value))
    {
        pw_strength_bar.css({
            "width":"100%",
            "background-color": "#5CB85C",
        });
        enter_btn.removeAttr("disabled");
        pw_strength_text.html('强');
    }
    else if (mediumRegex.test(value))
    {
        pw_strength_bar.css({
            "width":"75%",
            "background-color": "#5BC0DE"
        });
        enter_btn.removeAttr("disabled");
        pw_strength_text.html('中');
    }
    else
    {
        pw_strength_bar.css({
            "width":"50%",
            "background-color": "#F0AD4E"
        });
        enter_btn.removeAttr("disabled");
        pw_strength_text.html('弱');
    }

    if (value.length >= 20){
        pw_strength_bar.css({
            "width":"100%",
            "background-color": "#d9534f"
        });
        enter_btn.attr("disabled","disabled");
        pw_strength_text.html('太长');
    }
    return true;
}

$(document).ready(function () {
    $('input').eq(0).focus();

    //layer弹窗取消
    $("#layer_cancel").on("click", function(){
        var index = parent.layer.getFrameIndex(window.name); //先得到当前iframe层的索引
        parent.layer.close(index); //再执行关闭
    });
    
    $("#pw_input").keydown(function(){
        check($(this).val());
    }).keyup(function(){
        check($(this).val());
    }).keypress(function(){
        check($(this).val());
    }).change(function(){
        check($(this).val());
    })

});