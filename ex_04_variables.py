# -*- coding: utf-8 -*-

import bot_manager    

from bot_manager import (send_message, send_photo, send_location, 
    direct_user_to_state, repeatState, set_user_var_value, get_user_var_value)

#other imports
from utility import import_url_csv

##############################
# downloading RICETTE
# it's a list when each element is a dictionary with the following keys:
# 'Title', 'Ingredient', 'Category', 'Preparation', 'RecipeID'
##############################
RICETTE = import_url_csv(
    'http://dati.trentino.it/dataset/6f515d47-d3ce-42d0-bbc5-38941c2d36fd/'
    'resource/02b7405b-4d74-474f-b521-e133de52cc2c/download/ricette.csv')

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
        reply_text = ('Ciao, sono il ricettario Trentino.\n'
            'Puoi cercare le ricette per titolo o per ingredienti,' 
            'o andare alle tue ricette preferite')
        keyboard = [['Titolo','Ingredienti'], ['Preferiti']]
        send_message(user, reply_text, keyboard)
    else:
        if message.text:
            input_text = message.text
            if input_text == 'Titolo':
                direct_user_to_state(user, 'titolo')
            elif input_text == 'Ingredienti':
                direct_user_to_state(user, 'ingredienti')
            elif input_text == 'Preferiti':
                direct_user_to_state(user, 'preferiti')
            else:
                reply_text = "Input non riconosciuto, usa la tastiera."
                send_message(user, reply_text)
        else:
            reply_text = 'Input non riconosciuto, usa la tastiera.'
            send_message(user, reply_text)

def state_titolo(user, message):
    search_ricette(user, message, search_type='titoli')

def state_ingredienti(user, message):
    search_ricette(user, message, search_type='ingredienti')

def search_ricette(user, message, search_type):
    bot_turn = message is None
    if bot_turn:
        reply_text = 'Dammi un testo da cercare nei {} delle ricette.'.format(search_type)
        keyboard = [['🔙 Indietro']]
        send_message(user, reply_text, keyboard)
    else:
        if message.text:
            input_text = message.text
            if input_text == '🔙 Indietro':
                direct_user_to_state(user, '0')
            elif input_text.startswith('/ricetta'):
                ricetta_id = input_text.split('/ricetta')[1]
                send_ricetta(user, ricetta_id)
            elif input_text.startswith('/aggiungiRicettaInPreferiti'):            
                ricetta_id = input_text.split('/aggiungiRicettaInPreferiti')[1]
                aggiungi_ricetta_in_preferiti(user, ricetta_id)
            elif input_text.startswith('/rimuoviRicettaDaPreferiti'):            
                ricetta_id = input_text.split('/rimuoviRicettaDaPreferiti')[1]
                rimuovi_ricetta_da_preferiti(user, ricetta_id)
            else:
                search_field = 'Title' if search_type=='titoli' else 'Ingredient'
                ricette_trovate = [r for r in RICETTE if input_text.lower() in r[search_field].lower()]
                if ricette_trovate:
                    ricette_trovate_str = '\n'.join(['• /ricetta{} {}'.format(r['RecipeID'], r['Title']) for r in ricette_trovate])
                    reply_text = "Ricette trovate:\n\n{}\n\nPremi su una ricetta per visualizzarla.".format(ricette_trovate_str)
                else:
                    reply_text = "Nessuna ricetta trovata, riprova."
                send_message(user, reply_text)
        else:
            reply_text = 'Input non riconosciuto, usa la tastiera.'
            send_message(user, reply_text)

