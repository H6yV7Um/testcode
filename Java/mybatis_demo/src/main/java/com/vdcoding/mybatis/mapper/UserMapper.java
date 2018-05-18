package com.vdcoding.mybatis.mapper;

import java.util.List;
import java.util.Map;

import com.vdcoding.mybatis.pojos.*;  
  
public interface UserMapper { 
  
    //根据用户名列模糊查询用户列表  
    public List<User> findUserByName(String name)throws Exception;
    //根据id更新用户信息
    public int updateUser(User user);
    
    public <T> int addUser(Map<T, T> map);
      
}