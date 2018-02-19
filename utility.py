# -*- coding: utf-8 -*-

def import_url_csv(url_csv):	
	import csv
	import requests
	import io
	r = requests.get(url_csv)			 
	tsv_content = r.content.decode('utf-8')
	reader = csv.DictReader(io.StringIO(tsv_content))
	return [ row for row in reader ]

def import_url_json(url_json):	
	import requests
	r = requests.get(url_json)
	return r.json()

def save_user_variables(user_variables, outputfile):
	import json
	print("Saving user variables")
	with open(outputfile,'w') as f:
		json.dump(user_variables, f, sort_keys=True, indent=4)

def load_user_variables(input_file):
	import json
	print("Loading user variables")
	with open(input_file,'r') as f:
		return json.load(f)
