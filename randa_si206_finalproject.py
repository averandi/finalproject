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

#~~~~~~~~~~~~TWITTER FUNCTION TO GET AND CACHE DATA BASED ON SERACH TERM
def get_tweets(search_actor):
	unique_identifier = "twitter_{}".format(search_actor)

	if unique_identifier in CACHE_DICTION: 
		#print('using cached data for', search_tweets)
		twitter_results = CACHE_DICTION[unique_identifier] 
	else:
		#print('getting data from internet for', search_tweets)
		twitter_results = api.search_users(search_actor) 
		CACHE_DICTION[unique_identifier] = twitter_results
		cached_data = open(CACHE_FNAME,'w') 
		cached_data.write(json.dumps(CACHE_DICTION))
		cached_data.close()

	#response = CACHE_DICTION['search_actor']
	for x in twitter_results:
		return x
	
	#return twitter_results




#~~~~~~~~~~~~TWITTER FUNCTION TO GET AND CACHE DATA ABOUT A TWITTER USER
def get_user_tweets(user_timeline_tweets):
	#full_url = api.user_timeline(q = search_tweets)
	unique_identifier = "twitter_{}".format(user_timeline_tweets)
	
	if unique_identifier in CACHE_DICTION: 
		twitter_results = CACHE_DICTION[unique_identifier] 

	else:
		twitter_results = api.user_timeline(user_timeline_tweets) 
		CACHE_DICTION[unique_identifier] = twitter_results
		f = open(CACHE_FNAME,'w') 
		f.write(json.dumps(CACHE_DICTION))
		f.close()

	#return twitter_results
	for x in twitter_results:
		return x



#~~~~~~~~~~~~CLASS FOR TWITTER SEARCH DATA
	#~~~~~~~~~~~~TEXT OF TWEET, TWEET ID, USER POSTING IT, SEARCH TERM USED, NUM OF FAVORITES, NUM OF RETWEETS
class Tweet():
	def __init__(self, dict_for_tweets):
		#x = get_tweets()
		#self.search_term = dict_for_tweets
		self.text = dict_for_tweets['status']['text']
		self.tweet_id = dict_for_tweets['status']['id']
		self.user = dict_for_tweets['screen_name']
		self.faves = dict_for_tweets['status']['favorite_count']
		self.retweets = dict_for_tweets['status']['retweet_count']
		self.mentions = dict_for_tweets['status']['entities']['user_mentions']
		#print(type(dict_for_tweets))
	def __str__(self):
		return '\n Text: {} \n Tweet ID: {} \n User: {} \n Favorites: {} \n Retweets: {} \n'.format(self.text, self.tweet_id, self.user, self.faves, self.retweets)
	# def _tweet_text(self):
	# 	return self.text
	def _user_(self):
		return self.user
	def _mentions_(self):
		if len(self.mentions) != 0:
			return 'Mentioned Users {}'.format(self.mentions)
		else:
			return 'Mentioned Users: NONE'
	def _user_mentions_(self):
		if len(self.mentions) != 0:
			return 'Mentioned Users {}'.format(self.mentions)

#reg ex `` (\@)[0-9a-zA-Z_]+ ``


# ava = get_tweets('randi_pandi')
# # print(ava)
# ad = []
# bb = Tweet(ava)

# print(bb._mentions_())
# print(bb)


# for x in bb:
# 	xx = Tweet(x)
# 	b = xx._tweet_text()
# 	print(b)
#~~~~~~~~~~~~CLASS FOR TWITTER USER
	#~~~~~~~~~~~~USER ID, SCREENNAME, NUM OF FAVORITES THE USER HAS MADE, MAYBE NUMBER OF FOLLOWERS

class User():
	def __init__(self, dict_for_user):
		self.user_id = dict_for_user['user']['id_str']
		self.screen_name = dict_for_user['user']['screen_name']
		self.num_faves= dict_for_user['user']['favourites_count']
		self.num_followers = dict_for_user['user']['followers_count']
	def __str__(self):
		return '\n User ID: {} \n Screen Name: {} \n Favorites Made: {} \n Number of Followers: {} \n'.format(self.user_id, self.screen_name, self.num_faves, self.num_followers)
# avauser = get_user_tweets('randi_pandi')
# #print(avauser)
# ava = User(avauser)
# print(ava)

