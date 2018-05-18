//package spittr;
//
//import java.io.IOException;
//import java.io.PrintWriter;
//import java.nio.file.Paths;
//import java.text.DateFormatSymbols;
//import java.util.Arrays;
//import java.util.Calendar;
//import java.util.GregorianCalendar;
//import java.util.Scanner;
//
//
//public class TestCode {
//	public static final int CONSTANT = 991; //类常量，可供类中或是其他类调用
//	
//	public static void main(String[] args){
////		Scanner in= new Scanner(System.in);
////		System.out.println("Please type start code:");
////		int code=in.nextInt();
////		in.close();
////		String dir = System.getProperty("user.dir");
////		System.out.println(dir);
////		Scanner reader;
//		try {
////			reader = new Scanner(Paths.get("application.properties"));
////			if (reader.hasNextLine()){
////				System.out.println(in.nextLine());
////			}
////			reader.close();
//			PrintWriter writer = new PrintWriter("test.txt");
//			writer.write("helloworld");
//			writer.write("hellodog");
//			writer.flush();
//			writer.close();
//			int[] a={1,2,3,4};
//			int[][] b={{1,2},{2,3},{3,4},{4,5}};
//			System.out.println(Arrays.toString(a));
//			for (int ele:a){
//				System.out.println(ele);
//			}
//			for (int i=0;i<a.length;i++){
//				System.out.println(a[i]);
//			}
//			System.out.println((int)(Math.random()*5));
//			System.out.println(Arrays.binarySearch(a, 2));
//			System.out.println(Arrays.deepToString(b));
//			String h=Arrays.deepToString(b);
//			System.out.println(Arrays.toString(b));
//		} catch (IOException e) {
//			// TODO Auto-generated catch block
//			e.printStackTrace();
//		}
//		finally {
//
//		}
//		GregorianCalendar d=new GregorianCalendar();
//		System.out.println(d.getTime());
//		int today=d.get(Calendar.DAY_OF_MONTH);
//		System.out.println(today);
//		int month=d.get(Calendar.MONTH);
//		System.out.println(month);
//		d.set(Calendar.DAY_OF_MONTH, 1);
//		int weekday=d.get(Calendar.DAY_OF_WEEK);
//		int firstDayOfWeek=d.getFirstDayOfWeek();
//		System.out.println(firstDayOfWeek);
//		int ident=0;
//		while (weekday!=firstDayOfWeek){
//			ident++;
//			d.add(Calendar.DAY_OF_MONTH, -1);
//			weekday=d.get(Calendar.DAY_OF_WEEK);
//			
//		}
//		String[] weekdaynames=new DateFormatSymbols().getShortWeekdays();
//		do {
//			System.out.printf("%4s", weekdaynames[weekday]);
//			d.add(Calendar.DAY_OF_MONTH, 1);
//			weekday=d.get(Calendar.DAY_OF_WEEK);
//		}
//		while (weekday!=firstDayOfWeek);
//		System.out.println();
//		for (int i=0;i<ident;i++){
//			System.out.print("     ");
//			
//		}
//		
//		d.set(Calendar.DAY_OF_MONTH, 1);
//		do{
//			int day=d.get(Calendar.DAY_OF_MONTH);
//			System.out.printf("%4d", day);
//			if (day==today){
//				System.out.print("*");
//			}
//			else {
//				System.out.print(" ");
//			}
//			d.add(Calendar.DAY_OF_MONTH,1);
//			weekday=d.get(Calendar.DAY_OF_WEEK);
//			if (weekday == firstDayOfWeek){
//				System.out.println();
//			}
//			
//		}
//		while(d.get(Calendar.MONTH) == month);
//		if (weekday != firstDayOfWeek) System.out.println();
//
//		
//	}
//}
