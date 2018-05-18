package com.vdcoding;

import static org.junit.Assert.assertTrue;

import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.TestInfo;
import org.junit.platform.runner.JUnitPlatform;
import org.junit.runner.RunWith;

/*
 * 通过实现接口的方式，继承一些公共的初始化和清理方法，可以大大减少测试case中的样板代码
 */
@Tag("simpletest")
@RunWith(JUnitPlatform.class)
public class InterfaceImplTest implements TestLifecycleLogger, TimeExecutionLogger {
	
	@Test
	void simpleTest(TestInfo testInfo){
		System.out.println(testInfo.getTags());
		assertTrue(true);
	}
	
	/*output:
	 * 十二月 14, 2017 10:52:19 上午 com.vdcoding.TestLifecycleLogger beforeAllTests
		信息: Before all tests
		十二月 14, 2017 10:52:19 上午 com.vdcoding.TestLifecycleLogger beforeEachTest
		信息: About to execute [simpleTest(TestInfo)]
		[timed, simpletest]
		十二月 14, 2017 10:52:19 上午 com.vdcoding.TimingExtension afterTestExecution
		信息: Method [simpleTest] took 5 ms.
		十二月 14, 2017 10:52:19 上午 com.vdcoding.TestLifecycleLogger afterEachTest
		信息: Finished executing [simpleTest(TestInfo)]
		十二月 14, 2017 10:52:19 上午 com.vdcoding.TestLifecycleLogger afterAllTests
		信息: After all tests
	 */
}


