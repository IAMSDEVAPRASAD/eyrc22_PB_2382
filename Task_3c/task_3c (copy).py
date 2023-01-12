'''
*****************************************************************************************
*
*        		===============================================
*           		Pharma Bot (PB) Theme (eYRC 2022-23)
*        		===============================================
*
*  This script is to implement Task 3C of Pharma Bot (PB) Theme (eYRC 2022-23).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*
*****************************************************************************************
'''

# Team ID:			[ Team-ID ]
# Author List:		[ Names of team members worked on this file separated by Comma: Name1, Name2, ... ]
# Filename:			task_3c.py
# Functions:		[ perspective_transform, transform_values, set_values ]
# 					


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the five available  ##
## modules for this task                                    ##
##############################################################
import cv2 
import numpy 
from  numpy import interp
from zmqRemoteApi import RemoteAPIClient
import zmq
##############################################################

#################################  ADD UTILITY FUNCTIONS HERE  #######################

def und_undwrm(img):

    h = 316
    w = 467
    cameraMatrix = numpy.array( [[432.64843938,0.,323.04192955],[0.,431.83992831,245.06752113],[0.,0.,1.]])
    newCameraMatrix = numpy.array([[239.79382324,0.,342.27052461],[0.,245.33255005,268.8847273 ],[0.,0.,1.]])
    roi = (104, 105, 467, 316)
    dist = numpy.array([[-0.40167891,0.19897568,0.00285976,0.00067859,-0.04539993]])

    # Undistort
    dst = cv2.undistort(img, cameraMatrix, dist, None, newCameraMatrix)

    # crop the image
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]

    # Undistort with Remapping
    mapx, mapy = cv2.initUndistortRectifyMap(cameraMatrix, dist, None, newCameraMatrix, (w,h), 5)
    dst1 = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)

    # crop the image
    x, y, w, h = roi
    dst1 = dst[y:y+h, x:x+w]

    return dst,dst1

def centroid(vertexes):

     _x_list = [vertex [0] for vertex in vertexes]
     _y_list = [vertex [1] for vertex in vertexes]
     _len = len(vertexes)
     _x = sum(_x_list) / _len
     _y = sum(_y_list) / _len

     return(int(_x), int(_y))

#####################################################################################

def perspective_transform(image):

    """
    Purpose:
    ---
    This function takes the image as an argument and returns the image after 
    applying perspective transform on it. Using this function, you should
    crop out the arena from the full frame you are receiving from the 
    overhead camera feed.

    HINT:
    Use the ArUco markers placed on four corner points of the arena in order
    to crop out the required portion of the image.

    Input Arguments:
    ---
    `image` :	[ numpy array ]
            numpy array of image returned by cv2 library 

    Returns:
    ---
    `warped_image` : [ numpy array ]
            return cropped arena image as a numpy array
    
    Example call:
    ---
    warped_image = perspective_transform(image)
    """   
    warped_image = [] 
#################################  ADD YOUR CODE HERE  ###############################


    
    img_sent = image.copy()
    ArUco_details_dict, ArUco_corners = task_1b.detect_ArUco_details(img_sent)

    """
    x1 = ArUco_details_dict[1][0][0]
    y1 = ArUco_details_dict[1][0][1]
    x3 = ArUco_details_dict[3][0][0]
    y3 = ArUco_details_dict[3][0][1]
    
    roi = image[y3:y1, x3:x1]
    warped_image = roi
    """
    img  = image

    img_copy = numpy.copy(img)
    img_copy = cv2.cvtColor(img_copy,cv2.COLOR_BGR2RGB)

    """

    if len(ArUco_details_dict)>=4 :

        pt_A = [ArUco_details_dict[1][0][0], ArUco_details_dict[1][0][1]]
        pt_B = [ArUco_details_dict[2][0][0], ArUco_details_dict[2][0][1]]
        pt_C = [ArUco_details_dict[3][0][0], ArUco_details_dict[3][0][1]]
        pt_D = [ArUco_details_dict[4][0][0], ArUco_details_dict[4][0][1]]

    else:

    """

    pt_A = [362, 294]
    pt_B = [98, 284]
    pt_C = [99, 19]
    pt_D = [367, 15]


    width_AD = numpy.sqrt(((pt_A[0] - pt_D[0]) ** 2) + ((pt_A[1] - pt_D[1]) ** 2))
    width_BC = numpy.sqrt(((pt_B[0] - pt_C[0]) ** 2) + ((pt_B[1] - pt_C[1]) ** 2))
    maxWidth = max(int(width_AD), int(width_BC))


    height_AB = numpy.sqrt(((pt_A[0] - pt_B[0]) ** 2) + ((pt_A[1] - pt_B[1]) ** 2))
    height_CD = numpy.sqrt(((pt_C[0] - pt_D[0]) ** 2) + ((pt_C[1] - pt_D[1]) ** 2))
    maxHeight = max(int(height_AB), int(height_CD))

    input_pts = numpy.float32([pt_A, pt_B, pt_C, pt_D])
    output_pts = numpy.float32([[0, 0],[0, maxHeight - 1],[maxWidth - 1, maxHeight - 1],[maxWidth - 1, 0]])

    # Compute the perspective transform M
    M = cv2.getPerspectiveTransform(input_pts,output_pts)

    out = cv2.warpPerspective(img,M,(maxWidth, maxHeight),flags=cv2.INTER_LINEAR)
    out = cv2.rotate(out, cv2.ROTATE_90_CLOCKWISE)
    out = cv2.flip(out, 0)

    warped_image = out

