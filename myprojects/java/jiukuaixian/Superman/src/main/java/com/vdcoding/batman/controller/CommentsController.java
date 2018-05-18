package com.vdcoding.batman.controller;

import java.util.HashMap;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.vdcoding.batman.common.BaseResponse;
import com.vdcoding.batman.dao.CommentsDao;
import com.vdcoding.batman.pojos.Comments;

@RestController
@RequestMapping(path="/customer/comments")
public class CommentsController {
	@Autowired
	CommentsDao commentsDao;
	
	@RequestMapping(path="")
	public BaseResponse getComments(@RequestParam(name="goods_id")int goodsId, 
			@RequestParam(name="from", defaultValue="0") int from,
			@RequestParam(name="limit", defaultValue="10")int limit){
		List<Comments> comments = commentsDao.getComments(goodsId, from, limit);
		return new BaseResponse(comments);
	}
	
	@RequestMapping(path="/count")
	public BaseResponse getCommentsCount(@RequestParam(name="goods_id")int goodsId){
		HashMap<String, Object> commentsCount = commentsDao.getCommnetsCount(goodsId);
		return new BaseResponse(commentsCount);
	}
}
