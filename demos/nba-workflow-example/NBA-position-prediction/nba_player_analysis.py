from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
import requests

from sklearn.cluster import MeanShift
import numpy as np

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt



url = "http://stats.nba.com/leaders/"

# @BEGIN main
# @IN url
# @OUT mean_shift_visualization
# @OUT prediction_score
# @OUT scatter_plot
# @OUT pair_wise_plot
# @OUT correlation_heatmap

def main():
	browser = webdriver.Chrome()
	browser.get(url)

	# execute js scripts
	
	# @BEGIN select_year
	# @IN url
	# @IN stats
	# @IN player_page
	# @OUT stats_parsed
	# @OUT years
	# @OUT url_page
	data, years = select_year(browser)
	# @END select_year

	# create a new dataframe by year
	for i in range(len(data)):
		# @BEGIN create_dataframe
		# @IN stats_parsed
		# @IN years @AS years_parsed
		# @OUT dataframes
		create_dataframe(data[i], years[i])
		# @END create_dataframe

	# flatten our 3d list to 1d to create a dataframe containing data from all years
	total_list = []
	for i in range(len(data)):
		for j in range(len(data[i])):
			total_list.append(data[i][j])

	stat_labels = ["pos", "#","player","gp","min","pts", "fgm", "fga", "fg%", "3pm", "3pa", "3p%", "ftm", "fta", "ft%", "oreb", "dreb", "reb", "ast", "stl", "blk", "tov", "eff"]
	total_dataframe = pd.DataFrame(total_list, columns=stat_labels)
	total_dataframe.to_csv("total_dataframe", header=True, index=False)
	browser.quit()

# written by Carl Lundin
# this method takes a list of data and a string containing it's year
# method for creating dataframes seperated by what years the players played
def create_dataframe(data, years):
	# labels for each column of our dataframe
	stat_labels = ["pos", "#","player","gp","min","pts", "fgm", "fga", "fg%", "3pm", "3pa", "3p%", "ftm", "fta", "ft%", "oreb", "dreb", "reb", "ast", "stl", "blk", "tov", "eff"]
	
	df = pd.DataFrame(data, columns=stat_labels)
	path = str(years) + "_player_stats"
	df.to_csv(path, index=False, header=True)  # saves dataframe with labels

def select_year(browser):
	select = Select(WebDriverWait(browser,15).until(lambda browser: browser.find_element_by_name("Season")))
	# Data will be a 3D list that contains [year][player][stats]
	data = []
	years = []
	for option in select.options:
		years.append(option.text)
		select.select_by_visible_text(option.text)
		# append a 2D list that contains [player][stats]
		#@BEGIN parse_page
		# @IN url_page
		# @OUT stats
		data.append(parse_page(browser))
		#@END parse_page
	# returns our data list containg our stats and a list of years we extracted
	return data, years
def parse_page(browser):
	# list of players
	data = []
	select_class = "select.stats-table-pagination__select"
	try:
		# select page view to see all players at once instead of a limited amount
		select = Select(WebDriverWait(browser,2).until(lambda browser: browser.find_element_by_css_selector(select_class)))
		select.select_by_visible_text("All")
	except NoSuchElementException:
		print("limited entries (doesnt exist)")
	except TimeoutException:
		print("limited entries (timeout)")

	innerHTML = browser.execute_script("return document.body.innerHTML")
	
	# create soup and grab all the links of individual players profiles to grab their href link
	soup = bs(innerHTML, 'html.parser')
	# @BEGIN add_links
	# @IN url_page
	# @OUT player_page
	links = add_links(soup)
	# @END add_links

	table = soup.find("table")
	tbody = table.find("tbody")
	rows = tbody.find_all("tr")
	i=0
	for tr in rows:
		columns = tr.find_all("td")
		
		# create a new list within the list of players to store a player's stats
		data.append([])
		# set the first element in the player's stats to be a string representing the link to their personal page
		# this is important because later we will take this string and replace it with the player's position
		# it must be in this position of the 3D list we are creating for the position extraction to properly work
		data[i].append(links[i])
		for td in columns:
			# append the stats of the current player
			data[i].append(td.find(text=True))
		i += 1
	# returns a 2D list in which the first element is the player and the second element is their stats
	return data

def add_links(soup):
	links = []
	for a in soup.find_all('a', href=True):
		player_link = a['href']
		if "/player/" in player_link and "player//" not in player_link:
			links.append(player_link)
	return links

