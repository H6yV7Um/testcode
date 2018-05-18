package com.vdcoding.modules.superman.service.impl;

import java.time.LocalTime;
import java.util.Date;
import java.util.HashMap;

import org.apache.commons.lang.time.DateUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.vdcoding.modules.superman.dao.GoodsCategoryDao;
import com.vdcoding.modules.superman.dao.ShopDao;
import com.vdcoding.modules.superman.dao.ShopNoticeDao;
import com.vdcoding.modules.superman.dao.ShopStatusDao;
import com.vdcoding.modules.superman.pojos.ShopStatus;
import com.vdcoding.modules.superman.service.ShopService;

@Service
public class ShopServiceImpl implements ShopService{
	@Autowired
	ShopDao shopDao;
	@Autowired
	ShopStatusDao shopStatusDao;
	@Autowired
	ShopNoticeDao shopNoticeDao;
	@Autowired
	GoodsCategoryDao goodsCategoryDao;
	
	@Transactional
	public HashMap<String, Object> getFullShopInfo(int shopId){
		HashMap<String, Object> result = new HashMap<>();
		result.put("shop", shopDao.getShopById(shopId));
		result.put("shopStatusInfo", shopStatusDao.getByShopId(shopId));
		result.put("notices", shopNoticeDao.getByShopId(shopId));
		result.put("goodsInnerCategories", goodsCategoryDao.getShowCategory(shopId));
		result.put("customPageId", 1);
		result.put("homePageId", 2);
		return result;
	}
	
	/*
	 * 判断店铺是否营业
	 */
	public HashMap<String, Object> isShopOpen(int shopId){
		ShopStatus shopStatus = shopStatusDao.getByShopId(shopId);
		HashMap<String, Object> open = new HashMap<>();
		LocalTime now = LocalTime.now();
		LocalTime begin = LocalTime.parse(shopStatus.getBeginTime());
		LocalTime end = LocalTime.parse(shopStatus.getEndTime());
		if(shopStatus.isOpen()&&now.isAfter(begin)&&now.isBefore(end)){
			open.put("open", true);
		}
		else{
			open.put("open", false);
		}
		return open;
	}
}
