package com.vdcoding.modules.superman.service.impl;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import com.vdcoding.modules.superman.dao.GoodsCategoryDao;
import com.vdcoding.modules.superman.pojos.GoodsCategory;
import com.vdcoding.modules.superman.service.GoodsCategoryService;

@Service
public class GoodsCategoryServiceImpl implements GoodsCategoryService{
	@Autowired
	GoodsCategoryDao goodsCategoryDao;
	
	public List<GoodsCategory> getShowCategory(int shopId){
		return goodsCategoryDao.getShowCategory(shopId);
	}
	
}
