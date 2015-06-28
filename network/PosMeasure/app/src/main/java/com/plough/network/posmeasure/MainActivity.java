package com.plough.network.posmeasure;

import android.os.Bundle;
import android.support.v7.app.ActionBarActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.LinearLayout;
import android.widget.SeekBar;

import java.util.HashMap;

public class MainActivity extends ActionBarActivity {
    private myView myView;
    private WiFi wifi;
    private HashMap<String, ApInfo> apMap;
    private int oldProgress;
    private SeekBar seekBar;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
/*		requestWindowFeature(Window.FEATURE_NO_TITLE);
        this.getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN,
                WindowManager.LayoutParams.FLAG_FULLSCREEN);*/
        myView = new myView(this);
        setContentView(R.layout.fragment_m4b5f);
        LinearLayout ll = (LinearLayout) findViewById(R.id.iamgeid);
        ll.addView(myView);
//		new Thread(new myView()).start();
        wifi = new WiFi(this, myView);

        apMap = new HashMap<String, ApInfo>();
        new ReadExcel().Read(getAssets(), "m4b.xls", apMap);
		/*Iterator iter = apMap.entrySet().iterator();
		while (iter.hasNext()) {
			Map.Entry entry = (Map.Entry) iter.next();
			ApInfo a = new ApInfo();
			a = (ApInfo)entry.getValue();
			System.out.println(entry.getKey()+","+a.getDx()+","+a.getDy()+","+a.getRange());
		}*/
        wifi.setApinfoList(apMap);
        seekBar = (SeekBar) this.findViewById(R.id.seekBar);
        oldProgress = 6;
        seekBar.setProgress(oldProgress);
        seekBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress,
                                          boolean fromUser) {
                //          	System.out.println(progress);
                float n = progress-oldProgress;
                if(n>0)
                {
                    myView.zoom((float) Math.pow(1.25f,n));// 1.25*0.8 = 1
                }
                else
                {
                    myView.zoom((float) Math.pow(0.8f,-n));
                }
                oldProgress = progress;
            }
            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {
                // TODO Auto-generated method stub
            }
            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
                // TODO Auto-generated method stub
            }
        });
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        menu.add(0, 0, 0, R.string.rescan);
        menu.add(0, 1, 0, R.string.close_wifi);
        menu.add(0, 2, 0, R.string.exit);
/*		menu.add(0, 3, 0, "�Ŵ�");
		menu.add(0, 4, 0, "��С");*/
        menu.add(0, 5, 0, R.string.reset);
        getMenuInflater().inflate(R.menu.main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();
        if (id == 0)
        {
            wifi.scanWifi();
            //		Location();
        }
        else if (id == 1)
        {
            wifi.CloseWifi();
        }
        else if (id == 2)
        {
            this.finish();
        }
/*		else if (id == 3)
		{
			myView.zoom(1.25f);
		}
		else if (id == 4)
		{
			myView.zoom(0.8f);
		}*/
        else if (id == 5)
        {
            myView.setScale(1f);
            myView.zoom(1f);
            myView.setM_pos(0,0);
            myView.setCircle(0,0,0);
            oldProgress = 6;
            seekBar.setProgress(oldProgress);
        }
        return super.onOptionsItemSelected(item);
    }

    protected void onPause()
    {
        super.onPause();
        wifi.logoff();// ע���㲥
    }

    protected void onResume()
    {
        super.onResume();
        wifi.logon();// ע��㲥
    }
}
