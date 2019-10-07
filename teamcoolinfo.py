# -*- coding: utf-8 -*-
"""
Created on Thu Oct  3 17:11:48 2019

@author: Cyndi Wang
"""

def performanceInfo(team_name):
  
    import historyscoredf as s

    import pandas as pd
    pd.set_option('display.max_columns', None)

    selectteaminfo=s.scoredffinal[s.scoredffinal["team"]==team_name]
    totalmatches=len(selectteaminfo)
    totalwins=len(selectteaminfo[selectteaminfo["result"]=="Win"])
    totalloses=len(selectteaminfo[selectteaminfo["result"]=="Lose"])
    totalties=len(selectteaminfo[selectteaminfo["result"]=="Tie"])


    print("\n\nSome Cool information")
    print("**************************")
    print("\nIn year 2018 and year 2019, the performance statistics of "+team_name+" is as follows: \n")
    print("For "+str(totalmatches)+" matches "+team_name+ " was in:")
    print("Wins: "+str(totalwins))
    print("Wins%: "+str(100*totalwins/totalmatches)+"%")
    print("Loses: "+str(totalloses))
    print("Loses%: "+str(100*totalloses/totalmatches)+"%")

    # draw win,lose percentage as a pie chart
    import matplotlib.pyplot as plt
    labels = 'Wins', 'Loses', 'Ties'
    sizes = [len(selectteaminfo[selectteaminfo["result"]=="Win"]), len(selectteaminfo[selectteaminfo["result"]=="Lose"]), len(selectteaminfo[selectteaminfo["result"]=="Tie"])]
    colors = ['red', 'grey', 'lightcoral'] 
    explode = (0.1, 0, 0)  
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
    autopct='%1.1f%%', shadow=True, startangle=140)
    plt.title("Percentage of match results")
    plt.axis('equal')
    plt.show()


    print("\n\nDetailed Match information")
    print("**************************")
    print(selectteaminfo.iloc[:,1:].to_string(index=False))



