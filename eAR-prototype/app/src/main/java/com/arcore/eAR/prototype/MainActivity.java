package com.arcore.eAR.prototype;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintStream;
import java.io.PrintWriter;
import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.*;
import java.util.Queue;
import java.util.concurrent.BlockingQueue;
import java.util.concurrent.CompletableFuture;

import android.os.Handler;
import android.os.Looper;
import android.os.Message;
import android.util.Log;

import java.util.LinkedList;
import java.util.concurrent.LinkedBlockingQueue;
import java.util.concurrent.ThreadPoolExecutor;
import java.util.concurrent.TimeUnit;
import android.net.Uri;
import android.opengl.Matrix;
import android.os.Bundle;
import android.os.CountDownTimer;
import android.support.v7.app.AlertDialog;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.SeekBar;
import android.widget.Spinner;
import android.widget.Switch;
import android.widget.TextView;
import android.widget.Toast;

import com.google.ar.core.Anchor;
import com.google.ar.core.Camera;
import com.google.ar.core.Frame;
import com.google.ar.core.HitResult;
import com.google.ar.core.Plane;
import com.google.ar.core.Trackable;
import com.google.ar.core.TrackingState;
import com.google.ar.sceneform.AnchorNode;
import com.google.ar.sceneform.Node;
import com.google.ar.sceneform.math.Vector3;
import com.google.ar.sceneform.rendering.ModelRenderable;
import com.google.ar.sceneform.rendering.Renderable;
import com.google.ar.sceneform.ux.ArFragment;
import com.google.ar.sceneform.ux.TransformableNode;

import java.text.DecimalFormat;
import java.util.ArrayList;
import java.util.List;

import java.lang.Math;
import java.io.InputStream;

import static java.lang.Math.abs;


public class MainActivity extends AppCompatActivity implements AdapterView.OnItemSelectedListener {








    private ArFragment fragment;
    private PointerDrawable pointer = new PointerDrawable();
    private static MainActivity Instance = new MainActivity();

    public static MainActivity getInstance()
    {
        return Instance;
    }

    private boolean isTracking;
    private boolean isHitting;
     baseRenderable renderArray[] = new baseRenderable[100];
     float ratioArray[] = new float[100];
     float cacheArray[] = new float[100];
     float updateratio[] = new float[100];
    float updatednetw[] = new float[100];
    int maxtime=20; // should be even num
    // if 5, goes up to 2.5 s. if 10, goes up to 5s

    public int objectCount = 0;
    private String[] assetList = null;
    private Integer[] objcount = new Integer[]{1, 10, 20, 0, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 160, 170, 180, 190, 200, 220, 240, 260, 300, 340, 380, 430, 500};
    private String currentModel = null;
    //refswitch is for decimate all without predict key and it can also run the baseline approach if you push the predict key
    private boolean referenceObjectSwitchCheck = false;
    private boolean multipleSwitchCheck = false;
    private boolean askedbefore = false;
     int nextID = 0;
    boolean under_Perc = false; // it is used for seekbar and the percentages with 0.1 precios like 1.1%, I press 11% in app and /1000 here
    CountDownTimer countDownTimer;
    float agpu=4.10365E-05f;
    float gpu_min_tres=35000;
    float bgpu=44.82908722f;
    float bwidth= 600;

    List<String> mLines = new ArrayList<>();
    Map<String, Integer> time_tris = new HashMap<>();
    Map<String, Integer> time_gpu = new HashMap<>();


    ArFragment arFragment = (ArFragment)
            getSupportFragmentManager().findFragmentById(R.id.sceneform_fragment);


    private DecimalFormat posFormat = new DecimalFormat("###.##");
    private final int SEEKBAR_INCREMENT = 10;
    File dateFile;
    File Nil;
    File obj;
    File tris_num;
    File GPU_usage;

    int sum = 0;
    double total_area = 0;
    double total_vol = 0;
    float percReduction = 0;
    int decision_p=1;
    List<Integer> o_tris = new ArrayList<>();
    List<Double> volume_list = new ArrayList<>();
    List<Double> area_list = new ArrayList<>();
    List<Float> v_dist = new ArrayList<>();
    List<Float> old_percentage = new ArrayList<>();
    List<Float> new_percentage = new ArrayList<>();
    List<Boolean> redrawed = new ArrayList<>();

    List<Float> prevquality = new ArrayList<>();
    Process process2;
    List<Float> excel_alpha = new ArrayList<>();
    List<Float> excel_betta = new ArrayList<>();
    List<Float> excel_filesize = new ArrayList<>();
    List<Float> excel_c = new ArrayList<>();
    List<Float> excel_gamma = new ArrayList<>();
    List<Float> excel_maxd = new ArrayList<>();
    List<String> excelname = new ArrayList<>();
    List<Integer> excel_tris = new ArrayList<>();
    List<Float> excel_mindis = new ArrayList<>();
    List<Boolean> closer = new ArrayList<>();
    List<Float> max_d = new ArrayList<>();
    List<String> temppredict = new ArrayList<>();
    List<String> tempquality = new ArrayList<>();
    List<Float> best_cur_eb = new ArrayList<>();
    List<Float> gpusaving = new ArrayList<>();
    List<String> eng_dec = new ArrayList<>();
    List<Float> eng_blc = new ArrayList<>();
    List<Float> fthr = new ArrayList<>();
    List<String> quality_log = new ArrayList<>();
    List<String> time_log = new ArrayList<>();
    List<String> distance_log = new ArrayList<>();
    List<String> deg_error_log = new ArrayList<>();
    List<String> GPU_Ut_log = new ArrayList<>();
    List<Integer> Server_reg_Freq = new ArrayList<>();
    List<Thread> current_thread = new ArrayList<>();
    List<Thread> decimate_thread = new ArrayList<>();
    int decimate_count=0;

    String policy= "Mean";
    private String[] Policy_Selection = new String[]{"Aggressive", "Mean", "Conservative"};

    int temp_ww = (((maxtime/2)-1) - (decision_p-1))/ decision_p;
   // private int[] W_Selection = IntStream.range(1, temp_ww).toArray();
   private Integer[] W_Selection= new Integer[temp_ww];

    private Integer[] BW_Selection= new Integer[]{100, 200, 303, 400, 500,600,700,800,900,1000,1100,1200,1300,1400,1500,1600};
    private Integer[] MDE_Selection= new Integer []{2,6};
    int finalw=4;
    float max_d_parameter=0.2f;


    float area_percentage=0.5f;
    // Conservative , or mean are other options
    float total_tris=0;
    //List<Boolean>  = new ArrayList<>();
    private boolean hit_distance[] = new boolean[800];

    ///prediction
    private ArrayList<Float> timeLog = new ArrayList<>();
    ArrayList<Boolean> obj_backward = new ArrayList<>();
    Timer t2;
    private float timeInSec = 0;
    float phone_batttery_cap= 12.35f; // in w*h
    private ArrayList<ArrayList<Float> > current = new ArrayList<ArrayList<Float> >();
    private HashMap<Integer, ArrayList<ArrayList<Float>>> prmap=new HashMap<Integer, ArrayList<ArrayList<Float>>>();
    private HashMap<Integer, ArrayList<ArrayList<Float>>> marginmap=new HashMap<Integer, ArrayList<ArrayList<Float>>>();
    private HashMap<Integer, ArrayList<ArrayList<Float>>> errormap=new HashMap<Integer, ArrayList<ArrayList<Float>>>();
    private HashMap<Integer, ArrayList<ArrayList<Float>>> booleanmap=new HashMap<Integer, ArrayList<ArrayList<Float>>>();

    private LinkedList<LinkedList<Float> > last_errors = new LinkedList<LinkedList<Float> >();
    private LinkedList<Float>  last_errors_x = new LinkedList<Float> ();
    private LinkedList<Float>  last_errors_z = new LinkedList<Float> ();
     HashMap<Integer, ArrayList<Float> >predicted_distances=new HashMap<Integer, ArrayList<Float>>();
    private HashMap<Integer, ArrayList<Float> >nextfive_fourcenters=new HashMap<Integer, ArrayList<Float>>();
    List<Float> d1_prev= new ArrayList<Float>();// for prediction module we need to store dprev
    private float objX, objZ;
    private ArrayList<ArrayList<Float> > nextfivesec = new ArrayList<ArrayList<Float> >();

    private float alpha = 0.7f;
    int max_datapoint=25;


    private static final int KEEP_ALIVE_TIME = 500;
    private final int CORE_THREAD_POOL_SIZE = 10;

    private final int MAX_THREAD_POOL_SIZE = 10;
    private final TimeUnit KEEP_ALIVE_TIME_UNIT= TimeUnit.MILLISECONDS;
    private final BlockingQueue<Runnable> mWorkQueue= new LinkedBlockingQueue<Runnable>();
    private final ThreadPoolExecutor algoThreadPool=new ThreadPoolExecutor(CORE_THREAD_POOL_SIZE, MAX_THREAD_POOL_SIZE,
                                                 KEEP_ALIVE_TIME, KEEP_ALIVE_TIME_UNIT, mWorkQueue);


    //Code receives messages from modelrequest manager
    private final Handler handler = new Handler(Looper.getMainLooper()) {
        @Override
        public void handleMessage(Message inputMessage) {
            ModelRequest tempModelRequest = (ModelRequest) inputMessage.obj;
            Queue<Integer> tempIDArray = tempModelRequest.getSimilarRequestIDArray();

            if (referenceObjectSwitchCheck==true){//baseline 2
                int ind= tempModelRequest.getID();
                //redraw object based on ID;
                renderArray[ind].redraw(ind);

            }


            else{
                while (tempIDArray.isEmpty() == false) { // doesn't come here for baseline 2 - this is for eAR

                    for (int i = 0; i < objectCount; i++) {


                        if (renderArray[i].getID() == tempIDArray.peek()) {
                            Log.d("ModelRequest", "renderArray[" + i + "] ID: " + renderArray[i].getID()
                                    + " matches tempModelRequest SimilarRequestID: " + tempIDArray.peek());
                            renderArray[i].redraw(i);

                            //  }
                             }
                        }
                        tempIDArray.remove();

                    }
            }
        }
    };


    public Handler getHandler() {
        return handler;
    }

    //used for abstraction of reference renderable and decimated renderable
    public abstract class baseRenderable {
        public TransformableNode baseAnchor;
        public String fileName;
        private int ID;


