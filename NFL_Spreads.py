from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import pandas as pd

from openpyxl import Workbook
import re
import csv
import lxml
import requests

def scrape(url):
    response = requests.get(url)
    df_list = []
    score_stats = []
    drive_counter = 0
    OT_counter = 0

    page = requests.get(url)

    soup = BeautifulSoup(page.content, "html.parser")
    results = soup.find(id="gamepackage-drives-wrap")
    if results != None:

        drives = results.find_all("div", class_="accordion-header")
        for drive in drives:
            drive_counter +=1


        score = soup.find(id="gamepackage-matchup-wrap")
        df_list.append(score.find_all("span", class_="abbrev"))
        df_list.append(score.find_all("div", class_="score icon-font-after"))
        df_list.append(score.find_all("div", class_="score icon-font-before"))

        df_list.append(score.find_all("div", class_="record"))
        for item in df_list:
            for other_item in item:
                score_stats.append(other_item.text.strip())
        score_stats.append(drive_counter)

        return (score_stats)
    else:
        return 0

def make_df(start, end):
    games = []
    headers = ['Away_Team', 'Home_team', 'Away_Score', 'Home_Score',
               'Away_Record', 'Home_Record', 'Drives']
    for i in range(start, end):
        game = scrape("https://www.espn.com/nfl/playbyplay/_/gameId/" + str(i))
        if game != 0:
            games.append(game)
    df = pd.DataFrame(games, columns=headers)
    return df

def add_stats(df):
    df["Home_Games"] = 0
    df["Away_Games"] = 0
    for i in range(len(df["Away_Record"])):
        loc_1 = df['Away_Record'][i].find('-')
        loc_2 = df['Away_Record'][i].find(',')
        W = int(df['Away_Record'][i][:loc_1])
        L = df['Away_Record'][i][loc_1+1:loc_2]
        if len(L) > 2:
            loc_3 = df['Home_Record'][i].find('-')
            L = int(L[:loc_3])+int(L[loc_3+1:])
        else:
            L = int(L)
        df.at[i, 'Away_Games'] = W+L
    for i in range(len(df["Home_Record"])):

        loc_1 = df['Home_Record'][i].find('-')
        loc_2 = df['Home_Record'][i].find(',')
        W = int(df['Home_Record'][i][:loc_1])
        L = df['Home_Record'][i][loc_1+1:loc_2]
        if len(L) > 2:
            loc_3 = df['Home_Record'][i].find('-')
            L = int(L[:loc_3])+int(L[loc_3+1:])
        else:
            L = int(L)
        df.at[i, 'Home_Games'] = W+L




    df = df.drop(columns=['Away_Record', 'Home_Record'])
    #print(df)
    return df
def drive_num (df):
    df['NET_P/D'] = (df['Away_Score']-df['Home_Score'])/df['Drives']
    return df

def add_preseason(df):
    df1 = pd.read_csv('odds_2020.txt')
    df2 = df.merge(df1, left_on='Away_Team', right_on='Team',suffixes=('', '_Away'))
    df2 = df2.merge(df1, left_on='Home_team', right_on='Team',suffixes=('', '_Home'))
    df2.drop(df2.columns[[0, 12,16]], axis = 1, inplace = True)
    #df2['Away_Preseason_Rating'] = -8.48050449e-02*

    return df2
def model(df):
    import numpy as np
    import matplotlib.pyplot as plt
    import pandas as pd
    df_week1 = df[df['Away_Games'] <= 15]

    X = df_week1[["Proj_Wins", 'Proj_Wins_Home']]
    Y = df_week1['NET_P/D']
    print(X)
    from sklearn.linear_model import LinearRegression
    from sklearn.preprocessing import PolynomialFeatures
    lin_reg = LinearRegression()
    lin_reg.fit(X, Y)
    print('intercept:', lin_reg.intercept_)
    print('slope:', lin_reg.coef_)
    r_sq = lin_reg.score(X, Y)
    print(r_sq)














if __name__ == '__main__':
    df = pd.read_csv('p3.csv')
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    model(add_preseason(drive_num(add_stats(df))))







