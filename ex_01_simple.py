# -*- coding: utf-8 -*-

import bot_manager    

from bot_manager import (send_message, send_photo, send_location, 
    direct_user_to_state, repeatState, set_user_var_value, get_user_var_value)


##############################
# STATES FUNCTIONS
# * each function's name has to start with 'state_X' where X is the name of the state
# * each function is split in two parts: 
#   - if bot_turn: bot's turn to say something
#   - else: the user said something
##############################

def state_0(user, message):
    """
    state 0 is the initial state by default (see bot_manager) and must be defined
    This is where the bot sends the user after s/he starts the bot (or types the command /start)
    """
    bot_turn = message is None
    if bot_turn:
        reply_text = 'You are in the initial state'
        send_message(user, reply_text)
    else:
        if message.text:
            input_text = message.text
            reply_text = "Hi, {} you said: {}".format(user.first_name, input_text)
            send_message(user, reply_text)
        else:
            reply_text = "You sent me something which I cannot handle."
            send_message(user, reply_text)

##############################
# MAIN
##############################

if __name__ == '__main__':    
    bot_manager.startBot()