        public void setAnchor(TransformableNode base) {
            baseAnchor = base;
        }

        public String getFileName() {
            return fileName;
        }

        public int getID() {
            return ID;
        }

        public void setID(int mID) {
            ID = mID;
        }

        public abstract void redraw(int i);

        public abstract void decimatedModelRequest(float percentageReduction, int i, boolean rd);
        public abstract void indirect_redraw(float percentageReduction, int i);
        public abstract void print(AdapterView<?> parent, int pos);

        public abstract void distance();

        public abstract float return_distance();


        public abstract float return_distance_predicted(float x, float z);

        public void detach() {
            try {
                baseAnchor.getScene().onRemoveChild(baseAnchor.getParent());
                baseAnchor.setRenderable(null);
                baseAnchor.setParent(null);

            } catch (Exception e) {
                Log.w("Detach", e.getMessage());
            }

        }

    }

    //reference renderables, cannot be changed when decimation percentage is selected
    private class refRenderable extends baseRenderable {
        refRenderable(String filename) {
            this.fileName = filename;
            setID(nextID);
            nextID++;
        }

        public void decimatedModelRequest(float percentageReduction, int i, boolean rd) {
            return;
        }
        public void indirect_redraw(float percentageReduction, int i) {
            return;
        }


        public void redraw(int j) {
            return;
        }

        //used for reporting camera, obj position for debugging purposes
        public void print(AdapterView<?> parent, int pos) {
            Frame frame = fragment.getArSceneView().getArFrame();
            String item = "--REFERENCE OBJECT-- --" + fileName + "--\n" +
                    "User Score: " + parent.getItemAtPosition(pos).toString() + "\n" +
                    "Time: " + new SimpleDateFormat("yyyy_MM_dd_HH:mm:ss", java.util.Locale.getDefault()).format(new Date()) + "\n";

            item += "Camera position: " +
                    "[" + posFormat.format(frame.getCamera().getPose().tx()) +
                    "], [" + posFormat.format(frame.getCamera().getPose().ty()) +
                    "], [" + posFormat.format(frame.getCamera().getPose().tz()) +
                    "]\n";

            item += ("Object position: ["
                    + posFormat.format(baseAnchor.getWorldPosition().x) +
                    "], [" + posFormat.format(baseAnchor.getWorldPosition().y) +
                    "], [" + posFormat.format(baseAnchor.getWorldPosition().z) +
                    "]\n");

            item += ("Distance from camera: "
                    + Math.sqrt((Math.pow((baseAnchor.getWorldPosition().x - frame.getCamera().getPose().tx()), 2)
                    + Math.pow((baseAnchor.getWorldPosition().y - frame.getCamera().getPose().ty()), 2)
                    + Math.pow((baseAnchor.getWorldPosition().z - frame.getCamera().getPose().tz()), 2)))
                    + " m\n");

            item += "\n\n";


            try {
                FileOutputStream os = new FileOutputStream(dateFile, true);
                os.write(item.getBytes());
                os.close();
            } catch (IOException e) {
                Log.e("StatWriting", e.getMessage());
            }
        }


        public void distance() {
            {
                Frame frame = fragment.getArSceneView().getArFrame();

                float dist = ((float) Math.sqrt(Math.pow((baseAnchor.getWorldPosition().x - frame.getCamera().getPose().tx()), 2) + Math.pow((baseAnchor.getWorldPosition().y - frame.getCamera().getPose().ty()), 2) + Math.pow((baseAnchor.getWorldPosition().z - frame.getCamera().getPose().tz()), 2)));
                v_dist.add(dist);

            }
        }

        public float return_distance() {

            Frame frame = fragment.getArSceneView().getArFrame();

            float dist = ((float) Math.sqrt(Math.pow((baseAnchor.getWorldPosition().x - frame.getCamera().getPose().tx()), 2) + Math.pow((baseAnchor.getWorldPosition().y - frame.getCamera().getPose().ty()), 2) + Math.pow((baseAnchor.getWorldPosition().z - frame.getCamera().getPose().tz()), 2)));
            dist = (float)(Math.round((float)(dist * 100))) / 100;
            return dist;

        }



        public float return_distance_predicted(float px,float pz) {

            float dist = ((float) Math.sqrt(Math.pow((baseAnchor.getWorldPosition().x - px), 2)  + Math.pow((baseAnchor.getWorldPosition().z - pz), 2)));

            dist = (float)(Math.round((float)(dist * 100))) / 100;
            return dist;

        }

    }


    //Decimated renderable -- has the ability to redraw and make model request from the manager
    private class decimatedRenderable extends baseRenderable {
        decimatedRenderable(String filename) {
            this.fileName = filename;
            setID(nextID);
            nextID++;
        }


        public void indirect_redraw(float percentageReduction, int id) {

            percReduction = percentageReduction;
            renderArray[id].redraw(id);
        }


        public void decimatedModelRequest(float percentageReduction, int id, boolean redraw_direct) {
            percReduction = percentageReduction;
            ModelRequestManager.getInstance().add(new ModelRequest(cacheArray[id], fileName, percentageReduction, getApplicationContext(), MainActivity.this, id),redraw_direct );
        }

        public void distance() {
            Frame frame = fragment.getArSceneView().getArFrame();

            float dist = ((float) Math.sqrt(Math.pow((baseAnchor.getWorldPosition().x - frame.getCamera().getPose().tx()), 2) + Math.pow((baseAnchor.getWorldPosition().y - frame.getCamera().getPose().ty()), 2) + Math.pow((baseAnchor.getWorldPosition().z - frame.getCamera().getPose().tz()), 2)));
            v_dist.add(dist);
        }

        public float return_distance() {

            Frame frame = fragment.getArSceneView().getArFrame();

            float dist = ((float) Math.sqrt(Math.pow((baseAnchor.getWorldPosition().x - frame.getCamera().getPose().tx()), 2) + Math.pow((baseAnchor.getWorldPosition().y - frame.getCamera().getPose().ty()), 2) + Math.pow((baseAnchor.getWorldPosition().z - frame.getCamera().getPose().tz()), 2)));
            dist = (float)(Math.round((float)(dist * 100))) / 100;
            return dist;

        }

        public float return_distance_predicted(float px,float pz) {

            Frame frame = fragment.getArSceneView().getArFrame();

            float dist = ((float) Math.sqrt(Math.pow((baseAnchor.getWorldPosition().x - px), 2)  + Math.pow((baseAnchor.getWorldPosition().z - pz), 2)));

            dist = (float)(Math.round((float)(dist * 100))) / 100;
            return dist;

        }


        public void redraw(int j) {


            Log.d("ServerCommunication", "Redraw waiting is done");
            try {
                    Frame frame = fragment.getArSceneView().getArFrame();
                    while(frame==null)
                        frame = fragment.getArSceneView().getArFrame();

                } catch (Exception e) {
                    e.printStackTrace();
                }

                if (fragment.getContext()!=null){
                CompletableFuture<Void> renderableFuture =
                        ModelRenderable.builder()
                                .setSource(fragment.getContext(), Uri.fromFile(new File(getExternalFilesDir(null), "/decimated" + fileName + percReduction + ".glb")))
                                .setIsFilamentGltf(true)
                                .build()
                                .thenAccept(renderable -> baseAnchor.setRenderable(renderable))
                                .exceptionally((throwable -> {
                                    AlertDialog.Builder builder = new AlertDialog.Builder(getApplicationContext());
                                    builder.setMessage(throwable.getMessage())
                                            .setTitle("Codelab error!");
                                    AlertDialog dialog = builder.create();
                                    dialog.show();
                                    return null;
                                }));
            // update tris and gu log
            }
        }

        public void print(AdapterView<?> parent, int pos) {
            Frame frame = fragment.getArSceneView().getArFrame(); // it's OK
            SeekBar seekBar = (SeekBar) findViewById(R.id.simpleBar);
            String item =
                    "==DECIMATED OBJECT== ==" + fileName + "==\n" +
                            "Simplification Percentage: " + seekBar.getProgress() + "%" +
                            " - User Score: " + parent.getItemAtPosition(pos).toString() + "\n" +
                            "Date & time: " + new SimpleDateFormat("yyyy_MM_dd_HH:mm:ss", java.util.Locale.getDefault()).format(new Date()) + "\n";

            item += "Camera position: " +
                    "[" + posFormat.format(frame.getCamera().getPose().tx()) +
                    "[" + posFormat.format(frame.getCamera().getPose().tx()) +
                    "], [" + posFormat.format(frame.getCamera().getPose().ty()) +
                    "], [" + posFormat.format(frame.getCamera().getPose().tz()) +
                    "]\n";

            item += ("Object position: ["
                    + posFormat.format(baseAnchor.getWorldPosition().x) +
                    "], [" + posFormat.format(baseAnchor.getWorldPosition().y) +
                    "], [" + posFormat.format(baseAnchor.getWorldPosition().z) +
                    "]\n");

            item += ("Distance from camera: "
                    + Math.sqrt((Math.pow((baseAnchor.getWorldPosition().x - frame.getCamera().getPose().tx()), 2)
                    + Math.pow((baseAnchor.getWorldPosition().y - frame.getCamera().getPose().ty()), 2)
                    + Math.pow((baseAnchor.getWorldPosition().z - frame.getCamera().getPose().tz()), 2)))
                    + " m\n");

            item += "\n\n";


            try {
                FileOutputStream os = new FileOutputStream(dateFile, true);
                os.write(item.getBytes());
                os.close();
            } catch (IOException e) {
                Log.e("StatWriting", e.getMessage());
            }
        }


    }


    @Override
    protected void onCreate(Bundle savedInstanceState) {

        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);

        //create the file to store user score data
        dateFile = new File(getExternalFilesDir(null),
                (new SimpleDateFormat("yyyy_MM_dd_HH:mm:ss", java.util.Locale.getDefault()).format(new Date())) + ".txt");

        Nil = new File(getExternalFilesDir(null), "Nil.txt");
        obj = new File(getExternalFilesDir(null), "obj.txt");
        tris_num = new File(getExternalFilesDir(null), "tris_num.txt");
        GPU_usage= new File(getExternalFilesDir(null), "GPU_usage.txt");
        //user score setup
        Spinner ratingSpinner = (Spinner) findViewById(R.id.userScoreSpinner);
        ratingSpinner.setOnItemSelectedListener(this);
        ArrayAdapter<String> ratingAdapter = new ArrayAdapter<String>(MainActivity.this,
                android.R.layout.simple_list_item_1, getResources().getStringArray(R.array.user_score));
        ratingAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        ratingSpinner.setAdapter(ratingAdapter);

