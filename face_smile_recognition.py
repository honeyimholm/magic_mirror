import cv2
import numpy as np
import sys
import PIL
from PIL import Image

facePath = "C:\Users\sahol\Desktop\magic_mirror\haarcascade_frontalface_default.xml"
smilePath = "C:\Users\sahol\Desktop\magic_mirror\haarcascade_smile.xml"
faceCascade = cv2.CascadeClassifier(facePath)
smileCascade = cv2.CascadeClassifier(smilePath)

CV_CAP_PROP_FRAME_WIDTH = 3
CV_CAP_PROP_FRAME_HEIGHT = 4
CV_CAP_PROP_FPS = 5

cap = cv2.VideoCapture(0)
cap.set(CV_CAP_PROP_FRAME_WIDTH ,420)#400
cap.set(CV_CAP_PROP_FRAME_HEIGHT,240)#400
cap.set(CV_CAP_PROP_FPS, 30)

#load the halo into numpy array
halo_image = Image.open("Desktop\magic_mirror\halo_flat.png")
halo = np.array(halo_image)

sF = 1.05
counter = 0

while True:

    counter+=1
    ret, frame = cap.read() # Capture frame-by-frame
    img = frame
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    main_img = np.zeros((1080,1920,4), np.int_)
    faces = []

    if counter!=0: 
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor= sF,
            minNeighbors=8,
            minSize=(55, 55),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
        )
    # ---- Draw a rectangle around the faces
    if len(faces)==0:
            cv2.imshow('Halo2', main_img)
    for (x_1, y_1, w_1, h_1) in faces:
        cv2.rectangle(frame, (x_1, y_1), (x_1+w_1, y_1+h_1), (0, 0, 255), 2)
        roi_gray = gray[y_1:y_1+h_1, x_1:x_1+w_1]
        roi_color = frame[y_1:y_1+h_1, x_1:x_1+w_1]

        smile = smileCascade.detectMultiScale(
            roi_gray,
            scaleFactor= 1.7,
            minNeighbors=8,
            minSize=(10, 10),
            flags=cv2.cv.CV_HAAR_SCALE_IMAGE
            )
        #if smile found, draw halo above head -> cv2 ellipse
        # Set region of interest for smiles
        width = int(x_1+.5*w_1)
        height = int(y_1-h_1/2)
        row_offset = int(4*x_1)
        col_offset = int(4*y_1)
        #TODO: significant slowdown due to iteration -> change to iteration
        #for r_idx, row in enumerate(halo):
            #print row 
        #    for c_idx, col in enumerate(row):
                #print col
        #        if col[3] != 0:
        #            main_r=r_idx+col_offset
        #            main_c=c_idx-row_offset
                    #print main_r
                    #print main_c
        #            if main_r<0: main_r=0
        #            if main_c<0: main_c=0 
        #            main_img[ main_r, main_c] = [255,255,255]
        #cv2.ellipse(frame,(width,height),(100,50),0,0,360,(255,255,255),20)
        #halo resizing .
        #must reset halo every time
        halo_image = Image.open("Desktop\magic_mirror\halo_flat.png")
        basewidth = 6*w_1 #resize halo to the width of the face
        wpercent = (basewidth / float(halo_image.size[0]))
        #print "wpercent: " + str(wpercent)
        #print "halo_image_size: " + str(halo_image.size[1])
        hsize = int((float(halo_image.size[1]) * float(wpercent)))
        if hsize<=0:
            print "Error in halo resizing!"
            hsize=1
        #print "hsize: " + str(hsize)
        halo_image = halo_image.resize((basewidth, hsize))
        #for debugging:
        #halo_image.save(r'Desktop\magic_mirror\resized_halo.png')
        #color ordering error due to cv2 vs matplotlib pixel ordering  
        halo = np.array(halo_image)
        halo = cv2.blur(halo, (5,5))
        #print blur_halo.shape
        #print main_img.shape
        #blur_halo = cv2.GaussianBlur(halo, (5,5),0)
        #---------------------
        #smile detection phase
        for (x, y, w, h) in smile:
            print "Found", len(smile), "smiles!"
        #    thickness = 2;
        #    lineType = 8;
        #    cv2.rectangle(roi_color, (x, y), (x+w, y+h), (255, 0, 0), 1)
        #    #cv2.ellipse(img, center, axes, angle, startAngle, endAngle, color[, thickness[, lineType[, shift]]])
        #    #TODO: make the size of the ellipse correspond to the size of the head box
        #    if height<0: height=0
        #    cv2.ellipse(frame,(width,height),(int(w_1/2),int(w_1/6)),0,0,360,(255,255,255),7)
            #TODO: resize the halo to match reflection width 
            #140x289x4
        #    cv2.ellipse(main_img,(width,height),(int(w_1/2),int(w_1/6)),0,0,360,(255,255,255),7)
            #TODO: function that overlays image with existing black numpy array -> scale starting position from (width,height)
            #let's only find one smile
        #    break
        #-------------------------
        #TODO: clean code
        #TODO: add smoothing to halo repositioning
        #cv2.cv.Flip(frame, None, 1)
        #UNDO for debugging
        #cv2.imshow('Smile Detector', frame)
        #halo.resize()
        #main_img = halo+main_img
            
            break
        c_offset = int(float(x_1+30)/float(420)*1920)
        r_offset = int(float(y_1-h_1-30)/float(240)*1080)
        #print "r_offset: " + str(r_offset)
        #print "c_offset: " + str(c_offset)#
        r_extend = (1080-halo.shape[0])-r_offset
        c_extend = (1920-halo.shape[1])-c_offset
        #deals with negative values while mainting 1920x1080 dimensionality total
        #TODO: figure out why going out of bounds seems to crash the program
        if r_extend<0: 
            r_offset=r_offset-r_extend
            r_extend=1
        if c_extend<0:
            c_offset = c_offset-c_extend
            c_extend=1
        if r_offset<0: 
            r_extend=r_extend-r_offset
            r_offset=1
        if c_offset<0:
            c_extend = c_extend-c_offset
            c_offset=1
        #print "c_extend: " + str(c_extend)
        #print "r_extend: " + str(r_extend)
        #cv2.imshow('Halo', halo)
        #we switch the c_extend and offset to account for the flipping of the camera feed
        halo = np.pad(halo, ((r_offset,r_extend),(c_extend,c_offset),(0,0)), mode='constant', constant_values=0)
        cv2.imshow('Halo2', halo)
        break
    #wtf is this:
    c = cv2.cv.WaitKey(7) % 0x100
    if c == 27:
        break

cap.release()
cv2.destroyAllWindows()