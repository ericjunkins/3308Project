package com.example.lerrrrmps.myfirstapp;

import android.app.ActionBar;
import android.content.Context;
import android.content.Intent;
import android.os.Handler;
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
import java.net.InterfaceAddress;
import java.net.ServerSocket;
import java.net.Socket;
import java.nio.IntBuffer;
import java.util.concurrent.atomic.AtomicInteger;

import static android.R.attr.id;
import static android.R.attr.x;
import static android.provider.AlarmClock.EXTRA_MESSAGE;

public class MainActivity extends AppCompatActivity implements ControlStickView.JoystickListener,ControlStickViewRight.JoystickListener{
    private Context context;
    private ControlStickView controlStickView;
    private ControlStickViewRight controlStickViewRight;
    private Handler handler;
    //AtomicInteger throttle;
    //AtomicInteger steering;
    StringBuffer throttle;
    StringBuffer steering;

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
        controlStickView = new ControlStickView(this);
        controlStickViewRight = new ControlStickViewRight(this);
        setContentView(R.layout.activity_main);
        infoip = (TextView) findViewById(R.id.infoip);
        msg = (TextView) findViewById(R.id.msg);

        editTextAddress = (EditText) findViewById(R.id.addressEditText);
		editTextPort = (EditText) findViewById(R.id.portEditText);
		buttonConnect = (Button) findViewById(R.id.connectButton);
		buttonClear = (Button) findViewById(R.id.clearButton);
		response = (TextView) findViewById(R.id.responseTextView);
        //throttle = new AtomicInteger(0);
        //steering = new AtomicInteger(0);
        throttle = new StringBuffer();
        steering = new StringBuffer();
        throttle.append(0);
        steering.append(0);
        handler = new Handler();

        SocketRunnable socketrunnable = new SocketRunnable(throttle, steering);
        new Thread(socketrunnable).start();
        /*
		buttonConnect.setOnClickListener(new View.OnClickListener() {

			@Override
			public void onClick(View arg0) {
                int port = 5002;
				ericClient myClient = new ericClient("192.168.42.1", 5005, response);
				myClient.execute();

            }
		});



		//buttonClear.setOnClickListener(new View.OnClickListener() {

			@Override
			public void onClick(View v) {
				response.setText("");
			}
		});
        */

    }


    @Override
    public void onJoystickMoved(float xPercent, float yPercent, int source) {
        //Log.d("id","source" + source);
        switch (source)
        {
            //NOTE TO SELF SWAP DEFINITIONS OF LEFT/RIGHT JOYSTICKS!!

            case R.id.JoystickLeft:
                //Log.d("Left joystick", "X percent: " + xPercent + "Y percent: " + yPercent);
                //steering.set((int) (xPercent * 100));
                //Log.d("steering", steering.toString());
                steering.delete(0,steering.length());
                steering.append((int) (xPercent * 100));
                break;
            case R.id.JoystickRight:
                //Log.d("Right joystick","X percent: " + xPercent + "Y percent: " + yPercent);
                //throttle.set((int) (xPercent * 100));
                //Log.d("throttle", throttle.toString());
                throttle.delete(0,throttle.length());
                throttle.append((int) (xPercent * 100));
                break;
        }
    }
}
