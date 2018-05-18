package com.vdcoding.modules.superman.pojos;

import java.io.Serializable;
import java.util.Date;

public class Order implements Serializable{
	private static final long serialVersionUID = 1L;
	
	private int id;
	private int goodsId;
	private int customerId;
	private float dealPrice;
	private float finalPrice;
	private int paymentType;
	private int status;
	private Date orderTime;
	private Date paymentTime;
	private int couponUsedId;
	private String sellerNote;
	private String address;
	private String receiveName;
	private int receivePhone;
	private int shopId;
	private String shopName;
	private float postFee;
	private int orderType;
	private Date arriveTime;
	
	public int getId() {
		return id;
	}
	public void setId(int id) {
		this.id = id;
	}
	public int getGoodsId() {
		return goodsId;
	}
	public void setGoodsId(int goodsId) {
		this.goodsId = goodsId;
	}
	public int getCustomerId() {
		return customerId;
	}
	public void setCustomerId(int customerId) {
		this.customerId = customerId;
	}
	public int getStatus() {
		return status;
	}
	public void setStatus(int status) {
		this.status = status;
	}
	public float getDealPrice() {
		return dealPrice;
	}
	public void setDealPrice(float dealPrice) {
		this.dealPrice = dealPrice;
	}
	public float getFinalPrice() {
		return finalPrice;
	}
	public void setFinalPrice(float finalPrice) {
		this.finalPrice = finalPrice;
	}
	public int getPaymentType() {
		return paymentType;
	}
	public void setPaymentType(int paymentType) {
		this.paymentType = paymentType;
	}
	public Date getOrderTime() {
		return orderTime;
	}
	public void setOrderTime(Date orderTime) {
		this.orderTime = orderTime;
	}
	public Date getPaymentTime() {
		return paymentTime;
	}
	public void setPaymentTime(Date paymentTime) {
		this.paymentTime = paymentTime;
	}
	public int getCouponUsedId() {
		return couponUsedId;
	}
	public void setCouponUsedId(int couponUsedId) {
		this.couponUsedId = couponUsedId;
	}
	public String getSellerNote() {
		return sellerNote;
	}
	public void setSellerNote(String sellerNote) {
		this.sellerNote = sellerNote;
	}
	public String getAddress() {
		return address;
	}
	public void setAddress(String address) {
		this.address = address;
	}
	public String getReceiveName() {
		return receiveName;
	}
	public void setReceiveName(String receiveName) {
		this.receiveName = receiveName;
	}
	public int getReceivePhone() {
		return receivePhone;
	}
	public void setReceivePhone(int receivePhone) {
		this.receivePhone = receivePhone;
	}
	public int getShopId() {
		return shopId;
	}
	public void setShopId(int shopId) {
		this.shopId = shopId;
	}
	public String getShopName() {
		return shopName;
	}
	public void setShopName(String shopName) {
		this.shopName = shopName;
	}
	public float getPostFee() {
		return postFee;
	}
	public void setPostFee(float postFee) {
		this.postFee = postFee;
	}
	public int getOrderType() {
		return orderType;
	}
	public void setOrderType(int orderType) {
		this.orderType = orderType;
	}
	public Date getArriveTime() {
		return arriveTime;
	}
	public void setArriveTime(Date arriveTime) {
		this.arriveTime = arriveTime;
	}
	
	@Override
	public String toString() {
		StringBuilder builder = new StringBuilder();
		builder.append("Order [id=").append(id).append(", goodsId=").append(goodsId).append(", customerId=")
				.append(customerId).append(", finalPrice=").append(finalPrice).append("]");
		return builder.toString();
	}
	
}
