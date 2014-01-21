"""
TO DO :
	Try using requests instead of urllib

"""


import re
import urllib
import random
import os
import datetime
import sys


def clear_old_cache(cache_dir):
	"""
	This method takes the directory path as its argument and clears out all the files in that directory.
	"""

	root, dirs, files = os.walk(cache_dir).next()
	for filename in files:
		os.remove(os.path.join(root, filename))


def cache_text(complete_path, text):
	"""
	This method takes the file path and the text content as its arguments and stores this content in the file.
	"""

	cache_dir, filename = os.path.split(complete_path)
	if(not os.path.exists(cache_dir)):
		os.mkdir(cache_dir)
	with open(complete_path, 'w') as f:
		f.write(text)
		f.close()
	return


class TeamSet(object):

	def __init__(self):
		self.homepage_text = ""
		self.full_members = []

	def read_html_content(self):
		"""
		This method reads the HTML content from the Players list homepage on Cricinfo.
		"""

		cache_dir = "C:/TrumpCards_cache"
		filename = str(datetime.datetime.now())[:10] + "_homepage"
		complete_path = cache_dir + "/" + filename + ".txt"
		
		if os.path.exists(complete_path):
			with open(complete_path, 'r') as f:
				self.homepage_text = f.read()
				f.close()
		else:
			print '\nEXTRACTING DATA..\n(The time taken depends on the speed of your Internet connection..\n'
			homepage_url = "http://espncricinfo.com/ci/content/player/index.html"
			try:
				uf = urllib.urlopen(homepage_url)
			except Exception:
				sys.exit("\nPlease turn on your Internet connection to continue.")
			self.homepage_text = uf.read()
			clear_old_cache(cache_dir)
			cache_text(complete_path, self.homepage_text)

	def generate_teams(self):
		"""
		This method uses regular expressions to extract the links to the various team pages.
		"""

		team_generator_re = r'<li class="pad"><a href="([\w/\.?=]+)"[\s]*>([\w\s\']+)</a></li>'
		self.full_members = re.findall(team_generator_re, self.homepage_text)


class PlayerSet(TeamSet):

	def __init__(self):
		self.player_list = []
		self.player_set = set()
		self.read_html_content()
		self.generate_teams()

	def generate_player_list(self):
		"""
		This method reads the HTML content of all the team pages, and uses regular expressions 
		to extract links to each individual players page.
		"""

		text = ""

		cache_dir = "C:/TrumpCards_cache"
		filename = str(datetime.datetime.now())[:10] + "_teams"
		complete_path = cache_dir + "/" + filename + ".txt"
		
		if os.path.exists(complete_path):
			with open(complete_path) as f:
				text = f.read()
				f.close()
		else:
			for member in self.full_members:
				team_page_url = "http://espncricinfo.com" + member[0]
				try:
					uf_fm = urllib.urlopen(team_page_url)
				except Exception:
					sys.exit("\nPlease turn on your Internet connection.")
				text += uf_fm.read()
				cache_text(complete_path, text)

		player_generator_re =r'<td[\sclas="diver]*><a href="([\w/\.?=]+)">([\w\s\']+)</a>[\s]*</td>' 
		players = re.findall(player_generator_re, text)

		self.player_set = set(players)

		self.player_list = list(self.player_set)

"""
class Player(object):

	def __init__(self, player_link):
		# Initialize value holders for all stats

	def read_stats(self):
		# Read the data from the link and store the stats
"""

class Game(object):

	def __init__(self):
		self.player1_cards = []
		self.player2_cards = []
		self.list_maker = PlayerSet()
		self.list_maker.generate_player_list()
		self.generate_card_sets()

	def generate_card_sets(self):
		"""
		From the Player list obtained from the generate_player_list() method of the PlayerSet class,
		randomly select players for the card sets for the two card holders.
		"""

		for i in xrange(21):
			random.shuffle(self.list_maker.player_list)
			self.player1_cards.append(self.list_maker.player_list.pop())

		random.shuffle(self.player1_cards)

		for i in xrange(21):
			random.shuffle(self.list_maker.player_list)
			self.player2_cards.append(self.list_maker.player_list.pop())

		random.shuffle(self.player2_cards)

	def display(self):
		"""
		Displays the card sets of the two card holders.
		"""

		print "\nCARD HOLDER 1 ==> "
		for card in self.player1_cards:
			print card[1]

		print "\nCARD HOLDER 2 ==> "
		for card in self.player2_cards:
			print card[1]

		
def main():
	g = Game()
	g.display()


if __name__ == '__main__':
	main()
	