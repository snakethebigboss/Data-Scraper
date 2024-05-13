from bs4 import BeautifulSoup
import pandas as pd
import requests
import time

all_teams = []

html = requests.get("https://fbref.com/en/comps/9/Premier-League-Stats").text #Get the HTML of the page
soup = BeautifulSoup(html, "lxml") #Parse the HTML and look for specific elements

table = soup.find_all('table', class_= 'stats_table') [0] #Find the table with the class 'stats_table'

links = table.find_all('a') #Find all the links in the table
links = [l.get('href') for l in links] #Get the href attribute of the links
links = [l for l in links if l.startswith('/en/squads')] #Filter the links to only get the ones that start with '/en/squads'

team_urls = [f"https://fbref.com{l}" for l in links] #Add the base URL to the links to point to each team's page

for team_url in team_urls:
    team_name = team_url.split('/')[-1].replace("-Stats", "") #Get the team name from the URL
    data = requests.get(team_url).text #Get the HTML of the team's page
    soup = BeautifulSoup(data, "lxml") #Parse the HTML
    stats = soup.find_all('table', class_= 'stats_table')[0] #Find the table with the class 'stats_table'

    if stats and stats.columns: stats.columns = stats.columns.droplevel() #Drop the first level of the columns

    team_data = pd.read_html(str(stats))[0] #Read the table into a DataFrame
    team_data['Team'] = team_name #Add a column with the team's name
    all_teams.append(team_data) #Append the DataFrame to the list
    time.sleep(5)

stat_df = pd.concat(all_teams) #Concatenate all the DataFrames into one
stat_df.to_csv("stats.csv") #Save the DataFrame to a CSV file

print(stat_df) #Print the DataFrame to the console

