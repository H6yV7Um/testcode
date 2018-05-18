package com.vdcoding.modules.superman.service;

import java.util.HashMap;
import java.util.List;

import com.vdcoding.modules.superman.pojos.GoodsComment;

public interface CommentService {
	List<GoodsComment> getComments(int goodsId, String status, int from, int limit);
	HashMap<String, Object> getCommnetsCount(int goodsId);
}
