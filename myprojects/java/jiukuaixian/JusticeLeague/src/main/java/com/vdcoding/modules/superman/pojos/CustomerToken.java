package com.vdcoding.modules.superman.pojos;

import java.io.Serializable;
import java.util.Date;

public class CustomerToken implements Serializable{

	private static final long serialVersionUID = 1L;
	
	private int customerId;
	private String token;
	private Date expireTime;
	private Date updateTime;
	
	public int getCustomerId() {
		return customerId;
	}
	public void setCustomerId(int customerId) {
		this.customerId = customerId;
	}
	public String getToken() {
		return token;
	}
	public void setToken(String token) {
		this.token = token;
	}
	public Date getExpireTime() {
		return expireTime;
	}
	public void setExpireTime(Date expireTime) {
		this.expireTime = expireTime;
	}
	public Date getUpdateTime() {
		return updateTime;
	}
	public void setUpdateTime(Date updateTime) {
		this.updateTime = updateTime;
	}
	
	
}
