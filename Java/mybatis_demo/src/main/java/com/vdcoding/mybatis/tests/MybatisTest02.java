package com.vdcoding.mybatis.tests;

import com.vdcoding.mybatis.mapper.UserMapper;
import com.vdcoding.mybatis.pojos.User;
import java.util.List;
import org.apache.ibatis.session.SqlSession;

public class MybatisTest02 {
	public static void main(String[] args) throws Exception{
		SqlSession session = new Base().session;
		User user = session.selectOne("com.vdcoding.mybatis.mapper.UserMapper.findUserByName", "test");
		System.out.println(user);
		//UserMapper.xml中的namespace一定要写正确，否则会报Invalid bound statement (not found)
		UserMapper mapper = session.getMapper(UserMapper.class);
		List<User> users = mapper.findUserByName("superman");
		System.out.println(users);
		int num = mapper.updateUser(user);
		System.out.println(num);
	}
}
