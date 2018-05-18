package com.vdcoding.mybatis.tests;

import java.io.IOException;  
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.ibatis.session.SqlSession;  
  
import com.vdcoding.mybatis.pojos.User;  

public class MybatisTest {
    public static void main(String...args) throws IOException {  
    	
    	String qualName = "com.vdcoding.mybatis.mapper.UserMapper";
        SqlSession sqlSession = new Base("production").session;  
	    try{
	        // list中的user和映射文件中resultType所指定的类型一致  
	        List<User> list = sqlSession.selectList(qualName + ".findUserByName");  
	        User user = sqlSession.selectOne(qualName + ".findUserByName", "test");
	        user.setSex("9");
	        user.setAddress("China");
	        int num = sqlSession.update(qualName + ".updateUser", user);
	        sqlSession.commit();
	        Map<String,String> map = new HashMap<>();
	        map.put("username", "superman");
	        map.put("sex", "6");
	        map.put("address", "USA");
	        int i = sqlSession.insert(qualName + ".addUser", map);
	        sqlSession.commit();
	        if(i>0) System.out.println("Add user success!");
	        if(num>0) System.out.println("Update user success!");
	        //首次执行时报错无法找到com.mysql.jdbc.Driver, 开始使用的mysql-connector是6.0.6版本，改为5.1.6正常
	        System.out.println(list);
	        System.out.println(user);
    	} finally{
    		sqlSession.close();
    	}
        
  
    }  
}