        try {
            InputStream iS = getResources().getAssets().open("tris.txt");
            InputStreamReader inputreader = new InputStreamReader(iS);
            BufferedReader reader = new BufferedReader(inputreader);
            String line, line1 = "";

            while ((line = reader.readLine()) != null) {
                mLines.add(line);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }


        givenUsingTimer_whenSchedulingTaskOnce_thenCorrect();

        StringBuilder sb = new StringBuilder();

        int ind = 0;
        while (ind < mLines.size()) {
            sb.append(mLines.get(ind) + "\n ,");
            ind++;
        }


        Spinner MDESpinner = (Spinner) findViewById(R.id.MDE);
        MDESpinner.setOnItemSelectedListener(this);
        ArrayAdapter<Integer> MDESelectAdapter = new ArrayAdapter<Integer>(MainActivity.this,android.R.layout.simple_list_item_1, MDE_Selection);
        MDESelectAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        MDESpinner.setAdapter(MDESelectAdapter);



        try {

            InputStream inputStream = getResources().getAssets().open("degmodel_file.csv");
            // openFileInput("degmodel_file.csv");
            InputStreamReader inputStreamReader = new InputStreamReader(inputStream);

            BufferedReader br = new BufferedReader(inputStreamReader);
            String line = "";
            line = br.readLine();
            while ((line = br.readLine()) != null) {
                // use comma as separator
                String[] cols = line.split(",");
                excel_alpha.add(Float.parseFloat(cols[0]));
                excel_betta.add(Float.parseFloat(cols[1]));
                excel_c.add(Float.parseFloat(cols[2]));
                excel_gamma.add(Float.parseFloat(cols[3]));
                excel_maxd.add(Float.parseFloat(cols[4]));
                excel_tris.add(Integer.parseInt(cols[5]));
                excel_mindis.add(Float.parseFloat(cols[7]));
                excel_filesize.add(Float.parseFloat(cols[8]));
                excelname.add((String)(cols[6]));
                        //.substring(2, cols[6].length() - 2));

                max_d.add(max_d_parameter * Float.parseFloat(cols[4]));


            }

        } catch (FileNotFoundException e) {
            e.printStackTrace();
        } catch (IOException e) {
            e.printStackTrace();
        }


        // prediction code Requirements
        for ( int i=0; i<maxtime; i++) {
            prmap.put(i, new ArrayList<ArrayList<Float>>());
            marginmap.put(i, new ArrayList<ArrayList<Float>>());
            errormap.put(i, new ArrayList<ArrayList<Float>>());
            booleanmap.put(i, new ArrayList<ArrayList<Float>>());

        }


        for(int i=0;i < maxtime/2;i++) {
        nextfivesec.add(new ArrayList<Float>());

        nextfive_fourcenters.put(i, new ArrayList<>());
        }

        for ( int i=0; i<maxtime; i++) {
            marginmap.get(i).add(new ArrayList<Float>(Arrays.asList(0.3f, 0.3f)));
            errormap.get(i).add(new ArrayList<Float>(Arrays.asList(0f, 0f)));
        }


        //get the asset list for model select
        try {
            //get list of .glb's from assets
            //assetList = getAssets().list("models");
            assetList = getAssets().list("models");
            //take off .glb from every string for use with server communication
            for (int i = 0; i < assetList.length; i++) {
                assetList[i] = assetList[i].substring(0, assetList[i].length() - 4);
            }
        } catch (IOException e) {
            Log.e("AssetReading", e.getMessage());
        }

        //setup the model drop down menu
        Spinner modelSpinner = (Spinner) findViewById(R.id.modelSelect);
        modelSpinner.setOnItemSelectedListener(this);
        ArrayAdapter<String> modelSelectAdapter = new ArrayAdapter<String>(MainActivity.this,
                android.R.layout.simple_list_item_1, assetList);
        modelSelectAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        modelSpinner.setAdapter(modelSelectAdapter);


        //setup the model drop down for object count selection
        Spinner countSpinner = (Spinner) findViewById(R.id.modelSelect2);
        countSpinner.setOnItemSelectedListener(this);
        ArrayAdapter<Integer> countSelectAdapter = new ArrayAdapter<Integer>(MainActivity.this,
                android.R.layout.simple_list_item_1, objcount);
        countSelectAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        countSpinner.setAdapter(countSelectAdapter);


        for (int a = 0; a < temp_ww; a++) {
            W_Selection[a] = a + 1;
        }
        //setup the model drop down for object count selection
        Spinner WSpinner = (Spinner) findViewById(R.id.WSelect);
        WSpinner.setOnItemSelectedListener(this);
        ArrayAdapter<Integer> WSelectAdapter = new ArrayAdapter<Integer>(MainActivity.this,android.R.layout.simple_list_item_1, W_Selection);
        WSelectAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        WSpinner.setAdapter(WSelectAdapter);

        final int[] ww = {(int) WSpinner.getSelectedItem()};


        //setup the model drop down for object count selection
        Spinner BWSpinner = (Spinner) findViewById(R.id.Bwidth);
        BWSpinner.setOnItemSelectedListener(this);
        ArrayAdapter<Integer> BWSelectAdapter = new ArrayAdapter<Integer>(MainActivity.this,android.R.layout.simple_list_item_1, BW_Selection);
        BWSelectAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        BWSpinner.setAdapter(BWSelectAdapter);


        Spinner policySpinner = (Spinner) findViewById(R.id.policy);
        policySpinner.setOnItemSelectedListener(this);
        ArrayAdapter<String> policySelectAdapter = new ArrayAdapter<String>(MainActivity.this,
                android.R.layout.simple_list_item_1, Policy_Selection);
        policySelectAdapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
        policySpinner.setAdapter(policySelectAdapter);

        policy=policySpinner.getSelectedItem().toString();


        //decimate all obj at the same time
        Switch referenceObjectSwitch = (Switch) findViewById(R.id.refSwitch);
        referenceObjectSwitch.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton compoundButton, boolean b) {

                if (b) {
                    referenceObjectSwitchCheck = true;
                } else {
                    referenceObjectSwitchCheck = false;
                }
            }
        });

        // for prediction
        Switch multipleSwitch = (Switch) findViewById(R.id.refSwitch4);
        multipleSwitch.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton compoundButton, boolean b) {
                if (b) {
                    multipleSwitchCheck = true;


                } else {
                    multipleSwitchCheck = false;
                    // stopService(i);


                }
            }

        });


        Switch underpercSwitch = (Switch) findViewById(R.id.un_percSwitch3);
        underpercSwitch.setOnCheckedChangeListener(new CompoundButton.OnCheckedChangeListener() {
            @Override
            public void onCheckedChanged(CompoundButton compoundButton, boolean b) {
                if (b) {
                    under_Perc = true;
                } else {
                    under_Perc = false;
                }
            }
        });


        //create button listener for predict
        Button predictObjectButton = (Button) findViewById(R.id.predict);

        predictObjectButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                // int selectedCount = (int) countSpinner.getSelectedItem();

                    // if (multipleSwitchCheck == true) {

                bwidth= (int) BWSpinner.getSelectedItem();
                 for(int i=0; i< objectCount; i++)
                    d1_prev.set(i,predicted_distances.get(i).get(0) );

           //for eAR
            if (multipleSwitchCheck == true){// feb -> multiple = false

               Timer t = new Timer();
                final int[] count = {0};
                t.scheduleAtFixedRate(
                        new TimerTask() {
                            public void run() {

                                if(objectCount==0 || multipleSwitchCheck == false) {
                                    t.cancel();
                                    percReduction=1;
                                }
                                ww[0] = (int)WSpinner.getSelectedItem();


                                finalw=  ww[0];
                                int dindex = 0;// shows next time index
                                float  d1;

                                for (int ind = 0; ind < objectCount; ind++) {

                                    new DecisionAlgorithm(MainActivity.this, ind, finalw, dindex).run();

                                }

                                }
                            },
                            0,      // run first occurrence immediatetly
                        (long) (decision_p*1000));
            }




           else if (referenceObjectSwitchCheck==true)
            {

                Timer t = new Timer();
                final int[] count = {0}; // should be before here
                t.scheduleAtFixedRate(
                        new TimerTask() {
                            public void run() {

                                if(objectCount==0 || referenceObjectSwitchCheck==false   )
                                {t.cancel();
                                percReduction=1;}

                                int dindex = 0;// shows next time index

                                for (int ind = 0; ind < objectCount; ind++) {

                                    int finalInd = ind;

                                    float d1= renderArray[finalInd].return_distance();
                                    // search in excel file to find the name of current object and get access to the index of current object
                                    int indq = excelname.indexOf(renderArray[finalInd].fileName);
                                    float gamma = excel_gamma.get(indq);
                                    float a = excel_alpha.get(indq);
                                    float b = excel_betta.get(indq);
                                    float c = excel_c.get(indq);
                                    float q1= 0.5f;
                                    float q2= 0.8f;

                                    float deg_error1 =Calculate_deg_er(a, b, c, d1, gamma, q1);
                                    float deg_error2 =Calculate_deg_er(a, b, c,  d1, gamma, q2);

                                    float curQ=1;
                                    float cur_degerror=0;
                                    float maxd= max_d.get(indq);
                                    if(deg_error1 < maxd )
                                    {  curQ=q1;
                                        cur_degerror=deg_error1;
                                    }

                                    else if (deg_error2 <maxd) {
                                        curQ = q2;
                                        cur_degerror=deg_error2;
                                    }
                                    // update total tiri, deg log, quality log, time , and distance log, then redraw obj

                                    String last_dis=  distance_log.get(finalInd);
                                    distance_log.set(finalInd, last_dis +","+ d1);
                                    SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss:SSS");
                                    String last_time= time_log.get(finalInd);
                                    time_log.set(finalInd, last_time+ "," +dateFormat.format(new Date()).toString() );

                                    String lasterror= deg_error_log.get(finalInd);
                                    cur_degerror= (float)(Math.round((float)(cur_degerror * 10000))) / 10000;
                                    deg_error_log.set(finalInd, lasterror+ Float.toString(  cur_degerror) + ",");

                                    //'''upfdate everythong finally'''
                                    String lastq_log = quality_log.get(finalInd);
                                    quality_log.set(finalInd, lastq_log + curQ + ",");


                                    if ((curQ ) != updateratio[finalInd]  ) {
                                        total_tris = total_tris - (updateratio[finalInd] * excel_tris.get(indq));// total =total -1*objtris

                                        total_tris = total_tris + (curQ *  excel_tris.get(indq));// total = total + 0.8*objtris
                                        percReduction=curQ;
                                        renderArray[ind].decimatedModelRequest(curQ, ind, referenceObjectSwitchCheck);

                                    }

                                    updateratio[finalInd] = curQ;



                                }

                            }
                        },
                        0,      // run first occurrence immediatetly
                        (long) (decision_p*1000));


            } // end of baseline2



           }// on click
        });






        //create button listener for object placer
        Button placeObjectButton = (Button) findViewById(R.id.placeObjButton);

        placeObjectButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {

                policy= policySpinner.getSelectedItem().toString();


                int selectedCount = (int) countSpinner.getSelectedItem();

                if (multipleSwitchCheck == true && selectedCount != 1) {

                    countDownTimer = new CountDownTimer(Long.MAX_VALUE, 3000) {

                        // This is called after every 3 sec interval.
                        public void onTick(long millisUntilFinished) {

                            if (objectCount < selectedCount) {
                                renderArray[objectCount] = new decimatedRenderable(modelSpinner.getSelectedItem().toString());

                                addObject(Uri.parse("models/" + currentModel + ".glb"), renderArray[objectCount]);

                            }
                            if (objectCount == selectedCount)
                                countDownTimer.cancel();

                        }

                        public void onFinish() {
                            if (objectCount == selectedCount)
                                countDownTimer.cancel();


                        }
                    }.start();

                    // countDownTimer.start();


                } else {// define a counter 3 s to add obj ev time for gpu_model


                    renderArray[objectCount] = new decimatedRenderable(modelSpinner.getSelectedItem().toString());
                    addObject(Uri.parse("models/" + currentModel + ".glb"), renderArray[objectCount]);

                }

            }
        });


        //Clear all objects button setup
        Button clearButton = (Button) findViewById(R.id.clearButton);
        clearButton.setOnClickListener(new View.OnClickListener() {
            public void onClick(View view) {
                for (int i = 0; i < objectCount; i++) {
                    renderArray[i].detach();

                    ratioArray[i] = 1;
                    cacheArray[i] = 1;
                    updateratio[i]=1;
                    updatednetw[i]=0;
                }

              //  removePreviousAnchors(); // from net wrong
                ModelRequestManager.getInstance().clear();

                objectCount = 0;
                nextID=0;
                TextView posText = (TextView) findViewById(R.id.objnum);
                posText.setText("obj_num: " + objectCount);
                total_area = 0;
                total_vol = 0;
                redrawed.clear();
                sum = 0;
                total_tris=0;
                v_dist.clear();
                volume_list.clear();
                area_list.clear();
                o_tris.clear();
                new_percentage.clear();
                old_percentage.clear();
                obj_backward.clear();
                closer.clear();
                prevquality.clear();
                best_cur_eb.clear();
                gpusaving.clear();
                eng_dec.clear();
                eng_blc.clear();
                fthr.clear();
                quality_log.clear();
                time_log.clear();
                distance_log.clear();
                //nextfivesec.clear();
                GPU_Ut_log.clear();
                deg_error_log.clear();
                Server_reg_Freq.clear();
                current_thread.clear();
                decimate_thread.clear();
                renderArray = new baseRenderable[100];
            }
        });

        //seekbar setup
        SeekBar simpleBar = (SeekBar) findViewById(R.id.simpleBar);
        simpleBar.setOnSeekBarChangeListener(new SeekBar.OnSeekBarChangeListener() {
            @Override
            public void onProgressChanged(SeekBar seekBar, int progress, boolean b) {

                progress = ((int) Math.round(progress / SEEKBAR_INCREMENT)) * SEEKBAR_INCREMENT;
                seekBar.setProgress(progress);
                TextView simpleBarText = (TextView) findViewById(R.id.simpleBarText);
                simpleBarText.setText(progress + "%");
                int val = (progress * (seekBar.getWidth() - 2 * seekBar.getThumbOffset())) / seekBar.getMax();
                simpleBarText.setX(seekBar.getX() + val + seekBar.getThumbOffset() / 2);

            }

            @Override
            public void onStartTrackingTouch(SeekBar seekBar) {

            }

            //Nil
            @Override
            public void onStopTrackingTouch(SeekBar seekBar) {
                Log.d("ServerCommunication", "Tracking Stopped, redrawing...");
                //arFragment.getTransformationSystem().getSelectedNode()


                if (under_Perc == false)
                    percReduction = seekBar.getProgress() / 100f;
                else
                    percReduction = seekBar.getProgress() / 1000f;// for 1.1 % cases

                for (int i = 0; i < objectCount; i++) {
                    //Nil
                    if (redrawed.size() <= i)
                        redrawed.add(i, false);
                    else
                        redrawed.set(i, false);

                    if (!renderArray[i].baseAnchor.isSelected() && referenceObjectSwitchCheck == false)
                    //means that we have s==0 and decAll==0
                    {
                        referenceObjectSwitchCheck = false;
                    } else {

                        {

                            if (under_Perc == false)

                            {
                                total_tris  = total_tris- (ratioArray[i]* o_tris.get(i));// total =total -1*objtris
                                renderArray[i].decimatedModelRequest(seekBar.getProgress() / 100f, i, referenceObjectSwitchCheck);

                                ratioArray[i]=seekBar.getProgress() / 100f;
                                total_tris = total_tris+ (ratioArray[i]* o_tris.get(i));// total = total + 0.8*objtris
                            }
                            else {
                                total_tris= total_tris- (ratioArray[i]* o_tris.get(i));// total =total -1*objtris

                                renderArray[i].decimatedModelRequest(seekBar.getProgress() / 1000f, i, referenceObjectSwitchCheck);
                                ratioArray[i]=seekBar.getProgress() / 1000f;
                                total_tris = total_tris+ (ratioArray[i]* o_tris.get(i));// total = total + 0.8*objtris

                            }
                        }


                    }


                }
            }
        });


        fragment = (ArFragment)
                getSupportFragmentManager().findFragmentById(R.id.sceneform_fragment);
        fragment.getArSceneView().getScene().addOnUpdateListener(frameTime -> {fragment.onUpdate(frameTime);
            onUpdate();

        });


        //prediction REQ
        Timer t = new Timer();
        final int[] count = {0}; // should be before here
        t.scheduleAtFixedRate(
                new TimerTask() {
                    public void run() {

                        if(objectCount>= 1) { // Nil april 21 -> fixed
                            Frame frame = fragment.getArSceneView().getArFrame();//OK
                            current.add(new ArrayList<Float>(Arrays.asList(frame.getCamera().getPose().tx(), frame.getCamera().getPose().ty(), frame.getCamera().getPose().tz())));
                            timeLog.add(timeInSec);
                            timeInSec = timeInSec + 0.5f;


                            float  j=0.5f;
                            for ( int i=0; i<maxtime; i++)
                            { prmap.get(i).add(predictNextError2(j, i));
                                j+=0.5f;}


                            if (count[0] %2==0) { // means that we are ignoring 0.5 time data, 0-> next 1s, 2 is for next 2sec , 4 is for row fifth which is 4s in array of next1sec

                                for (int i = 0; i < maxtime/2; i++) // for next 5 sec
                                {
                                    nextfivesec.set(i, prmap.get(2 * i + 1).get(count[0]));

                                }

                                FindMiniCenters(area_percentage);
                                Findpredicted_distances();

                            }
                            count[0]++;

                        }

                    }

                },
                0,      // run first occurrence immediatetly
                500);





    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;

    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }



    //for user score selection
    @Override
    public void onItemSelected(AdapterView<?> parent, View view,
                               int pos, long id) {
        switch (parent.getId()) {
            case R.id.modelSelect:
                currentModel = parent.getItemAtPosition(pos).toString();
                break;

        }

    }

    @Override
    public void onNothingSelected(AdapterView<?> parent) {

    }

    // pay attention to process 2
    @Override
    public void onPause() {
        super.onPause();




        String currentFolder2 = getExternalFilesDir(null).getAbsolutePath();
        String FILEPATH2 = currentFolder2 + File.separator + "extra_inf.txt";
        Toast.makeText(this,"FILE PATH: " + FILEPATH2, Toast.LENGTH_LONG).show();
        PrintWriter fileOut2 = null;
        PrintStream streamOut2 = null;



        int size = current.size();
        errorAnalysis2(size);


        try {
            fileOut2 = new PrintWriter(new FileOutputStream(FILEPATH2, false));

            for (int ind = 0; ind < objectCount; ind++)
                fileOut2.println("quality_log_object " + ind + " "+renderArray[ind].fileName + " Time_log "+ time_log.get(ind)  +" QualityLog " + quality_log.get(ind) + " DistanceLog "+  distance_log.get(ind) +" DEGlog " + deg_error_log.get(ind)
                        + " calculated_GPU_eng_log " + GPU_Ut_log.get(ind) + " Engnetw " + eng_dec.get(ind)
                        + " server_req_freq " + Server_reg_Freq.get(ind));

            float total_gpu = compute_GPU_ut( decision_p / decision_p, total_tris); // for one second
            fileOut2.println("total_tris " + total_tris + " total_GPUusage_every_second " + total_gpu + " window " + finalw + " Bandwith "+ bwidth + " policy " + policy + " Maxdeg_parameter " + max_d_parameter);




            fileOut2.close();

        } catch (FileNotFoundException e) {
            e.printStackTrace();
        }

        String currentFolder = getExternalFilesDir(null).getAbsolutePath();
        String FILEPATH = currentFolder + File.separator + "output.txt";
        Toast.makeText(this,"FILE PATH: " + FILEPATH, Toast.LENGTH_LONG).show();
        PrintWriter fileOut = null;
        PrintStream streamOut = null;

        try {
            fileOut = new PrintWriter(new FileOutputStream(FILEPATH, false));


            double t=0;
            for (int j = 0; j < maxtime; j++)
            {
                t+=0.5;
                fileOut.println();
                fileOut.println("Predicted Confidence Area for "+ (t));
                for (int i = 0; i < size; i++) {

                    float lenght= Math.abs(prmap.get(j).get(i).get(4)- prmap.get(j).get(i).get(6));
                    float width= Math.abs(prmap.get(j).get(i).get(3)- prmap.get(j).get(i).get(5));
                    float carea= lenght*width;


                    fileOut.println(timeLog.get(i) + " " + current.get(i).get(0) + " " + current.get(i).get(1) + " " + current.get(i).get(2) + " " +
                            (timeLog.get(i) + t) + " " + prmap.get(j).get(i).get(0) + " " + prmap.get(j).get(i).get(1
                    ) + " " + prmap.get(j).get(i).get(2) + " " + prmap.get(j).get(i).get(3) + " " + prmap.get(j).get(i).get(4) + " " + prmap.get(j).get(i).get(5) + " " + prmap.get(j).get(i).get(6) + " " + prmap.get(j).get(i).get(7) + " " + prmap.get(j).get(i).get(8) + " " + prmap.get(j).get(i).get(9) + " " + marginmap.get(j).get(i).get(0) + " " + marginmap.get(j).get(i).get(1) + " " + errormap.get(j).get(i).get(0) + " " + errormap.get(j).get(i).get(1)+ " area " + carea);
                }

            }

            fileOut.println();
            fileOut.println("Error Analysis: ");
            //int k=0;
            for (int j = 0; j < size - maxtime; j++) {
                float l=0.5f;
                String s="";
                for (int k = 0; k < maxtime; k++) {

                        String s1= (timeLog.get(j) + l) + " " + booleanmap.get(k).get(j).get(0) + " " + booleanmap.get(k).get(j).get(1) + " ";
                        s+=s1;
                l+=0.5;
                }
                fileOut.println(s);
            }
            fileOut.close();
        } catch (IOException e) {
        }

        t2.cancel();
    }


    public ArrayList<ArrayList<Float>> findW (int ind)
    {


        int size = current.size();
        float upos_x= current.get(size-1).get(0);
        float upos_z=current.get(size-1).get(2);
        float obj_x= renderArray[ind].baseAnchor.getWorldPosition().x;
        float obj_z= renderArray[ind].baseAnchor.getWorldPosition().z;
        float w = 1;
        float u_x = upos_x;
        float u_y = upos_z;
        boolean userfarther = false;
        ArrayList<Float>newdistance= new ArrayList<Float>();
        int counter=1;

        newdistance.add(renderArray[ind].return_distance_predicted(upos_x, upos_z) ); // add current dis
        for (int i=1; i< decision_p; i++)
                newdistance.add(0f);

        while (userfarther == false &&  ((2*counter* decision_p)-1 <maxtime)  &&  counter< finalw ){
            float unext_x = prmap.get ( (2*counter* decision_p)-1).get(size-1).get(0);// middle point of c_area
            float unext_z = prmap.get( (2*counter* decision_p)-1).get(size-1).get(1);;//(uspeedy * decision_p) + u_y;

            if (upos_x <= obj_x && upos_z<=obj_z)
                 if (unext_x <= obj_x && unext_z<=obj_z && upos_x<=unext_x && upos_z<= unext_z )
                 {
                     w += 1;
                     newdistance.add(renderArray[ind].return_distance_predicted(unext_x, unext_z) );
                     for (int i=1; i< decision_p; i++)
                         newdistance.add(0f);


                 }
                 else
                     {userfarther = true;
                        break; }


            else if (upos_x <= obj_x && upos_z>=obj_z)
                if (unext_x <= obj_x && unext_z>=obj_z && upos_x<=unext_x && upos_z>= unext_z )
                {
                    w += 1;
                    newdistance.add(renderArray[ind].return_distance_predicted(unext_x, unext_z) );
                    for (int i=1; i< decision_p; i++)
                        newdistance.add(0f);


                }
                else
                     { userfarther = true;
                       break; }

             else if (upos_x >= obj_x && upos_z>=obj_z)
                    if (unext_x >= obj_x && unext_z>=obj_z && upos_x>= unext_x && upos_z>= unext_z)
                    {
                        w += 1;
                        newdistance.add(renderArray[ind].return_distance_predicted(unext_x, unext_z) );

                        for (int i=1; i< decision_p; i++)
                            newdistance.add(0f);


                    }
                     else
                     {userfarther = true;
                          break;}

              else if(upos_x >= obj_x && upos_z<=obj_z)
                  if (unext_x >= obj_x && unext_z<=obj_z && upos_x>= unext_x && upos_z<= unext_z)
                  {
                      w += 1;
                      newdistance.add(renderArray[ind].return_distance_predicted(unext_x, unext_z) );

                      for (int i=1; i< decision_p; i++)
                          newdistance.add(0f);


                  }
                  else
                      {  userfarther = true;
                     break;}

            u_x=unext_x;
            u_y = unext_z;
            counter++;
        }
        ArrayList<ArrayList<Float> > temp1 = new ArrayList<ArrayList<Float> >();
        for (int i=0;i<3; i++)
             temp1.add(new ArrayList<>());

        temp1.get(0).add(u_x);
        temp1.get(1).add(u_y);
        temp1.set(2,newdistance);
        return temp1;
    }




