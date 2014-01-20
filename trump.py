import re
import urllib
import random


class TeamSet(object):

	def __init__(self):
		self.homepage_text = ""
		self.full_members = []
		self.assoc_members = []

	def read_html_content(self):
		uf = urllib.urlopen("http://espncricinfo.com/ci/content/player/index.html")
		self.homepage_text = uf.read()

	def generate_teams(self):
		self.full_members = re.findall(r'<li class="pad"><a href="([\w/\.?=]+)"[\s]*>([\w\s\']+)</a></li>', self.homepage_text)
		self.assoc_members = []
#		self.assoc_members = re.findall(r'<td><a href="([\w/\.?=]+)" class="PopupLinks">([\w\s\']+)</a></td>', self.homepage_text)


class PlayerSet(TeamSet):

	def __init__(self):
		self.player_list = []
		self.player_set = set()
		self.read_html_content()
		self.generate_teams()

	def generate_player_list(self):
		text = ""

		for member in self.full_members + self.assoc_members:
			uf_fm = urllib.urlopen("http://espncricinfo.com" + member[0])
			text += uf_fm.read()

		players = re.findall(r'<td[\sclas="diver]*><a href="([\w/\.?=]+)">([\w\s\']+)</a>[\s]*</td>', text)

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
		for i in xrange(21):
			random.shuffle(self.list_maker.player_list)
			self.player1_cards.append(self.list_maker.player_list.pop())

		random.shuffle(self.player1_cards)

		for i in xrange(21):
			random.shuffle(self.list_maker.player_list)
			self.player2_cards.append(self.list_maker.player_list.pop())

		random.shuffle(self.player2_cards)

	def display(self):
		print ''
		print "PLAYER 1 ==> "
		for card in self.player1_cards:
			print card[1]

		print ''
		print "PLAYER 2 ==> "
		for card in self.player2_cards:
			print card[1]

		
def main():
	g = Game()
	g.display()


if __name__ == '__main__':
	main()