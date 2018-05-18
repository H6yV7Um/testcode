package com.vdcoding;

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.net.Socket;
import java.nio.channels.SocketChannel;

import com.google.protobuf.Message;
import com.google.protobuf.util.JsonFormat.Printer;
import com.google.protobuf.util.JsonFormat;

import com.vdcoding.ProtoDemo.OnlineUser;;

public class TestProto {
	private Socket socket;
	private SocketChannel channel = null;
	public TestProto(String ip, int port) throws IOException {
		channel = SocketChannel.open();
		socket = channel.socket();
		socket.connect(new InetSocketAddress(ip, port), 5000);
		System.out.println("Connect to server:" + socket.getRemoteSocketAddress());
	}
	
	public void sendData(Message message){
		try {
			OutputStream os = socket.getOutputStream();
			//将protobuf message写入输出流
			message.writeTo(os);
			os.flush();
			System.out.println("Send data:" + message);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
	
	public void messageListener(){
		Printer printer = JsonFormat.printer();
		while(socket.isConnected()){
			try {
				OnlineUser user = OnlineUser.parseFrom(socket.getInputStream());
				if(user.getRspCode()!=0){
					System.out.println("Received data:" + user);
					System.out.println("Convert user to json:" + printer.includingDefaultValueFields().print(user));
				}
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}
	public static void main(String[] args){
		OnlineUser.UserInfo.Builder userInfo = 
				OnlineUser.UserInfo.newBuilder()
				.setUid(123123123)
				.setUsreName("Paditon")
				.setCliType(16)
				.setPhoneNum(110)
				.setType(OnlineUser.PhoneType.MOBILE);
		OnlineUser.Builder builder = OnlineUser.newBuilder();
		builder.setRspCode(12);	//整型不设置值默认为0
		builder.setProduct("hello world");
		builder.setQueryTime(System.currentTimeMillis());
		builder.addRandom(999);
		builder.addRandom(888);
		builder.addUserList(userInfo);
		Message onlineuser = builder.build();
		try {
			TestProto tp = new TestProto("127.0.0.1", 6000);
			tp.sendData(onlineuser);
			Thread t = new Thread(new Runnable() {
				@Override
				public void run() {
					tp.messageListener();
				}
			});
			t.setDaemon(true);
			t.start();
			Thread.sleep(1000);
		} catch (InterruptedException e) {
				e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
}
