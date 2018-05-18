package jmeter_echo;

import java.awt.List;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.io.Writer;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.nio.ByteBuffer;
import java.nio.channels.SocketChannel;
import java.util.ArrayList;

public class SocketClient implements Runnable {
	private Socket socket;
	private  Writer sender = null;
	private SocketChannel channel = null;
	public SocketClient(String ip, int port) throws IOException {
		channel = SocketChannel.open();
		socket = channel.socket();
		socket.connect(new InetSocketAddress(ip, port), 5000);
		System.out.println("Connect to server:" + socket.getRemoteSocketAddress());
		System.out.println("channel connected:" + channel.isConnected());
		System.out.println("socket connected:" + socket.isConnected());

	}
	
	public void sendData(ByteBuffer buffer){
		
		try {
			sender = new PrintWriter(new OutputStreamWriter(socket.getOutputStream()));
			String text = "helloworld";
			int num = 777;
			
			sender.write(text);
			sender.write(num);
			sender.flush();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	public void sendByteData(){
		try {
			String text = "helloworld";
			int num = 888;
			ByteBuffer bb = ByteBuffer.wrap(text.getBytes());
			ByteBuffer cc = ByteBuffer.allocate(4);
			cc.putInt(num);
			while(bb.hasRemaining()){
				channel.write(bb);
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	public Boolean getStatus(){
		return socket.isConnected();
	}
	
	public void messageListener(){
		try {
			BufferedReader br = new BufferedReader(new InputStreamReader(socket.getInputStream()));
			while(true){
				String t = br.readLine();
				if(t != null){
					System.out.println(t);
					ByteBuffer bytes = ByteBuffer.wrap(t.getBytes());
					System.out.println(bytes.capacity());
					System.out.println(bytes.getLong());
					System.out.println(bytes.getLong());
					System.out.println(bytes.capacity());
					System.out.println(bytes.getLong());
				}
				
			}
		} catch (IOException e) {
			e.printStackTrace();
		}
		
	}
	
	public void channelListener(){
		ByteBuffer bb = ByteBuffer.allocate(1024);
		while(socket.isConnected()){
			try {
				channel.read(bb);
				bb.flip(); //flip会翻转buffer并将position指向0
//					bb.rewind();
				TestProtocal testProtocal = new TestProtocal(bb);
				System.out.println(testProtocal);
				bb = bb.slice();
//				bb.flip();
				int l = bb.capacity();
				System.out.println("l:" + bb.capacity());
				System.out.println("positon:" + bb.position());
				if(l!=0&&l<24){
					System.out.println(bb.capacity());
					byte[] remain = new byte[l];
					bb.get(remain);
					bb = ByteBuffer.allocate(1024);
					bb.put(remain);
				}
				System.out.println(bb.capacity());
			
				if(bb.capacity() == 10){
					bb.rewind();
					byte[] bytes = new byte[10];
					bb.get(bytes);
					System.out.println(new String(bytes));
					bb = bb.slice();
					System.out.println(bb.capacity());
				}
				
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}
	
	@Override
	public void run(){
//		messageListener();
		channelListener();
	}
	
	public static void main(String[] args){
		try {
			SocketClient socket = new SocketClient("127.0.0.1", 6000);
			Thread listener = new Thread(socket);
//			listener.setDaemon(true);
			listener.start();
			socket.sendByteData();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
}

class TestProtocal{
	public short head;
	public int packsize;
	public long protocal;
	public String body;
	private final int headSize = 14;
	
	public TestProtocal(ByteBuffer byteBuffer){
		head = byteBuffer.getShort();
		packsize = byteBuffer.getInt();
		System.out.println("packsize:" + packsize);;
		byte[] bbody = new byte[packsize-headSize];
		protocal = byteBuffer.getLong();
		byteBuffer.get(bbody);
		body = new String(bbody);
	}
	
	public String toString(){
		return "head:" + head + ";packsize:"+packsize+";protocal:"+protocal+";body:"+body;
	}
}
