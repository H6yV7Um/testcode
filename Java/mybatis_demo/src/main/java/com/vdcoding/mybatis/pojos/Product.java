package com.vdcoding.mybatis.pojos;


public class Product {
	private int id;
	private String productName;
	private Float price;
	private int type;
	
	public Product() {};
	
	public int getId(){
		return id;
	}
	public String getProductName(){
		return productName;
	}
	public void setProductName(String name){
		this.productName = name;
	}
	public Float getPrice(){
		return price;
	}
	public void setPrice(Float price){
		this.price = price;
	}
	public int getType(){
		return type;
	}
	public void setType(int type){
		this.type = type;
	}
	
	@Override
	public String toString(){
		return "Product-" + this.id;
	}

}
