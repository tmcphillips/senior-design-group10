# The purpose of this script is to exchange links stored in a dataframe of players and 
# changing it to the particular player's position

import pandas as pd
import requests
from bs4 import BeautifulSoup as bs

# this method will add the position of each player dataframes
# the input is a list containing the first part of each dataframe's name
# this will only work with dataframes that are in the current directory and follow
# the naming scheme used in scrape_nba.py
# @BEGIN add years 
# @IN list of years
# @OUT dataframe with positions added 
def add_pos_year(years):
	# This dictionary will contain the position of links we have already accessed
	players = {}

	# create a list to store the positions we find
	new_pos = []
	# outer loop will open all csv's we have by year
	for i in range(len(years)):
		# path csv by year
		path = years[i] + "_player_stats"
		df = pd.read_csv(path)
		# grab the current column of the dataframes that is storing a link to each player's position
		pos = df["pos"]
		for j in range(len(pos)):
			# extract url 
			url = "http://stats.nba.com" + str(pos[j])
			# this if block is currently untested but should work
			# the purpose of it is to create a dictionary that stores all links we have seen and it's corresponding position
			# this will be useful because the average NBA player plays 3 years so it should theoretically reduce our requests by 3
			if url in players:
				pos.append(players[site])
			else:
				# if we haven't seen a particilar url we open the hyperlink to it and extract the html of the page
				rq = requests.get(url)
				soup = bs(rq.content, 'lxml')
				# grab the position of via soup
				elements = soup.find_all('span', class_="player-summary__player-pos")
				# find elements with player position
				print(elements[0].text)
				# append the position to our new position list
				new_pos.append(elements[0].text)
				rq.close()
		# create a new dataframe from our and then replace the current dataframes position column with the positions we extracted
		df2 = pd.DataFrame({'pos':new_pos})
		df['pos'] = df2['pos']
		
		# finally write a dataframe to our directory organized by year 
		path = years[i] + "_player_stats"
		df.to_csv(path, index=False, header=True)  # saves dataframe with labels
		# @END add pos years

# written by Carl Lundin
# this method will take each years dataframe and concatenate it to one large dataframe 
# this large dataframe contains every stat from every year that stats.nba.com stores
# @BEGIN concatanate positions
# @IN dataframes containing positions by year
# @OUT dataframe with all years combined
def add_pos_total():
		# read all the dataframes we have in file 
		total_dataframes = []
		for i in range(len(years)):
			path = years[i] + "_player_stats"
			df = pd.read_csv(path)
			total_dataframes.append(df)
		# concat our list of dataframes to form one large dataframe
		result = pd.concat(total_dataframes)
		result.to_csv("total_dataframe", index=False, header=True) 
		# @END concatanate positions
		
# @BEGIN swap_positions
def swap_positions():
    # @IN total_dataframe2 
    # @PATH ./total_dataframe2.csv
    # vectorize player positions
    # pos_map = {'G':0, 'F':1, 'F-C':1, 'F-G':1, 'G-F':0, 'C-F':2, 'C':2}
    pos_map = {'G':0, 'F':1, 'F-C':2, 'F-G':3, 'G-F':4, 'C-F':5, 'C':6}
    

    # retrieve unedited data set
    df = pd.read_csv("total_dataframe")

    # map position strings to integers
    df['pos'].replace(pos_map, inplace=True)

    # replace '-' with 0 for now, we may consider predicting a player's 3 point stats using their other data
    df.replace('-',0, inplace=True)
    # df = df[df['3pa'] != '-']

    # drop irrelevant columns, we only care about player's stats and not mins played, games played, player number and name
    df = df.drop(['player', '#', 'gp', 'min'], axis=1)

    df.to_csv("nba_data", index=False, header=True)
    # @OUT vectorized positions
    # @END vectorize
swap_positions()
