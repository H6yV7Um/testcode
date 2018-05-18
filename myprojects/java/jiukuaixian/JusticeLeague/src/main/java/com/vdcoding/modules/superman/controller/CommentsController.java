package com.vdcoding.modules.superman.controller;

import java.util.HashMap;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import com.vdcoding.modules.superman.common.BaseResponse;
import com.vdcoding.modules.superman.pojos.GoodsComment;
import com.vdcoding.modules.superman.service.impl.CommentServiceImpl;


@RestController
@RequestMapping(path="/customer/comments")
public class CommentsController {
	@Autowired
	CommentServiceImpl commentsService;
	
	@RequestMapping(path="")
	public BaseResponse getComments(@RequestParam(name="goods_id")int goodsId, 
			@RequestParam(name="status", defaultValue="ALL") String status,
			@RequestParam(name="from", defaultValue="0") int from,
			@RequestParam(name="limit", defaultValue="10")int limit){
		List<GoodsComment> comments = commentsService.getComments(goodsId, status, from, limit);
		return new BaseResponse(comments);
	}
	
	@RequestMapping(path="/count")
	public BaseResponse getCommentsCount(@RequestParam(name="goods_id")int goodsId){
		HashMap<String, Object> commentsCount = commentsService.getCommnetsCount(goodsId);
		return new BaseResponse(commentsCount);
	}
}
