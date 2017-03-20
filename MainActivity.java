package com.example.vilok.rc_car;
import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.app.Activity;
import android.content.Context;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.content.Intent;
import android.content.IntentFilter;



public class MainActivity extends Activity {
    WifiManager mainWifiObj = (WifiManager) getSystemService(Context.WIFI_SERVICE);;

    class WifiScanReceiver extends BroadcastReceiver {
        public void onReceive(Context c, Intent intent) {
        }
    }
    WifiScanReceiver wifiReciever = new WifiScanReceiver();
    registerReceiver(wifiReciever, new IntentFilter(WifiManager.SCAN_RESULTS_AVAILABLE_ACTION));
    List<ScanResult> wifiScanList = mainWifiObj.getScanResults();
    String data = wifiScanList.get(0).toString();
    Button enableButton,disableButton;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        enableButton=(Button)findViewById(R.id.button1);
        disableButton=(Button)findViewById(R.id.button2);

        enableButton.setOnClickListener(new OnClickListener(){
            public void onClick(View v){
                WifiManager wifi = (WifiManager) getSystemService(Context.WIFI_SERVICE);
                wifi.setWifiEnabled(true);
            }
        });


        disableButton.setOnClickListener(new OnClickListener(){
            public void onClick(View v){
                WifiManager wifi = (WifiManager) getSystemService(Context.WIFI_SERVICE);
                wifi.setWifiEnabled(false);
            }
        });
    }

}
