## ~~~~~~~~~~~~Your name: Ava Randa
## ~~~~~~~~~~~~The option you've chosen: Option 2

# Put import statements you expect to need here!

import unittest
import json
import requests
import tweepy
import twitter_info # Requires you to have a twitter_info file in this directory
import re
import sqlite3
#######
## Tweepy authentication setup
## Fill these in in the twitter_info.py file
consumer_key = twitter_info.consumer_key
consumer_secret = twitter_info.consumer_secret
access_token = twitter_info.access_token
access_token_secret = twitter_info.access_token_secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#~~~~~~~~~~~~Set up to be able grab stuff from twitter with your authentication using Tweepy methods, and return it in a JSON format 
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
#######
CACHE_FNAME = "SI206_final_project_cache.json"
try:
	cache_data = open(CACHE_FNAME, 'r')
	cache_contents = cache_data.read()
	CACHE_DICTION = json.loads(cache_contents)
	cache_data.close()
except:
	CACHE_DICTION = {}

####

#~~~~~~~~~~~~PROJECT REMINDERS~~~~~~~~~~~~#
#~~~~~~~~~~~~You must process the data you gather and store and extract from the database in at least 4 of the following ways:
#~~~1~~~~~~~~~Set / dictionary comprehensions, and/or list comprehensions
#~~~~2~~~~~~~~Using new containers from the collections library
#~~~~~3~~~~~~~Using iteration methods from the itertools library
#~~~~~~4~~~~~~Accumulation in dictionaries and processing of the data (e.g. counts, lists associated with keys… like umsi_titles, but of course something different)
#~~~~~~~5~~~~~Using generator expressions and/or generator functions (recall HW6)
#~~~~~~~~6~~~~Sorting with a key parameter
#~~~~~~~~~7~~~Using the builtins: map or filter (which each return iterators) in order to filter a sequence or transform a sequence of data
#~~~~~~~~~~8~~Using regular expressions
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

#######
#~~~~~~~~~~~~OMDBAPI FUNCTION
def get_from_omdb(search_title):
	omdb_d = {}
	omdb_d['t'] = search_title
	omdb_base = 'http://www.omdbapi.com/?'
	full_url = requests.get(omdb_base, params = omdb_d)

	if full_url in CACHE_DICTION:
		CACHE_DICTION[search_title] = full_url
	else:
		#response = requests.get(omdb_base, params = omdb_d)
		full_url = json.loads(full_url.text)
		CACHE_DICTION[search_title] = full_url
		#resp = diction
		cache_data = open(CACHE_FNAME, 'w')
		cache_data.write(json.dumps(CACHE_DICTION))
		cache_data.close()
	return full_url
#~~~~~~~~~~~~CLASS MOVIE
	#~~~~~~~~~~~~CONSTRUCTOR ACCEPTS A DICTIONARY THAT REPRESENTS A MOVIE
	#~~~~~~~~~~~~3 INSTANCE VARIABLES, AT LEAST 2 METHODS BESIDES CONTRUCTOR
	#~~~~~~~~~~~~DATA TO SAVE ABOUT MOVIE
		#~~~~~~~~~~~~TITLE, DIRECTOR, IMDB RATING, LIST OF ACTORS, NUMBER OF LANGUAGES THE MOVIE IS IN, ANYTHING ELSE
class Movie():
	def __init__(self, construct_dict):
		self.title = construct_dict['Title']
		self.director_name = construct_dict['Director']
		self.imdb_rating = construct_dict['imdbRating']
		self.actor_names = construct_dict['Actors']
		self.num_lang = construct_dict['Language']
		self.year_released = construct_dict['Year']
		#print(type(construct_dict))
	
	def __str__(self):
		return "\n Title: {} \n Director: {} \n Rating: {} \n Starring: {} \n Languages: {} \n Year Released: {} ".format(self.title, self.director_name, self.imdb_rating, self.actor_names, self.num_lang, self.year_released)
		#def nums_of(self):
			#print "Year Released: " + str(self.year_released)
	def __int_for_num_lang___(self):
		#return ('Number of Languages: ' + len(self.year_released.split(',')))
		#langs = self.num_lang.split(',')
		#return(' Number of Languages: ' + str(len(langs)))
		return (' Number of Languages: ' + str(len(self.num_lang.split(','))))
	def _call_dir_name_(self):
		return self.director_name

# x = get_from_omdb('twilight')
# d = Movie(x)
# print(d)
# print(d.__int_for_num_lang___())
# print('')
