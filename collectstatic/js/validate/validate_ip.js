/**
 * Created by jane on 2015/11/20.
 */

//判断IP地址合法性(可带端口)
function checkIP(ip)
 {
     var ip_arry = ip.split(":");
     if(ip_arry.length > 2){
        return false;
     }
     if(ip_arry.length == 2){
         port = ip_arry[1];
         var reg_p = /^[1-9]\d*$/;
         if(!reg_p.test(port)){
             return false;
         }
     }
     var reg =  /^(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])\.(\d{1,2}|1\d\d|2[0-4]\d|25[0-5])$/;
     return reg.test(ip_arry[0]);
 }

//判断掩码合法性
function checkMask(mask)
 {
     obj=mask;
     var exp=/^(254|252|248|240|224|192|128|0)\.0\.0\.0|255\.(254|252|248|240|224|192|128|0)\.0\.0|255\.255\.(254|252|248|240|224|192|128|0)\.0|255\.255\.255\.(254|252|248|240|224|192|128|0)$/;
     var reg = obj.match(exp);
     if(reg==null)
     {
          return false; //"非法"
     }
      else
     {
          return true; //"合法"
     }
 }

//判断掩码、ip、网关合法性
function checkIpMaskGw( static_ip, static_mask, static_gw ){
    if (static_ip=='')
    {
        return false;
    }else if(!checkIP(static_ip))
    {
        return false;
    }

    if(static_mask=='')
    {
        return false;
    }else if(!checkMask(static_mask)){
        return false;
    }

    if(static_gw=='')
    {
        return false;
    }else if(!checkIP(static_gw))
    {
        return false;
    }
    if(static_ip == static_mask || static_mask == static_gw  || static_mask == static_gw)
    {
        return false; //3个地址不能相同
    }
    var static_ip_arr = new Array;
    var static_mask_arr = new Array;
    var static_gw_arr = new Array;

     static_ip_arr = static_ip.split(".");
     static_mask_arr = static_mask.split(".");
     static_gw_arr = static_gw.split(".");

     var res0 = parseInt(lan_ip_arr[0]) & parseInt(static_mask_arr[0]);
     var res1 = parseInt(lan_ip_arr[1]) & parseInt(static_mask_arr[1]);
     var res2 = parseInt(lan_ip_arr[2]) & parseInt(static_mask_arr[2]);
     var res3 = parseInt(lan_ip_arr[3]) & parseInt(static_mask_arr[3]);

     var res0_gw = parseInt(static_gw_arr[0]) & parseInt(static_mask_arr[0]);
     var res1_gw = parseInt(static_gw_arr[1]) & parseInt(static_mask_arr[1]);
     var res2_gw = parseInt(static_gw_arr[2]) & parseInt(static_mask_arr[2]);
     var res3_gw = parseInt(static_gw_arr[3]) & parseInt(static_mask_arr[3]);

     if(res0==res0_gw && res1==res1_gw && res2==res2_gw  && res3==res3_gw)
     {

     }else{
         //IP地址与子网掩码、网关地址不匹配
         return false;
     }

    return true;
}



