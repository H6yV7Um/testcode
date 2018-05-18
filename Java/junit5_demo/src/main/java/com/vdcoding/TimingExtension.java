package com.vdcoding;

import java.lang.reflect.Method;
import java.util.logging.Logger;

import org.junit.jupiter.api.extension.AfterTestExecutionCallback;
import org.junit.jupiter.api.extension.BeforeTestExecutionCallback;
import org.junit.jupiter.api.extension.ExtensionContext;
import org.junit.jupiter.api.extension.ExtensionContext.Namespace;
import org.junit.jupiter.api.extension.ExtensionContext.Store;

/*
 * 实现回调扩展，在每个要执行测试方法上使用注解@ExtendWith(TimingExtension.class)，可以为被注解方法输出执行时间
 * BeforeTestExecutionCallback在BeforeEach之后执行，AfterTestExecutionCallback在AfterEach之前执行，
 * 各回调扩展的执行顺序请参考官方文档图
 */
public class TimingExtension implements BeforeTestExecutionCallback, AfterTestExecutionCallback {
	private static final Logger LOG = Logger.getLogger(TimingExtension.class.getName());

    @Override
    public void beforeTestExecution(ExtensionContext context) throws Exception {
        getStore(context).put(context.getRequiredTestMethod(), System.currentTimeMillis());
    }

    @Override
    public void afterTestExecution(ExtensionContext context) throws Exception {
        Method testMethod = context.getRequiredTestMethod();
        long start = getStore(context).remove(testMethod, long.class);
        long duration = System.currentTimeMillis() - start;

        LOG.info(() -> String.format("Method [%s] took %s ms.", testMethod.getName(), duration));
    }

    private Store getStore(ExtensionContext context) {
        return context.getStore(Namespace.create(getClass(), context));
    }

}

