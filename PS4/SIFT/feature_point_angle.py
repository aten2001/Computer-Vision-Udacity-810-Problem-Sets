import numpy as np
import cv2 as cv
import sys
import ps12 as ps









def draw_line(description,angle, corners, img):
    for i in range(0, len(corners)):
        x1 = int(corners[i][1])
        y1 = int(corners[i][0])


        x2 = int(x1 + 10*np.cos(angle[y1,x1]))
        y2 = int(y1 + 10*np.sin(angle[y1,x1]))
        cv.line(img,(x1,y1), (x2,y2),(0,255,0),2)
    ps.display_image(description, img)

#function to calculate the harris corners
#input      img and the window size
#output     corners image

def harris_Corners(img, window_size):
    """ Harris corners function takes the image and builds the R corner
    response image"""
    smooth = cv.GaussianBlur(img,(3,3),0)
    gray = cv.cvtColor(smooth, cv.COLOR_BGR2GRAY)
    grad_x =  cv.Sobel(gray,-1,1,0,ksize = 3)
    grad_y =  cv.Sobel(gray,-1,0,1,ksize = 3)

    h,w = grad_x.shape
    corners = np.zeros((h,w), dtype = np.float64)
    grad_x = grad_x.astype(np.float64)
    grad_y = grad_y.astype(np.float64)

    grad_xx = grad_x**2
    grad_xx = cv.GaussianBlur(grad_xx,(3,3),0.5)
    grad_yy = grad_y**2
    grad_yy = cv.GaussianBlur(grad_yy,(3,3),0.5)
    grad_xy = grad_x *grad_y
    grad_xy = cv.GaussianBlur(grad_xy, (3,3), 0.5)



    offset = int(window_size/2)
    for i in range(offset, h-offset):
        for j in range(offset, w-offset):
            temp1 = grad_xx[i-offset:i+offset+1, j-offset:j+offset+1]
            temp2 = grad_yy[i-offset:i+offset+1, j-offset:j+offset+1]
            temp3 = grad_xy[i-offset:i+offset+1, j-offset:j+offset+1]
            a = np.sum(temp1)
            b = np.sum(temp2)
            c= np.sum(temp3)
            det  = a*b - (c*c)
            trace = a+b
            R = det - 0.04*(trace**2)
            corners[i,j] = R

    return corners










def thresholding_and_non_maximum_supression(corners, img):

    harris = np.asarray(corners)
    threshold = 0.1*np.amax(corners)
    max_overlap =8
    max_overlap*=max_overlap
    h,w = corners.shape
    window = 8
    offset =  window//2
    corner_ptr = []
    pick = []
    for m in range(offset , h-offset, offset):
        for n in range(offset, w-offset, offset):
            #window extracted
            temp =  harris[m-offset:m+offset, n-offset:n+offset]
            a,b  = np.nonzero(temp > threshold )
            if (len(a) >0):
                temp3 = temp[a,b]
                list1 = np.ones((len(a), 3))

                supress = []
                list1[:, 0] = a; list1[:,1] = b; list1[:, 2] =temp3;

                ind = np.argsort( list1[:,2] ); list1 = list1[ind]
                list1[:,2] = list1[:,2]//list1[0,2];

                #breakpoint()

                while(len(list1) > 0):
                    last = len(list1) - 1;
                    cor = np.copy(list1[last]);
                    i = list1[last]; cor[0]+=(m-offset); cor[1]+=(n-offset); b
                    #breakpoint()
                    pick.append(cor)
                    supress= [last]
                    temp_list = np.copy(list1[0:last])
                    temp_list[:,0]-=i[0]
                    temp_list[:,0]**=2
                    temp_list[:,1]-=i[1]
                    temp_list[:,1]**=2
                    list2 = np.copy(temp_list[:,0]+ temp_list[:, 1])
                    pos = np.nonzero(list2 <= max_overlap)
                    list1 = np.delete(list1, supress, 0)

                    list1 = np.delete(list1,pos, 0);




    key_points = np.ones((len(pick), 3))
    for i in range(len(pick)):
        key_points[i] = pick[i]
    ind = np.argsort( key_points[:,2] ); key_points = key_points[ind]
    return key_points[0:500]

def calculate_descriptors(description,img1):
    gray = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)

    sift = cv.xfeatures2d.SIFT_create()

    grad_x =  cv.Sobel(gray,-1,1,0,ksize = 3)
    grad_y =  cv.Sobel(gray,-1,0,1,ksize = 3)
    corners = harris_Corners(img1,5)

    corner_ptr = thresholding_and_non_maximum_supression(corners, img1)

    angle = np.arctan2(grad_y, grad_x)
    draw_line(description,angle,corner_ptr, img1)


def main(argv):

    if(len(argv) < 1):
        print("not enough parameters\n")
        print("usage PS1-1.py <path to image>\n")
        return -1


    img1 = cv.imread(argv[0],cv.IMREAD_COLOR)
    if img1 is None:
        print("Error opening image\n")
        return -1
    calculate_descriptors("image 1", img1)









# if someone import this module then this line makes sure that it does not Run
# on its own
if __name__ == "__main__":
    main(sys.argv[1:])
