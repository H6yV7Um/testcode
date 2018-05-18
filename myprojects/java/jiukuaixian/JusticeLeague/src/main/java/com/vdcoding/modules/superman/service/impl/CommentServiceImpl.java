package com.vdcoding.modules.superman.service.impl;

import java.util.HashMap;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.vdcoding.modules.superman.dao.CommentDao;
import com.vdcoding.modules.superman.pojos.GoodsComment;
import com.vdcoding.modules.superman.service.CommentService;


@Service
public class CommentServiceImpl implements CommentService{
	
	@Autowired
	private CommentDao commentsDao;
	
	public List<GoodsComment> getComments(int goodsId, String status, int from, int limit){
		return commentsDao.getComments(goodsId, status, from, limit);
	}
	
	public HashMap<String, Object> getCommnetsCount(int goodsId){
		return commentsDao.getCommentsCount(goodsId);
	}
}
