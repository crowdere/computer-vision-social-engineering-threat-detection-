<h1 style="color: #3a7aad">MCTI - 6510 - Final Project</h1>

Development environment structure 

* **face_classifier.py** contains the original face recognition class
* **opencv_eye_detection.py** contains the opencv eye detector class
* **yolo_human_detect.py** contains the yolo human detector class
* **security_features.py** contains the security features we've developed so far
* **main.py** Run the current model

<h1 style="color: #3a7aad">Artificial Intelligence</h1>

The primary tools used to classify the different instances of shoulder surfing were some popular pre-trained object 
detection Machine Learning (ML) models. The objective was to identify any actors in a laptop camera's field of view. 
This involved discovering who (inside or outside an organization/enterprise) is looking at the given laptop, what they 
are looking at, and how many actors exist in the background. 

In order to discover who was looking at the laptop, two methods were employed. **YOLO** Object Detection and **dlib**
based face recognition. The former is used in order to detect an actor who is not in range of the face recognition 
system, and the latter is used up to a certain range in order to classify the face (by name) of an authorized/unauthorized employee, 
or an unknown actor altogether. 

Regarding what the actor might be looking at, another **dlib and Computer Vision** based system was used in order to track an actor's 
eyes within a certain reasonable range. **If an actor's eyes are detected, it is assumed that the device is in danger 
of being compromised and the user's risk score increases**. 

The entire system comes together in order to assess the risk level after processing every frame. Depending on the situations 
described in **reference**, the employee's laptop will receive a risk score. 

<h2 style="color: #3a7aad">Face Recognition with dlib and Computer Vision</h2>

This face recognition model was taken from a library built with **dlib**, a C++ library that allows for the usage of various 
ML algorithms. It is 99.38% accurate and was benchmarked against the *labels of the wild* benchmark, a data set that is used 
to grade face recognition models. 

The library provides various tools, such as facial outlining, feature extraction and real time face recognition. For the 
purposes of this defense system, real time face recognition was the only tool required. On every frame, the model would 
attempt to discover all the faces in range and either recognize an employee, which the system then checks their authorization, 
or if they're an unknown actor. Moreover, the model requires only one photo in order to train per face. This helps in both 
preserving employee privacy and allowing the system to train only on the Active Directory photos that already exist. 

One should note that this model tends to make errors with children. This is a possible compromise if the person willing 
to commit a shoulder surfing attack wishes to send children to do their bidding.  

<h2 style="color: #3a7aad">Human Detection using YOLOv3-416 Object Detection</h2>

This model involves the famous YOLO detection model (You Only Look Once) that was trained on the COCO Dataset. Normally this model predicts 
20 classes, but for our system, we only required it to predict one class, humans. Only classifications on humans were extracted
from the model results, however, the model was not retrained, as that was thought unnecessary, the human predictions were
sliced out of the default prediction array. 

It is quite a robust model, and the detection is fast and accurate, able to predict humans obscured by certain obstacles, 
or far from the camera. It holds an mAP score of 55.3 and can operate at 35 fps. A pre-trained weights file is provided 
by DarkNet for open source usage, and was used for this system. 

Human detection in this system is essentially used to determine the type of environment the employee is located in. If they 
are in a cafe, they probably are not in an environment that is secure for their work. And in this current system, the number 
of human's detected in the background might easily rack up the employee's risk score and consequently, the security measures. 

<h2 style="color: #3a7aad">Gaze Detection with dlib and Computer Vision</h2>

This model is also built on top of dlib and was an open source project by "antoinelame". In his repo, he outlined his usage 
of dlib and computer vision in order to make a frontal face detection, estimate the location of the eyes, pupils and track
their subsequent movements. 

It is quite accurate, as it uses pre-existing methods in a well-rounded AI system, and gives resulting ratios and precise 
coordinates on the different elements of the eyes. Moreover, these calculations are used in order to determine a where the 
actor's gaze is set on through various thresholds. 

It should be noted that some changes were incorporated into this particular AI system's architecture. First, the model initially 
only supported the detection of one pair of eyes, however, it had to be enhanced in order to detect multiple pairs of eyes. Also, 
the system had certain limitations. If one of the actor's eyes were not present it would not make a successful detection. This had 
to be rectified by eliminating the limitation altogether. 

<h2 style="color: #3a7aad">Other tested models</h2>

Some other models were tested before these final three were selected. The first was a purely computer vision based eye 
detection and tracking model. However, it was not robust enough and did not provide sufficient details to make a conclusion 
regarding an actor's gaze. It was therefore not considered as part of this system. 

Another model was Facebook's famous Detectron2, however, it did not perform well on a standard CPU based system, and therefore
as part of this system which we consider to be scalable and affordable, it overworks the system for many kinds 
of detections and perhaps required retraining that was unnecessary. The human and face detection combination that was finally chosen 
was sufficient. 

A final model that was considered for this system was also a Computer Vision based human detection model. However, its detections 
were extremely sensitive to light and distance. It was not robust enough and was not considered to be part of this system. 

The selected models were finally combined in order to annotate each individual frame with Computer Vision and render a result 
in order to verify the integrity of the Machine Learning in the system. However, these are not to be included in the final product, 
as it is solely for developer usage and would put unnecessary processing on an enterprise's system. 

https://medium.com/@amrokamal_47691/yolo-yolov2-and-yolov3-all-you-want-to-know-7e3e92dc4899#:~:text=YOLO%20was%20trained%20to%20detect,%2C%20person%2C%E2%80%A6.)%20.

https://medium.com/@luanaebio/detecting-people-with-yolo-and-opencv-5c1f9bc6a810