package com.plough.network.posmeasure;

import java.io.InputStream;
import java.util.HashMap;

import android.content.res.AssetManager;
import jxl.Cell;
import jxl.Sheet;
import jxl.Workbook;

public class ReadExcel {

    public void Read(AssetManager am, String file, HashMap<String, ApInfo> ApInfoList){
        try {
            InputStream in = am.open(file);
            Workbook book = Workbook.getWorkbook(in);
            //获得第一个工作表对象
            Sheet sheet = book.getSheet(0);
            //得到第一列第一行的单元格
            int rows = sheet.getRows();
            String temp="";
            int column = sheet.getColumns();
            for (int i=1;i<rows;i++){
                ApInfo apinfo = new ApInfo();
                for (int j=0;j<column;j++){
                    Cell cell1 = sheet.getCell(j, i);
                    String result = cell1.getContents();
                    if(j == 0)
                        temp = result;
                    else if(j==1)
                    {
                        apinfo.setDx(Float.valueOf(result));
                    }
                    else if(j==2)
                    {
                        apinfo.setDy(Float.valueOf(result));
                    }
                    else if(j==3)
                    {
                        apinfo.setRange(Float.valueOf(result));
                    }
                }
                ApInfoList.put(temp,apinfo);
            }
            book.close();
            in.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
