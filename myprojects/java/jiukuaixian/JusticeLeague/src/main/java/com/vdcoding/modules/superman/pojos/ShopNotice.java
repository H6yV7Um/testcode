package com.vdcoding.modules.superman.pojos;

import java.io.Serializable;
import java.util.Date;

public class ShopNotice implements Serializable{
	private static final long serialVersionUID = 1L;
	
	private int id;
	private int shopId;
	private String content;
	private boolean isShow;
	private boolean isHome;
	private Date createTime;
	
	
	public int getId() {
		return id;
	}
	public void setId(int id) {
		this.id = id;
	}
	public int getShopId() {
		return shopId;
	}
	public void setShopId(int shopId) {
		this.shopId = shopId;
	}
	public String getContent() {
		return content;
	}
	public void setContent(String content) {
		this.content = content;
	}
	public boolean isShow() {
		return isShow;
	}
	public void setShow(boolean isShow) {
		this.isShow = isShow;
	}
	public boolean isHome() {
		return isHome;
	}
	public void setHome(boolean isHome) {
		this.isHome = isHome;
	}
	public Date getCreateTime() {
		return createTime;
	}
	public void setCreateTime(Date createTime) {
		this.createTime = createTime;
	}
	
}