# written by Carl Lundin
# this method will add the position of each player dataframes
# the input is a list containing the first part of each dataframe's name
# this will only work with dataframes that are in the current directory and follow
# the naming scheme used in scrape_nba.py
# @BEGIN add_pos
# @IN years
# @IN dataframes
# @OUT pos_added
def add_pos_year(years):

	# use of this dictionary is UNTESTED
	# DELETE players and it's use if code doesn't work
	# This dictionary will contain the position of links we have already accessed
	# should theoretically speed up code significantly 
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
		path = years[i] + "_player_stats2"
		df.to_csv(path, index=False, header=True)  # saves dataframe with labels
		# @END add_pos

# written by Carl Lundin
# this method will take each years dataframe and concatenate it to one large dataframe 
# this large dataframe contains every stat from every year that stats.nba.com stores
# @BEGIN merge_data
# @IN pos_added
# @OUT dataframe
def add_pos_total():
		# read all the dataframes we have in file 
		total_dataframes = []
		for i in range(len(years)):
			path = years[i] + "_player_stats2"
			df = pd.read_csv(path)
			total_dataframes.append(df)
		# concat our list of dataframes to form one large dataframe
		result = pd.concat(total_dataframes)
		result.to_csv("total_dataframe2", index=False, header=True) 
		# @END merge_data

# extract the years we are using from a years text file I extracted in scrape_NBA.py
years = []
years = [line.rstrip('\n') for line in open('years.txt')]
print(years)
add_pos_year(years)
add_pos_total()


def reducer():
    X = np.array([[-1, -1], [-2, -1], [-3, -2], [1, 1], [2, 1], [3, 2]])
    pca = PCA(n_components=18)

    df = pd.read_csv("clean_nba_data")
    X = df.as_matrix(columns=df.columns[1:23])
    y = df.as_matrix(columns=df.columns[:1]).ravel()
    X_r = pca.fit(X).transform(X)

    print(df.shape)

    print(pca.explained_variance_ratio_)  
    print(pca.singular_values_)  
    # plot_pca(X_r, y)
    return X_r, y

def plot_pca(X, y):
    plt.figure()
    target_names = ['G', 'F', 'F-C', 'F-G', 'G-F', 'C-F', 'C']    
    colors = ['navy', 'turquoise', 'darkorange', 'blue', 'red', 'purple', 'green']
    lw = 2

    for color, i, target_name in zip(colors, [0, 1, 2, 3, 4, 5, 6], target_names):
        plt.scatter(X_r[y == i, 0], X_r[y == i, 1], color=color, alpha=.8, lw=lw,
                    label=target_name)
    plt.legend(loc='best', shadow=False, scatterpoints=1)
    plt.title('PCA of NBA dataset')

    plt.savefig("nba_pca.png")


# @BEGIN vectorize_positions
def vectorize():
    # @IN dataframe 
    # vectorize player positions
    # pos_map = {'G':0, 'F':1, 'F-C':1, 'F-G':1, 'G-F':0, 'C-F':2, 'C':2}
    pos_map = {'G':0, 'F':1, 'F-C':2, 'F-G':3, 'G-F':4, 'C-F':5, 'C':6}
    

    # retrieve unedited data set
    df = pd.read_csv("total_dataframe2")

    # map position strings to integers
    df['pos'].replace(pos_map, inplace=True)

    # replace '-' with 0 for now, we may consider predicting a player's 3 point stats using their other data
    df.replace('-',0, inplace=True)
    # df = df[df['3pa'] != '-']

    # drop irrelevant columns, we only care about player's stats and not mins played, games played, player number and name
    df = df.drop(['player', '#', 'gp', 'min'], axis=1)

    df.to_csv("clean_nba_data", index=False, header=True)
    # @OUT clean_data
    # @END vectorize_positions



