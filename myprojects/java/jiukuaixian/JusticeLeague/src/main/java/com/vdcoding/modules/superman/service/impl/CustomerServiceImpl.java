package com.vdcoding.modules.superman.service.impl;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import com.vdcoding.modules.superman.dao.CustomerAddressDao;
import com.vdcoding.modules.superman.dao.CustomerDao;
import com.vdcoding.modules.superman.pojos.Customer;
import com.vdcoding.modules.superman.pojos.CustomerAddress;
import com.vdcoding.modules.superman.service.CustomerService;

import java.util.List;


@Service
public class CustomerServiceImpl implements CustomerService {
	@Autowired
	private CustomerDao customerDao;
	
	@Autowired
	private CustomerAddressDao customerAddressDao;
	
	@Override
	public Customer getCustomerById(int id){
		return customerDao.getCustomerById(id);
	}
	
	@Override
	public Customer getCustomerByOpenId(String openId){
		return customerDao.getCustomerByOpenId(openId);
	}
	
	@Override
	public void addCustomer(Customer customer){
		customerDao.save(customer);
	}
	
	@Override
	public void updateCustomer(Customer customer){
		customerDao.update(customer);
	}
	
	@Override
	@Transactional
	public Customer saveAndGet(Customer customer){
		customerDao.save(customer);
		return customerDao.getCustomerByOpenId(customer.getOpenId());
	}
	
	@Override
	public List<CustomerAddress> getAvailableAddress(int customerId) {
		return customerAddressDao.getAvailableAddress(customerId);
	}
	
	@Override
	@Transactional
	public void setDefaultAddress(int addressId) {
		CustomerAddress defaultAddress = customerAddressDao.getDefaultAddress();
		CustomerAddress targetAddress = customerAddressDao.getAddress(addressId);
		if(defaultAddress != null&&!defaultAddress.equals(targetAddress)){
			defaultAddress.setIsDefault(0);
			customerAddressDao.update(defaultAddress);
		}
		targetAddress.setIsDefault(1);
		customerAddressDao.update(targetAddress);
	}
	
	@Override
	public CustomerAddress getAddress(int addressId) {
		return customerAddressDao.getAddress(addressId);
	}
	
	@Override
	public void addAddress(CustomerAddress address) {
		customerAddressDao.save(address);
	}
	
	@Override
	public void updateAddress(CustomerAddress address) {
		customerAddressDao.update(address);
	}
	
}
