package com.vdcoding;

import static org.junit.Assert.assertTrue;

import java.util.Arrays;
import java.util.Collection;

import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;
import org.junit.jupiter.params.provider.ValueSource;
import org.junit.platform.runner.JUnitPlatform;
import org.junit.runner.RunWith;

/*
 * 首先，要使用ParameterizedTest注解需要配置junit-jupiter-params依赖；
 * @ParameterizedTest注解必须结合数据源注解使用，可以给同一个测试方法传入不同的参数，每次调用的生命周期与常规的测试方法一样。
 * 示例中演示了比较常用的@ValueSource和@MethodSource，
 * 其他的数据源注解有ArgumentsSource、CsvFileSource、CsvSource、EnumSource，用法请参考官方文档
 */
@RunWith(JUnitPlatform.class)
public class ParameterTest {
	
	/*
	 * @ParameterizedTest的name参数支持内置占位符:
	 * {index}为当前传入的参数值在数据源中的索引值，从1开始；
	 * {0}...{n}为当前传入的参数值，如果传入两个参数，则可以通过{0}{1}来获取参数值
	 * @ValueSource注解只支持简单的原生类型，如 int，string，long，double，参数名加个s，参数值可以为单个值或者数组.
	 */
	@DisplayName("paramTest")
	@ParameterizedTest(name="{index}-current param:{0}")
	@ValueSource(strings={"apple", "banana"})
	void paramTest(String param){
		assertTrue(param instanceof String);
	}
	
	/*
	 * @MethodSource注解引用的方法必须返回Stream、iterator、iterable或者数组。
	 * 被引用的方法必须为测试类中的static方法，如果测试类被@TestInstance(Lifecycle.PER_CLASS)修饰则没有该限制
	 */
	@ParameterizedTest
	@MethodSource("makeString")
	void methodSourceTest(String s){
		assertTrue(s instanceof String);
	}
	
	static Collection<String> makeString(){
		return Arrays.asList("pear", "watermelon");
	}
}
