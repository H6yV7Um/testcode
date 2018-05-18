package com.vdcoding.modules.superman.service;

import java.util.List;

import com.vdcoding.modules.superman.pojos.Customer;
import com.vdcoding.modules.superman.pojos.CustomerAddress;

public interface CustomerService {
	Customer getCustomerById(int id);
	Customer getCustomerByOpenId(String openId);
	void addCustomer(Customer customer);
	void updateCustomer(Customer customer);
	Customer saveAndGet(Customer customer);
	
	List<CustomerAddress> getAvailableAddress(int customerId);
	void setDefaultAddress(int addressId);
	CustomerAddress getAddress(int addressId);
	void addAddress(CustomerAddress address);
	void updateAddress(CustomerAddress address);
}
