package com.vdcoding.modules.superman.service;

import java.util.HashMap;

public interface ShopService {

	HashMap<String, Object> getFullShopInfo(int shopId);
	
	HashMap<String, Object> isShopOpen(int shopId);

}
