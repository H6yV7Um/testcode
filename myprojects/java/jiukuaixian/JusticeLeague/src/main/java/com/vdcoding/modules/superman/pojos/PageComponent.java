package com.vdcoding.modules.superman.pojos;


import java.io.Serializable;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

import com.vdcoding.common.utils.SpringContextUtils;
import com.vdcoding.modules.superman.service.GoodsService;


public class PageComponent implements Serializable{

	private static final long serialVersionUID = 1L;
	
	GoodsService goodsService = (GoodsService) SpringContextUtils.getBean("goodsService");
	
	private int id;
	private String type;
	private int seq;
	private int pageId;
	private int shopId;
	private String title;
	private String param;
	private boolean isUse;
	private List<Object> data;
	
	public int getId() {
		return id;
	}
	public void setId(int id) {
		this.id = id;
	}
	public String getType() {
		return type;
	}
	public void setType(String type) {
		this.type = type;
	}
	public int getSeq() {
		return seq;
	}
	public void setSeq(int seq) {
		this.seq = seq;
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
	public String getTitle() {
		return title;
	}
	public void setTitle(String title) {
		this.title = title;
	}
	
	public String getParam() {
		return param;
	}
	public void setParam(String param) {
		this.param = param;
	}
	public boolean getIsUse() {
		return isUse;
	}
	public void setIsUse(boolean isUse) {
		this.isUse = isUse;
	}
	public List<Object> getData() {
		return data;
	}
	public void setData(List<Object> data) {
		switch (this.id) {
		//推荐商品
		case 8:
			this.data = goodsService.getRecommendGoods(1);
			break;
		//白酒精选
		case 9:
			this.data = goodsService.getRecommendGoods(2);
			break;
		//工具栏
		case 15:
			this.data = splitDataList(data);
			break;
		default:
			this.data = data;
			break;
		}
	}
	/*
	 * @return 返回一个新的列表，其元素为长度为limit的子列表
	 */
	public static List<Object> splitDataList(List<Object> data){
		int limit = 4;
		int batch = data.size()/4;
		List<Object> result = new ArrayList<>();
		
		if(batch <= 0){
			result.add(data);
			return result;
		}
		
		for(int i=0; i<batch; i++){
			List<Object> subList = new ArrayList<>(data.subList(0, limit));
			result.add(subList);
			data.subList(0, limit).clear();
		}
		if(!data.isEmpty()){
			result.add(data);
		}
		return result;
	}
	
	public static void main(String...args){
		Object[] test = {1,5,6};
		List<Object> list = new ArrayList<>(Arrays.asList(test));
		System.out.println(PageComponent.splitDataList(list));
	}
	
	
}