private float computeWidth(ArrayList<Float> point){
        float width=Math.abs(point.get(3)- point.get(5));
        return width;
}

    private float computeLength(ArrayList<Float> point){
        float length=Math.abs(point.get(4)- point.get(6));
        return length;
    }

// this function returns array predicted_distances as a map from obj index to the list of predicted distances for time t
private  void Findpredicted_distances(){

        // centers is the output of FindMiniareas, just for one area , so 01 is for pointx1, 2-3 is for point x2, ... 67, is for point x4
        float distance=0;
        float tempdis=0;
        int jmindex;
        int jmaxdex;
        for (int t=0;t<maxtime/2; t++)

            for (int i=0;i<objectCount; i++) {

                float mindis=Integer.MAX_VALUE;
                float maxdis=0;

                for (int j = 0; j < 4; j++) // we have 4 points to calculate the distance ffrom
           {
               tempdis = renderArray[i].return_distance_predicted(nextfive_fourcenters.get(t).get(2 * j), nextfive_fourcenters.get(t).get((2 * j) + 1));
               if (tempdis > maxdis) {
                   maxdis = tempdis;
               }
               if (tempdis < mindis) {
                   mindis = tempdis;
               }
           }// after this, we'll get min and max dis plus their index



            if(policy== "Aggressive")
                predicted_distances.get(i).set(t,maxdis);
            else if (policy== "Conservative")
                predicted_distances.get(i).set(t,mindis);
            else { // middle case

                ArrayList<Float> point= nextfivesec.get(t);// get next five area coordinates for time t
                float pointcx= point.get(0); float pointcz= point.get(1);
                tempdis = renderArray[i].return_distance_predicted(pointcx, pointcz);
                predicted_distances.get(i).set(t, tempdis);
            }
       }

    }

    private float FindCons(ArrayList<Float> centers){ // conservative
        float distance=0;
        return distance;
    }

    //  Returns t lists of 8 coordinates for 4 points of mini area centers
    private void FindMiniCenters(float percentage ){
        // this is to find four middle points in x% of width and lenghth of main area


        for (int t=0;t<maxtime/2; t++)
        {
            ArrayList<Float> point= nextfivesec.get(t);// ith element shows what time, 1s, 2, ... or 5th sec
            ArrayList<Float> center= new ArrayList<>();
            float length= computeLength(point);
            float width= computeWidth(point);
            float point1x= point.get(2);
            float point1z= point.get(3);
            float point3x= point.get(6);
            float point3z= point.get(7);

            float wRatio=width * percentage;
            float lRatio=length * percentage;
            // now from point px1, we calculate new x1 and z1:

            float newx1= point1x- (length/2); center.add(newx1);//0
            float newz1= point1z- (width/2);   center.add(newz1);//1

            float newx3= point3x- (length/2);
            float newz3= point3z+ (width/2);

            float newx2= newx1; center.add(newx2);//2
            float newz2=newz3;  center.add(newz2);//3

            center.add(newx3);//4
            center.add(newz3);//5
            float newx4= newx3; center.add(newx4);//6
            float newz4=newz1; center.add(newz4);//7

            nextfive_fourcenters.put(t , center);
        }


    }


    private float[] Findmed(ArrayList<Float> point){
        float [] center= new float[2];
        center[0]= point.get(0); // xcenter
        center[1]=point.get(1);//z center
        return center;
    }



    private void onUpdate() {
       boolean trackingChanged = updateTracking();
        View contentView = findViewById(android.R.id.content);
        if (trackingChanged) {
            if (isTracking) {
                contentView.getOverlay().add(pointer);
            } else {
                contentView.getOverlay().remove(pointer);
            }
            contentView.invalidate();
        }

        if (isTracking) {
            boolean hitTestChanged = updateHitTest();
            if (hitTestChanged) {
                pointer.setEnabled(isHitting);
                contentView.invalidate();
            }
        }
    }

    private boolean updateTracking() {
        Frame frame = fragment.getArSceneView().getArFrame();//OK not being used for now
        boolean wasTracking = isTracking;
        isTracking = frame != null &&
                frame.getCamera().getTrackingState() == TrackingState.TRACKING;



        if (multipleSwitchCheck == true) // eAR
            for (int i = 0; i < objectCount; i++) {

                float ratio = updateratio[i];

                if ((ratio ) != ratioArray[i]   ) {
                    total_tris= total_tris- (ratioArray[i]* o_tris.get(i));// total =total -1*objtris
                    ratioArray[i] = ratio;
                    total_tris = total_tris+ (ratioArray[i]* o_tris.get(i));// total = total + 0.8*objtris

                    if(updatednetw[i]==0) // we have that obj in another local cache/ no need to add req
                      renderArray[i].decimatedModelRequest(ratio , i, true);
                    else{ // we need to req to the server

                        renderArray[i].decimatedModelRequest(ratio , i, false);
                        Server_reg_Freq.set(i, Server_reg_Freq.get(i)+1);
                    }

                    if (ratio  != 1 && ratio !=cacheArray[i] ) {
                        cacheArray[i] = (ratio); // updates the cache

                    }
                }



            }///for
        return isTracking != wasTracking;
    }


    public List<String> predictwindow( MainActivity ma,List<Boolean> cls, float fath, float qprev, float d11, int ww, int ind, int dindex, ArrayList<Float> predicted_d) {

        List<String> temppredict = new ArrayList<String>();
        String qlog = "";
        String logbesteb = "";

        if (ww == 0) {

            temppredict.add("0");
            temppredict.add(qlog);
            temppredict.add(logbesteb);
            return temppredict;
        }
        else if (ww > 0) {

            float curdis= d11;
            float nextdis1= predicted_d.get(dindex); //next d1
            if(closer.get(ind) && d11<=nextdis1)
                d11=d11;
            else if (closer.get(ind) && d11> nextdis1)
                d11=nextdis1;
            else // ! closer
                d11=d11;

            float father = 1;
            if (qprev != 1) {
                cacheArray[ind] = qprev;
                father = qprev;
            } else if (qprev == 1) {
                cacheArray[ind] = fath;
                father = cacheArray[ind];
            }

            prevquality.set(ind, qprev);


            List<String> tempq = new ArrayList<>(ma.QualitySelection(ind, d11));


            float qual1 = Float.parseFloat(tempq.get(0));
            float qual2 = Float.parseFloat(tempq.get(1));
            float eb1 = Float.parseFloat(tempq.get(2));
            float eb2 = Float.parseFloat(tempq.get(3));
            float d1 =  predicted_d.get(dindex);// =dis in simulation code which is next possible d1
            updatecloser(curdis, d1,ind);


            float currdis=d1;
            float nextdis=  predicted_d.get(dindex+decision_p); // next of next d1
            if(closer.get(ind) && d1<=nextdis)
                d1=d1;
            else if (closer.get(ind) && d1> nextdis)
                d1=nextdis;
            else // ! closer
                d1=d1;


            List<String> temppredict1 = new ArrayList<>(ma.predictwindow(ma, closer,father, qual1, d1, ww - 1, ind, dindex + decision_p, predicted_d));
            float eb3 = Float.parseFloat(temppredict1.get(0));
            eb3 += eb1;
            String qq1 = temppredict1.get(1);
            String eblog1 = temppredict1.get(2);

            List<String> temppredict2 = new ArrayList<>(ma.predictwindow(ma, closer,father,
                    qual2, d1, ww - 1, ind, dindex + decision_p, predicted_d));
            float eb4 = Float.parseFloat(temppredict2.get(0));
            eb4 += eb2;
            String qq2 = temppredict2.get(1);
            String eblog2 = temppredict2.get(2);



            if (eb3 >= eb4) {
                prevquality.set(ind, ((float)(Math.round((float)(qual1 * 10))) / 10));
                best_cur_eb.set(ind, ((float)(Math.round((float)(eb1 * 1000))) / 1000));
                logbesteb = eblog1 + (String.valueOf((float)(Math.round((float)(eb1 * 1000))) / 1000)) + ",";
                qlog = (qq1) + (String.valueOf((float)(Math.round((float)(qual1 * 10))) / 10)) + ",";

            } else {
                prevquality.set(ind, ((float)(Math.round((float)(qual2 * 10))) / 10));// precision is up to 0.1 for simplicity of decimation now ( to have almost all decimation levels now)
                best_cur_eb.set(ind, ((float)(Math.round((float)(eb2 * 1000))) / 1000));
                logbesteb = eblog2 + (String.valueOf((float)(Math.round((float)(eb2 * 1000))) / 1000)) + ",";
                qlog = (qq2) + (String.valueOf((float)(Math.round((float)(qual2 * 10))) / 10)) + ",";
            }

            temppredict.clear();
            temppredict.add(String.valueOf((float)(Math.round((float)(Math.max(eb3, eb4) * 1000))) / 1000));

            temppredict.add(qlog);
            temppredict.add(logbesteb);
        }

        return temppredict;


    }

    public void updatecloser(float prevdis, float nextdis, int ind ){
        if (prevdis-nextdis>=0.09)// to avoid small errors while standing
            closer.set(ind, true);
        else
            closer.set(ind, false);

    }

    public List<String> QualitySelection(int ind, float d11) {

       int indq = excelname.indexOf(renderArray[ind].fileName);

        float gamma = excel_gamma.get(indq);
        float a = excel_alpha.get(indq);
        float b = excel_betta.get(indq);
        float c = excel_c.get(indq);
        float filesize= excel_filesize.get(indq);

        float c1 = (float) (c - ((Math.pow(d11, gamma) * max_d.get(indq)))); //# ax2+bx+c= (d^gamma) * max_deg

        float finalinp = delta(a, b, c1, c, d11, gamma, indq);
        if (finalinp<0.1 && finalinp >0)
            finalinp=0.1f;


        //float degerror;
        String qresult;

        float q1=1,q2=1;
        float eb1=0,eb2=0;
        float GPU_usagemax=0;
        float quality=1;
        if (closer.get(ind)) {
            qresult = adjustcloser(finalinp, prevquality.get(ind), a, b, c, d11, gamma, ind, indq);

            GPU_usagemax = compute_GPU_eng( decision_p, total_tris);
            q1 = q2 = 1.0f;

        } else {

            qresult = adjustfarther(finalinp, prevquality.get(ind), ind);
            GPU_usagemax = compute_GPU_eng( decision_p, total_tris);
            q1 = q2 = prevquality.get(ind);
        }




        float GPU_usagedec=0, GPU_usagedec2=0;

        float current_tris=0;
        if (qresult=="qprev forall")
           // for whole period p show i"' quality '''calculate gpu saving for qprev againsat q=1 eb= saving - dec = saving'''
        {
            quality = prevquality.get(ind);
            if (quality == 0)
                quality = 1;

            //gpu gaused without this obj totally
             current_tris= total_tris - (  (1- quality) * excel_tris.get(indq));
            GPU_usagedec = compute_GPU_eng( decision_p, current_tris);

            q1 = quality;
            gpusaving.set(ind, GPU_usagemax - GPU_usagedec);
            eb1 = gpusaving.get(ind);

            current_tris= total_tris - (  (1- q2) * excel_tris.get(indq));
            GPU_usagedec2 = compute_GPU_eng( decision_p, current_tris);
            eb2 = GPU_usagemax - GPU_usagedec2; // in milli joule
        }
        else if (qresult=="iz") //: # for whole period p show i"' quality
        {
            quality = finalinp;
            if (quality == 0)
              quality = 1;
            current_tris= total_tris - (   (1-quality) * excel_tris.get(indq));
            GPU_usagedec = compute_GPU_eng(decision_p, current_tris);

            gpusaving.set(ind, GPU_usagemax - GPU_usagedec);
            float dec_eng=0f;
            if (quality == cacheArray[ind])
                dec_eng=0f;

            else
                dec_eng=update_e_dec_req( filesize, quality);

            //for object with index at ti

            eb1 = gpusaving.get(ind) -dec_eng;
                    //eng_dec.get(ind);
            q1 = quality;

            current_tris= total_tris - (   (1-q2) * excel_tris.get(indq));
            GPU_usagedec2 = compute_GPU_eng(decision_p, current_tris);
            eb2 = GPU_usagemax - GPU_usagedec2;

        }


        else if (qresult=="cache forall") {
            current_tris= total_tris - (   (1-cacheArray[ind]) * excel_tris.get(indq));
            GPU_usagedec = compute_GPU_eng( decision_p, current_tris);

            quality = cacheArray[ind];
            if (quality == 0)
                quality = 1;

            q1 = quality;
      //  #eb1 =
            gpusaving.set(ind, GPU_usagemax - GPU_usagedec);
            eb1= gpusaving.get(ind);


        }

        else if (qresult=="delta1") {
            GPU_usagedec = GPU_usagemax;
            quality = 1;
            q1 = 1;
            eb1 = 0;
            current_tris= total_tris - (  (1-q2) * excel_tris.get(indq));
            GPU_usagedec2 = compute_GPU_eng( decision_p, current_tris);
            eb2 = GPU_usagemax - GPU_usagedec2;

        }
        List<String> tempquality = new ArrayList<String>();
        tempquality.add(Float.toString(q1));
        tempquality.add(Float.toString(q2));
        tempquality.add(Float.toString(eb1));
        tempquality.add(Float.toString(eb2));


        return tempquality;


    }


  public float  update_e_dec_req(  float size, float qual){
        //'''this is to update energy consumption for decimation '''

      if (qual==1)
            return 0;

      //assume net is 5g
      float eng_network=  (size/ (1000000f * bwidth )) * 1.5f * 1000f;// in milli joule
      return eng_network;// in mili joule
}




    public float compute_GPU_eng(float period, float current_tris) // returns gpu percentage if we decimate obj1 to qual
    {
        //'''this is to calculate gpu utilization having quality
        float gpu_perc=0;
        if(current_tris< gpu_min_tres)
            gpu_perc= bgpu;// baseline }

        else
           gpu_perc = (agpu * current_tris) + bgpu; // gets gpu utilization in percentage for 1 sec

      float gpu_power_eng= ((7.42f * gpu_perc) + 422.9f) * period; // in milli joule
      return gpu_power_eng;

    }


    public float compute_actual_GPU_eng(float period, float gpu_perc) // returns gpu percentage if we decimate obj1 to qual
    {
        //'''this is to calculate gpu utilization having quality

        float gpu_power_eng= ((7.42f * gpu_perc) + 422.9f) * period; // in milli joule
        return gpu_power_eng;

    }


    public float compute_GPU_ut(float period, float current_tris) // returns gpu percentage if we decimate obj1 to qual
    {
        //'''this is to calculate gpu utilization having quality
        float gpu_perc=0;
        if(current_tris< gpu_min_tres)
            gpu_perc= bgpu;// baseline }

        else
            gpu_perc = (agpu * current_tris) + bgpu; // gets gpu utilization in percentage for 1 sec

        return gpu_perc;

    }

    public String adjustcloser(float x1, float prevq, float a, float b, float c, float d11, float gamma, int ind, int indq)//: # four cases we need to adjust xs to 0 or 1 which are cases with at least two '1's
    {
        String value = "";
        if (x1 != 0)//: # 111 or 110
        {
            if (Math.abs(x1 - prevq) < 0.1)
                value = "qprev forall"; //#means i '' for all

            else if (Math.abs(cacheArray[ind] - x1) < 0.1 && Testerror(a, b, c, d11, gamma, prevq, indq) == true)
                //: #if we can use the prev downloaded quality instead of the closer quality
                value = "cache forall";// #means i '' for all

            else
                value = "iz"; //#means i '' for d1
        }
        else//:#000, 001
            value = "delta1"; //#means delta1

        return value;

    }


    public boolean Testerror(float a, float b, float creal, float d, float gamma, float r1, int ind) {

    float error = (float) ((a*(Math.pow(r1,2))+b*r1 +creal)/(Math.pow(d,gamma)));
            if(error<=max_d.get(ind))
                return true;
            else
             return false;
    }


    public String adjustfarther(float x1,float prevq, int ind)//: # four cases we need to adjust xs to 0 or 1 which are cases with at least two '1's
    {
        String value="";
         if (x1!=0)//: # 11 or 10
         {
             if (Math.abs(prevq - x1) < 0.1)
                  value = "qprev forall";// #means i '' for all
             else if(Math.abs(cacheArray[ind] - x1) < 0.1)
                  value = "cache forall";

             else
                     value = "iz"; //#means i '' for d1
         }

    else if (x1==0 )//: # case 100 and 101
         value="qprev forall"; //#means i'' for all

 return value;

    }

    public float checkerror(float a,float b,float creal,float d,float gamma, int ind) {


       float r1 = 0.1f;
       float error;


       for (int i =0; i< 18; i++) {

           error = (float) (((a * Math.pow(r1,2)) + (b * r1) + creal) / (Math.pow(d , gamma)));
           if (error < max_d.get(ind))
                return r1;
           r1 += 0.05;


       }
       return 0;

   }

    public float Calculate_deg_er(float a,float b,float creal,float d,float gamma, float r1) {

        float error;
        if(r1==1)
          return  0f;
        error = (float) (((a * Math.pow(r1,2)) + (b * r1) + creal) / (Math.pow(d , gamma)));
        return error;
    }


