package com.vdcoding.modules.superman.pojos;

import java.io.Serializable;

public class PagePlugin implements Serializable{

	private static final long serialVersionUID = 1L;
	
	private int id;
	private int pageId;
	private int shopId;
	private String type;
	private boolean isUse;
	
	public int getId() {
		return id;
	}
	public void setId(int id) {
		this.id = id;
	}
	public int getPageId() {
		return pageId;
	}
	public void setPageId(int pageId) {
		this.pageId = pageId;
	}
	public int getShopId() {
		return shopId;
	}
	public void setShopId(int shopId) {
		this.shopId = shopId;
	}
	public String getType() {
		return type;
	}
	public void setType(String type) {
		this.type = type;
	}
	public boolean getIsUse() {
		return isUse;
	}
	public void setIsUse(boolean isUse) {
		this.isUse = isUse;
	}
	

}
