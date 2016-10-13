/**
 * Created by mudong on 2016/4/28.
 */
var vdpApp = angular.module('vdpApp',['vdpAppControllers','vdpAppServices']);

vdpApp.config(function($httpProvider){
    $httpProvider.defaults.withCredentials = true;
});

vdpApp.config(function($interpolateProvider){
    $interpolateProvider.startSymbol("{[{");
    $interpolateProvider.endSymbol("}]}");
});

vdpApp.config(["$httpProvider", function ($httpProvider) {
    var $injector = angular.injector(['ngCookies']);
    $injector.invoke(['$cookies', function ($cookies) {
        $httpProvider.defaults.headers.common['X-CSRFToken'] = $cookies.csrftoken;
    }])
}]);