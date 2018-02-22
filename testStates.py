# -*- coding: utf-8 -*-

import requests
import telegram
import sys
from time import sleep
import utility
from key import myToken
from telegram.error import NetworkError, TelegramError, Unauthorized

import logging

# set up logging to standard output, put:
info_level = logging.INFO #logging.DEBUG
logging.basicConfig(level=info_level,
                    format='%(asctime)s - %(levelname)s - %(message)s')

##############################
# INITIALIZE BOT
##############################

bot = telegram.Bot(myToken)  

##############################
# USER VARIABLES
##############################

user_variables = utility.load_user_variables("./user_vars.txt") # chat_id -> variables

def userIsNew(user):
	user_id_str = str(user.id)
	return user_id_str not in user_variables.keys()

def getVariables(user):
	user_id_str = str(user.id)
	if user_id_str not in user_variables.keys():
		user_variables[user_id_str] = {}
	return user_variables[user_id_str]

##############################
# STATES MANAGEMENT 
##############################

INITIAL_STATE = '0'

def getState(user):
	vars = getVariables(user)
	if 'state' not in vars:
		vars['state'] = INITIAL_STATE
	return vars['state']

def setState(user, new_state):
	vars = getVariables(user)
	vars['state'] = new_state

def repeatState(user, message):
	new_state = getState(user)
	goToState(user, new_state, message)

def goToState(user, new_state, message):
	methodName = "goToState{}".format(new_state)
	method = possibles.get(methodName)
	if not method:
		logging.error("Methos '{}' does not exists!".format(method))
	else:
		setState(user, new_state)
		method(user, message)

##############################
# send functions
##############################

def send_message(chat_id, reply_text, keyboard=None, resize_keyboard=True, one_time_keyboard=False):
	rm = None
	if keyboard:
		rm = telegram.ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
	bot.send_message(chat_id=chat_id, text=reply_text, reply_markup=rm)
	#else:
	#	bot.send_message(chat_id=chat_id, text=reply_text)

##############################
# STATES FUNCTIONS
# * each functions' name has to start with 'goToStateX' where X is the name of the state
# * is split in two parts if message is None (first time user is sent to this state) and ELSE when it replies to the option within this state
##############################

def goToState0(user, message):	
	bot_turn = message is None
	if bot_turn:
		reply_text = 'You are in the initial state.'		
		keyboard = [['State1'], ['State2']]
		send_message(user.id, reply_text, keyboard)
	else:
		if message.text:			
			input_text = message.text
			if input_text=='State1':
				reply_text = "I'm sending you to state 1."
				send_message(user.id, reply_text)
				goToState(user, '1', message=None)				
			elif input_text=='State2':
				reply_text = "I'm sending you to state 2."
				send_message(user.id, reply_text)
				goToState(user, '2', message=None)				
			else:
				reply_text = "Please use the keyboard below."
				send_message(user.id, reply_text)
		else:
			reply_text = 'Only text is allowed here.'
			send_message(user.id, reply_text)

def goToState1(user, message):	
	bot_turn = message is None
	if bot_turn:
		reply_text = 'You are in state 1'		
		keyboard = [['Option1', 'Option2'],['🔙 Back']]		
		send_message(user.id, reply_text, keyboard)
	else:
		if message.text:
			input_text = message.text
			if input_text=='Option1':
				reply_text = "Thanks, you selected option 1"
				send_message(user.id, reply_text)
			elif input_text=='Option2':
				reply_text = "Thanks, you selected option 2"
				send_message(user.id, reply_text)
			elif input_text=='🔙 Back':
				reply_text = "I'm sending back to the initial state."
				send_message(user.id, reply_text)
				goToState(user, INITIAL_STATE, message=None)				
			else:
				reply_text = "Please use the keyboard below."
				send_message(user.id, reply_text)
		else:
			reply_text = 'Only text is allowed here.'
			send_message(user.id, reply_text)


def goToState2(user, message):	
	bot_turn = message is None
	if bot_turn:
		reply_text = 'You are in state 2'				
		keyboard = [['Option1', 'Option2'],['🔙 Back']]
		rm = telegram.ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
		send_message(user.id, reply_text, keyboard)
	else:
		if message.text:
			input_text = message.text
			if input_text=='Option1':
				reply_text = "Thanks, you selected option 1"
				send_message(user.id, reply_text)
			elif input_text=='Option2':
				reply_text = "Thanks, you selected option 2"
				send_message(user.id, reply_text)
			elif input_text=='🔙 Back':
				reply_text = "I'm sending back to the initial state."
				send_message(user.id, reply_text)
				goToState(user, INITIAL_STATE, message=None)				
			else:
				reply_text = "Please use the keyboard below."
				send_message(user.id, reply_text)
		else:
			reply_text = 'Only text is allowed here.'
			send_message(user.id, reply_text)

##############################
# PROCESS EACH UPDATE
##############################

def process_update(update):
	if update.message:  		
		# your bot can receive updates without messages
		# but messages include most of the things (text, image, voice, location, ...)
		message = update.message
		user = message.from_user
		if userIsNew(user):
			# first time we encounter this user (welcome, record info such as name, last name, ....)
			reply_text = 'Welcome {}!'.format(user.first_name)
			send_message(user.id, reply_text)
			goToState(user, INITIAL_STATE, message=None)
		else:
			repeatState(user, message)
	else:
		logging.error("User sent an updated which is not a message: " + str(update))	

##############################
# START BOT
##############################

EXIT = False

def startBot():	
	new_update_id = None 
	while True:	   
		if EXIT:
			utility.save_user_variables(user_variables, "./user_vars.txt")
			return
		try:
			updates = bot.get_updates()
		except telegram.error.TimedOut:
			sleep(0.5)	
			continue				
		if updates:
			new_update_id = updates[-1].update_id + 1
		break
	logging.info('BOT READY!')
	while True:	   
		if EXIT:
			utility.save_user_variables(user_variables, "./user_vars.txt")
			return
		try:
			new_updates = bot.get_updates(offset=new_update_id, timeout=5)	   
			for u in new_updates:
				process_update(u)		   
				new_update_id = u.update_id + 1 
		except telegram.error.TimedOut:
			sleep(0.5)
		except requests.RequestException:
			logging.warning("A RequestException has occured")
			return
		except Unauthorized:  # user has removed or blocked the bot
			update_id += 1


############################################################
# Collect all above function to parametrize state functions
############################################################

possibles = globals().copy()
possibles.update(locals())

############################################################
# Save user variables when ctrl-c is hit and exit gracefully
############################################################

import signal

def signal_handler(signal, frame):	
	global EXIT	
	logging.info("Preparing to exit...")
	EXIT = True

##############################
# MAIN
##############################

if __name__ == '__main__':	
	signal.signal(signal.SIGINT, signal_handler)
	startBot()
