package com.vdcoding.modules.superman.common;

public class BaseResponse {
    private int code;
    private String msg;
    private Object data;
    
    public BaseResponse(int code, String msg) {
        super();
        this.code = code;
        this.msg = msg;
    }
    
    public BaseResponse(Object object){
    	this.code = 0;
    	this.msg = "success";
    	this.data = object;
    }
    
    public static BaseResponse ok(){
    	BaseResponse response = new BaseResponse(0, "success");
    	return response;
    }
    
    public static BaseResponse ok(Object object){
    	BaseResponse response = new BaseResponse(object);
    	return response;
    }
    
    public static BaseResponse fail(String msg){
    	BaseResponse response = new BaseResponse(1, msg);
    	return response;
    }
    
    public static BaseResponse fail(Object object){
    	BaseResponse response = new BaseResponse(object);
    	return response;
    }
    
    public int getCode() {
        return code;
    }
    public void setCode(int code) {
        this.code = code;
    }
    public String getMsg() {
        return msg;
    }
    public void setMsg(String msg) {
        this.msg = msg;
    }
    public Object getData(){
    	return data;
    }
    public void setData(Object object){
    	this.data = object;
    }
}
