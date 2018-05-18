package com.vdcoding.modules.superman.service;

import java.util.List;

import com.vdcoding.modules.superman.pojos.Goods;

public interface GoodsService {
	
	Goods getGoodsById(int goodsId);
	List<Goods> getGoods(int catetoryId, String content, int from, int limit);
	List<Object> getRecommendGoods(int categoryId);
	
}
