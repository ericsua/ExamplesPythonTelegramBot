# -*- coding: utf-8 -*-

import telegram
import sys
from time import sleep
import utility
from key import myToken
from telegram.error import NetworkError, TelegramError, Unauthorized
import logging

##############################
# INITIALIZE BOT
##############################

bot = telegram.Bot(myToken)  

##############################
# USER VARIABLES
##############################

user_variables = utility.load_user_variables("./user_vars.txt") # chat_id -> variables

def getVariables(user):
	if user.id not in user_variables.keys():
		user_variables[user.id] = {}
	return user_variables[user.id]

##############################
# STATES MANAGEMENT 
##############################

INIT_STATE = '0'

def getState(user):
	vars = getVariables(user)
	if 'state' not in vars:
		vars['state'] = INIT_STATE
	return vars['state']

def setState(user, new_state):
	vars = getVariables(user)
	vars['state'] = new_state

def repeatState(user, message):
	new_state = getState(user)
	redirectToState(user, new_state, message)

def redirectToState(user, new_state, message):
	methodName = "goToState" + str(new_state)
	method = possibles.get(methodName)
	if not method:
		logging.error("Methos '{}' does not exists!".format(method))
	else:
		setState(user, new_state)
		method(user, message)

##############################
# STATES FUNCTIONS
# * each functions' name has to start with 'goToStateX' where X is the name of the state
# * is split in two parts if message is None (first time user is sent to this state) and ELSE when it replies to the option within this state
##############################

def goToState0(user, message):	
	if message is None:
		reply_text = 'You are in the initial state.'		
		keyboard = [['State1'], ['State2']]
		rm = telegram.ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
		bot.send_message(chat_id=user.id, text=reply_text, reply_markup=rm)
	else:
		if message.text:			
			input_text = message.text
			if input_text=='State1':
				reply_text = "I'm sending you to state 1."
				bot.send_message(chat_id=user.id, text=reply_text)
				redirectToState(user, '1', message=None)				
			elif input_text=='State2':
				reply_text = "I'm sending you to state 2."
				bot.send_message(chat_id=user.id, text=reply_text)
				redirectToState(user, '2', message=None)				
			else:
				reply_text = "Please use the keyboard below."
				bot.send_message(chat_id=user.id, text=reply_text)
		else:
			reply_text = 'Only text is allowed here.'
			bot.send_message(chat_id=user.id, text=reply_text)

def goToState1(user, message):	
	if message is None:
		reply_text = 'You are in state 1'		
		keyboard = [['Option1', 'Option2'],['🔙 Back']]
		rm = telegram.ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
		bot.send_message(chat_id=user.id, text=reply_text, reply_markup=rm)
	else:
		if message.text:
			input_text = message.text
			if input_text=='Option1':
				reply_text = "Thanks, you selected option 1"
				bot.send_message(chat_id=user.id, text=reply_text)
			elif input_text=='Option2':
				reply_text = "Thanks, you selected option 2"
				bot.send_message(chat_id=user.id, text=reply_text)
			elif input_text=='🔙 Back':
				reply_text = "I'm sending back to the initial state."
				bot.send_message(chat_id=user.id, text=reply_text)
				redirectToState(user, INIT_STATE, message=None)				
			else:
				reply_text = "Please use the keyboard below."
				bot.send_message(chat_id=user.id, text=reply_text)
		else:
			reply_text = 'Only text is allowed here.'
			bot.send_message(chat_id=user.id, text=reply_text)


def goToState2(user, message):	
	if message is None:
		reply_text = 'You are in state 2'				
		keyboard = [['Option1', 'Option2'],['🔙 Back']]
		rm = telegram.ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
		bot.send_message(chat_id=user.id, text=reply_text, reply_markup=rm)
	else:
		if message.text:
			input_text = message.text
			if input_text=='Option1':
				reply_text = "Thanks, you selected option 1"
				bot.send_message(chat_id=user.id, text=reply_text)
			elif input_text=='Option2':
				reply_text = "Thanks, you selected option 2"
				bot.send_message(chat_id=user.id, text=reply_text)
			elif input_text=='🔙 Back':
				reply_text = "I'm sending back to the initial state."
				bot.send_message(chat_id=user.id, text=reply_text)
				redirectToState(user, INIT_STATE, message=None)				
			else:
				reply_text = "Please use the keyboard below."
				bot.send_message(chat_id=user.id, text=reply_text)
		else:
			reply_text = 'Only text is allowed here.'
			bot.send_message(chat_id=user.id, text=reply_text)

##############################
# PROCESS EACH UPDATE
##############################

def process_update(update, bot):
	global last_message_id
	if update.message:  		
		# your bot can receive updates without messages
		# but messages include most of the things (text, image, voice, location, ...)
		message = update.message
		user = message.from_user
		if user.id not in user_variables.keys():
			# first time we encounter this user (welcome, record info such as name, last name, ....)
			reply_text = 'Welcome {}!'.format(user.first_name)
			bot.send_message(chat_id=user.id, text=reply_text)
			repeatState(user, message=None)
		else:
			repeatState(user, message)
	else:
		logging.error("User sent an updated which is not a message: " + str(update))	

##############################
# START BOT
##############################

def startBot():	
	updates = bot.get_updates()
	new_update_id = None # we only care about the new incoming updates
	if updates:
		new_update_id = updates[-1].update_id + 1
	while True:	   
		try:
			new_updates = bot.get_updates(offset=new_update_id, timeout=10)	   
			for u in new_updates:
				process_update(u, bot)		   
				new_update_id = u.update_id + 1 
		except telegram.error.TimedOut:
			sleep(1)
		except Unauthorized:  # user has removed or blocked the bot
			update_id += 1

##############################
# MAIN
##############################

possibles = globals().copy()
possibles.update(locals())

if __name__ == '__main__':
	try:
		startBot()
	except KeyboardInterrupt:
		utility.save_user_variables(user_variables, "./user_vars.txt")
		sys.exit(0)
