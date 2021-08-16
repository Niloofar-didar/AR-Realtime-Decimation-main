
package com.arcore.eAR.prototype;

import java.text.SimpleDateFormat;
import java.util.Date;

public class Baseline2 implements Runnable {


    private final MainActivity mInstance;
    private int objind;
    int dindex;



    public Baseline2(MainActivity mInstance, int objindex,  int dindex) {
        this.mInstance=mInstance;
        this.objind=objindex;
        this.dindex=dindex;
    }

    @Override
    public void run() {



            int ind= objind;
            int finalInd = ind;

            float d1= mInstance.renderArray[finalInd].return_distance();
            // search in excel file to find the name of current object and get access to the index of current object
            int indq = mInstance.excelname.indexOf(mInstance.renderArray[finalInd].fileName);
            // excel file has all information for the degredation model
            float gamma = mInstance.excel_gamma.get(indq);
            float a = mInstance.excel_alpha.get(indq);
            float b = mInstance.excel_betta.get(indq);
            float c = mInstance.excel_c.get(indq);
            float q1= 0.5f;
            float q2= 0.8f;



          float deg_error1 =Calculate_deg_er(a, b, c, d1, gamma, q1);

          float deg_error2 =Calculate_deg_er(a, b, c,  d1, gamma, q2);

          float curQ=1;
           float cur_degerror=0;
       float maxd= mInstance.max_d.get(indq);
          if(deg_error1 < maxd )
          {  curQ=q1;
              cur_degerror=deg_error1;
          }

          else if (deg_error2 <maxd) {
              curQ = q2;
              cur_degerror=deg_error2;
          }
          // update total tiri, deg log, quality log, time , and distance log, then redraw obj

        String last_dis=  mInstance.distance_log.get(finalInd);
        mInstance.distance_log.set(finalInd, last_dis +","+ d1);
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss:SSS");
        String last_time= mInstance.time_log.get(finalInd);
        mInstance.time_log.set(finalInd, last_time+ "," +dateFormat.format(new Date()).toString() );

        String lasterror= mInstance.deg_error_log.get(finalInd);
        cur_degerror= (float)(Math.round((float)(cur_degerror * 10000))) / 10000;
        mInstance.deg_error_log.set(finalInd, lasterror+ Float.toString(  cur_degerror) + ",");

        //'''update everything finally'''
        String lastq_log = mInstance.quality_log.get(finalInd);
        mInstance.quality_log.set(finalInd, lastq_log + curQ + ",");


        if ((curQ ) != mInstance.updateratio[finalInd]  ) {
            mInstance.total_tris = mInstance.total_tris - (mInstance.updateratio[finalInd] * mInstance.excel_tris.get(indq));// total =total -1*objtris

            mInstance.total_tris = mInstance.total_tris + (curQ *  mInstance.excel_tris.get(indq));// total = total + 0.8*objtris
            mInstance.percReduction=curQ;
            mInstance.
                    renderArray[finalInd].indirect_redraw( curQ,  finalInd ); // you should have 0.8 and 0.5 for all objects

        }

        mInstance.updateratio[finalInd] = curQ;


    }



    public float Calculate_deg_er(float a,float b,float creal,float d,float gamma, float r1) {

        if(r1==1)
            return  0f;
        float error;
        error = (float) (((a * Math.pow(r1,2)) + (b * r1) + creal) / (Math.pow(d , gamma)));
        return error;
    }


    }
