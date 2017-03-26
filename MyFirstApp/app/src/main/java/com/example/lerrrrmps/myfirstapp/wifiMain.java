package com.example.vilok.rc_car;
import android.content.BroadcastReceiver;
import android.net.wifi.ScanResult;
import android.net.wifi.WifiConfiguration;
import android.net.wifi.WifiManager;
import android.os.Bundle;
import android.app.Activity;
import android.content.Context;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.content.Intent;
import android.content.IntentFilter;
import android.widget.CompoundButton;
import android.widget.Switch;
import android.widget.TextView;

import com.example.sairamkrishna.myapplication.R;

import java.util.List;


public class MainActivity extends Activity {
    Switch aSwitch;
    TextView textView;
    WifiManager wifiManager;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        aSwitch = (Switch)findViewById(R.id.myswitch);
        wifiManager = (WifiManager) getSystemService(WIFI_SERVICE);
        textView = (TextView)findViewById(R.id.textView);
        WifiConfiguration wifiConfig = new WifiConfiguration();
        wifiConfig.SSID = String.format("\"%s\"", ssid);
        wifiConfig.preSharedKey = String.format("\"%s\"", key);
        int netId = wifiManager.addNetwork(wifiConfig);
        wifiManager.disconnect();
        wifiManager.enableNetwork(netId, true);
        wifiManager.reconnect();
        //Register Switch for event handling
        aSwitch.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
                if (isChecked && !wifiManager.isWifiEnabled()){
                    wifiManager.setWifiEnabled(true);
                }
                //Switch Off
                else if(!isChecked && wifiManager.isWifiEnabled()){
                    wifiManager.setWifiEnabled(false);
                }
            }
        });
        MyBroadCastReciever myBroadCastReciever = new MyBroadCastReciever();
        // Register broadcast reciever
        registerReceiver(myBroadCastReciever, new IntentFilter(WifiManager.SCAN_RESULTS_AVAILABLE_ACTION));
    }

    class MyBroadCastReciever extends BroadcastReceiver {

        @Override
        public void onReceive(Context context, Intent intent) {
            StringBuffer stringBuffer = new StringBuffer();
            List<ScanResult> list = wifiManager.getScanResults();
            for(ScanResult scanResult : list){
                stringBuffer.append(scanResult);
            }
            textView.setText(stringBuffer);
        }
    }


}
