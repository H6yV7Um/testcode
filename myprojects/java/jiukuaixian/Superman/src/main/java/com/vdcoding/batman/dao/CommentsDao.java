package com.vdcoding.batman.dao;

import java.util.HashMap;
import java.util.List;

import org.apache.ibatis.session.SqlSessionFactory;
import org.springframework.stereotype.Repository;

import com.vdcoding.batman.mapper.CommentsMapper;
import com.vdcoding.batman.pojos.Comments;


@Repository
public class CommentsDao extends BaseDao{
	
	private CommentsMapper mapper;
	
	public CommentsDao(SqlSessionFactory factory){
		super(factory);
		this.mapper = sqlSession.getMapper(CommentsMapper.class);
	}
	
	public List<Comments> getComments(int goodsId, int from, int limit){
		return mapper.getComments(goodsId, from, limit);
	}
	
	public HashMap<String, Object> getCommnetsCount(int goodsId){
		return mapper.getCommentsCount(goodsId);
	}
}
