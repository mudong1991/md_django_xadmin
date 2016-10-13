$(function () {
    //重新定义form-actions的悬浮效果
    var action_bar = $('.form-actions');
    action_bar.removeClass("fixed");
    if ($(window).scrollLeft() <= 768){
        action_bar.css("bottom", "60px");
    }
    $(window).resize(function () {
        if ($(window).scrollLeft() <= 768){
            action_bar.css("bottom", "60px");
        }
    })
});