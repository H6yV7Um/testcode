package com.vdcoding.modules.superman.pojos;

import java.io.Serializable;
import java.util.Date;

public class GoodsImage implements Serializable{
	private static final long serialVersionUID = 1L;
	
	private int id;
	private int goodsId;
	private String url;
	private Date createTime;
	
	public int getId() {
		return id;
	}
	
	public void setId(int id){
		this.id = id;
	}

	public int getGoodsId() {
		return goodsId;
	}
	
	public void setGoodsId(int goodsId){
		this.goodsId = goodsId;
	}

	public String getUrl() {
		return url;
	}
	public void setUrl(String url) {
		this.url = url;
	}
	public Date getCreateTime() {
		return createTime;
	}
	public void setCreateTime(Date createTime) {
		this.createTime = createTime;
	}

	@Override
	public String toString() {
		StringBuilder builder = new StringBuilder();
		builder.append("GoodsImage [id=").append(id).append(", goodsId=").append(goodsId).append("]");
		return builder.toString();
	}
	
}
