
![image](https://github.com/Niloofar-didar/AR-Realtime-Decimation-main/assets/27611369/15bd9abb-07a4-4c47-9e8f-e0de572fd3b3)

![image](https://github.com/Niloofar-didar/AR-Realtime-Decimation-main/assets/27611369/467474b8-7e3e-4b3c-97b6-18c29b114f39)


If you wanna leverage the coding, please cite this paper

@article{didar2022ear,
  title={eAR: an Edge-Assisted and Energy-Efficient Mobile Augmented Reality Framework},
  author={Didar, Niloofar and Brocanelli, Marco},
  journal={IEEE Transactions on Mobile Computing},
  year={2022},
  publisher={IEEE}
}



## Instriction to Run the demo

**Runtime Environment:**
- Ubuntu 20.4.2 LTS
- Android Studio 4.1.2
- Android API 30 Revision 3
- OpenJDK Version 11.0.9.1
- Blender v2.80 (sub 75)
- Python 3.8.5

Blender version v2.8 is recommended.

Two things must be done in order to successfully run the app. First, the IPv4 of the host computer
will need to be added to ``MainActivity.java`` in variable ``SERVER_IP`` and port added to ``SERVER_PORT``

Second, the server must be running on the host computer. Go to the base directory of the server and use ``java -cp ./ server.ARServer server.ServerThread``
 in order to get the server running.
 
 In order to add models into the app, a `.glb` model file should be added to assets/models/ inside of the project. Within the folder Server/input/ and Server/output, a folder must be made with the same name as the filename (without the .glb). Then, a copy of the model placed inside of assests/models/ should be placed inside of Server/input/yourfilename/. For example, if my model is andy.glb, it will be placed in Server/input/andy/andy.glb and a folder should be made in ouput for it as well, output/andy/.
 
 ## Using the code in your project
 
 In order to use the code in your project, the files from Source>Android must be added directly into the source folder of the project and the package name changed due to the way communication between threads is handled. Copy all of the Source>Android java files into your source folder (i.e. yourproject/app/src/main/java/com/example) and change the package name to your package name on the files you just copied.

Next, sceneformsrc and sceneformux from source>sceneform must be added to the project. Instructions for that can be found [here](https://github.com/google-ar/sceneform-android-sdk/blob/master/README.md) where further Sceneform documentation can be found. The version of sceneform used in this is made to work with android x and can be found [here](https://github.com/anacoimbrag/sceneform-android-sdk).

Lastly, a `Handler` object and `getHandler()` function must be established in MainActivity in order to recieve incoming `ModelRequest` objects from `ModelRequestManager`. For example:
```java    
private final Handler handler = new Handler(Looper.getMainLooper()){
        @Override
        public void handleMessage(Message inputMessage)
        {
            ModelRequest tempModelRequest = (ModelRequest) inputMessage.obj;
        }
    };

public Handler getHandler() { return handler; }
```