public float delta (float a, float b , float c1,float creal,  float d, float gamma, int ind){

        float r=0f;
        float r1, r2=r;
        float dlt = (float) (Math.pow(b, (2f)) - (4f *(a*c1)));
        //float deg_error;

        // two roots
        if (dlt>0) {
            r1 = (float) (((-b) + Math.sqrt(dlt)) / (2 * a));
            r2 = (float) (((-b) - Math.sqrt(dlt)) / (2 * a));

            if (0.001 < r1 && r1 < 1.0 && 0.001 < r2 && r2 < 1.0)
            {
                r = Math.min(r1, r2);


                return r;
            }
            else if (0.001 < r1 && r1 < 1)
                r2 = checkerror(a, b, creal, d, gamma, ind);

            else if (0.001<r2 && r2<1)
                r1=checkerror(a, b,creal, d, gamma, ind);
     // #x=1

             else {
                r = checkerror(a, b, creal, d, gamma, ind);
                return r;
            }
        }

        else if (dlt==0){
            r1 = (-b) / 2*a;
            if (r1>1 || r1<0)
                r1=checkerror(a, b,creal, d, gamma, ind);
            r2=0;

        }


        else{
            r=checkerror(a, b,creal, d, gamma, ind);
            return r;
        }



        if (r2==0f || r2==1f)
            r=r1;

        else if (r1==0f || r1==1f)
            r=r2;

        else
            r= Math.min(r1,r2);


        return r;
}



    private boolean updateHitTest() {
        Frame frame = fragment.getArSceneView().getArFrame();
        android.graphics.Point pt = getScreenCenter();
        List<HitResult> hits;
        boolean wasHitting = isHitting;
        isHitting = false;
        if (frame != null) {
            hits = frame.hitTest(pt.x, pt.y);
            for (HitResult hit : hits) {
                Trackable trackable = hit.getTrackable();
                if (trackable instanceof Plane &&
                        ((Plane) trackable).isPoseInPolygon(hit.getHitPose())) {
                    isHitting = true;
                    break;
                }
            }
        }
        return wasHitting != isHitting;
    }

    private android.graphics.Point getScreenCenter() {
        View vw = findViewById(android.R.id.content);
        return new android.graphics.Point(vw.getWidth()/2, vw.getHeight()/2);
    }



    //this came with the app, it sends out a ray to a plane and wherever it hits, it makes an anchor
    //then it calls placeobject
    private void addObject(Uri model, baseRenderable renderArrayObj) {
        Frame frame = fragment.getArSceneView().getArFrame();
        android.graphics.Point pt = getScreenCenter();
        List<HitResult> hits;
        if (frame != null) {
            hits = frame.hitTest(pt.x, pt.y);
            for (HitResult hit : hits) {
                Trackable trackable = hit.getTrackable();
                if (trackable instanceof Plane &&
                        ((Plane) trackable).isPoseInPolygon(hit.getHitPose())) {
                    Anchor newAnchor = hit.createAnchor();
                    placeObject(fragment, newAnchor, model, renderArrayObj);
                    break;
                }
            }
        }



    }



    private void placeObject(ArFragment fragment, Anchor anchor, Uri model, baseRenderable renderArrayObj) {
        try {
            CompletableFuture<Void> renderableFuture =
                    ModelRenderable.builder()
                            .setSource(fragment.getContext(), model)
                            .setIsFilamentGltf(true)
                            .build()
                            .thenAccept(renderable -> addNodeToScene(fragment, anchor, renderable, renderArrayObj))
                            .exceptionally((throwable -> {
                                AlertDialog.Builder builder = new AlertDialog.Builder(this);
                                builder.setMessage(throwable.getMessage())
                                        .setTitle("Codelab error!");
                                AlertDialog dialog =
                                        builder.create();
                                dialog.show();
                                return null;
                            }));
        } catch (Exception e) {
            e.printStackTrace();
        }

    }



    private void removePreviousAnchors()
    { List<Node> nodeList = new ArrayList<>(arFragment.getArSceneView().getScene().getChildren());
    for (Node childNode : nodeList) {
        if (childNode instanceof AnchorNode) {
            if (((AnchorNode) childNode).getAnchor() != null) {

        ((AnchorNode) childNode).getAnchor().detach();
        ((AnchorNode) childNode).setParent(null); } } } }

    //takes both the renderable and anchor and actually adds it to the scene.
    private void addNodeToScene(ArFragment fragment, Anchor anchor, Renderable renderable, baseRenderable renderArrayObj) {


        AnchorNode anchorNode = new AnchorNode(anchor);
        TransformableNode node = new TransformableNode(fragment.getTransformationSystem());
        node.setRenderable(renderable);
        node.setParent(anchorNode);
        renderArrayObj.setAnchor(node);
        int value=0;
        float volume=0;
        float area=0;

        String objname= renderArrayObj.fileName+ "\n";
        String name= renderArrayObj.fileName;
        System.out.println("name is "+name);

        ratioArray[objectCount]=1;
        cacheArray[objectCount]=1;
        updateratio[objectCount]=1;
        updatednetw[objectCount]=0;
        predicted_distances.put(objectCount, new ArrayList<>());

        for (int i=0; i<maxtime/2; i++)
            predicted_distances.get(objectCount).add(0f);// initiallization, has next distance for every 1 sec
        Server_reg_Freq.add(objectCount,0);

        current_thread.add(objectCount, new Thread());

       int indq = excelname.indexOf(renderArray[objectCount].fileName);// search in excel file to find the name of current object and get access to the index of current object


        o_tris.add( (Integer) excel_tris.get(indq));
        d1_prev.add(objectCount, 0f);
        total_tris+= o_tris.get(objectCount);



        distance_log.add(objectCount, Float.toString( renderArray[objectCount].return_distance()) );
        SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss:SSS");

        time_log.add(objectCount,  dateFormat.format(new Date()).toString() );


        objectCount++;


        gpusaving.add(0f);
        eng_dec.add("");
        eng_blc.add(0f);
        closer.add(true);
        obj_backward.add(false);
        prevquality.add(1f);
        best_cur_eb.add(0f);
        fthr.add(1f);
        quality_log.add("");

        GPU_Ut_log.add("");
        deg_error_log.add("");



        TextView posText = (TextView) findViewById(R.id.objnum);
        posText.setText( "obj_num: " +objectCount);

        File file = new File(this.getExternalFilesDir(null), "/degmodel_file.csv");

        File tris = new File(MainActivity.this.getFilesDir(), "text");

        Date d1 = null;
        Date d2 = null;



        fragment.getArSceneView().getScene().addChild(anchorNode);// ask for drawing new obj


        sum+=value;




        renderArray[objectCount-1].distance();

        if(v_dist.size()==0) {
            total_vol = 0;
            total_area = 0;
            volume_list.add((double)(0));
            area_list.add((double)(0));


        }



        else{
            old_percentage.add((float)1.0);
            new_percentage.add((float)1.0);
        }


        node.select();






    }


    private float nextPoint(float x1, float x2, float y1, float y2, float time)
    {
        float slope = (y2 - y1)/(x2 - x1);
        float y3 = slope*(x2 + time) -(slope*x1) + y1;
        return y3;
    }

    private float nextPointEstimation(float actual, float predicted)
    {
        return (alpha * actual) + ((1 - alpha) * predicted);
    }


    private float[] rotate_point(double rad_angle, float x, float z)
    {
        float[] rotated = new float[2];

        rotated[0] = x* (float)Math.cos(rad_angle) - z * (float)Math.sin(rad_angle);
        rotated[1] = x* (float)Math.sin(rad_angle) + z * (float)Math.cos(rad_angle);

        return rotated;
    }

    private float[] rotate_around_point(double rad_angle, float x, float z, float orgX, float orgZ)
    {
        float[] rotated = new float[2];

        rotated[0] = (x - orgX)* (float)Math.cos(rad_angle) - (z - orgZ) * (float)Math.sin(rad_angle) + orgX;
        rotated[1] = (x - orgX)* (float)Math.sin(rad_angle) + (z - orgZ) * (float)Math.cos(rad_angle) + orgZ;

        return rotated;
    }

