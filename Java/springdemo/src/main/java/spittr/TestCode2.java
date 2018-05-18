package spittr;

import java.awt.Toolkit;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.*;

import javax.swing.JOptionPane;
import javax.swing.Timer;

public class TestCode2 {
	public static void main(String[] args){
		TimePrinter t = new TimePrinter();
		Timer timer = new Timer(5000, t);
		timer.start();
		JOptionPane.showMessageDialog(null, "Quit?");
		System.exit(0);
	}
}

class TimePrinter implements ActionListener{
	public void actionPerformed(ActionEvent event){
		Date now = new Date();
		System.out.println(now);
		Toolkit.getDefaultToolkit().beep();
	}
}
