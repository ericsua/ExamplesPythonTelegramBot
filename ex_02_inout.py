# -*- coding: utf-8 -*-

import bot_manager    

from bot_manager import (send_message, send_photo, send_location, 
    direct_user_to_state, repeatState, set_user_var_value, get_user_var_value)

#other imports
import random

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
        reply_text = ('You are in the initial state, please enter one of the following commands:\n'
            '/text, /keyboard, /photo, /location,\n'
            'or send me a photo, a voice recording or a location.')
        send_message(user, reply_text, remove_keyboard=True)
    else:
        if message.text:
            input_text = message.text
            if input_text == '/text':
                reply_text = "This is a simple text"
                send_message(user, reply_text)
            if input_text == '/keyboard':
                keyboard=[['Row1 Button A','Row1 Button B'],['Row2 Button C']]
                reply_text = "This is a text with a keyboard"
                send_message(user, reply_text, keyboard)
            elif input_text == '/photo':
                # sending an image
                url_photo = 'http://placehold.it/400x300&text=test_image'
                send_photo(user, url_photo)
            elif input_text == '/location':                
                random_lat = 46.0 + random.random()
                random_lon = 11.0 + random.random()
                # sending a random location                
                send_location(user, random_lat, random_lon)
            else:
                reply_text = "You sent me a text I cannot handle."
                send_message(user, reply_text)
        elif message.photo:
            # user has sent a photo
            reply_text = "Nice photo!"
            send_message(user, reply_text)
        elif message.voice:
            # user has sent an audio    
            reply_text = "Nice voice!"
            send_message(user, reply_text)
        elif message.location:
            # user has sent a location
            reply_text = "Nice location!"
            send_message(user, reply_text)
        else:
            reply_text = "You sent me something which I cannot handle."
            send_message(user, reply_text)

'''
This is a newly defined state.
Any state can be a function whose name starts with 'state_'
To redirect a user to this state use the function direct_user_to_state(user,'X') 
which will invoke the function state_X(user) 
'''
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
                direct_user_to_state(user, INITIAL_STATE)
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
