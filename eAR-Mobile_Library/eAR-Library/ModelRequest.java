package com.arcore.eAR.prototype;


import android.content.Context;
import android.util.Log;

import java.lang.ref.WeakReference;
import java.util.Queue;
import java.util.concurrent.LinkedBlockingQueue;

public class ModelRequest {

    private String filename;
    private float percentageReduction;
    private Context appContext;
    private WeakReference<MainActivity> mainActivityWeakReference;
    private int ID;
    private Queue<Integer> similarRequestIDArray;
    private float cache;
    //private List<Float> cacheratio ;

    ModelRequest(float cr,String filename, float percentageReduction, Context context, MainActivity mainActivity, int mID)
    {
        Log.d("ModelRequest", "Created ModelRequest - filename: " + filename);
        this.filename = filename;
        this.percentageReduction = percentageReduction;
        this.appContext = context;
        this.mainActivityWeakReference = new WeakReference<MainActivity>(mainActivity);
        this.ID = mID;
        this.similarRequestIDArray = new LinkedBlockingQueue<Integer>();
        this.similarRequestIDArray.add(this.ID);
        this.cache=cr;
    }


    ModelRequest(String filename, float percentageReduction, Context context, MainActivity mainActivity)
    {
        Log.d("ModelRequest", "Created ModelRequest - filename: " + filename);
        this.filename = filename;
        this.percentageReduction = percentageReduction;
        this.appContext = context;
        this.mainActivityWeakReference = new WeakReference<MainActivity>(mainActivity);
    }



    public float getCache()
    {
        return cache;
    }
    public float getPercentageReduction()
    {
        return percentageReduction;
    }
    public String getFilename()
    {
        return filename;
    }

    public Context getAppContext()
    {
        return appContext;
    }

    public int getID() { return ID; }
    public Queue<Integer> getSimilarRequestIDArray() { return similarRequestIDArray; }
    public void addIDToArray(int ID)
    {
        similarRequestIDArray.offer(ID);
    }
    public WeakReference<MainActivity> getMainActivityWeakReference()
    {
        return mainActivityWeakReference;
    }






}
