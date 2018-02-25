# -*- coding: utf-8 -*-

import bot_manager    

from bot_manager import (send_message, send_photo, send_location, 
    direct_user_to_state, repeatState, set_user_var_value, get_user_var_value)

##############################
# STATES FUNCTIONS
# * each functions' name has to start with 'state_X' where X is the name of the state
# * it is split in two parts if message is None (first time user is sent to this state) and ELSE when it replies to the option within this state
##############################

'''
state 0 is the initial state by default (see bot_manager)
'''
def state_0(user, message):
    bot_turn = message is None
    if bot_turn:
        reply_text = 'You are in the initial state.'
        keyboard = [['State1'], ['State2']]
        send_message(user, reply_text, keyboard)
    else:
        if message.text:
            input_text = message.text
            if input_text == 'State1':
                reply_text = "I'm sending you to state 1."
                send_message(user, reply_text)
                direct_user_to_state(user, '1')
            elif input_text == 'State2':
                reply_text = "I'm sending you to state 2."
                send_message(user, reply_text)
                direct_user_to_state(user, '2')
            else:
                reply_text = "Please use the keyboard below."
                send_message(user, reply_text)
        else:
            reply_text = 'Only text is allowed here.'
            send_message(user, reply_text)


def state_1(user, message):
    bot_turn = message is None
    if bot_turn:
        reply_text = 'You are in state 1'
        keyboard = [['Option1', 'Option2'], ['🔙 Back']]
        send_message(user, reply_text, keyboard)
    else:
        if message.text:
            input_text = message.text
            if input_text == 'Option1':
                reply_text = "Thanks, you selected option 1"
                send_message(user, reply_text)
            elif input_text == 'Option2':
                reply_text = "Thanks, you selected option 2"
                send_message(user, reply_text)
            elif input_text == '🔙 Back':
                reply_text = "I'm sending back to the initial state."
                send_message(user, reply_text)
                direct_user_to_state(user, '0')
            else:
                reply_text = "Please use the keyboard below."
                send_message(user, reply_text)
        else:
            reply_text = 'Only text is allowed here.'
            send_message(user, reply_text)


def state_2(user, message):
    bot_turn = message is None
    if bot_turn:
        reply_text = 'You are in state 2'
        keyboard = [['Option1', 'Option2'], ['🔙 Back']]
        send_message(user, reply_text, keyboard)
    else:
        if message.text:
            input_text = message.text
            if input_text == 'Option1':
                reply_text = "Thanks, you selected option 1"
                send_message(user, reply_text)
            elif input_text == 'Option2':
                reply_text = "Thanks, you selected option 2"
                send_message(user, reply_text)
            elif input_text == '🔙 Back':
                reply_text = "I'm sending back to the initial state."
                send_message(user, reply_text)
                direct_user_to_state(user, '0')
            else:
                reply_text = "Please use the keyboard below."
                send_message(user, reply_text)
        else:
            reply_text = 'Only text is allowed here.'
            send_message(user, reply_text)


##############################
# MAIN
##############################

if __name__ == '__main__':
    bot_manager.startBot()