#~~~~~~~~~~~~GRABBING DATA
#~~~~~~~~~~~~PICK 3 MOVIE TITLE SEARCH TERMS FOR OMDB, PUT THOSE STRINGS IN A LIST
#~~~~~~~~~~~~MAKE A REQUEST TO OMDB FOR EACH OF THOSE 3 SEARCH TERMS USING MY FUNCTION, ACCUMUILATE DICTIONARIES
#~~~~~~~~~~~~I GET FROM DOING THIS, EACH REPRESENTING ONE MOVIE, INTO A LIST

movie_titles_to_search_for = ['Twilight', 'Get Out', 'The Great Gatsby']

#~~~~~~~~~~~~ this puts the dictionaries of each movie into 1 list
# list_of_dicts = []
# for x in movie_titles_to_search_for:
# 	m_dicts = get_from_omdb(x)
# 	list_of_dicts.append(m_dicts)
#^^^^^^^^^refer to for list comp^^^^^^^^^
list_of_dicts = [get_from_omdb(x) for x in movie_titles_to_search_for]
#print(type(list_of_dicts))
#~~~~~~~~~~~~this is to organize through the dictionaries with the Movie class, and put them in 1 list, list_of_instcs
#~~~~~~~~~~~~run through dict using Movie class
print('')
print('~~~~~~~~~~~~MOVIE INFORMATION~~~~~~~~~~~~')
print('')
list_of_instcs = []
for x in list_of_dicts:
	d = Movie(x)
	p = d.__int_for_num_lang___()
	list_of_instcs.append(d)
	list_of_instcs.append(p)
	print(d)
	print(p)
	print('')
#list_of_instcs = [(print(Movie(x))) for x in list_of_dicts]
#print(list_of_instcs)

#~~~~~~~~~~~~list of names of directors to look up on Twitter
dir_name_list = []
for x in list_of_dicts:
	# dir_name_list = []
	d = Movie(x)
	p = d._call_dir_name_()
	dir_name_list.append(p)
# print(dir_name_list)
# print(type(dir_name_list))





#~~~~~~~~~~~~get director of each movie to search them on Twitter
print('')
print('~~~~~~~~~~~~SEARCH RESULTS FOR DIRECTORS ON TWITTER~~~~~~~~~~~~')
print('')

dirs_for_twitter = [get_tweets(x) for x in dir_name_list]
def organizedtwitterinfo(listofusers):
#print(dirs_for_twitter)
	for x in listofusers:
		d = Tweet(x)
		p = d._mentions_()
		print (d,p)
	#print(p)
x = organizedtwitterinfo(dirs_for_twitter)

print('')
#~~~~~~~~~~~~Twitter profile info for each Director



print('~~~~~~~~~~~~USER INFO FOR DIRECTOR (AND MENTIONED USERS, IF ANY)~~~~~~~~~~~~')
print('')
#print(type(tt))

# listy = []
# for x in tt:
# 	listy.append(x)
# 	print(listy)
# print(type(tt))
#~~~~~~~~~~~~THIS SEARCHES THE DIRECTOR AND GETS THEIR PROFILE
#~~~~~~~~~~~~this function takes the director's name, gets their twitter screenname, and any will provide
#~~~~~~~~~~~~the screenname of anyone mentioned in their tweet provided from the Tweet class
#~~~~~~~~~~~~this function passes the handles to the User class to provide information

def gettinguserinfo(name):
	for x in name:
		inst = Tweet(x)
		handle = inst._user_()
		makestr = str(handle)
		twitter = get_user_tweets(makestr)
		#print(twitter)
		userclass = User(twitter)
		print(userclass)
		if len(inst.mentions) != 0:
			#print(inst._mentions_)
			handment = inst.mentions()
			makestr = str(handment)
			tform = get_user_tweets(makestr)
			menuc = User(tform)
			print(menuc)
datatwituser = gettinguserinfo(dirs_for_twitter)

# avauser = get_user_tweets('randi_pandi')
# #print(avauser)
# ava = User(avauser)
# print(ava)


#~~~~~~~~~~~~~~~~~~~~~~~~FOR DATABASES~~~~~~~~~~~~~~~~~~~~~~~~

conn = sqlite3.connect('proj_final.db')
cur = conn.cursor()

# #~~~~~~~~~~~~MOVIES TABLE
# #~~~~~~~~~~~~ID (primary key) (NOTE title is dangerous for a primary key, 2 movies could have the same title!)
# #~~~~~~~~~~~~Title of the movie
# #~~~~~~~~~~~~Director of the movie 
# #~~~~~~~~~~~~Number of languages the movie has
# #~~~~~~~~~~~~IMDB rating of the movie
# #~~~~~~~~~~~~The top billed (first in the list) actor in the movie







