package produce_connsume_demo;

public class Producer implements Runnable {
	
	private Resource resource;
	
	public Producer(Resource resource) {
		this.resource = resource;
	}
	
	@Override
	public void run(){
		while(true){
			try {
				Thread.sleep(100);
				resource.produce();
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
	}
}
