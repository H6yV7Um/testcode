package produce_connsume_demo;

public class Consumer implements Runnable{
	
	private Resource resource;
	
	public Consumer(Resource resource) {
		this.resource = resource;
	}
	
	@Override
	public void run(){
		while(true){
			try {
				Thread.sleep(1000);
				resource.consume();
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}
	}
}
