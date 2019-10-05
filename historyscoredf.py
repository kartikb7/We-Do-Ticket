# -*- coding: utf-8 -*-
"""
Created on Sat Sep 28 22:51:58 2019

@author: Cyndi Wang
"""
#the final output for historical match data 
import pandas as pd
scoredffinal= pd.DataFrame({'team':[],'time':[],'detail':[],'scores':[],'result':[]})

#Find the pattern of url and create a list for all urls
url_list = []
for i in range(1,5): #2019regularweek4
    url_list.append('https://www.footballdb.com/scores/index.html?lg=NFL&yr=2019&type=reg&wk='+str(i))
for i in range(1,6): #2019preweek5
    url_list.append('https://www.footballdb.com/scores/index.html?lg=NFL&yr=2019&type=pre&wk='+str(i))
for i in range(1,18): #2018 regularweek17
    url_list.append('https://www.footballdb.com/scores/index.html?lg=NFL&yr=2018&type=reg&wk='+str(i))
for i in range(1,6):#2018 preweek5
    url_list.append('https://www.footballdb.com/scores/index.html?lg=NFL&yr=2018&type=pre&wk='+str(i))
#print(url_list)

from urllib.request import urlopen  
from bs4 import BeautifulSoup 


for url in url_list:
    html=urlopen(url)
    soup = BeautifulSoup(html.read(), "lxml") #create a soup object
    teams=soup.find_all('td',attrs={'class':'left'})
    #scrape all team names
    teamlist=[] 
    for i in teams:
         teamlist.append(' '.join(i.a['title'].split(" ")[:-1]))
    scores=soup.find_all('td',attrs={'class':'center'})
    #scrape all team scores
    scorelist=[] 
    for i in scores:
         scorelist.append(i.b.string)  
    #scrape match time
    rawtime=soup.find('h1').string
    time=rawtime.split('-')[0].split(' ')[0]+rawtime.split('-')[1]
    
    team1=[] #split team names into two groups with team1[i] VS team2[i]
    team2=[]
    for i in range(len(teamlist)):
        if (i%2==0):
            team1.append(teamlist[i])
        else:
            team2.append(teamlist[i])
    team1score=[] #split team scores into two groups with team1score[i] VS team2score[i]
    team2score=[]
    for i in range(len(scorelist)):
        if (i%2==0):
            team1score.append(scorelist[i])
        else:
            team2score.append(scorelist[i])
    # create columns for better readability and easy join
    #create a mainteam list 
    mainteam=[] #create a list of all team names for searching and joining purpose
    for i in range(len(team1)):
        mainteam.append(team1[i])
    for j in range(len(team2)):
        mainteam.append(team2[j])
    vsteam=[]
    for i in range(len(team2)):
        vsteam.append(team2[i])
    for j in range(len(team1)):
        vsteam.append(team1[j])
    matchdetail=[]  # create a list with two teams names
    for i in range(len(mainteam)):
        matchdetail.append(mainteam[i]+"  VS  "+vsteam[i])
    mainteamscore=[] 
    for i in range(len(team1score)):
        mainteamscore.append(team1score[i])
    for j in range(len(team2score)):
        mainteamscore.append(team2score[j])
    vsteamscore=[]
    for k in range(len(team2score)):
        vsteamscore.append(team2score[k])
    for m in range(len(team1score)):
        vsteamscore.append(team1score[m])    
    scoredetail=[] # create a list with two teams scores
    for n in range(len(mainteamscore)):
        scoredetail.append(mainteamscore[n]+"  VS  "+vsteamscore[n]) 
    result=[]#create a list with the result of the mainteam we care
    for i in range(len(scoredetail)):
        if int(scoredetail[i].split(' ')[0])>int(scoredetail[i].split(' ')[-1]):
            result.append("Win")
        elif int(scoredetail[i].split(' ')[0])<int(scoredetail[i].split(' ')[-1]):
            result.append("Lose")
        else:
            result.append("Tie")    
    #turn all the info into a dataframe
    import pandas as pd
    df = pd.DataFrame()
    df['team']=mainteam
    df['time']=time
    df['detail']=matchdetail
    df['scores']=scoredetail
    df['result']=result
    
    
    scoredffinal=scoredffinal.append(df)
#reset the row indexes    
scoredffinal=scoredffinal.reset_index(drop=True)   
    



    #write dataframe to csv
    #with open('teamscores.csv', 'a') as f:       
     #    df.to_csv(f, header=False)