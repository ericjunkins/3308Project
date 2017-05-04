package com.example.lerrrrmps.myfirstapp;

import android.app.ActionBar;
import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.net.wifi.WifiConfiguration;
import android.net.wifi.WifiManager;
import android.os.Handler;
import android.support.v7.app.ActionBarActivity;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.EditText;

import android.widget.TextView;

import android.net.Uri;
import android.widget.MediaController;
import android.widget.VideoView;

import android.os.Vibrator;

import com.cardiomood.android.controls.gauge.SpeedometerGauge;
import org.w3c.dom.Text;

import java.util.List;
import java.util.concurrent.TimeUnit;

import static android.R.attr.checked;

/**
 * Contains the joysticks and video for display
 */
public class MainActivity extends AppCompatActivity implements ControlStickView.JoystickListener,ControlStickViewRight.JoystickListener{
    private Context context;
    private ControlStickView controlStickView;
    private ControlStickViewRight controlStickViewRight;
    private Handler handler;
    private Vibrator myVib; // For Haptic Feedback
    StringBuffer throttle;
    StringBuffer steering;

    TextView infoip, msg;
    TextView response;
	EditText editTextAddress, editTextPort;
	Button buttonConnect, buttonClear;
    public SpeedometerGauge speedometerV;
    public SpeedometerGauge speedometerS;
    private CheckBox connected;


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
        connected = (CheckBox) findViewById(R.id.checkBox);
        throttle = new StringBuffer();
        steering = new StringBuffer();
        throttle.append(0);
        steering.append(0);
        handler = new Handler();
        Button socketButton = (Button) findViewById(R.id.SocketConnect);
        myVib = (Vibrator) this.getSystemService(VIBRATOR_SERVICE); //For Haptic Feedback
        VideoView vidView = (VideoView)findViewById(R.id.myVideo);

        //Wifi network on the Raspberry Pi
        String networkSSID = "WiPi";
        String networkPass = "Durka1234!";

        WifiConfiguration conf = new WifiConfiguration();
        conf.SSID = "\"" + networkSSID + "\"";

        conf.preSharedKey = "\"" + networkPass + "\"";
        WifiManager wifiManager = (WifiManager)context.getSystemService(Context.WIFI_SERVICE);
        wifiManager.addNetwork(conf);

        List<WifiConfiguration> list = wifiManager.getConfiguredNetworks();
        int numTries = 0;
        while(numTries < 10 && wifiManager.getConnectionInfo().getSSID() != networkSSID) {
            for (WifiConfiguration i : list) {
                if (i.SSID != null && i.SSID.equals("\"" + networkSSID + "\"")) {
                    wifiManager.disconnect();
                    wifiManager.enableNetwork(i.networkId, true);
                    wifiManager.reconnect();
                    break;
                }
            }
            try {
                TimeUnit.MILLISECONDS.sleep(100);
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
            numTries += 1;
        }
        try {
            TimeUnit.MILLISECONDS.sleep(500);
        } catch (InterruptedException e) {
            e.printStackTrace();
        }

        String RTSP_URL = "rtsp://192.168.1.80:8554/";
        //String RTSP_URL = "rtsp://wowzaec2demo.streamlock.net/vod/mp4:BigBuckBunny_115k.mov";

        Uri vidUri = Uri.parse(RTSP_URL);
        MediaController mediaController = new MediaController(this);
        mediaController.setAnchorView(vidView);
        vidView.setMediaController(mediaController);
        vidView.setVideoURI(vidUri);
        vidView.start();

        overridePendingTransition(R.anim.fade_in,R.anim.fade_out);
        //connects to the wifi socket to send data
        socketButton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                connected.setChecked(true);
                SocketRunnable socketrunnable = new SocketRunnable(throttle, steering);
                new Thread(socketrunnable).start();

            }
        });

        speedometerV = (SpeedometerGauge) findViewById(R.id.speedometerV);
        speedometerV.setMaxSpeed(40);
        speedometerV.setLabelConverter(new SpeedometerGauge.LabelConverter() {
            @Override
            public String getLabelFor(double progress, double maxProgress){
                return String.valueOf((int) Math.round(progress));
            }
        });

        speedometerS = (SpeedometerGauge) findViewById(R.id.speedometerS);
        speedometerS.setMaxSpeed(40);
        speedometerS.setLabelConverter(new SpeedometerGauge.LabelConverter() {
            @Override
            public String getLabelFor(double progress, double maxProgress){
                return String.valueOf((int) Math.round(progress));
            }
        });
        speedometerV.setMaxSpeed(40);
        speedometerV.setMajorTickStep(5);
        speedometerV.setMinorTicks(3);
        speedometerV.setLabelTextSize(20);
        speedometerV.addColoredRange(0,25, Color.GREEN);
        speedometerV.addColoredRange(25,35, Color.YELLOW);
        speedometerV.addColoredRange(35,40, Color.RED);

        speedometerS.setMaxSpeed(90);
        speedometerS.setMajorTickStep(5);
        speedometerS.setMinorTicks(3);
        //speedometerS.setLabelTextSize(20);
        speedometerS.addColoredRange(0,10, Color.RED);
        speedometerS.addColoredRange(10,25, Color.YELLOW);
        speedometerS.addColoredRange(25,65, Color.GREEN);
        speedometerS.addColoredRange(65,80, Color.YELLOW);
        speedometerS.addColoredRange(80,90, Color.RED);
        speedometerS.setSpeed(45);
    }

    /**
     *
     * @param xPercent Displacement of joystick in X direction
     * @param yPercent Displacement of joystick in Y direction
     * @param source Id of each joystick
     */
    @Override
    public void onJoystickMoved(float xPercent, float yPercent, int source) {
        switch (source)
        {
            case R.id.JoystickLeft:
                steering.delete(0,steering.length());
                steering.append((int) (yPercent * -100));
                myVib.vibrate((int) Math.abs((100* yPercent)/3));
                speedometerS.setSpeed(Math.abs((int) (yPercent* -45) + 45));
                break;

            case R.id.JoystickRight:
                throttle.delete(0,throttle.length());
                throttle.append((int) (yPercent * -100));
                speedometerV.setSpeed(Math.abs(yPercent *40));
                myVib.vibrate((int) Math.abs((100* yPercent)/3));
                break;
        }
    }
}
