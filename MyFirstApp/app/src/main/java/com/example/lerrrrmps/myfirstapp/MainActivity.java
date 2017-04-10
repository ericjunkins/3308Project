package com.example.lerrrrmps.myfirstapp;

import android.app.ActionBar;
import android.content.Context;
import android.content.Intent;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.EditText;
import android.widget.LinearLayout;
import android.widget.TextView;


import com.example.lerrrrmps.myfirstapp.ControlStickView;

import org.w3c.dom.Text;

import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

import static android.provider.AlarmClock.EXTRA_MESSAGE;

public class MainActivity extends AppCompatActivity implements ControlStickView.JoystickListener{
    private Context context;
    private ControlStickView controlStickView;
    private ControlStickViewRight controlStickViewRight;

    TextView infoip, msg;
    TextView response;
	EditText editTextAddress, editTextPort;
	Button buttonConnect, buttonClear;


    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        this.getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN,WindowManager.LayoutParams.FLAG_FULLSCREEN);
        requestWindowFeature(Window.FEATURE_NO_TITLE);
        context = getApplicationContext();
        controlStickView = new ControlStickView(context);
        controlStickViewRight = new ControlStickViewRight(context);
        setContentView(R.layout.activity_main);
        infoip = (TextView) findViewById(R.id.infoip);
        msg = (TextView) findViewById(R.id.msg);

        editTextAddress = (EditText) findViewById(R.id.addressEditText);
		editTextPort = (EditText) findViewById(R.id.portEditText);
		buttonConnect = (Button) findViewById(R.id.connectButton);
		buttonClear = (Button) findViewById(R.id.clearButton);
		response = (TextView) findViewById(R.id.responseTextView);

		buttonConnect.setOnClickListener(new View.OnClickListener() {

			@Override
			public void onClick(View arg0) {
                int port = 5002;
				ericClient myClient = new ericClient("127.0.1.1", 5002, response);
				myClient.execute();

                /*
                try {
                    Socket socket = new Socket("192.168.42.14",5002);
                    DataOutputStream DOS = new DataOutputStream(socket.getOutputStream());
                    DOS.writeUTF("HELLO WORLD!");
                    socket.close();
                } catch (IOException e) {
                    e.printStackTrace();
                }
                */

            }
		});

		buttonClear.setOnClickListener(new View.OnClickListener() {

			@Override
			public void onClick(View v) {
				response.setText("");
			}
		});


    }
    /*
    @Override
    protected void onDestroy() {
        MainActivity.super.onDestroy();
        server.onDestroy();
    }
    */
    @Override
    public void onJoystickMoved(float xPercent, float yPercent, int source) {
        Log.d("Main Method", "X percent: " + xPercent + "Y percent: " + yPercent);
    }
}
