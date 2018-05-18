package com.vdcoding;

import static org.junit.jupiter.api.Assertions.assertEquals;

import java.util.Random;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.RepeatedTest;
import org.junit.jupiter.api.RepetitionInfo;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.TestInfo;
import org.junit.platform.runner.JUnitPlatform;
import org.junit.runner.RunWith;

import com.vdcoding.Calculator;


/*
 * @RepeatedTest 重复执行指定的次数，每次的重复执行与正常单次执行的用例生命周期是一样的。
 */
@Tag("repeat")
@RunWith(JUnitPlatform.class)
public class CalculatorRepeatTest {
	/*
	 * 每次用例执行前先输出用例名称与当前执行的次数编号
	 */
	@BeforeEach
	void beforeEach(TestInfo testInfo, RepetitionInfo repetitionInfo){
		System.out.println(
					"Display Name:" +
					testInfo.getDisplayName() +
					";CurrentRepetition:" +
					repetitionInfo.getCurrentRepetition()
				);
	}
	/*
	 * 重复执行10次
	 */
	@RepeatedTest(10)
	void repeatTest01(TestInfo testInfo){
		Calculator calculator = new Calculator();
		int a = new Random().nextInt();
		int b = new Random().nextInt();
		long result = a - b;
		assertEquals(result, calculator.sub(a, b), "1 + 1 should equal 2");
	}
	/*
	 * 重复执行10次，并指定了一个固定的执行名称Repeat test
	 */
	@RepeatedTest(value=10, name="Repeat test")
	void repeatTest02(TestInfo testInfo){
		Calculator calculator = new Calculator();
		int a = new Random().nextInt();
		int b = new Random().nextInt();
		long result = a - b;
		assertEquals(result, calculator.sub(a, b), "1 + 1 should equal 2");
	}
	
	/*
	 * {displayName}、{currentRepetition}、{totalRepetitions}为RepeatedTest内置的占位符，分别代表
	 * 用例展示名称，当前执行次数编号，总共重复执行次数。其中displayName占位符默认值为方法名称，
	 * 可以通过@DisplayName注解覆盖其值
	 * output:
	 * RepeatTest::1/10
	 * RepeatTest::2/10
	 * ...
	 */
	@RepeatedTest(value=10, name="{displayName}::{currentRepetition}/{totalRepetitions}")
	@DisplayName("RepeatTest")
	void repeatTest03(TestInfo testInfo){
		Calculator calculator = new Calculator();
		int a = new Random().nextInt();
		int b = new Random().nextInt();
		long result = a+b;
		assertEquals(result, calculator.add(a, b), "1 + 1 should equal 2");
	}
	/*
	 * output name:
	 * RepeatTest :: repetition 1 of 10
	 * RepeatTest :: repetition 2 of 10
	 * ...
	 */
	@RepeatedTest(value=10, name=RepeatedTest.LONG_DISPLAY_NAME)
	@DisplayName("RepeatTest")
	void repeatTest04(TestInfo testInfo){
		Calculator calculator = new Calculator();
		int a = new Random().nextInt();
		int b = new Random().nextInt();
		long result = a+b;
		assertEquals(result, calculator.add(a, b), "1 + 1 should equal 2");
	}

}
