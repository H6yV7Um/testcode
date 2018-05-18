package com.vdcoding.modules.superman.pojos;

import java.io.Serializable;
import java.text.SimpleDateFormat;
import java.time.LocalTime;
import java.util.Date;

import org.apache.ibatis.type.JdbcType;
import org.apache.ibatis.type.MappedJdbcTypes;
import org.apache.ibatis.type.MappedTypes;

public class ShopStatus implements Serializable{
	private static final long serialVersionUID = 1L;
	private SimpleDateFormat formatter = new SimpleDateFormat("HH:mm:ss");
	
	private String status;
	private boolean open;
	private String beginTime;
	private String endTime;
	
	public String getStatus() {
		return status;
	}
	public void setStatus(String status) {
		this.status = status;
	}
	public boolean isOpen() {
		return open;
	}
	public void setOpen(boolean open) {
		this.open = open;
	}
	public String getBeginTime() {
		return beginTime;
	}
	public void setBeginTime(String beginTime) {
//		this.beginTime = formatter.format(beginTime);
		this.beginTime = beginTime;
	}
	public String getEndTime() {
		return endTime;
	}
	public void setEndTime(String endTime) {
//		this.endTime = formatter.format(endTime);
		this.endTime = endTime;
	}
	
}
