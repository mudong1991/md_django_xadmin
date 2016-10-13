/**
 * Created by Administrator on 2016/9/8.
 */
$(function () {
   //让共同视图中的图片都可以做预览效果
    $('img').viewer();

    $(".grid-item").css('cursor', 'pointer');
    //单击一行进行选择
    $(".grid-item").on("click", function () {
        var select_input = $(this).children('.action-checkbox').children(".action-select");
        select_input.click();
        //阻止冒泡事件
        select_input.on('click', function (even) {
            even.stopPropagation();
        })
    });

});