def mean_shift():

	df = pd.read_csv("clean_nba_data")
	# X = df.as_matrix(columns=df.columns[1:23])
	# @BEGIN matrix_reducer
	# @IN clean_data
	# @OUT pca_data
	X, _ = reducer()
	# @END matrix_reducers

	# @BEGIN mean_shift
	# @IN pca_data
	# @OUT mean_shift_visualization

	ms = MeanShift(bin_seeding=False)
	ms.fit(X)
	labels = ms.labels_
	cluster_centers = ms.cluster_centers_

	labels_unique = np.unique(labels)
	n_clusters_ = len(labels_unique)

	print("number of estimated clusters : %d" % n_clusters_)

	# plot results here using matplot
	import matplotlib.pyplot as plt
	from itertools import cycle

	plt.figure(1)
	plt.clf()

	colors = cycle('bgrcmykbgrcmykbgrcmykbgrcmyk')
	for k, col in zip(range(n_clusters_), colors):
		my_members = labels == k
		cluster_center = cluster_centers[k]
		plt.plot(X[my_members, 0],X[my_members, 1], col + '.')
		plt.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,
				markeredgecolor='k', markersize=14)
	plt.title('Estimated number of clusters: %d' % n_clusters_)
	plt.savefig("pca_data_mshift.png")
	#@END mean_shift

# @BEGIN svm
# @IN clean_data
# @OUT position_guess
# @OUT prediction_score
def svm_data():
	# retrieve nba data set 
	df = pd.read_csv("clean_nba_data")
	# df.drop(['3pm', '3pa', '3p%'], axis=1)
	# df = df[~df['3pm'].isin(['-'])]
	print(df.head())

	X = df.as_matrix(columns=df.columns[1:23])
	y = df.as_matrix(columns=df.columns[:1]).ravel()
	X_trn, X_tst, y_trn, y_tst = train_test_split(X, y, test_size=0.4)

	# print numpy arrays to make sure the data sets are correct
	# print(X)
	# print(y)

	# create a SVM using the ovr type seperator
	clf = svm.LinearSVC()
	# train SVM with test split data
	clf.fit(X_trn, y_trn)
	# test SVM with the x test data set
	print(clf.predict(X_tst))
	# score with the y test data set
	print(clf.score(X_tst, y_tst))

	# cross validate
	# basically repeats what we just did with the earlier code
	cv_results = cross_validate(clf, X_tst, y_tst, return_train_score=False)
	print(sorted(cv_results.keys()))                         
	print(cv_results['test_score'])   
	# @END svm


df = pd.read_csv("clean_nba_data")
def scatter_nba(df):
    matplotlib.rc('figure', figsize=(10, 5))
    # scatter_matrix(df, alpha=0.2, figsize=(6, 6), diagonal='kde')
    scatter_matrix = scatter_matrix(
        df,
        figsize  = [20, 20],
        marker   = ".",
        s        = 0.6,
        diagonal = "kde"
    )

    for ax in scatter_matrix.ravel():
        ax.set_xlabel(ax.get_xlabel(), fontsize = 20, rotation = 90)
        ax.set_ylabel(ax.get_ylabel(), fontsize = 20, rotation = 0)

    plt.savefig("nba-data-scattermatrix.png")
def pairwise_nba(df):
    
    # Pair-wise Scatter Plots
    cols = ['pts','fgm','fga','fg%','3pm','3pa' ,'3p%','ftm','fta','ft%', 'oreb','dreb','reb','ast','stl','blk','tov','eff']
    pp = sns.pairplot(df[cols], size=1.8, aspect=1.8, diag_kind="kde")

    fig = pp.fig 
    fig.subplots_adjust(top=0.93, wspace=0.3)
    t = fig.suptitle('NBA Attributes Pairwise Plots', fontsize=14)
    fig.savefig("pairwise_nba.png")
def correlation_heat_map_nba(df):

# Correlation Matrix Heatmap
	f, ax = plt.subplots(figsize=(10, 6))
	corr = df.corr()
	hm = sns.heatmap(round(corr,2), annot=True, ax=ax, cmap="coolwarm",fmt='.2f',
					linewidths=.05)
	f.subplots_adjust(top=0.93)
	t= f.suptitle('NBA Attributes Correlation Heatmap', fontsize=14)
	f.savefig("heatmap_nba.png")

# @BEGIN scatter_matrix
# @IN clean_data
# @OUT scatter_plot
scatter_matrix(df)    
# @END scatter_matrix

# @BEGIN pairwise_nba
# @IN clean_data
# @OUT pair_wise_plot
pairwise_nba(df)  
# @END pairwise_nba

# @BEGIN correlation_heatmap_nba
# @IN clean_data
# @OUT correlation_heatmap
correlation_heat_map_nba(df)
# @END correlation_heatmap_nba

df.plot()
plt.show()


vectorize()

mean_shift()

svm_data()

main()
#@END MAIN



