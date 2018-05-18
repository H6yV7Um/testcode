package com.vdcoding.modules.superman.pojos;

import java.io.Serializable;
import java.util.Date;

public class ComponentTarget implements Serializable{
	private static final long serialVersionUID = 1L;
	
	private int id;
	private String content;
	private int categoryId;
	private Date createTime;
	
	public int getId() {
		return id;
	}
	public void setId(int id) {
		this.id = id;
	}
	public String getContent() {
		return content;
	}
	public void setContent(String content) {
		this.content = content;
	}
	public int getCategoryId() {
		return categoryId;
	}
	public void setCategoryId(int categoryId) {
		this.categoryId = categoryId;
	}
	public Date getCreateTime() {
		return createTime;
	}
	public void setCreateTime(Date createTime) {
		this.createTime = createTime;
	}
	
}
