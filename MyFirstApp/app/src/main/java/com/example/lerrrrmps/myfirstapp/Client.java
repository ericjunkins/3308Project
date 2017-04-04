package com.example.vilok.rc_car;

import java.net.Socket;
import java.io.InputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.io.PrintWriter;
import java.io.ObjectInputStream;
import java.net.UnknownHostException;
import java.util.ArrayList;

class Client{

    public static void main(String args[])
    {
        if(args.length == 0){
            System.out.println("usage: java client <port>");
            System.exit(1);
        }

        int port = isParseInt(args[0]);
        if(port == -1){
            System.out.println("usage: java client <port>");
            System.out.println("<port>: integer");
            System.exit(1);
        }

        try{
            //IP is hard coded
            //port is user entry
            Socket socket = new Socket("192.168.111.109", port);

            ArrayList<String> myList;

            ObjectInputStream objectInputStream =
                    new ObjectInputStream(socket.getInputStream());
            try{
                Object object = objectInputStream.readObject();
                myList = (ArrayList<String>)object;

                for (String s : myList) {
                    System.out.println(s);
                }

            }catch(ClassNotFoundException ex){
                System.out.println(ex.toString());
            }

            socket.close();
        }catch(UnknownHostException e){
            System.out.println(e.toString());
        }catch(IOException e){
            System.out.println(e.toString());
        }

    }

    private static int isParseInt(String str){

        int num = -1;
        try{
            num = Integer.parseInt(str);
        } catch (NumberFormatException e) {
        }

        return num;
    }

}
