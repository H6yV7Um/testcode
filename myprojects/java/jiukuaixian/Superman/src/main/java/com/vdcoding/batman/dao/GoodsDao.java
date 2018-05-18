package com.vdcoding.batman.dao;

import java.util.List;

import org.apache.ibatis.session.SqlSessionFactory;
import org.springframework.stereotype.Repository;

import com.vdcoding.batman.mapper.GoodsMapper;
import com.vdcoding.batman.pojos.Goods;


@Repository
public class GoodsDao extends BaseDao {
	
	private GoodsMapper mapper;
	
	public GoodsDao(SqlSessionFactory factory){
		super(factory);
		this.mapper = sqlSession.getMapper(GoodsMapper.class);
	}
	
	public Goods getGoodsById(int goodsId){
		return mapper.getGoodsById(goodsId);
	}
	
	public List<Goods> getGoods(int catetoryId, String content, int from, int limit){
		return mapper.getGoods(catetoryId, content, from, limit);
	}
	
}
