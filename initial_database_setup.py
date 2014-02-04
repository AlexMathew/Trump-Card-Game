from bs4 import BeautifulSoup as Soup
import urllib
import psycopg2
import trump


def modify_stats_types(q):
	for item in q:
		if '*' in item:
			yield int(item[:-1])
		elif '.' in item:
			yield float(item)
		elif '/' in item:
			yield str(item)
		elif item == '':
			yield 0
		else:
			yield int(item)


def extract_stats(soup):
	nws = soup.findAll(nowrap = "nowrap")

	stats = [tuple(nws[15*j + i].text 
			 if nws[15*j + i].text != u'-' else u'0' 
			 for i in xrange(1, 15)) + 

			 tuple(nws[105 + 14*j + i].text 
			 if nws[105 + 14*j + i].text != u'-' else u'0' 
			 for i in xrange(1, 14)) 

			 for j in xrange(1, 5)]

	stats = [tuple(modify_stats_types(item)) for item in stats]

	return stats


def update_database():
	conn = psycopg2.connect("dbname = stat_database user = postgres password = postgres")
	c = conn.cursor()

	stats_types = """(matches_played_bat , innings_batted , not_outs , 
					  runs_scored , highest_inns_score , batting_average , balls_faced , 
					  batting_strike_rate , hundreds_scored , fifties_scored , boundary_fours , 
					  boundary_sixes , catches_taken , stumpings_made , matches_played_bowl , 
					  innings_bowled_in , balls_bowled , runs_conceded , wickets_taken , 
					  best_innings_bowling , best_match_bowling , bowling_average , economy_rate , 
					  bowling_strike_rate , four_wkts_in_an_inns , five_wkts_in_an_inns , 
					  ten_wkts_in_a_match )"""

	command_create_test = """CREATE TABLE test_stats (id serial PRIMARY KEY, matches_played_bat integer, innings_batted integer, 
							not_outs integer, runs_scored integer, highest_inns_score integer, batting_average real, 
							balls_faced integer, batting_strike_rate real, hundreds_scored integer, fifties_scored integer, 
							boundary_fours integer, boundary_sixes integer, catches_taken integer, stumpings_made integer, 
							matches_played_bowl integer, innings_bowled_in integer, balls_bowled integer, runs_conceded integer, 
							wickets_taken integer, best_innings_bowling varchar, best_match_bowling varchar, bowling_average real, 
							economy_rate real, bowling_strike_rate real, four_wkts_in_an_inns integer, 
							five_wkts_in_an_inns integer, ten_wkts_in_a_match integer)"""

	command_create_odi = """CREATE TABLE odi_stats (id serial PRIMARY KEY, matches_played_bat integer, innings_batted integer, 
							not_outs integer, runs_scored integer, highest_inns_score integer, batting_average real, 
							balls_faced integer, batting_strike_rate real, hundreds_scored integer, fifties_scored integer, 
							boundary_fours integer, boundary_sixes integer, catches_taken integer, stumpings_made integer, 
							matches_played_bowl integer, innings_bowled_in integer, balls_bowled integer, runs_conceded integer, 
							wickets_taken integer, best_innings_bowling varchar, best_match_bowling varchar, bowling_average real, 
							economy_rate real, bowling_strike_rate real, four_wkts_in_an_inns integer, 
							five_wkts_in_an_inns integer, ten_wkts_in_a_match integer)"""

	command_create_t20i = """CREATE TABLE t20i_stats (id serial PRIMARY KEY, matches_played_bat integer, innings_batted integer, 
							not_outs integer, runs_scored integer, highest_inns_score integer, batting_average real, 
							balls_faced integer, batting_strike_rate real, hundreds_scored integer, fifties_scored integer, 
							boundary_fours integer, boundary_sixes integer, catches_taken integer, stumpings_made integer, 
							matches_played_bowl integer, innings_bowled_in integer, balls_bowled integer, runs_conceded integer, 
							wickets_taken integer, best_innings_bowling varchar, best_match_bowling varchar, bowling_average real, 
							economy_rate real, bowling_strike_rate real, four_wkts_in_an_inns integer, 
							five_wkts_in_an_inns integer, ten_wkts_in_a_match integer)"""

	command_create_fc = """CREATE TABLE fc_stats (id serial PRIMARY KEY, matches_played_bat integer, innings_batted integer, 
							not_outs integer, runs_scored integer, highest_inns_score integer, batting_average real, 
							balls_faced integer, batting_strike_rate real, hundreds_scored integer, fifties_scored integer, 
							boundary_fours integer, boundary_sixes integer, catches_taken integer, stumpings_made integer, 
							matches_played_bowl integer, innings_bowled_in integer, balls_bowled integer, runs_conceded integer, 
							wickets_taken integer, best_innings_bowling varchar, best_match_bowling varchar, bowling_average real, 
							economy_rate real, bowling_strike_rate real, four_wkts_in_an_inns integer, 
							five_wkts_in_an_inns integer, ten_wkts_in_a_match integer)"""

	placeholder = '(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'

	command_insert_base = "INSERT INTO base_table (name, img_link) VALUES (%s, %s)"
	command_insert_test = "INSERT INTO test_stats " + stats_types + " VALUES " + placeholder
	command_insert_odi = "INSERT INTO odi_stats " + stats_types + " VALUES " + placeholder 
	command_insert_t20i = "INSERT INTO t20i_stats " + stats_types + " VALUES " + placeholder 
	command_insert_fc = "INSERT INTO fc_stats " + stats_types + " VALUES " + placeholder 		

	c.execute("CREATE TABLE base_table (id serial PRIMARY KEY, name varchar, img_link varchar)")
	c.execute(command_create_test)
	c.execute(command_create_odi)
	c.execute(command_create_t20i)
	c.execute(command_create_fc)

	player_set = trump.PlayerSet()
	player_list = player_set.generate_player_list()

	for i, player in enumerate(player_list[150:250]):
		print 'Currently updating stats of player ' + str(150 + i + 1) + " -- " + str(player[1]) + "..." 

		playerHtml = urllib.urlopen(player[0])
		soup = Soup(playerHtml)
	
		name = str(soup.title.text.split(' |')[0])
		img_link = "http://espncricinfo.com" + soup.findAll('img')[1].get('src')

		try:
			stats = extract_stats(soup)		

		except:
			continue

		c.execute(command_insert_base, (name, img_link))
		c.execute(command_insert_test, stats[0])
		c.execute(command_insert_odi, stats[1])
		c.execute(command_insert_t20i, stats[2])
		c.execute(command_insert_fc, stats[3])

	conn.commit()

	c.close()
	conn.close()

	return


def main():
	try:
		update_database()
	except:
		print "ERROR ENCOUNTERED !!\n"
		print "> Make sure you have trump.py in the same directory as this database setup program."
		print "> Make sure you have the stat_database DB set up in PostgreSQL."
		print "> Make sure that this is the first time you are running this program. If it isn't, reset the DB in PostgreSQL."
		print "> Make sure that you are connected to the Internet."

	return


if __name__ == '__main__':
	main()