# This mess has been created by GearsOfLaw https://github.com/gearsoflaw
""" This module is used to automatically perform the grinding needed to level up FF3 jobs """
import time
from collections import Counter
import numpy as np
import cv2
from grabscreen import grab_screen
from image_processing_common import ImageProcessing
from image_processing_ff3 import ImageProcessingFF3
from ff3_commands import FF3Commands
#from ff3_consts_training import FF3
from ff3_consts_running import FF3

def process_battle_commands(captured_image, pre_processed_image):
    mask_vertices = np.array([FF3.ROI_TP_LF_BATTLE, FF3.ROI_TP_RG_BATTLE, FF3.ROI_BT_RG_BATTLE, FF3.ROI_BT_LF_BATTLE], np.int32)
    masked_image = ImageProcessing.region_of_interest(pre_processed_image, [mask_vertices])

    lines = ImageProcessingFF3.get_houghlinesP_battle(masked_image)
    votes_cmd1, votes_cmd2, votes_cmd3, spoiled_vote = ImageProcessingFF3.find_battle_commands_to_vote_for(captured_image, lines)
    
    return masked_image, votes_cmd1, votes_cmd2, votes_cmd3, spoiled_vote

def process_fanfare(captured_image, pre_processed_image):
    mask_vertices = np.array([FF3.ROI_TP_LF_FAN, FF3.ROI_TP_RG_FAN, FF3.ROI_BT_RG_FAN, FF3.ROI_BT_LF_FAN], np.int32)
    masked_image = ImageProcessing.region_of_interest(pre_processed_image, [mask_vertices])

    lines = ImageProcessingFF3.get_houghlinesP_fan(masked_image)
    votes_action = ImageProcessingFF3.find_fan_commands_to_vote_for(captured_image, lines)
    
    return masked_image, votes_action

def delay_start():
    if(FF3.DELAY_START):
        print("Start count down beginning...")
        # Delay with Countdown before processing begins
        for i in list(range(FF3.DELAY_START_SECONDS))[::-1]:
            print(i+1)
            time.sleep(1)

def draw_hit_box(image):
    # Command Box 1 Range
    cv2.line(image, (2, FF3.CMD_BOX_UP_Y_1), (2, FF3.CMD_BOX_BT_Y_1), (0, 220, 255), 2)
    cv2.line(image, (2, FF3.CMD_BOX_UP_Y_1), (200, FF3.CMD_BOX_UP_Y_1), (0, 220, 255), 2)
    cv2.line(image, (2, FF3.CMD_BOX_BT_Y_1), (200, FF3.CMD_BOX_BT_Y_1), (0, 220, 255), 2)
    # Command Box 2 Range
    cv2.line(image, (2, FF3.CMD_BOX_UP_Y_2), (2, FF3.CMD_BOX_BT_Y_2), (255, 0, 0), 2)        
    cv2.line(image, (2, FF3.CMD_BOX_UP_Y_2), (200, FF3.CMD_BOX_UP_Y_2), (255, 0, 0), 2)
    cv2.line(image, (2, FF3.CMD_BOX_BT_Y_2), (200, FF3.CMD_BOX_BT_Y_2), (255, 0, 0), 2)
    # Command Box 3 Range
    cv2.line(image, (2, FF3.CMD_BOX_UP_Y_3), (2, FF3.CMD_BOX_BT_Y_3), (220, 220, 0), 2)        
    cv2.line(image, (2, FF3.CMD_BOX_UP_Y_3), (200, FF3.CMD_BOX_UP_Y_3), (220, 220, 0), 2)
    cv2.line(image, (2, FF3.CMD_BOX_BT_Y_3), (200, FF3.CMD_BOX_BT_Y_3), (220, 220, 0), 2)

def reset_votes():
    return 0, 0, 0, 0, 0

def get_min_result(results, vote_index=1):
    return min(results, key=lambda t: t[vote_index])

def perform_world_action(go_right):
    FF3Commands.release_all()
    if go_right:
        print("Moving Right...")
        FF3Commands.hold_right()
    else:
        print("Moving Left...")
        FF3Commands.hold_left()

