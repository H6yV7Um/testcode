package com.vdcoding.modules.superman.dao;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

import com.vdcoding.datasources.DataSourceNames;
import com.vdcoding.datasources.annotation.DataSource;
import com.vdcoding.modules.superman.pojos.Order;


@DataSource(name=DataSourceNames.SECOND)
@Mapper
public interface OrderDao {
	
	Order getOrderById(int orderId);
	List<Order> getOrders();

}
