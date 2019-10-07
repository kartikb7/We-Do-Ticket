

#Packages
import csv as ccc
import pandas as pd


#os.chdir('C:\\Users\\Kartik\\Desktop\\Study Material\\Python\\Project Draft\\We-Do-Ticket-master')

#User Files
import teamcoolinfo as ci
import weatherDisplay as weather
import flightDisplay as flight
import tripadvisorScrap as hotel

def read_csv():
    # open csv file for data
    with open('TicketInfo.csv') as ticket_csv:
        csv_reader = ccc.reader(ticket_csv, delimiter=',')
        line_count = 0
        content = []
        # read the csv file line by line
        for row in csv_reader:
            if line_count == 0:
                header = row
            else:
                content.append(row)
            line_count += 1
    ticket_csv.close()
    # create a DataFrame
    ticket_df = pd.DataFrame(content, columns=header)
    return ticket_df


def create_team(ticket_df):
    # get all the teams in sorted order
    team = list(set(ticket_df["Host Team"]))
    team.sort()
    # create a string which will be printed later, the string contains 4 teams in a row and 8 rows
    team_print = ""
    for i in range(8):
        for k in range(4):
            team_print += "{:>2}. {:<30s}".format(((k + 1) + 4 * i), team[k + 4 * i])
        team_print += "\n"
    team_print = team_print[:-1]
    return team, team_print


