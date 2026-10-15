import numpy as np
import cv2
import os
import sklearn
import matplotlib.pyplot as plt

x = []
y = []
dashed_path = "dataset/dashed"
solid_path = "dataset/solid"

for filename in os.listdir(dashed_path):

    image_path = os.path.join(dashed_path, filename)

    image = cv2.imread(image_path)
    if image is None:
        print('no image')

    else:
        
        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
       
        def region_interest(image):
            height = image.shape[0]
            weidth = image.shape[1]

            traingle = np.array([[(0,height),
                                (weidth,height),
                                (int(weidth*0.7),int(height*0.6)),
                                (int(weidth*0.3),int(height*0.6))]], np.int32)
            mask = np.zeros_like(image)
            cv2.fillPoly(mask,traingle,255)
            masked_image = cv2.bitwise_and(image,mask)
            return masked_image
       
            
        grey_img = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
        
        edges = cv2.Canny(grey_img, 160, 190)

        roi = region_interest(edges)
        
        lines = cv2.HoughLinesP(roi,1,np.pi/180,70,minLineLength=100,maxLineGap=150)

        if lines is None:
            continue

        line_image = np.zeros_like(image)
        if lines is not None:
            for line in lines:
                x1,y1,x2,y2 = line[0]
                cv2.line(line_image,(x1,y1),(x2,y2),(0,255,0),5)

        final_image = cv2.addWeighted(image,0.8,line_image,1,1)

        #plt.imshow(final_image )
        #plt.title('MULTIPLE LINE DETECTED')
        #plt.axis('off')
        #plt.show()

        def average_slope_intercept(image,lines):
            left_lines = []
            right_lines = []
            if lines is not None:
                for line in lines:
                    x1,y1,x2,y2 = line[0]

                    if x2-x1 == 0:
                        continue
                    slope = (y2-y1)/(x2-x1)
                    intercept = y1- slope * x1
                    if slope <0:
                        left_lines.append((slope,intercept))
                    else:
                        right_lines.append((slope,intercept))
            
            average_left_line = np.mean(left_lines,axis=0) if left_lines else None
            average_right_line = np.mean(right_lines,axis=0) if right_lines else None
            return average_left_line,average_right_line
        average_left_line,average_right_line = average_slope_intercept(image,lines)
    
        num_segments = len(lines)

        lengths = []

        for line in lines:

            x1, y1, x2, y2 = line[0]

            length = ((x2-x1)**2 + (y2-y1)**2)**0.5

            lengths.append(length)

        avg_length = sum(lengths) / len(lengths)

        left_slope = average_left_line[0] if average_left_line is not None else 0
        right_slope = average_right_line[0] if average_right_line is not None else 0

        features = [num_segments,avg_length,left_slope,right_slope]
        x.append(features)
        y.append("dashed")


for filename in os.listdir(solid_path):

    image_path = os.path.join(solid_path, filename)

    image = cv2.imread(image_path)
    if image is None:
        print('no image')

    else:
       
        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        
        grey_img = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
        
        edges = cv2.Canny(grey_img, 160, 190)
        
        def region_interest(image):
            height = image.shape[0]
            weidth = image.shape[1]

            traingle = np.array([[(0,height),
                                (weidth,height),
                                (int(weidth*0.7),int(height*0.6)),
                                (int(weidth*0.3),int(height*0.6))]], np.int32)
            mask = np.zeros_like(image)
            cv2.fillPoly(mask,traingle,255)
            masked_image = cv2.bitwise_and(image,mask)
            return masked_image
        roi = region_interest(edges)
        
        lines = cv2.HoughLinesP(roi,1,np.pi/180,70,minLineLength=100,maxLineGap=150)
        if lines is None:
            continue

        line_image = np.zeros_like(image)
        if lines is not None:
            for line in lines:
                x1,y1,x2,y2 = line[0]
                cv2.line(line_image,(x1,y1),(x2,y2),(0,255,0),5)

        final_image = cv2.addWeighted(image,0.8,line_image,1,1)

        
        def average_slope_intercept(image,lines):
            left_lines = []
            right_lines = []
            for line in lines:
                x1,y1,x2,y2 = line[0]

                if x2-x1 == 0:
                    continue
                slope = (y2-y1)/(x2-x1)
                intercept = y1- slope * x1
                if slope <0:
                    left_lines.append((slope,intercept))
                else:
                    right_lines.append((slope,intercept))
            
            average_left_line = np.mean(left_lines,axis=0) if left_lines else None
            average_right_line = np.mean(right_lines,axis=0) if right_lines else None
            return average_left_line,average_right_line
        average_left_line,average_right_line = average_slope_intercept(image,lines)
    
        num_segments = len(lines)

        lengths = []

        for line in lines:

            x1, y1, x2, y2 = line[0]

            length = ((x2-x1)**2 + (y2-y1)**2)**0.5

            lengths.append(length)

        avg_length = sum(lengths) / len(lengths)

        left_slope = average_left_line[0] if average_left_line is not None else 0
        right_slope = average_right_line[0] if average_right_line is not None else 0

        features = [num_segments,avg_length,left_slope,right_slope]
        x.append(features)
        y.append("solid")

