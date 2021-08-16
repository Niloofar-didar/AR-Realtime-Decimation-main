package com.arcore.eAR.prototype;
import android.content.Context;
import android.os.Message;
import android.util.Log;

import java.io.BufferedInputStream;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;

/**
 *      Communication with server running on a thread
 */



public class ModelRequestRunnable implements Runnable {

    private final ModelRequest modelRequest;

    // File name indicates the name of the file to send
    private final String filename;

    // Context needed to save the image in the internal storage
    private final Context context;

    //percent reduction
    private final String percReduc;
    private final float cacheratio;
    private final float perc;
   // private List<Float> cacheratio;
    private final ModelRequestManager mInstance;

    static final int DOWNLOAD_FAILED = -1;
    static final int DOWNLOAD_PENDING = 1;
    static final int DOWNLOAD_STARTED = 2;
    static final int DOWNLOAD_COMPLETE = 3;


    //download chunk size, make sure to match on server thread
    private final int BUFFER_SIZE = 16000;


    public ModelRequestRunnable(ModelRequest modelRequest, ModelRequestManager mInstance ) {
        this.modelRequest = modelRequest;

        this.filename = modelRequest.getFilename();
        this.context = modelRequest.getAppContext();
        this.percReduc = Float.toString(modelRequest.getPercentageReduction());
        this.perc=modelRequest.getPercentageReduction();
        this.mInstance = mInstance;
        this.cacheratio=modelRequest.getCache();
    }


    @Override
    public void run() {


    try{
        File new_file = new File(context.getExternalFilesDir(null), "/decimated" + filename + percReduc + ".glb");
        //instead of chechking all ratios you can check cache andddd also check if percreduc !=1

        // for using the local memory undo the comment
     //   if (!new_file.exists()) {
       if(((perc!=cacheratio || !new_file.exists() ) && perc!=1)||  (!new_file.exists() && perc==1) ){



            Log.d("ModelRequest", "Entering Runnable");


            try {

                if (Thread.interrupted()) {
                    throw new InterruptedException();
                }

                try {
                    // Establish connection with the server
                    //@@@pc address
                    Socket socket = new Socket("35.16.116.212", 4444);


                    // Open output stream
                    PrintWriter out = new PrintWriter(socket.getOutputStream(), true);
                    BufferedReader in = new BufferedReader(new InputStreamReader(socket.getInputStream()));
                    //send desired % reduction
                    out.println(percReduc);
                    //flush stream
                    out.flush();
                    //send filename
                    out.println(filename);
                    // flush stream
                    out.flush();


                    FileOutputStream fout = new FileOutputStream(new_file);


                    //start to read tris 15 sep
                    //File Updated_Tris = new File(context.getExternalFilesDir(null), "/updated_Tris_" + filename+ ".txt");
                    //open stream to write new file
                    //FileOutputStream fout1 = new FileOutputStream(Updated_Tris);
                    BufferedInputStream socketInputStream1;
                    socketInputStream1 = new BufferedInputStream(socket.getInputStream());
                    byte[] buffer1 = new byte[BUFFER_SIZE];
                    int read1;
                    int totalRead1 = 0;
                    long startTime2 = System.currentTimeMillis();
                    boolean first = false;


                    while ((read1 = socketInputStream1.read(buffer1)) != -1) {
                        String message = new String(buffer1, 0, read1);
                        if (message.endsWith("!]]!][!")) {
                            // don't write last -7 bytes, those are for the delimiter
                            fout.write(buffer1, 0, read1 - 7);
                            break;
                        }
                        long startTime = System.currentTimeMillis();
                        totalRead1 += read1;
                        fout.write(buffer1, 0, read1);
                        long endTime = System.currentTimeMillis();
                        Log.d("ModelRequestRunnable", "Buffer write time: " + (endTime - startTime) + " milliseconds");
                    }

                    long endTime2 = System.currentTimeMillis();
                    Log.d("ModelRequestRunnable", "Total execution Time: " + (endTime2 - startTime2) + " milliseconds");

                    fout.flush();


                    // tell server that file is received so it doesn't close connection
                    PrintWriter outM = new PrintWriter(socket.getOutputStream(), true);
                    outM.println("File received");
                   // mInstance.handleState(DOWNLOAD_COMPLETE, modelRequest);

                    //added from modelreqmanager
                    Message msg = modelRequest.getMainActivityWeakReference().get().getHandler().obtainMessage();
                    msg.obj = modelRequest;
                    modelRequest.getMainActivityWeakReference().get().getHandler().sendMessage(msg);
                    ModelRequestManager.mRequestList.remove(modelRequest);





                    outM.flush();
                    // close all the streams
                    fout.close();
                    socketInputStream1.close();
                    outM.close();
                    in.close();
                    fout.close();
                    out.close();
                    socket.close();


                }//}


                catch (Exception e) {
                    mInstance.handleState(DOWNLOAD_FAILED, modelRequest);
                    Log.w("ModelRequestRunnable", e.getMessage());
                }


            } catch (InterruptedException e) {

                Log.w("ModelRequestRunnable", e.getMessage());
            }

        }
    else {
            Log.d("ModelRequest", "Recieved DOWNLOAD_COMPLETE state");

            Message msg = modelRequest.getMainActivityWeakReference().get().getHandler().obtainMessage();
            msg.obj = modelRequest;
            modelRequest.getMainActivityWeakReference().get().getHandler().sendMessage(msg);
            ModelRequestManager.mRequestList.remove(modelRequest);
        }

    }
        catch (Exception e) {
            mInstance.handleState(DOWNLOAD_FAILED, modelRequest);
            Log.w("ModelRequestRunnable", e.getMessage());
        }
    }
}
