package com.vdcoding.modules.superman.dao;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;
import org.apache.ibatis.annotations.Param;

import com.vdcoding.modules.superman.pojos.Goods;


@Mapper
public interface GoodsDao {
	
	Goods getGoodsById(int goodsId);
	List<Goods> getGoods(
			@Param("categoryId") int categoryId, 
			@Param("content")String content,
			@Param("from")int from, 
			@Param("limit")int limit);
	
	List<Object> getRecommendGoods(int categoryId);
}
