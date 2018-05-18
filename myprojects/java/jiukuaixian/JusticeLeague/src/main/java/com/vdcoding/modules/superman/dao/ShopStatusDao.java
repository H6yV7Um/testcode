package com.vdcoding.modules.superman.dao;

import org.apache.ibatis.annotations.Mapper;

import com.vdcoding.modules.superman.pojos.ShopStatus;
import com.vdcoding.modules.sys.dao.BaseDao;

@Mapper
public interface ShopStatusDao extends BaseDao<ShopStatus>{
	ShopStatus getByShopId(int shopId);
}
