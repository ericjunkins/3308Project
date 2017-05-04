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
 * Initializes the wifi socket with the raspberry pi
 */

public class SocketRunnable implements Runnable {

    private StringBuffer throttle;
    private StringBuffer steering;
    private String message;

    /**
     * Sets this instance of the Socket runnables throttle and steering values to be the values
     * passed in by the joysticks
     * @param throttle
     * @param steering
     */
    protected SocketRunnable(StringBuffer throttle, StringBuffer steering){
        this.throttle = throttle;
        this.steering = steering;

    }

    /**
     * Wifi connection to the raspberry pi
     */
    String dstAddress = "192.168.42.1";
    int dstPort = 5005;
    String response = "";
    Socket socket = null;

    /**
     * Finds the socket, and will send joystick data every 50ms
     */
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
                    Log.d("run", message);

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
