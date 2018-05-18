package com.vdcoding;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.when;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.platform.runner.JUnitPlatform;
import org.junit.runner.RunWith;
import org.mockito.Mock;

/*
 * 加载自定义的mock扩展类，调用被@Mock注解的类的getName时会返回设置的名称test
 * 自定义的扩展类MockitoExtension中需要定义参数解析器，否则传入测试方法的person参数无法被解析注入。
 */
@RunWith(JUnitPlatform.class)
@ExtendWith(MockitoExtension.class)
public class PersonMockTest {
	@BeforeEach
	void init(@Mock Person person){
		when(person.getName()).thenReturn("test");
		when(person.getAge()).thenReturn(30);
	}
	
	@Test
	void mockTest01(@Mock Person person){
		assertEquals("test", person.getName(), "Person name should be test");
	}
	
	@Test
	void mockTest02(@Mock Person person){
		assertEquals(30, person.getAge());
	}
}
