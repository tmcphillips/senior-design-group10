import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import Select, WebDriverWait


# @BEGIN main
# @IN nba_url @AS input_url
# @OUT nba_data @AS nba_data @URI file:../extracted_nba_position_data/nba_data
# @OUT nba_data_year @URI file:../extracted_nba_position_data/{year}_player_stats
def main():
    # open a chrome instance at the root nba webpage
    nba_url = "http://stats.nba.com/leaders/"
    browser = webdriver.Chrome()
    browser.get(nba_url)

    # @BEGIN scrape_player_data
    # @IN raw_player_data
    # @OUT raw_data
    # @OUT nba_url
    data, years = scrape_player_data(browser)
    # @END scrape_player_data

    # create a new dataframe by year
    for i in range(len(data)):
        # @BEGIN create_dataframe
        # @IN raw_data
        # @OUT nba_data_no_position
        # @OUT nba_data_year
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

    swap_positions()

    browser.quit()

# this method takes a list of data and a string containing it's year
# method for creating dataframes seperated by what years the players played
def create_dataframe(data, years):
    # labels for each column of our dataframe
    stat_labels = ["pos", "#","player","gp","min","pts", "fgm", "fga", "fg%", "3pm", "3pa", "3p%", "ftm", "fta", "ft%", "oreb", "dreb", "reb", "ast", "stl", "blk", "tov", "eff"]
        
    df = pd.DataFrame(data, columns=stat_labels)
    path = str(years) + "_player_stats"
    df.to_csv(path, index=False, header=True)  # saves dataframe with labels

def scrape_player_data(browser):
    select = Select(WebDriverWait(browser,15).until(lambda browser: browser.find_element_by_name("Season")))
    # Data will be a 3D list that contains [year][player][stats]
    data = []
    years = []
    for option in select.options:
        years.append(option.text)
        select.select_by_visible_text(option.text)
        # append a 2D list that contains [player][stats]
        #@BEGIN parse_page
        # @IN nba_url
        # @OUT players_page
        data.append(parse_page(browser))
        #@END parse_page
    # returns our data list containg our stats and a list of years we extracted
    return data, years

def parse_page(browser):
    # list of players
    players = []

    try:
        # view all players 
        select = Select(WebDriverWait(browser,2).until(lambda browser: browser.find_element_by_css_selector("select.stats-table-pagination__select")))
        select.select_by_visible_text("All")
    except NoSuchElementException:
        print("No Element Existed")
    except TimeoutException:
        print("Time Out Exception")

    # data of current page
    inner_html = browser.execute_script("return document.body.innerHTML")
    # grab player page hrefs
    soup = bs(inner_html, 'html.parser')

    # @BEGIN extract_player_page
    # @IN players_page
    # @OUT raw_player_data
    player_pages = extract_player_page(soup)
    # @END extract_player_page

    table = soup.find("table")
    tbody = table.find("tbody")
    i=0

    for tr in tbody.find_all("tr"):
        columns = tr.find_all("td")
        
        # nested list to contain a player's stats
        players.append([])
        players[i].append(player_pages[i])

        for td in columns:
            # append the stats of the current player
            players[i].append(td.find(text=True))

        i += 1
    # returns a 2D list in which the first element is the player and the second element is their stats
    return players

def extract_player_page(soup):
    player_pages = []
    for a in soup.find_all('a', href=True):
        player_link = a['href']
        if "/player/" in player_link and "player//" not in player_link:
            player_pages.append(player_link)
    return player_pages

# @BEGIN swap_positions
def swap_positions():
    # @IN nba_data_no_position
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
    # @OUT nba_data
    # @END swap_positions
# @END main

if __name__ == "__main__":
    main()
