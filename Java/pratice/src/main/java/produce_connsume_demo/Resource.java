package produce_connsume_demo;

import java.util.concurrent.atomic.AtomicInteger;


public class Resource {
//	private int counter=0;
	private AtomicInteger counter = new AtomicInteger(0);
	private int current;
	
	public synchronized void produce() throws InterruptedException{
		if(counter.get() >= 5){
			System.out.println("Full! pause to produce");
			wait();
		}
		if(counter.get() >=5) return;
		current = counter.incrementAndGet();
		notifyAll();
		System.out.println(Thread.currentThread().getName() + "produce counter:" + current);
	}
	
	public synchronized void consume() throws InterruptedException{
		if(counter.get() <= 0){
			System.out.println("Empty! wait to consume");
			wait();
		}
		if(counter.get() <= 0) return;
		current = counter.decrementAndGet();
		notifyAll();
		System.out.println(Thread.currentThread().getName() + "consume counter:" + current);
	}
}
