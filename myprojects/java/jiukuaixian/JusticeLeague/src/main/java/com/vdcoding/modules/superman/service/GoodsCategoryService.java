package com.vdcoding.modules.superman.service;

import java.util.List;

import com.vdcoding.modules.superman.pojos.GoodsCategory;

public interface GoodsCategoryService {
	List<GoodsCategory> getShowCategory(int shopId);
	default int updateCategory(int cid){
		return 0;
	};
}
