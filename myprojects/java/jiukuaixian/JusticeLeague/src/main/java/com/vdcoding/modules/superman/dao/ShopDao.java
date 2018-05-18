package com.vdcoding.modules.superman.dao;

import org.apache.ibatis.annotations.Mapper;

import com.vdcoding.modules.superman.pojos.Shop;
import com.vdcoding.modules.sys.dao.BaseDao;

@Mapper
public interface ShopDao extends BaseDao<Shop>{
	Shop getShopById(int shopId);
}
