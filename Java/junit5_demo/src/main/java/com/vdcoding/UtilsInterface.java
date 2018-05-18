package com.vdcoding;

import java.util.logging.Logger;

import org.junit.jupiter.api.AfterAll;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeAll;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Tag;
import org.junit.jupiter.api.TestInfo;
import org.junit.jupiter.api.TestInstance;
import org.junit.jupiter.api.TestInstance.Lifecycle;
import org.junit.jupiter.api.extension.ExtendWith;

public interface UtilsInterface {}

/*
 * 1、junit5 允许将@Test,@RepeatedTest,@ParameterizedTest,@TestFactory,@TestTemplate, @BeforeEach, @AfterEach
 * 使用在接口的default方法上
 *2、 如果接口类或测试类被@TestInstance(Lifecycle.PER_CLASS)注解，则@BeforeAll和@AfterAll注解可以直接使用在
 * 其default方法上，没有必须使用在static方法上的限制了
 */
@TestInstance(Lifecycle.PER_CLASS)
interface TestLifecycleLogger {

    static final Logger LOG = Logger.getLogger(TestLifecycleLogger.class.getName());

    @BeforeAll
    default void beforeAllTests() {
        LOG.info("Before all tests");
    }

    @AfterAll
    default void afterAllTests() {
        LOG.info("After all tests");
    }

    @BeforeEach
    default void beforeEachTest(TestInfo testInfo) {
        LOG.info(() -> String.format("About to execute [%s]", testInfo.getDisplayName()));
    }

    @AfterEach
    default void afterEachTest(TestInfo testInfo) {
        LOG.info(() -> String.format("Finished executing [%s]", testInfo.getDisplayName()));
    }

}

@Tag("timed")
@ExtendWith(TimingExtension.class)
interface TimeExecutionLogger {
}
