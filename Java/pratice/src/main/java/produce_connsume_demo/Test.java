package produce_connsume_demo;

public class Test {
	public static void main(String[] args){
		Resource resource = new Resource();
//		Thread p1 = new Thread(new Producer(resource));
		for(int i=0;i<20;i++){
			new Thread(new Producer(resource)).start();
		}
		for(int i=0; i<100;i++){
			new Thread(new Consumer(resource)).start();
		}
//		int s = 123;
//		String h = "hello";
//		System.out.println(Integer.toHexString(s));
//		System.out.println(h.getBytes());
//		String b = "123";
//		Byte byte1 = new Byte(b);
//		System.out.println(byte1.longValue());
//		System.out.println(byte1.toString());
		
	}
}
