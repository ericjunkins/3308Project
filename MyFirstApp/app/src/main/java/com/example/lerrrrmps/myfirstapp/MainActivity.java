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

import android.widget.TextView;
import android.net.Uri;
import android.widget.MediaController;
import android.widget.VideoView;
import org.w3c.dom.Text;


public class MainActivity extends AppCompatActivity implements ControlStickView.JoystickListener,ControlStickViewRight.JoystickListener{
    private Context context;
    private ControlStickView controlStickView;
    private ControlStickViewRight controlStickViewRight;
    private Handler handler;
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
        throttle = new StringBuffer();
        steering = new StringBuffer();
        throttle.append(0);
        steering.append(0);
        handler = new Handler();
        Button socketButton = (Button) findViewById(R.id.SocketConnect);

        VideoView vidView = (VideoView)findViewById(R.id.myVideo);

        //String RTSP_URL = "rtsp://192.168.1.80:8554/myvid1.mp4";
        String RTSP_URL = "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov";
        Uri vidUri = Uri.parse(RTSP_URL);
        //Log.d("uri parse:", vidUri.toString());
        MediaController mediaController = new MediaController(this);
        mediaController.setAnchorView(vidView);
        vidView.setMediaController(mediaController);
        vidView.setVideoURI(vidUri);
        vidView.start();

        overridePendingTransition(R.anim.fade_in,R.anim.fade_out);
        
        socketButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                SocketRunnable socketrunnable = new SocketRunnable(throttle, steering);
                new Thread(socketrunnable).start();
            }
        });

    }


    @Override
    public void onJoystickMoved(float xPercent, float yPercent, int source) {
        //Log.d("id","source" + source);
        TextView myTextViewV = (TextView) findViewById(R.id.velocity_amount);
        TextView myTextViewS = (TextView) findViewById(R.id.steering_amount);


        switch (source)
        {
            //NOTE TO SELF SWAP DEFINITIONS OF LEFT/RIGHT JOYSTICKS!!

            case R.id.JoystickLeft:
                //Log.d("Left joystick", "X percent: " + xPercent + "Y percent: " + yPercent);
                //steering.set((int) (xPercent * 100));
                //Log.d("steering", steering.toString());
                steering.delete(0,steering.length());
                steering.append((int) (yPercent * -100));
                myTextViewS.setText((int) (yPercent*-45) +" deg");

                break;
            case R.id.JoystickRight:
                //Log.d("Right joystick","X percent: " + xPercent + "Y percent: " + yPercent);
                //throttle.set((int) (xPercent * 100));
                //Log.d("throttle", throttle.toString());
                throttle.delete(0,throttle.length());
                throttle.append((int) (yPercent * -100));
                myTextViewV.setText((int) (yPercent*-40/2) + " mi/hr");
                break;
        }
    }
}
