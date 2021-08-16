package server;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;
import java.io.PrintWriter;
import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.util.Arrays;
import java.net.Socket;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.text.SimpleDateFormat;
import java.util.Arrays;
import java.util.Date;
import java.util.*;
import  java.text.SimpleDateFormat;
import java.util.Queue;
import java.util.concurrent.CompletableFuture;
import java.util.Date;
import java.util.concurrent.LinkedBlockingQueue;
import java.text.ParseException;
import java.text.SimpleDateFormat;




/**
 * 
 *	Server thread handling single connection
 */
public class
ServerThread extends Thread {
	private final Socket socket;
	//download chunk size, make sure to match on ModelRequestRunnable
	private final int BUFFER_SIZE = 200;
    ARServer ser;
	public ServerThread(Socket socket, ARServer server) {
		this.socket = socket;
		this.ser=server;
	}



	//run a thread to handle a connection
	public void run() {
		try {


			BufferedWriter writer = null;

			writer = new BufferedWriter(new OutputStreamWriter(
					new FileOutputStream("Latency.txt", true)));

			BufferedInputStream inStrean = new BufferedInputStream(socket.getInputStream());
			BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
			PrintWriter outM = new PrintWriter(socket.getOutputStream(), true);

			//recieve percent reduction in 0.0 to 1.0 format
			String perc_reduc = in.readLine();

			String filename = in.readLine();
			System.out.println("Received: " + perc_reduc + ", " + filename);
			Process process;


			/////Nil start decimation

			File file = new File("./output/" + String.valueOf(filename) + "/" + String.valueOf(filename) + String.valueOf(perc_reduc) + ".glb");


			String command;
			if (file.exists() == false) {
				System.out.println("it is decimating");

				command = "blender-2.80-linux-glibc217-x86_64/blender -b -P blenderSimplifyV2.py -- --ratio " + String.valueOf(perc_reduc) + " --inm ./input/" + filename + "/" + filename + ".obj --outm  ./output/" +filename + "/" + filename +perc_reduc+ "  --tris ./input/" + filename + "/tris.txt";
				System.out.println(command);
				long startT1 = System.currentTimeMillis();

				writer.append("Start Decimation at " + new Date() + " for object " + filename + "\n");


				try {
					process = Runtime.getRuntime().exec(command);

					process.waitFor();

				} catch (IOException e) {
					System.out.println(e.getMessage());

					try{
						ser.serve();}// avoid the crash in server, server continues to listen
					catch (IOException ee) {
						ee.printStackTrace();
					}


				}


				long endT1 = System.currentTimeMillis();
				System.out.println(" decimation time : " + (endT1 - startT1) + " milliseconds");
				writer.append("decimation time : " + (endT1 - startT1) + " milliseconds \n");


			} else
				System.out.println("we already have the decimated object, plz wait for communication...");




			SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss:SSS");
			dateFormat.format(new Date());
			// time_tris.put(dateFormat.format(new Date()), sum);


			File out_file1, out_file;



			OutputStream socketOutputStream1 = socket.getOutputStream();

			//for decimated
			out_file = new File("./output/" + filename + "/" + filename + String.valueOf(perc_reduc) + ".glb");



			FileInputStream outputFile = new FileInputStream(out_file);
			PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
			OutputStream socketOutputStream = socket.getOutputStream();

			//wait for input stream of file
			int read;
			int readTotal = 0;
			byte[] buffer = new byte[160000];





			//write chunks of bytes
			int writingtime=0;
			while ((read = outputFile.read(buffer)) != -1) {
				long startTime = System.currentTimeMillis();
				socketOutputStream.write(buffer, 0, read);
				long endTime = System.currentTimeMillis();
				System.out.println("socketOutputStream buffer [" + read + " bytes] write time 1: " + (endTime - startTime) + " milliseconds");
				//System.out.println("Sending " + out_file + "(" + mybytearray.length + " bytes)");
				writingtime+= (endTime - startTime);
				socketOutputStream.flush();
				readTotal += read;


			}

			writer.append("Writing time : " + writingtime + " milliseconds \n");


			//send end of message
			out.print("!]]!][!");
			out.flush();


			while (!((new String(in.readLine())).equals("File received"))) ;

			//close all stream
			inStrean.close();
			outM.close();

			//out1.close();
			//out2.close();
			out.close();
			in.close();
			outputFile.close();
			//outputFile2.close();
			socketOutputStream.close();
			//	socketOutputStream2.close();
			socket.close();

			//decrement the number of clients
			ARServer.number_of_clients--;

			writer.close();

		} catch (Exception e) {
			System.out.println(e.getMessage());
			try{
			ser.serve();}// avoid the crash in server, server continues to listen
			catch (IOException ee) {
				ee.printStackTrace();
			}


		}
	}


}



