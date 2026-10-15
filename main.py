import numpy as np
import cv2
import matplotlib.pyplot as plt
lane = True
while lane:

    input_image = input('enter the exact image path\n   OR\n(type "off" to close program): ')

    image = cv2.imread(input_image)
    if image is None:
        print('no image')

        if input_image == "off":
            print('program turned off \n thanks ')
            lane = False
        else:
            print('invalid input')
    

    else:
        print('HI')

        image = cv2.cvtColor(image,cv2.COLOR_BGR2RGB)
        print(image)
        plt.imshow(image)
        plt.title('IMAGE LOADED SUCCESSFULLY')
        plt.axis('off')
        plt.show()
        grey_img = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
        plt.imshow(grey_img , cmap='gray')
        plt.title('GRAY SCALE img')
        plt.axis('off')
        plt.show()

        edges = cv2.Canny(grey_img, 160, 190)
        plt.imshow(edges,cmap='gray' )
        plt.title('All Detected Edges')
        plt.axis('off')
        plt.show()

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
        plt.imshow(roi,cmap='gray' )
        plt.title('ROI SELECTED')
        plt.axis('off')
        plt.show()

        lines = cv2.HoughLinesP(roi,1,np.pi/180,70,minLineLength=100,maxLineGap=150)

        line_image = np.zeros_like(image)
        if lines is not None:
            for line in lines:
                x1,y1,x2,y2 = line[0]
                cv2.line(line_image,(x1,y1),(x2,y2),(0,255,0),5)

        final_image = cv2.addWeighted(image,0.8,line_image,1,1)

        plt.imshow(final_image )
        plt.title('MULTIPLE LINE DETECTED')
        plt.axis('off')
        plt.show()

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
            
        def make_cordinates(image,line_params):
            slope,intercept = line_params

            y1 = image.shape[0]
            y2 = int(y1 * 0.6)

            x1 = int((y1-intercept)/slope)
            x2 = int((y2-intercept)/slope)

            return [x1,y1,x2,y2]

        line_img = np.zeros_like(image)
        if average_left_line is not None:
            x1,y1,x2,y2 =make_cordinates(image, average_left_line)
            cv2.line(line_img,(x1,y1),(x2,y2),(0,255,0),5)

        if average_right_line is not None:
            x1,y1,x2,y2 =make_cordinates(image, average_right_line)
            cv2.line(line_img,(x1,y1),(x2,y2),(0,255,0),9)

        correct_line_img = cv2.addWeighted(image,0.8,line_img,1,1)
        plt.imshow(correct_line_img )
        plt.title('DETECTED LANE')
        plt.axis('off')
        plt.show()

    






    
