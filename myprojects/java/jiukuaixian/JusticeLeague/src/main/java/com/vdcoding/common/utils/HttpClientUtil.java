package com.vdcoding.common.utils;

import java.io.IOException;
import java.net.URI;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Map.Entry;


import org.apache.http.Consts;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.client.ResponseHandler;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.message.BasicNameValuePair;
import org.apache.http.util.EntityUtils;

import com.alibaba.fastjson.JSON;


/**
 * 基于HttpClient 4.5.2的发送HTTP请求的工具类，包括post和get方法
 * @author: yinzhixin
 * @date: 2018-05-10
 */
public class HttpClientUtil {
	/**
	 * 支持回调的post方法
	 * @param url	
	 * @param params	post参数
	 * @param rh	处理response的回调方法
	 * @throws IOException
	 */
	public static String doPost(URI url, Map<String, String> params, ResponseHandler<String> rh) throws IOException{
		CloseableHttpClient httpClient = HttpClients.createDefault();
		HttpPost httpPost = makeHttpPost(url, params);
		try {
			return httpClient.execute(httpPost, rh);
		} catch (Exception e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		finally {
			httpClient.close();
		}
		return null;
	}
	
	/**
	 * 普通的只带参数的post方法
	 * @param url
	 * @param params
	 * @throws IOException
	 */
	public static String doPost(URI url, Map<String, String> params) throws IOException{
		CloseableHttpClient httpClient = HttpClients.createDefault();
		HttpPost httpPost = makeHttpPost(url, params);
		try {
			HttpResponse response = httpClient.execute(httpPost);
			return EntityUtils.toString(response.getEntity());
		} catch (Exception e) {
			// TODO: handle exception
			e.printStackTrace();
		}
		finally {
			httpClient.close();
		}
		return null;
	}
	
	public static String doGet(URI url) throws Exception {
		CloseableHttpClient httpClient = HttpClients.createDefault();
		HttpGet httpGet = new HttpGet(url);
		try {
			HttpResponse response = httpClient.execute(httpGet);
			String result = EntityUtils.toString(response.getEntity());
			
			return result;
		}
		catch (Exception e) {
			e.printStackTrace();
		}
		finally {
			httpClient.close();
		}
		return null;
	}
	
	public static String doGet(URI url, ResponseHandler<String> rh) throws IOException{
		CloseableHttpClient httpClient = HttpClients.createDefault();
		HttpGet httpGet = new HttpGet(url);
		try {
			return httpClient.execute(httpGet, rh);
		}
		catch (Exception e) {
			e.printStackTrace();
		}
		finally {
			httpClient.close();
		}
		return null;
	}
	
	private static HttpPost makeHttpPost(URI url, Map<String, String> params){
		UrlEncodedFormEntity entity = null;
		HttpPost httpPost = new HttpPost(url);
		List<NameValuePair> form = new ArrayList<NameValuePair>();
		for (Entry<String, String> entry: params.entrySet()){
			form.add(new BasicNameValuePair(entry.getKey(), entry.getValue()));
		}
		if(form.size() > 0){
			entity = new UrlEncodedFormEntity(form, Consts.UTF_8);
		}
		httpPost.setEntity(entity);
		return httpPost;
	}
	
	
}