def perform_battle_action(command_pointer, character_id, end_round):
    # Release all keys incase a world key direction is being pressed
    FF3Commands.release_all()
    command_target = [0]
    if end_round:
        # When end of round force action to Attack
        command_target = FF3.CMD_STD_ATT
    else:
        command_target = FF3.GRIND_CMD[character_id]

    command_count = 0
    for desired_command in command_target:
        if desired_command == 0:
            # Do nothing
            continue

        print(f"Desired command {desired_command}")
        command_distance = command_pointer - desired_command
        command_direction_up = command_distance > 0 # MOVE UP
        command_direction_down = command_distance < 0 # MOVE DOWN
        moves = abs(command_distance)
        print(f"Desired command {desired_command} :: Moves {moves} :: Up {command_direction_up} :: Down {command_direction_down}")
        # Move into possition
        while moves > 0:
            if(command_direction_up):
                FF3Commands.quick_up()
            elif(command_direction_down):

                FF3Commands.quick_down()
            # else do nothing

            moves -= 1

        if command_count > 0:
            # Need to slow down for subsequent commands to ensure the screen has the option before pressing the action key
            time.sleep(0.2)

        # Press Action key
        FF3Commands.quick_action()
        # Set command_pointer to 1 for any subsequent windows TODO: This will be problematic in more complex chains, especially if Memorize is enabled
        command_pointer = 1
        command_count += 1

def perform_fan_action():
    # Release all keys incase a world key direction is being pressed
    FF3Commands.release_all()
    # Press Action key
    FF3Commands.quick_action()

def setup_next_action(current_character, current_round, is_end_of_rounds):
    print(f"current character {current_character} current round {current_round} end of rounds {is_end_of_rounds}")
    if current_character >= 3 and is_end_of_rounds:
        # Round is complete and is reset to await start of a new round
        # TODO: This assumes your end round will kill the enemies, if not the round will start over
        return FF3.CHAR_1, 0
    if current_character >= 3:
        # A new round will be starting, we reset to the first character and increment the round
        return FF3.CHAR_1, current_round + 1
    else:
        # Move to the next character, still on the current round
        return current_character + 1, current_round

