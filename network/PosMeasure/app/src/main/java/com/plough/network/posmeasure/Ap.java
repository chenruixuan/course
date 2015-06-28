package com.plough.network.posmeasure;

public class Ap {
    private int level;
    private String name;
    private String mac;
    public Ap(String m, String n, int l)
    {
        this.mac = m;
        this.name = n;
        this.level = l;
    }
    public String getMac()
    {
        return mac;
    }
    public String getName() {
        return name;
    }
    public int getLevel()
    {
        return level;
    }
}
