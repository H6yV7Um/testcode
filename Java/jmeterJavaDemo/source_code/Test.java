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

	// ���ÿ��ò�������Ĭ��ֵ��
	public Arguments getDefaultParameters() {
		Arguments params = new Arguments();
		params.addArgument("num1", "");
		params.addArgument("num2", "");
		return params;
	}

	// ��ʼ��������ʵ������ʱÿ���߳̽�ִ��һ�Σ��ڲ��Է�������ǰִ�У�������LoadRunner�е�init����
	public void setupTest(JavaSamplerContext arg0) {
		results = new SampleResult();
	}

	// ����ִ�е�ѭ���壬�����߳�����ѭ�������Ĳ�ͬ��ִ�ж�Σ�������LoadRunner�е�Action����
	public SampleResult runTest(JavaSamplerContext arg0) {
		a = arg0.getParameter("num1");
		b = arg0.getParameter("num2");
		results.sampleStart(); // ����һ�����񣬱�ʾ�����������ʼ�㣬������LoadRunner��lr.start_transaction
		try {
			TestDemo test = new TestDemo();
			sum = String.valueOf(test.testSum(Integer.parseInt(a), Integer.parseInt(b)));
			if (sum != null && sum.length() > 0) {
				results.setResponseData("����ǣ�" + sum, null);
				results.setDataType(SampleResult.TEXT);
			} // ����ʾ�ڽ��������Ӧ������
			System.out.println(sum);// �������Jmeter�������������
			results.setSuccessful(true);
		} catch (Throwable e) {
			results.setSuccessful(false);
			e.printStackTrace();
		} finally {
			results.sampleEnd(); // ����һ�����񣬱�ʾ��������Ľ����㣬������LoadRunner��lr.end_transaction
		}
		return results;
	}

	// ����������ʵ������ʱÿ���߳̽�ִ��һ�Σ��ڲ��Է������н�����ִ�У�������LoadRunner�е�end����
	public void teardownTest(JavaSamplerContext arg0) {
		System.out.println("finish!");
	}
}