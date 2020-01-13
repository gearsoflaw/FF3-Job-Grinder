# This mess has been created by GearsOfLaw https://github.com/gearsoflaw
""" This module conatins all constants used for FF3 when executing against training recordings """
import numpy as np

class FF3:
    """ FF3 constants for screen location and ROI """
    # Screengrab co-ordinates and size
    GRAB_OFFSET_X = 30
    GRAB_OFFSET_Y = 250
    GRAB_SIZE_X = 820
    GRAB_SIZE_Y = 790

    # Region of interest for command waiting area
    ROI_TP_LF_BATTLE = [5, 320]
    ROI_BT_LF_BATTLE = [5, 540]
    ROI_TP_RG_BATTLE = [240, 320]
    ROI_BT_RG_BATTLE = [240, 540]

    # Region of interest for Fan fare screen
    ROI_TP_LF_FAN = [25, 5]
    ROI_BT_LF_FAN = [25, 15]
    ROI_TP_RG_FAN = [750, 5]
    ROI_BT_RG_FAN = [750, 15]

    # Canny and Gauss parameters
    CANNY_THRESHOLD_1 = 350
    CANNY_THRESHOLD_2 = 450
    CANNY_APERTURE = 3
    GAUSS_KSIZE = (3, 3)
    GAUSS_SIGMA_X = 0
    GAUSS_SIGMA_Y = 0

    # Hough Line Parameters for battle screen
    HOUGH_RHO_BATTLE = 1
    HOUGH_THETA_BATTLE = np.pi/180
    HOUGH_THRESHOLD_BATTLE = 110
    HOUGH_MINLINELENGTH_BATTLE = 45
    HOUGH_MAXLINEGAP_BATTLE = 2

    # Hough Line Parameters for fanfare screen
    HOUGH_RHO_FAN = 1
    HOUGH_THETA_FAN = np.pi/180
    HOUGH_THRESHOLD_FAN = 180
    HOUGH_MINLINELENGTH_FAN = 300
    HOUGH_MAXLINEGAP_FAN = 50

    # Detecting Line Restrictions for battle
    MIN_ANGLE_VERTICLE_BATTLE = 85
    MAX_ANGLE_VERTICLE_BATTLE = 95

    # Co-ordinates where each command box can be found
    CMD_BOX_UP_Y_1 = 329
    CMD_BOX_BT_Y_1 = 406
    CMD_BOX_UP_Y_2 = 387
    CMD_BOX_BT_Y_2 = 473
    CMD_BOX_UP_Y_3 = 454
    CMD_BOX_BT_Y_3 = 539

    # Command Constants
    CMD_STD_GRIND = [3, 0] # Standard Command Box to use when Grinding with no follow up action
    CMD_STD_ATT = [1, 1] # Standard Command Box to use when Attacking with no follow up action
    CMD_SP_STEAL = [2, 1] # Command box to use when Thief is in party with  follow up action to use command box 1

    # Character Placements
    CHAR_1 = 0 # Luneth
    CHAR_2 = 1 # Arc
    CHAR_3 = 2 # Refia
    CHAR_4 = 3 # Ingus

    # How many rounds to grind for JP before the battle can be ended
    GRIND_ROUNDS = 6

    # Command sequence to grind
    GRIND_CMD = {CHAR_1: CMD_STD_GRIND, CHAR_2: CMD_STD_GRIND, CHAR_3: CMD_SP_STEAL, CHAR_4: CMD_STD_GRIND}
    
    # Other Functions
    DISABLE_ACTIONS = True # Set to true if you do not want any keyboard commands performed
    DELAY_START = True
    DELAY_START_SECONDS = 1
    SHOW_SCREEN = True
    SHOW_PREPROCESSED_SCREEN = True
    SHOW_BATTLE_MASK_SCREEN = False
    SHOW_FAN_MASK_SCREEN = False
    SHOW_FRAME_CAPTURE_TIME = False
    FINAL_VOTE_INTERVAL = 1.5 # Time in seconds for votes to be cast
    VOTE_COOLDOWN = 1 # Time in seconds between actioning votes before voting begins again
    MARGIN_FOR_VICTORY = 20 # The first command to 5 point lead will be chosen
    IS_IN_WORLD_INTERVAL_CHECK = 2 # Time in seconds per in world move command is pressed