def Main():
    current_char = FF3.CHAR_1
    current_round = 0
    frame_count = 0
    voting_start_time = time.time()
    current_time = voting_start_time
    cooldown_start_time = 0
    is_voting = True # Is the state of the program in voting mode
    is_cooldown = False # Is the state of the program in cooldown mode, we start in cooldown to warm up
    in_world_time = current_time
    in_world_go_right = True # we start by going right
    total_votes_cmd1, total_votes_cmd2, total_votes_cmd3, total_spoiled_vote, total_fan_action_vote = reset_votes()

    print(f"Begin Voting for {FF3.FINAL_VOTE_INTERVAL} seconds...")
    print("Winner has the LEAST amount of votes and indicates where the cursor is present")
    while True:
        
        # If the current votes cast is low and we are not in a cooldown period assume we are in world
        # the in_world_time check allows us to press the direction key without having to initiate a time delay to the program
        # i.e. press and carry on processing
        is_in_world = total_votes_cmd1 + total_votes_cmd2 + total_votes_cmd3 + total_fan_action_vote <= 5
        if is_cooldown is False and is_in_world and current_time - in_world_time >= FF3.IS_IN_WORLD_INTERVAL_CHECK:
            perform_world_action(in_world_go_right)
            in_world_go_right = not in_world_go_right # invert the direction for the next time
            in_world_time = time.time()

        captured_image = grab_screen(region=(FF3.GRAB_OFFSET_X, FF3.GRAB_OFFSET_Y, FF3.GRAB_SIZE_X, FF3.GRAB_SIZE_Y))
        pre_processed_image = ImageProcessingFF3.image_preprocessing(captured_image)
        #draw_hit_box(captured_image)
        
        battle_mask, votes_cmd1, votes_cmd2, votes_cmd3, spoiled_vote = process_battle_commands(captured_image, pre_processed_image)
        fan_mask, votes_fan_action = process_fanfare(captured_image, pre_processed_image)
        frame_count += 1
        if FF3.SHOW_SCREEN:
            cv2.imshow('window_original_with_overlay', cv2.cvtColor(captured_image, cv2.COLOR_BGR2RGB))
        if FF3.SHOW_PREPROCESSED_SCREEN:
            cv2.imshow('window_preprocessed', cv2.cvtColor(pre_processed_image, cv2.COLOR_BGR2RGB))
        if FF3.SHOW_BATTLE_MASK_SCREEN:
            cv2.imshow('window_battle_mask', cv2.cvtColor(battle_mask, cv2.COLOR_BGR2RGB))
        if FF3.SHOW_FAN_MASK_SCREEN:
            cv2.imshow('window_fan_mask', cv2.cvtColor(fan_mask, cv2.COLOR_BGR2RGB))
        if FF3.SHOW_FRAME_CAPTURE_TIME:
            print('Frame took {} seconds'.format(time.time()-current_time))

        current_time = time.time()
        if(is_voting and current_time - voting_start_time >= FF3.FINAL_VOTE_INTERVAL):
            # Time to Tally the votes
            print(f"Frames in session {frame_count}")
            frame_count = 0
            print(f"Cmd 1 Votes: {total_votes_cmd1}")
            print(f"Cmd 2 Votes: {total_votes_cmd2}")
            print(f"Cmd 3 Votes: {total_votes_cmd3}")
            print(f"Fan Action Votes: {total_fan_action_vote}")
            print(f"Spoiled Votes: {total_spoiled_vote}")

            results = [(1, total_votes_cmd1), (2, total_votes_cmd2), (3, total_votes_cmd3)]
            winner = get_min_result(results)
            winner_id = winner[0]
            winner_score = winner[1]
            counts = Counter(x[1] for x in results)
            instances_min_votes = counts[winner_score]
            has_winner = False

            if(total_fan_action_vote >= FF3.MARGIN_FOR_VICTORY):
                print(f"Fanfare Action being performed {total_fan_action_vote}")
                if FF3.DISABLE_ACTIONS is False:
                    perform_fan_action()
                
                total_votes_cmd1, total_votes_cmd2, total_votes_cmd3, total_spoiled_vote, total_fan_action_vote = reset_votes()
                has_winner = True
                #current_round = 0
                #current_char = FF3.CHAR_1
            elif(instances_min_votes == 1):
                results.remove(winner) # Remove the leader from the results to get runner-up
                runner_up = get_min_result(results)
                runner_up_id = runner_up[0]
                runner_up_score = runner_up[1]
                current_margin = runner_up_score - winner_score

                if(current_margin >= FF3.MARGIN_FOR_VICTORY):
                    print(f"Winner: {winner_id} Votes: {winner_score}")
                    print(f"Runner Up: {runner_up_id} Votes: {runner_up_score}")
                    total_votes_cmd1, total_votes_cmd2, total_votes_cmd3, total_spoiled_vote, total_fan_action_vote = reset_votes()
                    has_winner = True

                    is_end_of_round = current_round >= FF3.GRIND_ROUNDS
                    if FF3.DISABLE_ACTIONS is False:
                        perform_battle_action(winner_id, current_char, is_end_of_round)

                    current_char, current_round = setup_next_action(current_char, current_round, is_end_of_round)
                else:
                    print(f"A margin of {FF3.MARGIN_FOR_VICTORY} is required for victory, Current margin is {current_margin}. Voting will continue.")
                    print(f"Leader: {winner_id} Votes: {winner_score}")
                    print(f"Runner Up: {runner_up_id} Votes: {runner_up_score}")
            else:
                print("Votes tied no winner. Rollover will occur.")
                print(f"Winner instances: {instances_min_votes}")
            
            if(has_winner):
                print(f"Cooldown will now be in effect for {FF3.VOTE_COOLDOWN} seconds...")
                
                is_voting = False # No more voting allowed
                is_cooldown = True # Begin cooldown period
                voting_start_time = 0
                cooldown_start_time = time.time()
            else:
                # Initiate another round of voting
                voting_start_time = time.time()

        elif(is_cooldown and current_time - cooldown_start_time >= FF3.VOTE_COOLDOWN):
            # Cooldown period over, voting may begin again
            print(f"Cooldown ended. Voting is now in effect for {FF3.FINAL_VOTE_INTERVAL} seconds...")
            voting_start_time = time.time()
            cooldown_start_time = 0

            is_voting = True # Voting allowed again
            is_cooldown = False # Cooldown period over
        else:
            # Voting in progress
            total_votes_cmd1 += votes_cmd1
            total_votes_cmd2 += votes_cmd2
            total_votes_cmd3 += votes_cmd3
            total_spoiled_vote += spoiled_vote
            total_fan_action_vote += votes_fan_action

        # Press q to exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

# Execution begins here
delay_start()
Main()
