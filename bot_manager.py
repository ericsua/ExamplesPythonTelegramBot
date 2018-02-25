# -*- coding: utf-8 -*-

import telegram
import utility
from key import myToken
import logging
from time import sleep
import __main__

# set up logging to standard output, put:
info_level = logging.INFO  # logging.DEBUG
logging.basicConfig(level=info_level,
                    format='%(asctime)s - %(levelname)s - %(message)s')

##############################
# INITIALIZE BOT
##############################

if myToken == None:
    import sys
    logging.error('You must set your bot token in key.py')
    sys.exit()

bot = telegram.Bot(myToken)

##############################
# USER VARIABLES
##############################

USERS_VARS = utility.load_users_vars("./user_vars.txt")  # chat_id -> variables

def get_USERS_VARS(user):
    user_id_str = str(user.id)
    if user_id_str not in USERS_VARS.keys():
        return None        
    return USERS_VARS[user_id_str]

def get_user_var_value(user, var_name):
    user_vars = get_USERS_VARS(user)
    if var_name in user_vars:
        return user_vars[var_name]
    return None

def set_user_var_value(user, var_name, var_value):
    user_id_str = str(user.id)
    if user_id_str not in USERS_VARS.keys():
        USERS_VARS[user_id_str] = {}
    USERS_VARS[user_id_str][var_name] = var_value

def set_users_info(user):
    set_user_var_value(user, 'FIRST NAME', user.first_name)
    set_user_var_value(user, 'LAST NAME', user.last_name)
    set_user_var_value(user, 'USERNAME', user.username)
    set_user_var_value(user, 'LANGUAGE', user.language_code)

##############################
# STATES MANAGEMENT
##############################

INITIAL_STATE = '0'

def repeatState(user, message=None):
    user_state = get_user_var_value(user, 'STATE')
    direct_user_to_state(user, user_state, message)


def direct_user_to_state(user, new_state, message=None):
    methodName = "state_{}".format(new_state)
    #method = possibles.get(methodName)
    method = getattr(__main__, methodName)
    if not method:
        logging.error("Methos '{}' does not exists!".format(method))
    else:
        set_user_var_value(user, 'STATE', new_state)
        method(user, message)

##############################
# send functions
##############################

'''
Send a text message with or without a keyboard
'''
def send_message(user, reply_text, keyboard=None, resize_keyboard=True, 
        one_time_keyboard=False, remove_keyboard=False, markdown=False):
    rm = None
    parse_mode = telegram.ParseMode.MARKDOWN if markdown else None
    if keyboard:
        rm = telegram.ReplyKeyboardMarkup(
            keyboard, resize_keyboard=resize_keyboard, 
            one_time_keyboard=one_time_keyboard)
    if remove_keyboard:
        rm = telegram.ReplyKeyboardRemove()
    try:        
        bot.send_message(user.id, text=reply_text, reply_markup=rm, parse_mode=parse_mode)
    except telegram.error.Unauthorized:  # user has removed or blocked the bot
        logging.info('User {} has removed or blocked the bot'.format(chat_id))

'''
Send a photo
note: the photo argument can be either a file_id, an URL or a file from disk, e.g, open(filename, 'rb')
'''
def send_photo(user, photo, keyboard=None, resize_keyboard=True, 
        one_time_keyboard=False, remove_keyboard=False):
    rm = None
    if keyboard:
        rm = telegram.ReplyKeyboardMarkup(
            keyboard, resize_keyboard=resize_keyboard, 
            one_time_keyboard=one_time_keyboard)
    if remove_keyboard:
        rm = telegram.ReplyKeyboardRemove()
    try:        
        bot.send_photo(user.id, photo=photo, reply_markup=rm)
    except Unauthorized:  # user has removed or blocked the bot
        logging.info('User {} has removed or blocked the bot'.format(chat_id))

'''
Send a photo
note: the photo argument can be either a file_id, an URL or a file from disk, e.g, open(filename, 'rb')
'''
def send_location(user, latitude, longitude, keyboard=None, resize_keyboard=True, 
        one_time_keyboard=False, remove_keyboard=False):
    rm = None
    if keyboard:
        rm = telegram.ReplyKeyboardMarkup(
            keyboard, resize_keyboard=resize_keyboard, 
            one_time_keyboard=one_time_keyboard)
    if remove_keyboard:
        rm = telegram.ReplyKeyboardRemove()
    try:        
        bot.send_location(user.id, latitude, longitude, reply_markup=rm)
    except Unauthorized:  # user has removed or blocked the bot
        logging.info('User {} has removed or blocked the bot'.format(chat_id))

##############################
# PROCESS EACH UPDATE
##############################

def process_update(update):
    if update.message:
        # your bot can receive updates without messages
        # but messages include most of the things (text, image, voice, location, ...)
        message = update.message
        user = message.from_user
        if get_USERS_VARS(user) is None or message.text=='/start':
            # first time we encounter this user (welcome, record info such as name, last name, ....)
            reply_text = 'Welcome {}!'.format(user.first_name)
            send_message(user, reply_text, remove_keyboard=True)
            set_users_info(user)
            direct_user_to_state(user, INITIAL_STATE, message=None)            
        else:
            repeatState(user, message)
    else:
        logging.info("User sent an updated which is not a message: " + str(update))

##############################
# START BOT
##############################

EXIT = False

def startBot():    
    last_update_id = None
    while True:
        if EXIT:
            utility.save_users_vars(USERS_VARS, "./user_vars.txt")
            return
        try:
            updates = bot.get_updates()
        except telegram.error.TimedOut:
            sleep(0.5)
            continue
        if updates:
            last_update_id = updates[-1].update_id + 1
        break
    logging.info('BOT READY!')
    while True:
        if EXIT:
            utility.save_users_vars(USERS_VARS, "./user_vars.txt")
            return
        try:
            new_updates = bot.get_updates(offset=last_update_id, timeout=10)
            for u in new_updates:
                process_update(u)
                last_update_id = u.update_id + 1
        except telegram.error.TimedOut:
            sleep(0.5)

############################################################
# Save user variables when ctrl-c is hit and exit gracefully
############################################################

import signal

def signal_handler(signal, frame):
    global EXIT
    logging.info("Preparing to exit...")
    EXIT = True

signal.signal(signal.SIGINT, signal_handler)

