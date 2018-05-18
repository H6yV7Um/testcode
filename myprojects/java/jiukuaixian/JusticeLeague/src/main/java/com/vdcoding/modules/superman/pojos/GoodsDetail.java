package com.vdcoding.modules.superman.pojos;

import java.io.Serializable;

public class GoodsDetail implements Serializable{
	private static final long serialVersionUID = 1L;
	
	private int id;
	private int goodsId;
	private int sequence;
	private String content;
	private int type;
	
	public int getId() {
		return id;
	}
	public void setId(int id){
		this.id =id;
	}

	public int getGoodsId() {
		return goodsId;
	}
	
	public void setGoodsId(int goodsId){
		this.goodsId = goodsId;
	}

	public int getSequence() {
		return sequence;
	}
	public void setSequence(int sequence) {
		this.sequence = sequence;
	}
	public String getContent() {
		return content;
	}
	public void setContent(String content) {
		this.content = content;
	}
	public int getType() {
		return type;
	}
	public void setType(int type) {
		this.type = type;
	}

	@Override
	public String toString() {
		StringBuilder builder = new StringBuilder();
		builder.append("GoodsDetail [id=").append(id).append(", goodsId=").append(goodsId).append("]");
		return builder.toString();
	}
	
	

}
