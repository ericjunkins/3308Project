package com.example.vilok.rc_car;

import java.io.IOException;
import java.io.OutputStream;
import java.io.ObjectOutputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.util.ArrayList;

public class Server {

    static ArrayList<String> myList;

    public static void main(String srgs[]) {

        int count = 0;

        initList();

        //hard code to use port 8080
        try (ServerSocket serverSocket = new ServerSocket(8080)) {

            System.out.println("I'm waiting here: " + serverSocket.getLocalPort());

            while (true) {

                try {
                    Socket socket = serverSocket.accept();

                    count++;
                    System.out.println("#" + count + " from "
                            + socket.getInetAddress() + ":"
                            + socket.getPort());

                    HostThread myHostThread = new HostThread(socket, count);
                    myHostThread.start();

                } catch (IOException ex) {
                    System.out.println(ex.toString());
                }
            }
        } catch (IOException ex) {
            System.out.println(ex.toString());
        }
    }

    private static class HostThread extends Thread{

        private Socket hostThreadSocket;
        int cnt;

        HostThread(Socket socket, int c){
            hostThreadSocket = socket;
            cnt = c;
        }

        @Override
        public void run() {

            OutputStream outputStream;
            try {
                outputStream = hostThreadSocket.getOutputStream();
                try (ObjectOutputStream objectOutputStream =
                             new ObjectOutputStream(outputStream)) {
                    objectOutputStream.writeObject(myList);
                }
            } catch (IOException ex) {
                System.out.println(ex.toString());
            }finally{
                try {
                    hostThreadSocket.close();
                } catch (IOException ex) {
                    System.out.println(ex.toString());
                }
            }

        }
    }

    private static void initList(){
        // init myList with test data
        myList =  new ArrayList<String>();
        myList.add("Hello");
        myList.add("Raspberry Pi");
    }
}