######################################################################################

    return warped_image

def transform_values(image):

    """
    Purpose:
    ---
    This function takes the image as an argument and returns the 
    position and orientation of the ArUco marker (with id 5), in the 
    CoppeliaSim scene.

    Input Arguments:
    ---
    `image` :	[ numpy array ]
            numpy array of image returned by camera

    Returns:
    ---
    `scene_parameters` : [ list ]
            a list containing the position and orientation of ArUco 5
            scene_parameters = [c_x, c_y, c_angle] where
            c_x is the transformed x co-ordinate [float]
            c_y is the transformed y co-ordinate [float]
            c_angle is the transformed angle [angle]
    
    HINT:
        Initially the image should be cropped using perspective transform 
        and then values of ArUco (5) should be transformed to CoppeliaSim
        scale.
    
    Example call:
    ---
    scene_parameters = transform_values(image)
    """   
    scene_parameters = []
#################################  ADD YOUR CODE HERE  ###############################

    image_sended = image.copy()
    ArUco_details_dict, ArUco_corners = task_1b.detect_ArUco_details(image_sended)

    """
    x1y1 = ArUco_details_dict[1][0]
    x2y2 = ArUco_details_dict[2][0]
    x3y3 = ArUco_details_dict[3][0]
    x4y4 = ArUco_details_dict[4][0]
    """

    x1y1 = [362, 294]
    x2y2 = [98, 284]
    x3y3 = [99, 19]
    x4y4 = [367, 15]

    

    if len(ArUco_details_dict) == 5:

        x5y5 = ArUco_details_dict[5][0]

        

        polygon_data = (x1y1, x2y2, x3y3,x4y4)
        centroid_point = centroid(polygon_data) 

        xcg = -centroid_point[0]
        ycg = -centroid_point[1]

        """

        xcg = image.shape[0]/2
        ycg = image.shape[1]/2

        """

        T = [[1, 0, 0, xcg],[0, 1, 1, ycg],[0, 0, 0, 0],[0, 0, 0, 1]]
        pb = [[x5y5[0]], [x5y5[1]], [0], [1]]

        T = numpy.array(T,ndmin=4)
        pb = numpy.array(pb,ndmin=4)

        result=numpy.matmul(T,pb) 

        xgr = result[0][0][0][0]
        ygr = result[0][0][1][0]


        """
        sx = int(240/(x4y4[0]-x3y3[0]))
        sy = int(240/(x4y4[1]-x3y3[1]))
        """

        sx = -30
        sy = -30       
        
        """
        sx = int(240/316)
        sy = int(240/417)
        """

        #print(image.shape)

        S = [[sx,0],[0,sy]]
        P = [[xgr],[ygr]]

        S = numpy.array(S)
        P = numpy.array(P)

        result=numpy.matmul(T,pb) 

        xgr = (result[0][0][0][0]/100)
        ygr = (result[0][0][1][0]/100)

        scene_parameters = [xgr,ygr,ArUco_details_dict[5][1]]

    else:

        scene_parameters = [2,2,0]

        print("x5y5 is missing")

        
######################################################################################

    return scene_parameters


def set_values(scene_parameters):
    """
    Purpose:
    ---
    This function takes the scene_parameters, i.e. the transformed values for
    position and orientation of the ArUco marker, and sets the position and 
    orientation in the CoppeliaSim scene.

    Input Arguments:
    ---
    `scene_parameters` :	[ list ]
            list of co-ordinates and orientation obtained from transform_values()
            function

    Returns:
    ---
    None

    HINT:
        Refer Regular API References of CoppeliaSim to find out functions that can
        set the position and orientation of an object.
    
    Example call:
    ---
    set_values(scene_parameters)
    """   
    aruco_handle = sim.getObject('/aruco_5')
#################################  ADD YOUR CODE HERE  ###############################

    position_robot = (-scene_parameters[0]*0.765,scene_parameters[1]*0.72,+0.030)
    eulerAngles_robot = [0.0, 3.141592502593994,-((scene_parameters[2]*(3.141592502593994/180))-3.141592502593994)]
    
    sim.setObjectPosition(aruco_handle,sim.handle_parent, position_robot)
    sim.setObjectOrientation(aruco_handle,sim.handle_parent,eulerAngles_robot)

######################################################################################

    return None

if __name__ == "__main__":
    client = RemoteAPIClient()
    sim = client.getObject('sim')
    task_1b = __import__('task_1b')
#################################  ADD YOUR CODE HERE  ################################

    vid = cv2.VideoCapture(0)
  
    while(True):
          
        ret, frame = vid.read()
        dst,dst1 = und_undwrm(frame)
        frame1 = dst
        #frame1 = frame
        frame2 = frame1.copy() 
      
        warped_image = perspective_transform(frame1)
        kernel = numpy.array([[0, -1, 0],[-1, 5,-1],[0, -1, 0]])
        image_sharp = cv2.filter2D(src=warped_image, ddepth=-1, kernel=kernel)
        img = image_sharp

        scene_parameters = transform_values(frame2)
        set_values(scene_parameters)

        #cv2.imshow('frame', frame)
        cv2.imshow('frame',img)
 

        #print(scene_parameters)
    
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
      
    vid.release()
    cv2.destroyAllWindows()


#######################################################################################