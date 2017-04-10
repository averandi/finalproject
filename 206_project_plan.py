## Your name: Ava Randa
## The option you've chosen: 2

# Put import statements you expect to need here!

import unittest
import json
import requests
import tweepy
import twitter_info # Requires you to have a twitter_info file in this directory
import re

#######
CACHE_FNAME = "SI206_finalproject_cache.json"
try:
	cache_data = open(CACHE_FNAME, 'r')
	cache_contents = cache_data.read()
	CACHE_DICTION = json.loads(cache_contents)
	cache_data.close()
except:
	CACHE_DICTION = {}

#######
class Movie():
		def __init__(self, movie_name, director, actors, year, ):
			self.title = movie_name
			self.director_name = director
			self.actor_names = actors
			self.year_released = year
	
		def __str__(self):
			return "Title: {} \nDirector: {} \nStarring: {} ".format(self.title, self.director_name)
		def nums_of(self):
			print "Year Released: " + str(self.year_released)



mov_ins_1 = Movie("The Hunger Games")

class MyUnitTest(unittest.TestCase):
	def test_1_movie_instance(self):
		self.assertIsInstance(mov_ins_1, Movie) #good
	def test_2_movie_return_list(self):
		self.assertTrue(type(mov_ins_1) == type({})) #good
	def test_3_movie_instance(self):
		self.assertTrue(type("The Hunger Games") == type("a"))
	def test_4_movie_instance(self):
		self.assertTrue(type(self.title) == type("a"))
	def test_5_movie_instance(self):
		self.assertTrue(type(self.director_name) == type("a"))
	def test_6_movie_instance(self):
		self.assertTrue(type(self.actor_names) == type("a"))
	def test_7_movie_instance(self):
		self.assertTrue(type(self.year_released) == type("a"))
	def test_8_caching(self):
		filename = open("SI206_finalproject_cache.json", 'r').read()
		self.assertTrue('Director' in filename)



# Write your test cases here.
class MyUnitTest(unittest.TestCase):


unittest.main(verbosity=2)
## Remember to invoke all your tests...