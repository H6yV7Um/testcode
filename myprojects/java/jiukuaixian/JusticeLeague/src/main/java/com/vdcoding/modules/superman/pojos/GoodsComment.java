package com.vdcoding.modules.superman.pojos;

import java.io.Serializable;
import java.util.Date;

public class GoodsComment implements Serializable{
	
	private static final long serialVersionUID = 1L;
	
	private int id;
	private int orderId;
	private int customerId;
//	private int shopId;
	private int goodsId;
	//goods应该是至少包含images和name的对象,前期先不返回该字段，即商品评价列表不会展示商品的图片和名称
//	private String goods;
	private int star;
	private String comment;
	private String images;
	private Date createTime;
	private Date updateTime;
	private Date orderTime;
	private Customer customer;
	
	public int getId() {
		return id;
	}
	public void setId(int id) {
		this.id = id;
	}
	public int getOrderId() {
		return orderId;
	}
	public void setOrderId(int orderId) {
		this.orderId = orderId;
	}
	public int getCustomerId() {
		return customerId;
	}
	public void setCustomerId(int customerId) {
		this.customerId = customerId;
	}
//	public int getShopId() {
//		return shopId;
//	}
//	public void setShopId(int shopId) {
//		this.shopId = shopId;
//	}
	public int getGoodsId() {
		return goodsId;
	}
	public void setGoodsId(int goodsId) {
		this.goodsId = goodsId;
	}
	public int getStar() {
		return star;
	}
	public void setStar(int star) {
		this.star = star;
	}
	public String getComment() {
		return comment;
	}
	public void setComment(String comment) {
		this.comment = comment;
	}
	public String getImages() {
		return images;
	}
	public void setImages(String images) {
		this.images = images;
	}
	public Date getCreateTime() {
		return createTime;
	}
	public void setCreateTime(Date createTime) {
		this.createTime = createTime;
	}
	public Date getUpdateTime() {
		return updateTime;
	}
	public void setUpdateTime(Date updateTime) {
		this.updateTime = updateTime;
	}
	public Date getOrderTime() {
		return orderTime;
	}
	public void setOrderTime(Date orderTime) {
		this.orderTime = orderTime;
	}

	public Customer getCustomer() {
		return customer;
	}
	public void setCustomer(Customer customer) {
		this.customer = customer;
	}
	
	@Override
	public String toString() {
		StringBuilder builder = new StringBuilder();
		builder.append("Comments [id=").append(id).append(", orderId=").append(orderId).append(", customerId=")
				.append(customerId).append(", goodsId=").append("]");
		return builder.toString();
	}
	

}
