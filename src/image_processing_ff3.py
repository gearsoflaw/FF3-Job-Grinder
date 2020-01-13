# This mess has been created by GearsOfLaw https://github.com/gearsoflaw
""" This module contains FF3 specific image processing functions """
import numpy as np
import cv2
#from ff3_consts_training import FF3
from ff3_consts_running import FF3

class ImageProcessingFF3:
    """ This class contains FF3 specific image processing functions """
    @staticmethod
    def find_battle_commands_to_vote_for(image, lines):
        """ Draws the Verticle lines on the command box and vote for commands """
        vote_for_cmd_1 = 0
        vote_for_cmd_2 = 0
        vote_for_cmd_3 = 0
        spoiled_vote = 0
        
        if(lines is None):
            return vote_for_cmd_1, vote_for_cmd_2, vote_for_cmd_3, spoiled_vote
            
        real_lines = lines.shape[0]
        for line in range(real_lines):
            x1 = lines[line][0][0]
            y1 = lines[line][0][1]
            x2 = lines[line][0][2]
            y2 = lines[line][0][3]

            angle = abs(np.arctan2(y2 - y1, x2 - x1) * 180. / np.pi)
            if angle >= FF3.MIN_ANGLE_VERTICLE_BATTLE and angle <= FF3.MAX_ANGLE_VERTICLE_BATTLE:
                cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)            

                # Checks if y1 (top point) and y2 (bottom point) is within a command box
                if(y1 >= FF3.CMD_BOX_UP_Y_1 and y1 <= FF3.CMD_BOX_BT_Y_1 and y2 >= FF3.CMD_BOX_UP_Y_1 and y2 <= FF3.CMD_BOX_BT_Y_1):
                    vote_for_cmd_1 = 1
                elif(y1 >= FF3.CMD_BOX_UP_Y_2 and y1 <= FF3.CMD_BOX_BT_Y_2 and y2 >= FF3.CMD_BOX_UP_Y_2 and y2 <= FF3.CMD_BOX_BT_Y_2):
                    vote_for_cmd_2 = 1
                elif(y1 >= FF3.CMD_BOX_UP_Y_3 and y1 <= FF3.CMD_BOX_BT_Y_3 and y2 >= FF3.CMD_BOX_UP_Y_3 and y2 <= FF3.CMD_BOX_BT_Y_3):
                    vote_for_cmd_3 = 1
                else:
                    spoiled_vote = 1

        # A valid vote will be where two commands have lines and 1 command has no line
        is_valid_votes = vote_for_cmd_1 + vote_for_cmd_2 + vote_for_cmd_3 == 2

        if is_valid_votes:
            return vote_for_cmd_1, vote_for_cmd_2, vote_for_cmd_3, spoiled_vote
        else: # Return result as a spoiled vote
            return 0, 0, 0, 1

    @staticmethod
    def find_fan_commands_to_vote_for(image, lines):
        """ Draws the Horizontal lines on the info box and vote if an action command is needed """
        votes_for_cmd_action = 0

        if(lines is None):
            return votes_for_cmd_action
            
        real_lines = lines.shape[0]
        for line in range(real_lines):

            x1 = lines[line][0][0]
            y1 = lines[line][0][1]
            x2 = lines[line][0][2]
            y2 = lines[line][0][3]
            cv2.line(image, (x1, y1), (x2, y2), (255, 100, 0), 2)

            # can only get here if there is a sufficiently long line
            # NOTE: This will need to be tweaked with more logic if more complex logic like Job changing/Saving is added
            # NOTE: This also assumes that you are not in battles that result in info boxes displaying (i.e. it assumes you are Job Grinding), i.e. This is a naive approach
            votes_for_cmd_action = 1

        return votes_for_cmd_action

    @staticmethod
    def image_preprocessing(image):
        """ Prepares image detecting edges and blurring and other pre-processing"""
        # edge detection
        processed_img = cv2.Canny(image, threshold1=FF3.CANNY_THRESHOLD_1, threshold2=FF3.CANNY_THRESHOLD_2, apertureSize=FF3.CANNY_APERTURE)

        processed_img = cv2.GaussianBlur(processed_img, FF3.GAUSS_KSIZE, FF3.GAUSS_SIGMA_X)
        return processed_img

    @staticmethod
    def get_houghlinesP_battle(image):
        """ Process image to get the Predictive Hough Lines"""
        # more info: http://docs.opencv.org/3.0-beta/doc/py_tutorials/py_imgproc/py_houghlines/py_houghlines.html        
        lines = cv2.HoughLinesP(image, \
            rho=FF3.HOUGH_RHO_BATTLE, theta=FF3.HOUGH_THETA_BATTLE, threshold=FF3.HOUGH_THRESHOLD_BATTLE,\
            minLineLength=FF3.HOUGH_MINLINELENGTH_BATTLE, maxLineGap=FF3.HOUGH_MAXLINEGAP_BATTLE)
        return lines

    @staticmethod
    def get_houghlinesP_fan(image):
        """ Process image to get the Predictive Hough Lines"""      
        lines = cv2.HoughLinesP(image, \
            rho=FF3.HOUGH_RHO_FAN, theta=FF3.HOUGH_THETA_FAN, threshold=FF3.HOUGH_THRESHOLD_FAN,\
            minLineLength=FF3.HOUGH_MINLINELENGTH_FAN, maxLineGap=FF3.HOUGH_MAXLINEGAP_FAN)
        return lines
