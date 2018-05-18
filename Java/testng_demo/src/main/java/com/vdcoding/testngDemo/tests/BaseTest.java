package com.vdcoding.testngDemo.tests;

import org.testng.annotations.BeforeMethod;
import org.testng.annotations.AfterMethod;
import org.testng.annotations.DataProvider;

import com.vdcoding.testngDemo.pojos.Calculator;

import org.testng.annotations.BeforeClass;
import org.testng.annotations.AfterClass;
import org.testng.annotations.BeforeTest;
import org.testng.annotations.AfterTest;
import org.testng.annotations.BeforeSuite;
import org.testng.annotations.AfterSuite;

/*
 * 测试基类，用于定义测试中需要用到的公共方法（比如初始化和清理动作）和提供数据的方法法
 * 其他被执行的测试类继承自该类，避免重复的样板代码
 */
public class BaseTest {
  Calculator calculator = new Calculator();
  
  @BeforeSuite
  public void beforeSuite() {
	  System.out.println("Before suite");
  }

  @AfterSuite
  public void afterSuite() {
	  System.out.println("After suite");
  }
  
  @BeforeTest
  public void beforeTest() {
	  System.out.println("Before test");
  }

  @AfterTest
  public void afterTest() {
	  System.out.println("After test");
  }
  
  @BeforeClass
  public void beforeClass() {
	  System.out.println("Before class");
  }

  @AfterClass
  public void afterClass() {
	  System.out.println("After class");
  }
	
  @BeforeMethod
  public void beforeMethod() {
	  System.out.println("Before method");
  }

  @AfterMethod
  public void afterMethod() {
	  System.out.println("After method");
  }
  
  @DataProvider(name="dp", parallel=true)
  public Object[][] dp() {
    return new Object[][] {
      new Object[] { 1, 3 },
      new Object[] { 2, 4 },
    };
  }
  
  @DataProvider(name="dp2")
  public Object[][] dp2(){
	  return new Object[][] {
	      new Object[] { 1, 3 },
	      new Object[] { 2, 4 },
	    };
  }

}
