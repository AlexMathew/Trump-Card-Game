import urllib
import random
import os
import datetime
import sys
from bs4 import BeautifulSoup as Soup
import itertools
import lxml

def clear_old_cache(cache_dir):
	"""
	This method takes the directory path as its argument and clears out all the files in that directory.
	"""

	for item in os.listdir(cache_dir):
		os.remove(str(cache_dir + item))


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

		cache_dir = "C:/TrumpCards_cache/"
		filename = str(datetime.datetime.now())[:10] + "_homepage"
		complete_path = cache_dir + filename + ".txt"
		
		if os.path.exists(complete_path):
			with open(complete_path, 'r') as f:
				self.homepage_text = f.read()
				f.close()
		else:
			print '\nEXTRACTING DATA..\n(The time taken depends on the speed of your Internet connection)\n'
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
		This method parse the HTML of the page to extract the links to the various team pages.
		"""

		soup = Soup(self.homepage_text, "lxml")
		li_set = soup.findAll('li')
		self.full_members = [(li_set[i+1].a.get('href'), li_set[i+1].text) 
							 for i, link in enumerate(li_set) if link.text == '|'][:10]



def key_fn(s):
	return s[1]


class PlayerSet(TeamSet):

	def __init__(self):
		self.player_list = []
		self.player_set = set()
		self.read_html_content()
		self.generate_teams()

	def generate_player_list(self):
		"""
		This method reads the HTML content of all the team pages, and uses HTML parsing
		to extract links to each individual players page.
		"""

		text = ""

		cache_dir = "C:/TrumpCards_cache/"
		filename = str(datetime.datetime.now())[:10] + "_"
		complete_path = cache_dir + filename
		existence_test_file_path = complete_path + ("India.txt")

		players = []
		
		if os.path.exists(existence_test_file_path):
			for filename in os.listdir(cache_dir):
				if "homepage" in filename:
					continue
				team = cache_dir + filename
				team_text = open(team).read()
				soup = Soup(team_text, "lxml")
				td_list = soup.findAll('td')
				players.extend([("http://espncricinfo.com" + link.a.get('href'), link.text) 
								for link in soup.find(id = "rectPlyr_Playerlisttest").findAll('td')])
				
		else:
			for member in self.full_members:
				team_page_url = "http://espncricinfo.com" + member[0]
				try:
					uf = urllib.urlopen(team_page_url)
				except Exception:
					sys.exit("\nPlease turn on your Internet connection.")
				team_text = uf.read()
				soup = Soup(team_text)
				players.extend([("http://espncricinfo.com" + link.a.get('href'), link.text) 
								for link in soup.find(id = "rectPlyr_Playerlisttest").findAll('td')])
				team_path = complete_path + member[1] + ".txt"
				cache_text(team_path, team_text)

		self.player_set = set(players)

		self.player_list = list(sorted(self.player_set, key = key_fn))

		print 'TOTAL NUMBER OF PLAYERS : ', len(self.player_list)

		return self.player_list


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
