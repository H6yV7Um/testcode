package java_learning;

import org.apache.jmeter.config.Arguments;
import org.apache.jmeter.protocol.java.sampler.AbstractJavaSamplerClient;
import org.apache.jmeter.protocol.java.sampler.JavaSamplerContext;
import org.apache.jmeter.samplers.SampleResult;

/**
 * @author test
 * 
 */
public class Test extends AbstractJavaSamplerClient {
	private SampleResult results;
	private String a;
	private String b;
	private String sum;

	// 设置可用参数及的默认值；
	public Arguments getDefaultParameters() {
		Arguments params = new Arguments();
		params.addArgument("num1", "");
		params.addArgument("num2", "");
		return params;
	}

	// 初始化方法，实际运行时每个线程仅执行一次，在测试方法运行前执行，类似于LoadRunner中的init方法
	public void setupTest(JavaSamplerContext arg0) {
		results = new SampleResult();
	}

	// 测试执行的循环体，根据线程数和循环次数的不同可执行多次，类似于LoadRunner中的Action方法
	public SampleResult runTest(JavaSamplerContext arg0) {
		a = arg0.getParameter("num1");
		b = arg0.getParameter("num2");
		results.sampleStart(); // 定义一个事务，表示这是事务的起始点，类似于LoadRunner的lr.start_transaction
		try {
			TestDemo test = new TestDemo();
			sum = String.valueOf(test.testSum(Integer.parseInt(a), Integer.parseInt(b)));
			if (sum != null && sum.length() > 0) {
				results.setResponseData("结果是：" + sum, null);
				results.setDataType(SampleResult.TEXT);
			} // 会显示在结果树的响应数据里
			System.out.println(sum);// 会输出在Jmeter启动的命令窗口中
			results.setSuccessful(true);
		} catch (Throwable e) {
			results.setSuccessful(false);
			e.printStackTrace();
		} finally {
			results.sampleEnd(); // 定义一个事务，表示这是事务的结束点，类似于LoadRunner的lr.end_transaction
		}
		return results;
	}

	// 结束方法，实际运行时每个线程仅执行一次，在测试方法运行结束后执行，类似于LoadRunner中的end方法
	public void teardownTest(JavaSamplerContext arg0) {
		System.out.println("finish!");
	}
}