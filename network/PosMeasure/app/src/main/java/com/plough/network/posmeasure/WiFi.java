package com.plough.network.posmeasure;


import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import android.app.ProgressDialog;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.graphics.PointF;
import android.net.wifi.ScanResult;
import android.net.wifi.WifiManager;
import android.widget.Toast;

public class WiFi{
    private String MaxAp;
    private WifiManager mainWifi;
    private WifiReceiver receiverWifi;
    private List<ScanResult> wifiList;
    private List<Ap> apList;
    private HashMap<String, ApInfo> apinfoList;
    private ProgressDialog dialog;
    private Context context;
    private myView view;
    PointF cPos;
    private float width, height;

    WiFi(Context context, myView myView){
        this.context = context;
        mainWifi = (WifiManager) context.getSystemService(Context.WIFI_SERVICE);
        receiverWifi = new WifiReceiver();
        context.registerReceiver(receiverWifi, new IntentFilter(
                WifiManager.SCAN_RESULTS_AVAILABLE_ACTION));// ע��㲥
        view = myView;
        apList = new ArrayList<Ap>();
        cPos = new PointF();
    }

    public void setApinfoList(HashMap<String, ApInfo> apinfoList) {
        this.apinfoList = apinfoList;
    }

    public void OpenWifi()
    {
        if (!mainWifi.isWifiEnabled())
        {
            mainWifi.setWifiEnabled(true);
        }
    }

    public void logoff()
    {
        context.unregisterReceiver(receiverWifi);// ע���㲥
    }

    public void logon()
    {
        context.registerReceiver(receiverWifi, new IntentFilter(
                WifiManager.SCAN_RESULTS_AVAILABLE_ACTION));// ע��㲥
    }

    public void CloseWifi()
    {
        if (mainWifi.isWifiEnabled())
        {
            mainWifi.setWifiEnabled(false);
        }
    }

    public void scanWifi()//context = MainActivity.this
    {
        OpenWifi();
        dialog = ProgressDialog.show(context, "", "正在扫描WIFI热点,请稍候");
        mainWifi.startScan();
    }

    class WifiReceiver extends BroadcastReceiver
    {
        public void onReceive(Context context, Intent intent)
        {
            wifiList = mainWifi.getScanResults();
            if (dialog != null)
                dialog.dismiss();
            apList.clear();
            String mac;
            String name; // AP的名字
            int level;
            for (int i = 0; i < wifiList.size(); i++) {
                mac = wifiList.get(i).BSSID;
                name = wifiList.get(i).SSID;
                level = wifiList.get(i).level;
                if (name.equals("seu-wlan")) {
                    Ap ap = new Ap(mac, name, level);
                    apList.add(ap);
                }
            }
            // 调试用
            String aps = "";
            for (Ap ap : apList) {
                aps += ap.getMac() + " " + ap.getName() + " " + ap.getLevel() + "\n";
            }
            //Toast.makeText(context, aps, Toast.LENGTH_LONG).show();
            MaxAp = Max(apList);
            Toast.makeText(context, MaxAp, Toast.LENGTH_LONG).show();
            Location(MaxAp);
        }
    }
    public void Location(String mac){
        cPos = view.getPos();
        float scale = view.getScale();
        width = view.getBmpWidth()*scale;
        height = view.getBmpHeight()*scale;
        if(apinfoList.containsKey(mac))
        {
            ApInfo temp = new ApInfo();
            temp = apinfoList.get(mac);
            view.setCircle((cPos.x + temp.getDx()*width), (cPos.y+temp.getDy()*height), temp.getRange()*width);
        }
        else{
            view.setCircle(0,0,0);
            Toast.makeText(context, R.string.location_error, Toast.LENGTH_LONG).show();
        }
    }

    public String Max(List<Ap> apList) {
        // TODO Auto-generated method stub
        int max = apList.get(0).getLevel();
        String maxMac = apList.get(0).getMac();
        int temp = 0;
        for(int i = 1;i < apList.size(); i ++){
            temp = apList.get(i).getLevel();
            if(max<temp)
            {
                max = temp;
                maxMac = apList.get(i).getMac();
            }
        }
        return maxMac;
    }

    public String getMaxAp(){
        return MaxAp;
    }

}