# #movies db
drop_movies_table = ("DROP TABLE IF EXISTS Movies")

#table_spec = "CREATE TABLE IF NOT EXISTS "
create_movies_table = 'CREATE TABLE Movies (title TEXT, director TEXT, imdbRating PRIMARY KEY, actor_names TEXT, num_lang TEXT, year_released TEXT)'

cur.execute(drop_movies_table)
cur.execute(create_movies_table)

# #~~~~~~~~~~~~TWEETS TABLE
# #~~~~~~~~~~~~Tweet text
# #~~~~~~~~~~~~Tweet ID (primary key)
# #~~~~~~~~~~~~The user who posted the tweet (represented by a reference to the users table)
# #~~~~~~~~~~~~The movie search this tweet came from (represented by a reference to the movies table)
# #~~~~~~~~~~~~Number favorites
# #~~~~~~~~~~~~Number retweets

#tweets db
drop_tweets_table = ("DROP TABLE IF EXISTS Tweets")

#table_spec = "CREATE TABLE IF NOT EXISTS "
create_tweets_table = 'CREATE TABLE Tweets (text TEXT, tweet_id PRIMARY KEY, user TEXT, favorites INTEGER, retweets INTEGER, director_searched TEXT)'

cur.execute(drop_tweets_table)
cur.execute(create_tweets_table)

# #~~~~~~~~~~~~USERS TABLE
# #~~~~~~~~~~~~User ID (primary key)
# #~~~~~~~~~~~~User screen name
# #~~~~~~~~~~~~Number of favorites that user has ever made

#users db
drop_users_table = ("DROP TABLE IF EXISTS Users")

# table_spec = "CREATE TABLE IF NOT EXISTS "
create_users_table = 'CREATE TABLE Users (user_id PRIMARY KEY, screen_name TEXT, favorites INTEGER, num_followers INTEGER)'

cur.execute(drop_users_table)
cur.execute(create_users_table)

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ LOADING INTO DATABASE ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

movieslist = []
tweetslist = []
userslist = []

# load_tweets = 'INSERT INTO Tweets VALUES (?,?,?,?,?,?)'
# for userdata in tweets:
# 	cur.execute(load_tweets, userdata)

# load_users = 'INSERT OR IGNORE INTO Users VALUES(?,?,?,?)'
# for userdata in umich_tweets:
# 	user_id = userdata['user']['id_str']
# 	screen_name = userdata['user']['screen_name']
# 	num_favs = userdata['user']['favourites_count']
# 	description = userdata['user']['description']

# 	comp = (user_id, screen_name, num_favs, description)
# 	cur.execute(load_users, comp)

# user_list = []
# for userdata in umich_tweets:
# 	x = userdata['entities']['user_mentions']
# 	for y in range(len(x)):
# 		user_list.append(x[y]['screen_name'])

# for userdata in user_list:
# 	load = 'INSERT OR IGNORE INTO Users VALUES (?,?,?,?)'
# 	val = get_user_tweets(userdata)
# 	for y in val:
# 		user_id = y['user']['id_str']
# 		screen_name = y['user']['screen_name']
# 		num_favs = y['user']['favourites_count']
# 		description = y['user']['description']

# 		comp = (user_id, screen_name, num_favs, description)
# 		cur.execute(load_users, comp)

#conn.commit()

























conn.close()

#~~~~~~~~~~~~~~~~~~~~~~~~UNIT TESTS~~~~~~~~~~~~~~~~~~~~~~~~
print('~~~~~~~~~~~~UNIT TESTS~~~~~~~~~~~~')
print('')
class MyUnitTest(unittest.TestCase):
	# def test_1_movie_instance(self):
	# 	self.assertIsInstance(list_of_instcs, Movie) #good
	# def test_2_movie_return_(self):
	# 	self.assertTrue(type(list_of_instcs) == type({})) #good
	# def test_3_twitter_return_(self):
	# 	self.assertTrue(type(x) == type({Movie(x))) 
	# def test_4_user_return(self):
	# 	self.assertTrue(type(trying) == type({})) 
	def test_5_caching(self):
		filename = open("SI206_final_project_cache.json", 'r').read()
		self.assertTrue('Director' in filename)








unittest.main(verbosity=2)






