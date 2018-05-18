package com.vdcoding.batman.mapper;

import java.util.List;

import com.vdcoding.batman.pojos.Order;

public interface OrderMapper {
	
	Order getOrderById(int orderId);
	List<Order> getOrders();

}