def state_preferiti(user, message):
    bot_turn = message is None
    if bot_turn:
        ricette_preferite = get_user_var_value(user, 'RICETTE_PREFERITE')
        if ricette_preferite:
            ricette_trovate = []
            for r_id in ricette_preferite:
                r = get_ricetta(r_id)
                ricette_trovate.append('• /ricetta{} {}'.format(r['RecipeID'], r['Title']))             
            ricette_trovate_str = '\n'.join(ricette_trovate)
            reply_text = "Ricette preferite:\n\n{}\n\nPremi su una ricetta per visualizzarla.".format(ricette_trovate_str)
            keyboard = [['🗑 Reset preferiti'],['🔙 Indietro']]
        else:
            reply_text = 'Nessuna ricetta preferita trovata'
            keyboard = [['🔙 Indietro']]
        send_message(user, reply_text, keyboard)
    else:
        if message.text:
            input_text = message.text
            if input_text == '🔙 Indietro':
                direct_user_to_state(user, '0')
            elif input_text == '🗑 Reset preferiti':
                set_user_var_value(user, 'RICETTE_PREFERITE', [])
                reply_text = "Ricette preferite eliminate."
                send_message(user, reply_text)
                direct_user_to_state(user, '0')
            elif input_text.startswith('/aggiungiRicettaInPreferiti'):            
                ricetta_id = input_text.split('/aggiungiRicettaInPreferiti')[1]
                aggiungi_ricetta_in_preferiti(user, ricetta_id)
                repeatState(user)
            elif input_text.startswith('/rimuoviRicettaDaPreferiti'):            
                ricetta_id = input_text.split('/rimuoviRicettaDaPreferiti')[1]
                rimuovi_ricetta_da_preferiti(user, ricetta_id)
                repeatState(user)
            elif input_text.startswith('/ricetta'):
                ricetta_id = input_text.split('/ricetta')[1]
                send_ricetta(user, ricetta_id)
            else:
                reply_text = 'Input non riconosciuto, usa la tastiera.'
                send_message(user, reply_text)
        else:
            reply_text = 'Input non riconosciuto, usa la tastiera.'
            send_message(user, reply_text)

def get_ricetta(ricetta_id):
    match = [r for r in RICETTE if r['RecipeID']==ricetta_id]
    if not match:
        return None
    return match[0]

def send_ricetta(user, ricetta_id):
    r = get_ricetta(ricetta_id)
    if r is None:
        reply_text = "Nessuna ricetta trovata."
    else:
        ricette_preferite = get_user_var_value(user, 'RICETTE_PREFERITE')
        aggiungi_rimuovi = '/rimuoviRicettaDaPreferiti' if r['RecipeID'] in ricette_preferite else '/aggiungiRicettaInPreferiti'
        reply_text = (
            "*Titolo*: {}\n"
            "*Ingredienti*: {}\n"
            "*Preparatione*: {}\n\n"
            "{}{}"            
        ).format(r['Title'],r['Ingredient'],r['Preparation'],aggiungi_rimuovi,r['RecipeID'])
    send_message(user, reply_text, markdown=True)
    
def aggiungi_ricetta_in_preferiti(user, ricetta_id):
    r = get_ricetta(ricetta_id)
    if r is None:
        reply_text = "Nessuna ricetta trovata."
    else:
        ricette_preferite = get_user_var_value(user, 'RICETTE_PREFERITE')
        if not ricette_preferite:
            ricette_preferite = []
            set_user_var_value(user, 'RICETTE_PREFERITE', ricette_preferite)
        ricette_preferite.append(ricetta_id)
        ricette_preferite = sorted(set(ricette_preferite))
        reply_text = ('Ricetta aggiunta in preferiti ({}).'.format(r['Title']))
    send_message(user, reply_text, markdown=True)

def rimuovi_ricetta_da_preferiti(user, ricetta_id):
    r = get_ricetta(ricetta_id)
    if r is None:
        reply_text = "Nessuna ricetta trovata."
    else:
        ricette_preferite = get_user_var_value(user, 'RICETTE_PREFERITE')
        if not ricette_preferite:
            ricette_preferite = []
            set_user_var_value(user, 'RICETTE_PREFERITE', ricette_preferite)
        ricette_preferite.remove(ricetta_id)
        ricette_preferite = sorted(set(ricette_preferite))
        reply_text = ('Ricetta rimossa da preferiti ({}).'.format(r['Title']))
    send_message(user, reply_text, markdown=True)

##############################
# MAIN
##############################

if __name__ == '__main__':
    bot_manager.startBot()
