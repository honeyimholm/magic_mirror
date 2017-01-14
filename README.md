# Augmented Reality "Magic Mirror"

This project tracks the users head position to overlay a halo when the user smiles. 
Below we can see a demo of the basic premise:

![alt tag](https://github.com/honeyimholm/magic_mirror/blob/master/demo.gif)

Because the screen is covered by a one way mirror, the user sees their reflection augmented with the new angelic decoration.

In this iteration we only enable the halo when the user smiles.

# How It Works

![alt tag](https://github.com/honeyimholm/magic_mirror/blob/master/smile_detection_demo.png)

We grab a webcam screenshot and then use OpenCV haar cascades to identify the face region and then another set of pre-trained haar cascades to identify a smile within the face dectected region. The halo is resized and repositioned with each webcam screenshot to follow the user's head. In the picture above we can see the face detected region in red and the smile detected region in blue and a simulation of the halo drawn onto the frame 

In reality, the output is the halo with a black screen. The black background does not come through the one way mirror, while the halo does.
Below we can see the output with and without the one way mirror.

# Next Steps

I'll probably add another haar cascade for detecting crazy smiles like the one above that will immidiately call the police. 

:)
