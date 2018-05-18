package com.vdcoding;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import java.util.HashMap;
import java.util.Map;
import java.util.Random;

import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.TestInfo;
import org.junit.jupiter.api.TestInstance;
import org.junit.jupiter.api.TestReporter;
import org.junit.jupiter.api.TestInstance.Lifecycle;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.platform.runner.JUnitPlatform;
import org.junit.runner.RunWith;

/*
 * @RunWith注解作用：用junit4框架运行junit5的case
 * 由于目前的IDE只有IntelliJ IDEA和Eclipse 4.7(Oxygen)支持junit5，所以此处用该注解的方式运行算是最优方式了，可以兼容大部分IDE
 * 只不过输出内容的格式有些区别，但不影响case的执行及结果
 * 通过RunWith注解运行需要安装依赖junit-4.12、junit-platform-runner、junit-jupiter-api
 * junit-jupiter-engine。
 * 还有一种运行junit5的方式是通过Console Launcher，一种命令行工具，需要单独下载一个jar包
 * 
 * @Tag注解作用：相当于junit4中的Categories，用于分组，可用于类或方法上，没个类或方法可有多个Tag
 * 
 * 所有被@Test, @TestTemplate, @RepeatedTest, @BeforeAll, @AfterAll, @BeforeEach, or @AfterEach注解的方法
 * 不能有返回值即必须用void修饰
 * 
 * 所有的用例类或者方法都无需用public修饰
 * 
 * junit5中的断言可能不是特别全面，可以依靠第三方库的断言功能来弥补，官方推荐的第三方库： AssertJ, Hamcrest, Truth
 * 直接导入对应的断言方法使用即可。
 */
@Tag("standard")
@RunWith(JUnitPlatform.class)
@TestInstance(Lifecycle.PER_CLASS)
public class CalculatorStandardTest {
	/*
	 * 必须为静态方法，在开始执行用例前只初始化一次，相当于junit4中的Before
	 */
	@BeforeAll
	static void beforeAll(){
		System.out.println("Ready to start test!");
		//to do
		
	}
	
	/*
	 * 每开始执行一条用例前都会初始化一次
	 */
	@BeforeEach
	void beforeEach(TestInfo testInfo){
		//to do
		System.out.println(testInfo.getDisplayName());
	}
	
	/*
	 * 必须为静态方法，所有用例执行完后只执行一次，相当于junit4的After
	 */
	@AfterAll
	static void afterAll() {
		System.out.println("All tests finished!");
		//to do
	}
	
	/*
	 * 每执行完一条用例都会执行一次
	 */
	@AfterEach
	void afterEach(TestInfo testInfo){
		System.out.println(testInfo.getTags().toString());
		//to do
	}
	/*
	 * TestInfo为junit内置的注入型参数，包括了当前执行的测试方法的信息，如displayName，tags等
	 */
	@Test
	@DisplayName("standard test")
	@ExtendWith(TimingExtension.class)
	void standardTest01(TestInfo testInfo) {
		Calculator calculator = new Calculator();
		int a = new Random().nextInt();
		int b = new Random().nextInt();
		assertEquals(a + b, calculator.add(a, b), "wrong result");
		assertEquals("standard test", testInfo.getDisplayName(), () -> "TestInfo is injected correctly");
	}
	
	/*
	 * TestReporter为junit内置的注入型参数，可以在执行测试方法时添加额外的数据并默认输出到stdout
	 */
	@Test
	void standardTest02(TestReporter testReporter){
		Map<String, String> map = new HashMap<>();
		map.put("hello", "world");
		testReporter.publishEntry(map);
		testReporter.publishEntry("test", "666");
		assertTrue(true);
	}
	
	/*
	 * @Disabled注解的类或者方法不会被执行，string参数可省略，相当于junit4中的@Ignore
	 * 一般用于某些废弃的case上，还可以保留版本信息
	 */
	@Disabled("no need to test")
	@Test
	void disableTest(){
		//to do
	}
	
	/*控制台输出如下：
	 *  Ready to start test!
		standard test
		十二月 13, 2017 2:36:22 下午 com.vdcoding.TimingExtension afterTestExecution
		信息: Method [standardTest01] took 10 ms.
		[standard]
		standardTest02(TestReporter)
		ReportEntry [timestamp = 2017-12-13T14:36:22.289, hello = 'world']
		ReportEntry [timestamp = 2017-12-13T14:36:22.292, test = '666']
		[standard]
		All tests finished!
	 */

}
