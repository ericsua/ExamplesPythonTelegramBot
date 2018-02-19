# -*- coding: utf-8 -*-

import telegram
import sys
from time import sleep
import utility
from key import myToken

user_variables = utility.load_user_variables("./user_vars.txt") # chat_id -> variables
ricette = utility.import_url_csv('http://dati.trentino.it/dataset/6f515d47-d3ce-42d0-bbc5-38941c2d36fd/resource/02b7405b-4d74-474f-b521-e133de52cc2c/download/ricette.csv')

def switch_keyboard(chat_id):
	if chat_id in user_variables.keys():
		user_variables[chat_id] = not user_variables[chat_id]
	else:
		user_variables[chat_id] = False
	#save_user_variables()
	return user_variables[chat_id]

def process_update(u, bot):
	global last_message_id
	if u.message:  # your bot can receive updates without messages
		msg = u.message
		user = msg.from_user
		if msg.text: # your bot can receive not only text but ...
			input_text = msg.text
			if input_text == '/image':
				url = 'https://www.marconirovereto.it/images/logoITTMarconi.jpg'
				bot.send_photo(chat_id=user.id, photo=url)
			elif input_text.isdigit():
				number = int(input_text)
				reply_text = 'Ti invio la ricetta in posizione {}'.format(number)
				bot.send_message(chat_id=user.id, text=reply_text)
				ricetta = ricette[number]
				reply_text = '*Titolo*: {}'.format(ricetta['Title'])				
				bot.send_message(chat_id=user.id, text=reply_text, parse_mode=telegram.ParseMode.MARKDOWN)
			elif input_text == '/keyboard':
				if switch_keyboard(user.id):
					reply_text = 'Ti elimino la keyboard'
					rm = telegram.ReplyKeyboardRemove()
					bot.send_message(chat_id=user.id, text=reply_text, reply_markup=rm)
					#bot.edit_message_text(chat_id=user.id, text=reply_text, message_id=last_message_id, reply_markup=rm)
				else:
					reply_text = 'Ti invio una keyboard di prova'
					keyboard = [['bottone1'],['bottone2'],['bottone3']]
					rm = telegram.ReplyKeyboardMarkup(keyboard, resize_keyboard=False, one_time_keyboard=False)
					bot.send_message(chat_id=user.id, text=reply_text, reply_markup=rm)
			else:
				reply_text = 'Ciao {}, hai detto {}'.format(user.first_name, msg.text)
				bot.send_message(chat_id=user.id, text=reply_text)
			#last_message_id = msg.message_id	

def startBot():
	bot = telegram.Bot(myToken)  
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

if __name__ == '__main__':
	try:
		startBot()
	except KeyboardInterrupt:
		utility.save_user_variables(user_variables, "./user_vars.txt")
		sys.exit(0)