def user_interface(ticket_df, team, team_print):
    choice_of_team = 9999
    # enter in the loop which allows user to select team they are interested in
    while choice_of_team != -1:
        try:
            print()
            print(team_print)
            print("Choose your favorite team and I will show their up-coming matches (input an integer only)")
            print("Choose 0 to quit the program")
            choice_of_team = int(input("Enter your choice here: "))
            # if user enter 0, quit the program
            if choice_of_team == 0:
                print()
                print("Thank you for using We Do Ticket, see you next time!")
                break
            # if user enter wrong input, go to the catch block
            if not 0 < choice_of_team <= len(team):
                x = 1/0

            # create a dataframe of hostes match and guest matches
            team_name = team[choice_of_team - 1]
            host_df = ticket_df[ticket_df["Host Team"] == team_name]
            guest_df = ticket_df[ticket_df["Guest Team"] == team_name]

            choice_of_match = 9999

            # create loop which allows user to select the match
            while choice_of_match != -2:
                try:
                    print()
                    print("Here displays all matches of " + team_name)
                    print("{:<3}{:<50s}{:<15}{:<10}{:<30s}{:<20}{:<10}{:<10}".format("", "Match Info", "Date", "Time",
                                                                                     "Stadium", "City", "State", "Price"))
                    print(team_name + " as Host: ")
                    # display match info
                    for i in range(len(host_df.index)):
                        print("{:>2}.{:<50s}{:<15}{:<10}{:<30s}{:<20}{:<10}{:<10}".format((i + 1),
                                                                                          host_df.iloc[i]["Match Info"],
                                                                                          host_df.iloc[i]["Date"],
                                                                                          host_df.iloc[i]["Time"],
                                                                                          host_df.iloc[i]["Stadium"],
                                                                                          host_df.iloc[i]["City"],
                                                                                          host_df.iloc[i]["State"],
                                                                                          host_df.iloc[i][
                                                                                              "Lowest Ticket Price"]))
                    print(team_name + " as Guest: ")
                    for i in range(len(guest_df.index)):
                        print("{:>2}.{:<50s}{:<15}{:<10}{:<30s}{:<20}{:<10}{:<10}".format((len(host_df.index) + i + 1),
                                                                                          guest_df.iloc[i]["Match Info"],
                                                                                          guest_df.iloc[i]["Date"],
                                                                                          guest_df.iloc[i]["Time"],
                                                                                          guest_df.iloc[i]["Stadium"],
                                                                                          guest_df.iloc[i]["City"],
                                                                                          guest_df.iloc[i]["State"],
                                                                                          guest_df.iloc[i][
                                                                                              "Lowest Ticket Price"]))
                    print("Choose a match that you are interested in watching (input an integer only)")
                    print("Choose 0 to quit the program")
                    print("Choice -1 to go back to team selection")
                    choice_of_match = int(input("Enter your choice here: "))
                    # menu selection section
                    if choice_of_match == -1:
                        choice_of_team = 9999
                        break
                    elif choice_of_match == 0:
                        print()
                        print("Thank you for using We Do Ticket, see you next time!")
                        choice_of_team = -1
                        break
                    elif not 0 < choice_of_match <= (len(host_df.index) + len(guest_df.index)):
                        x = 1/0

                    if choice_of_match > len(host_df.index):
                        match = guest_df.iloc[choice_of_match - len(host_df.index) - 1]
                    else:
                        match = host_df.iloc[choice_of_match - 1]

                    choice_of_operation = 9999
                    # create a loop to for user to choose operation on selected match
                    while choice_of_operation != 0:
                        try:
                            print()
                            # display detailed info about the match
                            print("Here is detailed information of " + match["Match Info"] + " on " + match["Date"])
                            print("{:<25}{:<25}{:<15}{:<10}{:<30s}{:<40}{:<20}{:<10}{:<10}{:<10}".format(
                                    "Guest Team", "Host Team", "Date", "Time", "Stadium", "Address", "City",
                                    "State", "Zip Code", "Price"))
                            print("{:<25}{:<25}{:<15}{:<10}{:<30s}{:<40}{:<20}{:<10}{:<10}{:<10}".format(
                                    match["Guest Team"], match["Host Team"], match["Date"],
                                    match["Time"], match["Stadium"], match["Address"], match["City"], match["State"],
                                    match["Zip"], match["Lowest Ticket Price"]))
                            print("You can buy ticket here: " + match["Ticket Website"])
                            print()
                            # display various of options
                            print("You can choose from the following options:")
                            print("1. Weather in " + match["City"] + " on " + match["Date"])
                            print("2. Flight to " + match["City"])
                            print("3. Hotel in " + match["City"])
                            print("4. Past matches and performance of " + team_name)
                            print("Choose the information you want to browse (input an integer only")
                            print("Input 0 to quit the program")
                            print("Input -1 to go back to match information and selection")
                            print("Input -2 to go back to team selection")
                            choice_of_operation = int(input("Enter your choice here: "))
                            # weather option
                            if choice_of_operation == 1:
                                weather.weatherInfo(match["Date"],match["City"])
                                input("Press enter to continue")
                            # flight info option
                            elif choice_of_operation == 2:
                                flight.flightDisplay(match["City"], match["Date"])
                                input("Press enter to continue")
                            # hotel info option
                            elif choice_of_operation == 3:
                                hotel.hotel_scrap(match["City"])
                                hotel.hotel_visual()
                                input("Press enter to continue")
                            # past performance option
                            elif choice_of_operation == 4:
                                ci.performanceInfo(team_name)
                                input("Press enter to continue")
                            # handle menu jump option
                            if choice_of_operation == -2:
                                choice_of_match = -2
                                choice_of_team = 9999
                                break
                            elif choice_of_operation == -1:
                                choice_of_match = 9999
                                break
                            elif choice_of_operation == 0:
                                print()
                                print("Thank you for using We Do Ticket, see you next time!")
                                choice_of_match = -2
                                choice_of_team = -1
                                break
                            elif not 0 < choice_of_operation <= 4:
                                x = 1/0
                        # exception handling
                        except:
                            print()
                            print("Incorrect operation input")
                            input("Press enter to continue")
                            print()
                            choice_of_operation = 9999
                except:
                    print()
                    print("Incorrect match input")
                    input("Input anything to continue")
                    print()
                    choice_of_match = 9999
        except:
            print()
            print("Incorrect team input")
            input("Press enter to continue")
            print()
            choice_of_team == 9999


# main program
ticket_df = read_csv()
team, team_print = create_team(ticket_df)
user_interface(ticket_df, team, team_print)
