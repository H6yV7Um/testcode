package com.vdcoding.modules.superman.utils;

import java.net.URI;
import java.util.HashMap;

import com.alibaba.fastjson.JSON;
import com.vdcoding.common.utils.HttpClientUtil;

/*
 * wepy工具类
 * @author yinzhixin
 */
public class WepyUtil {
	/*
	 * 调用微信api获取用户的openid和session_key
	 * @return 
	 * 		调用成功则返回包含openid和session_key
	 * 		调用失败则返回包含errcode和errmsg
	 */
	@SuppressWarnings("unchecked")
	public static HashMap<String, Object> getSessionKey(String loginCode) throws Exception{
		String appId = "wxbf987ab48beeeec3";
		String appSecret = "8485eaf6074668b9223f493224e1e6e4";
		String url_template = "https://api.weixin.qq.com/sns/jscode2session?appid=%1$s&secret=%2$s&js_code=%3$s&grant_type=authorization_code";
		URI url = new URI(String.format(url_template, appId, appSecret, loginCode));
		String result = HttpClientUtil.doGet(url);
		return JSON.parseObject(result, HashMap.class);
	}
	
	public static void main(String[] args){
		try {
			HashMap<String, Object> result = getSessionKey("test");
			System.out.println(result.get("errcode").toString() + result.get("errmsg").toString());
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}
}