from sklearn.ensemble import RandomForestClassifier

model = RandomForestClassifier()

model.fit(x, y)

lane = True
while lane:
    user_decision = input("Would you like to predict(type 'yes'/'no'): ")
    if user_decision.lower() == 'no':
        print("Program Turned OFF\nTHANKS")
        lane=False
    elif user_decision.lower() =='yes':
        os.system('cls')
               
        input_image = input('enter the exact image path: ')

        image = cv2.imread(input_image)
        if image is None:
            print('no image')

            #if input_image == "off":
                #print('program turned off \n thanks ')
                #lane = False
            #else:
                #print('invalid input')
        

        else:
            
            image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
            plt.imshow(image)
            plt.title('IMAGE LOADED SUCCESSFULLY')
            plt.axis('off')
            plt.show()

                # Convert RGB to HSV
            hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

            # Yellow color range
            lower_yellow = np.array([20, 100, 100])
            upper_yellow = np.array([35, 255, 255])

            # White color range
            lower_white = np.array([0, 0, 200])
            upper_white = np.array([180, 30, 255])

            # Create masks
            yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
            white_mask = cv2.inRange(hsv, lower_white, upper_white)

            # Apply ROI to masks
            yellow_roi = region_interest(yellow_mask)
            white_roi = region_interest(white_mask)

            # Count pixels
            yellow_pixels = cv2.countNonZero(yellow_roi)
            white_pixels = cv2.countNonZero(white_roi)

            # Decide lane color
            if yellow_pixels > white_pixels:
                lane_color = "yellow"
            else:
                lane_color = "white"

            print("Lane Color:", lane_color)
            grey_img = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
            
            edges = cv2.Canny(grey_img, 160, 190)
            
            def region_interest(image):
                height = image.shape[0]
                weidth = image.shape[1]

                traingle = np.array([[(0,height),
                                    (weidth,height),
                                    (int(weidth*0.7),int(height*0.6)),
                                    (int(weidth*0.3),int(height*0.6))]], np.int32)
                mask = np.zeros_like(image)
                cv2.fillPoly(mask,traingle,255)
                masked_image = cv2.bitwise_and(image,mask)
                return masked_image
            roi = region_interest(edges)
            
            lines = cv2.HoughLinesP(roi,1,np.pi/180,70,minLineLength=100,maxLineGap=150)

            line_image = np.zeros_like(image)
            if lines is not None:
                for line in lines:
                    x1,y1,x2,y2 = line[0]
                    cv2.line(line_image,(x1,y1),(x2,y2),(0,255,0),5)

            final_image = cv2.addWeighted(image,0.8,line_image,1,1)

            #plt.imshow(final_image )
            #plt.title('MULTIPLE LINE DETECTED')
            #plt.axis('off')
            #plt.show()

            def average_slope_intercept(image,lines):
                left_lines = []
                right_lines = []
                for line in lines:
                    x1,y1,x2,y2 = line[0]

                    if x2-x1 == 0:
                        continue
                    slope = (y2-y1)/(x2-x1)
                    intercept = y1- slope * x1
                    if slope <0:
                        left_lines.append((slope,intercept))
                    else:
                        right_lines.append((slope,intercept))
                    
                average_left_line = np.mean(left_lines,axis=0) if left_lines else None
                average_right_line = np.mean(right_lines,axis=0) if right_lines else None
                return average_left_line,average_right_line
            average_left_line,average_right_line = average_slope_intercept(image,lines)

            num_segments = len(lines)

            lengths = []

            for line in lines:

                x1, y1, x2, y2 = line[0]

                length = ((x2-x1)**2 + (y2-y1)**2)**0.5

                lengths.append(length)

            avg_length = sum(lengths) / len(lengths)

            left_slope = average_left_line[0] if average_left_line is not None else 0
            right_slope = average_right_line[0] if average_right_line is not None else 0

            new_features = [num_segments,avg_length,left_slope,right_slope]


            prediction = model.predict([new_features])
            #print(prediction)
            if prediction == 'dashed':
                print("this lane is DASHED\nyou can overtake.")
            else:
                print("this lane is solid\nyou cannot overtake from here.\nwait for the dashed lane")
    else:
        print('invalid input')  