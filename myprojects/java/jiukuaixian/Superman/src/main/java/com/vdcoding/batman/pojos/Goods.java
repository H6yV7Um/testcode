package com.vdcoding.batman.pojos;

import java.util.Date;
import java.util.List;

public class Goods {
	private int id;
	private String name;
	private String subhead;
	private int shopId;
	private int status;
	private float originalPrice;
	private float sellPrice;
	private int isRecommend;
	private int favoriteCount;
	private int categoryId;
	private int postType;
	private float postFee;
	private int salesVolume;
	private int totalStock;
	private Date createTime;
	private Date updateTime;
	private List<GoodsImage> images = null;
	private List<GoodsDetail> goodsDetails = null;
	
	public int getId(){
		return this.id;
	}
	
	public void setId(int id){
		this.id = id;
	}
	
	public String getName(){
		return this.name;
	}
	public void setName(String name){
		this.name = name;
	}
	
	public String getSubhead(){
		return subhead;
	}
	public void setSubhead(String subhead){
		this.subhead = subhead;
	}

	public int getShopId() {
		return shopId;
	}

	public void setShopId(int shopId) {
		this.shopId = shopId;
	}

	public int getStatus() {
		return status;
	}

	public void setStatus(int status) {
		this.status = status;
	}

	public float getOriginalPrice() {
		return originalPrice;
	}

	public void setOriginalPrice(float originalPrice) {
		this.originalPrice = originalPrice;
	}

	public float getSellPrice() {
		return sellPrice;
	}

	public void setSellPrice(float sellPrice) {
		this.sellPrice = sellPrice;
	}

	public int getIsRecommend() {
		return isRecommend;
	}

	public void setIsRecommend(int isRecommend) {
		this.isRecommend = isRecommend;
	}

	public int getFavoriteCount() {
		return favoriteCount;
	}

	public void setFavoriteCount(int favoriteCount) {
		this.favoriteCount = favoriteCount;
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

	public Date getUpdateTime() {
		return updateTime;
	}

	public void setUpdateTime(Date updateTime) {
		this.updateTime = updateTime;
	}
	
	public int getPostType() {
		return postType;
	}

	public void setPostType(int postType) {
		this.postType = postType;
	}

	public float getPostFee() {
		return postFee;
	}

	public void setPostFee(float postFee) {
		this.postFee = postFee;
	}

	public int getSalesVolume() {
		return salesVolume;
	}

	public void setSalesVolume(int salesVolume) {
		this.salesVolume = salesVolume;
	}

	public int getTotalStock() {
		return totalStock;
	}

	public void setTotalStock(int totalStock) {
		this.totalStock = totalStock;
	}

	public List<GoodsImage> getImages(){
		return images;
	}
	public void setImages(List<GoodsImage> images){
		this.images = images;
	}
	
	public List<GoodsDetail> getGoodsDetails(){
		return goodsDetails;
	}
	public void setGoodsDetails(List<GoodsDetail> goodsDetails){
		this.goodsDetails = goodsDetails;
	}

	@Override
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result + id;
		return result;
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		Goods other = (Goods) obj;
		if (id != other.id)
			return false;
		return true;
	}

	@Override
	public String toString() {
		StringBuilder builder = new StringBuilder();
		builder.append("Goods [id=");
		builder.append(id);
		builder.append(", name=");
		builder.append(name);
		builder.append(", status=");
		builder.append(status);
		builder.append(", originalPrice=");
		builder.append(originalPrice);
		builder.append(", sellPrice=");
		builder.append(sellPrice);
		builder.append(", favoriteCount=");
		builder.append(favoriteCount);
		builder.append(", categoryId=");
		builder.append(categoryId);
		builder.append("]");
		return builder.toString();
	}	
	
}
