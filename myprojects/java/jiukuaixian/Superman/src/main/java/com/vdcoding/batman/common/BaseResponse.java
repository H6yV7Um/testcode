package com.vdcoding.batman.common;


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
