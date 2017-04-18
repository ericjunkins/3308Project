package com.example.lerrrrmps.myfirstapp;


import android.util.Log;
import android.widget.TextView;

import java.io.ByteArrayOutputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.Socket;
import java.net.UnknownHostException;


/**
 * Created by Lerrrrmps on 4/11/2017.
 */

public class SocketRunnable implements Runnable {

    private StringBuffer throttle;
    private StringBuffer steering;
    private String message;


    protected SocketRunnable(StringBuffer throttle, StringBuffer steering){
        Log.d("throttle",throttle.toString()+"!@#awelsjdlfkas");
        this.throttle = throttle;
        this.steering = steering;

    }

    String dstAddress = "192.168.42.1";
    int dstPort = 5005;
    String response = "";
    Socket socket = null;
    int garbage = 100;

    @Override
    public void run(){
        try {
            socket = new Socket(dstAddress, dstPort);
            DataOutputStream DOS = new DataOutputStream(socket.getOutputStream());
            long lastTimeSent = System.currentTimeMillis();
            long now;

            while (true){
                now = System.currentTimeMillis();
                if (now > lastTimeSent + 50){

                    //Log.d("run", throttle.toString());
                    //String message = garbage + "," + throttle.get() + "," + steering.get();
                    message = 100 + "," + throttle + "," + steering;
                    Log.d("run", message.toString());

                    DOS.writeUTF(message);
                    lastTimeSent= now;
                }
                else {
                    try{
                        Thread.sleep(10);
                    }
                    catch (Exception e) {
                        //do nuffin
                    }
                }
            }

        } catch (UnknownHostException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
            response = "UnknownHostException: " + e.toString();
        } catch (IOException e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
            response = "IOException: " + e.toString();
        } finally {
            if (socket != null) {
                try {
                    socket.close();
                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
            }
        }
    }
}
