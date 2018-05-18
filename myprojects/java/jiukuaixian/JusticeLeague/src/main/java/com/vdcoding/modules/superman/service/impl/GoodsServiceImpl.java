package com.vdcoding.modules.superman.service.impl;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.vdcoding.modules.superman.dao.GoodsDao;
import com.vdcoding.modules.superman.pojos.Goods;
import com.vdcoding.modules.superman.service.GoodsService;


@Service("goodsService")
public class GoodsServiceImpl implements GoodsService{
	
	@Autowired
	private GoodsDao goodsDao;
	
	public Goods getGoodsById(int goodsId){
		return goodsDao.getGoodsById(goodsId);
	}
	
	public List<Goods> getGoods(int catetoryId, String content, int from, int limit){
		return goodsDao.getGoods(catetoryId, content, from, limit);
	}
	
	public List<Object> getRecommendGoods(int categoryId){
		return goodsDao.getRecommendGoods(categoryId);
	}
	
}
