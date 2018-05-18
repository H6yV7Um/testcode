package com.vdcoding.testngDemo.tests;

import static org.testng.Assert.assertEquals;

import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.Iterator;

import org.testng.annotations.DataProvider;
import org.testng.annotations.Ignore;
import org.testng.annotations.Test;

import com.vdcoding.testngDemo.pojos.Calculator;

/*
 * 利用注解@Test声明test case的方式(文中所出现的case表示被@Test注解的类或者方法)：
 * 1、标注在方法上，该方法被标记为要执行的测试case
 * 2、标注在类上，则该类下的所有public方法都被标记为要执行的case，一般情况下，都应该使用将@Test标注在类上的方式。
 * Notes：
 * 使用了@Ignore或者@Test(enabled=false)的方法不会被执行，
 * 官方文档上说在方法上使用@Ignore注解等同于使用@Test(enabled=false)，但实际测试@Ignore标注的方法还是会执行。
 * 
 */

public class StandardTest extends BaseTest{
  @Test(dataProvider = "dp", groups={"p0"})
  public void test(int a, int b) {
	  Calculator calculator = new Calculator();
	  assertEquals(a + b, calculator.sum(a, b));
  }
}

@Test(groups={"p1"})
class StandardTest2 extends BaseTest{
	
	public void test1(){
		System.out.println("hellodog");
	}
	
	@Ignore
	public void test2(){
		System.out.println("Ignored test!");
		
	}
	
	@Test(enabled=false)
	public void test3(){
		System.out.println("Disabled test");
	}
	
}

@Test(groups={"p2"})
class StandardTest3 extends BaseTest{
	/*
	 * depengsOnGroups=p1表示该用例的执行依赖于分组为p1的case，需要等p1的所有case都执行完了才会执行。
	 * 如果p1中有任意case执行失败了，则会跳过该case即StandardTest3.test1的执行。
	 * 如果属性alwaysRun=true，则不管p1的case是否执行成功，都会执行 StandardTest3.test1。
	 * 这种依赖其他方法的方式一般用来控制某些特殊case的执行顺序
	 */
	@Test(dataProvider="dp2", dependsOnGroups={"p1"}, alwaysRun=true)
	public void test1(int a, int b){
		assertEquals(a + b, calculator.sum(a, b));
	}
	/*
	 * dependsOnMethods={"test1"}表示test1执行成功后才会执行test2
	 */
	@Test(dependsOnMethods={"test1"})
	public void test2(){
		System.out.println("hello world");
	}
}

class MyDataProvider {
	/*
	 * 作为一个dataprovider是要有职业操守的:首先它职能作用在方法上，其次它只能返回如下两种数据结构：
	 * 1、返回一个元素类型为Object的二维数组，该二维数组长度指定了case的执行次数，也就是case会遍历该数组；
	 * 数组的元素Object[]则会按照顺序传给测试方法定义的形参，所以无论是数据类型还是个数，都必须与测试方法的形参匹配。
	 * 2、返回一个迭代器Iterator<Object[]>,这种方式与直接返回二维数组的唯一区别就是你懂得
	 */
	@DataProvider(name="mydp")
	public static Object[][] dp() {
		return new Object[][] {
			new Object[] { 1, 3 },
			new Object[] { 2, 4 },
		};
	}
	
	@DataProvider(name="iterdp")
	public static Iterator<Object[]> iterdp(){
		ArrayList<Object[]> list = new ArrayList<Object[]>();
		list.add(new Object[] { 1, 3 });
		list.add(new Object[] { 2, 4 });
		return list.listIterator();
	}
	
	/*
	 * 如果给dataprovider方法传入参数java.lang.reflect.Method，则该Method对应的是使用这个dp方法的测试方法
	 * 参考StandardTest4中的test3和test4
	 */
	@DataProvider(name="dprouter")
	public static Object[][] dpRouter(Method m) {
		if(m.getName().equals("test3")){
			return new Object[][] {new Object[] { 1, 3 }};
		}
		else if(m.getName().equals("test4")){
			return new Object[][] {new Object[] {2, 4}};
		}
		else{
			return new Object[][] {
				new Object[] { 1, 3 },
				new Object[] { 2, 4 },
			};
		}
		
	}
}

@Test(groups={"p3"})
class StandardTest4 extends BaseTest{
	/*
	 * 默认情况下，如果某个case声明了dataprovider则会在该case所在的当前类或其父类中查找。
	 * 如果想要引用其他类中定义的dataprovider方法，则该方法必须声明为static，如上边的MyDataProvider类所示，然后按照如下
	 * 方式引用即可
	 */
	@Test(dataProvider="mydp", dataProviderClass=MyDataProvider.class)
	public void test1(int a, int b){
		assertEquals(a + b, calculator.sum(a, b));
	}
	
	@Test(dataProvider="iterdp", dataProviderClass=MyDataProvider.class)
	public void test2(int a, int b){
		assertEquals(a + b, calculator.sum(a, b));
	}
	
	/*
	 * test3使用了dprouter，此时只会传入参数{ 1, 3 }
	 */
	@Test(dataProvider="dprouter", dataProviderClass=MyDataProvider.class)
	public void test3(int a, int b){
		assertEquals(a + b, calculator.sum(a, b));
	}
	
	/*
	 * test4使用了dprouter，此时只会传入参数{ 2, 4 }
	 */
	@Test(dataProvider="dprouter", dataProviderClass=MyDataProvider.class)
	public void test4(int a, int b){
		assertEquals(a + b, calculator.sum(a, b));
	}
	
}