//has prmap with too many inf -> enhance this fucntion
    private ArrayList<Float>
    predictNextError2(float time, int ind)
    {
        ArrayList<Float> predictedValues = new ArrayList<>();
        ArrayList<Float> margin = new ArrayList<>();
        ArrayList<Float> error = new ArrayList<>();
        int curr_size = current.size();
        float predictedX = 0f;
        float predictedZ = 0f;
        float actual_errorX = 0f;
        float actual_errorZ = 0f;
        float predict_diffX, predict_diffZ;


        // ind 0,   1,  2,  3,  4, 5 , 6, 7 , 8 , 9 , 10
        //time 0.5, 1, 1.5, 2, 2.5, 3, 3.5,  4,  4.5, 5
        // currsize - i1  2 , 3,  4,   5,   6
        //prmap.get(0) is equall to predicted05
        //prmap.get(10).get(curr_size - 1).get(1) = predicted z value in next 5 sec
        int i1 = ind +2;

        if(curr_size >1 )
        {

            float marginx = 0.3f, marginz = 0.3f;

            if (curr_size > maxtime) {
                predict_diffX =  prmap.get(ind).get(curr_size - i1).get(0) - current.get(curr_size - i1).get(0);
                predict_diffZ = prmap.get(ind).get(curr_size - i1).get(1) - current.get(curr_size - i1).get(2);
                float actual_diffX = current.get(curr_size - 1).get(0) - current.get(curr_size - i1).get(0);
                float actual_diffZ = current.get(curr_size - 1).get(2) - current.get(curr_size - i1).get(2);
                predictedX = nextPointEstimation(actual_diffX,predict_diffX) + current.get(curr_size - 1).get(0);
                predictedZ = nextPointEstimation(actual_diffZ,predict_diffZ)+ current.get(curr_size - 1).get(2);
            }
            else{
                predictedX = nextPoint(timeLog.get(curr_size - 2), timeLog.get(curr_size - 1), current.get(curr_size - 2).get(0), current.get(curr_size - 1).get(0), time);
                predictedZ = nextPoint(timeLog.get(curr_size - 2), timeLog.get(curr_size - 1), current.get(curr_size - 2).get(2), current.get(curr_size - 1).get(2), time);
            }

            if (curr_size > i1) {


                actual_errorX = abs(current.get(curr_size - 1).get(0) - prmap.get(ind).get(curr_size - i1).get(0));// err btw actual coo and predicted point
                actual_errorZ = abs(current.get(curr_size - 1).get(2) - prmap.get(ind).get(curr_size - i1).get(1));
                float margin_x = abs(nextPointEstimation(actual_errorX, marginmap.get(ind).get(curr_size-2).get(0)));
                float margin_z = abs(nextPointEstimation(actual_errorZ, marginmap.get(ind).get(curr_size-2).get(1)));

                if (curr_size>max_datapoint){ // we need to compare the margin with 100 percentile error

                    List<Float> sortedlist_x = new LinkedList<>(last_errors_x);
                    List<Float> sortedlist_z = new LinkedList<>(last_errors_z);
                    Collections.sort(sortedlist_x);
                    Collections.sort(sortedlist_z);
                    float max_x= sortedlist_x.get(sortedlist_x.size() - 1);
                    float max_z= sortedlist_x.get(sortedlist_z.size() - 1);

                    marginx = Math.max(margin_x ,max_x );
                    marginz= Math.max(margin_z, max_z);


                }
                else // traditional point, cur data points are less thatn 25 as an eg,
                {
                        marginx = Math.max( marginmap.get(ind).get(curr_size-2).get(0),margin_x );
                        marginz= Math.max( margin_z , marginmap.get(ind).get(curr_size-2).get(1));
            }

            }

            margin.add(marginx);
            margin.add(marginz);
            marginmap.get(ind).add(margin);
            error.add(actual_errorX);
            error.add(actual_errorZ);
            errormap.get(ind).add(error);

            if (last_errors_x.size()<max_datapoint) {

                last_errors_x.add( actual_errorX);
                last_errors_z.add( actual_errorZ);
            }
            else{

                last_errors_x.remove();// remove the head, or oldest one
                last_errors_z.remove();
                last_errors_x.add( actual_errorX);// add new one
                last_errors_z.add( actual_errorZ);
            }


            double tan_val = (double)((predictedZ-current.get(curr_size - 1).get(2))/(predictedX-current.get(curr_size - 1).get(0)));
            double angle = Math.atan(tan_val);
            predictedValues.add(predictedX); //predicted X value
            predictedValues.add(predictedZ); //predicted Z value


            float[] rotated = rotate_point(angle, marginx,marginz);
            predictedValues.add(predictedX + rotated[0]); //Confidence area X coordinate 1
            predictedValues.add(predictedZ + rotated[1]); //Confidence area Y coordinate 1

            rotated = rotate_point(angle, marginx,-marginz);
            predictedValues.add(predictedX + rotated[0]); //Confidence area X coordinate 2
            predictedValues.add(predictedZ + rotated[1]); //Confidence area Y coordinate 2

            rotated = rotate_point(angle, -marginx,-marginz);
            predictedValues.add(predictedX + rotated[0]); //Confidence area  X coordinate 3
            predictedValues.add(predictedZ + rotated[1]); //Confidence area Y coordinate 3

            rotated = rotate_point(angle, -marginx,marginz);
            predictedValues.add(predictedX + rotated[0]); //Confidence area X coordinate 4
            predictedValues.add(predictedZ + rotated[1]); //Confidence area Y coordinate 4

        }
        else {
            int count=0;
            for (count=0; count<=9; count++)// we have 10 points for cofidence area
                predictedValues.add(0f);

        }
        return predictedValues;
    }




    private float area_tri(float x1, float y1, float x2, float y2, float x3, float y3)
    {
        return (float)Math.abs((x1*(y2-y3) + x2*(y3-y1)+ x3*(y1-y2))/2.0);
    }



    private ArrayList<Float> check_rect(float x1, float y1, float x2, float y2, float x3, float y3, float x4, float y4, float x, float y)
    {
        ArrayList<Float> bool_val;
        /* Calculate area of rectangle ABCD */
        float A = area_tri(x1, y1, x2, y2, x3, y3) + area_tri(x1, y1, x4, y4, x3, y3);

        /* Calculate area of triangle PAB */
        float A1 = area_tri(x, y, x1, y1, x2, y2);

        /* Calculate area of triangle PBC */
        float A2 = area_tri(x, y, x2, y2, x3, y3);

        /* Calculate area of triangle PCD */
        float A3 = area_tri(x, y, x3, y3, x4, y4);

        /* Calculate area of triangle PAD */
        float A4 = area_tri(x, y, x1, y1, x4, y4);

        /* Check if sum of A1, A2, A3 and A4  is same as A */
        float sum = A1 + A2 + A3 + A4;
        if(Math.abs(A - sum) < 1e-3)
            bool_val = new ArrayList<Float>(Arrays.asList(1f, A));
        else
            bool_val = new ArrayList<Float>(Arrays.asList(0f, A));

        return bool_val;
    }



    private void errorAnalysis2(int size)
    {
        float area = 0f;
        for(int i = 0; i < size - maxtime; i++) {
            for (int k = 0; k < maxtime ; k++) {

                booleanmap.get(k).add(check_rect(prmap.get(k).get(i).get(2), prmap.get(k).get(i).get(3), prmap.get(k).get(i).get(4), prmap.get(k).get(i).get(5),
                        prmap.get(k).get(i).get(6), prmap.get(k).get(i).get(7), prmap.get(k).get(i).get(8), prmap.get(k).get(i).get(9),
                        current.get(i + 1 + k).get(0), current.get(i + 1+ k).get(2)));

            }
        }
    }

    public void givenUsingTimer_whenSchedulingTaskOnce_thenCorrect() {


        Timer  t = new Timer();

        t.scheduleAtFixedRate(

                new TimerTask() {
                    public void run() {
                   Float mean_gpu = 0f;
                   float dist = 0;
                   if (renderArray[1] != null)
                       dist = renderArray[0].return_distance();

                   String filname=" ";

                   if(objectCount>0)
                       filname= renderArray[objectCount-1].fileName;

                   SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss:SSS");
                   dateFormat.format(new Date());
                   String current_gpu = null;
                   try {
                       //Process process;
                     //  int i = 0;
                     //  for (i = 0; i < 3; i++) {
                           String[] InstallBusyBoxCmd = new String[]{
                                   "su", "-c", "cat /sys/class/kgsl/kgsl-3d0/gpu_busy_percentage"};

                           process2 = Runtime.getRuntime().exec(InstallBusyBoxCmd);
                           BufferedReader stdInput = new BufferedReader(new
                                   InputStreamReader(process2.getInputStream()));
                            // Read the output from the command
                           current_gpu = stdInput.readLine();
                           if (current_gpu != null) {
                               String[] separator = current_gpu.split("%");
                               mean_gpu = mean_gpu + Float.parseFloat(separator[0]);
                           }

                     //  }
                       //mean_gpu = mean_gpu / i;

                   } catch (IOException e) {
                       e.printStackTrace();
                   }

                   int sreqs = 0;
                   for (int value : Server_reg_Freq)
                       sreqs += value;

                   String item2 = dateFormat.format(new Date()) + " num_of_tris: " + total_tris + " current_gpu " + mean_gpu + " dis " + dist + " serv_req "
                           + sreqs + " lastobj "+ filname + objectCount+ "\n";
                   // + " virtual area " + total_area + " virtual vol " + total_vol + " " + fileName + "\n";
                   try {
                       FileOutputStream os = new FileOutputStream(GPU_usage, true);
                       os.write(item2.getBytes());
                       os.close();
                       System.out.println(item2);


                   } catch (IOException e) {
                       Log.e("StatWriting", e.getMessage());
                   }

               }

          //  }
                },
                0,      // run first occurrence immediatetly
                1000);
    };



    private boolean isObjectVisible(Vector3 worldPosition)
    {
        float[] var2 = new float[16];
        Frame frame = fragment.getArSceneView().getArFrame(); // OK not used
        Camera camera = frame.getCamera();

        float[] projmtx = new float[16];
        camera.getProjectionMatrix(projmtx, 0, 0.1f, 100.0f);

        float[] viewmtx = new float[16];
        camera.getViewMatrix(viewmtx, 0);
        Matrix.multiplyMM(var2,0,projmtx,0, viewmtx, 0);

        float var5= worldPosition.x;
        float var6 = worldPosition.y;
        float var7 = worldPosition.z;

        float var8 = var5 * var2[3]+ var6 * var2[7] + var7 * var2[11] + 1.0f * var2[15];
        if (var8 < 0f) {
            return false;
        }

        Vector3 var9 = new Vector3();
        var9.x = var5 * var2[0] + var6 * var2[4] + var7 * var2[8] + 1.0f * var2[12];
        var9.x = var9.x / var8;
        if (var9.x < -1f || var9.x > 1f) {
            return false;
        }

        var9.y = var5 * var2[1] + var6 * var2[5] + var7 * var2[9] + 1.0f * var2[13];
        var9.y = var9.y / var8;
        if (var9.y < -1f || var9.y > 1f) {
            return false;
        }

        return true;
    }
}
