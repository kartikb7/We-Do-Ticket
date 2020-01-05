# We-Do-Ticket

Part 1 - Module Installation and Browser Requirement
1.	Module Installation: PrettyTable
a.	Download prettyTable file from https://pypi.org/project/PrettyTable/
b.	Use cmd to input “pip install prettytable”
 
2.	Module Installation: selenium
To install the selenium module, type the command:
 “pip install -U selenium”
3.	Module Installation: unicodecsv
To install the unicodecsv module, type the command:
“pip install -U selenium Installation: selenium”
4.	Other packages that might need installation –
Pandas and Bs4
5.	Browser Requirement
If you are using Google Chrome with a version below 77, the flight scraping functionality will not work. The chromedriver is compatible with the latest version of chrome i.e. 77. To check the version of your chrome or update it, inside chrome menu click “ Help ---> About Google Chrome ”.
 

Part 2 - Usage Instructions
1.	Download and Run File
Download zip file, extract it, open and run < UserInterface.py> 
 
2.	Choose a Favorite Team
•	Names of 32 Teams are listed on the screen. 
•	Choose your favorite team and input the number of that team. (Integer only)
•	In this example, we input 2 and choose <Atlanta Falcons>.
 

3.	Choose a Match
•	Information of all the matches in recent 3 months of the chosen team are shown on the screen. Matches are divided into 2 parts according to whether the team is as host or as guest. 
•	Choose one match and input the number of it.
•	For this example, we enter 1 to choose < 1.Los Angeles Rams at Atlanta Falcons> as shown in the screenshot below.
 
4.	Learn Further Detailed Information 
Detailed information (Guest Team, Host Team, Date, Time, Stadium, Address, City, State, Zip Code, Price) of that match are displayed on the screen. 
Input Corresponding number to get further information about Weather, Flight, Hotel, and Past Matches’ performance:
•	Input 1 to get Weather information on the match day of the city where the selected match is located
•	Input 2 to get Flight information from Pittsburgh to the city where the selected match is located
•	Input 3 to get Hotel information of the city where the selected match is located
•	Input 4 to get Matches between similar teams in the past and their performance
In this example, we choose 1 to get into next step.
 

5.	Check Weather Info.
As we choose “1” in last step, predicted weather information on the match day as well as days before and after the match day are displayed. (The graph may display in IDLE or as pop-up)
Press Enter Key to continue.
 
6.	Back to Selection Menu
•	After pressing Enter Key, the platform back to the menu interface that can input a number to display other information.
•	In this example, we input 2 to display Flight Information.
 

7.	Check Flight Info.
After pressing 2, it shows flights Information on one day before the match day from Pittsburgh to the city that the match is located. (Assumption: People fly to watch the match one day before the match day.)
Also, ticket booking website is also shown on the screen , so that people can find the website and buy tickets easily.
Press Any Key to continue.
 

8.	Check Hotel Info.---Input Check In & Out Dates 
After pressing any key, if we input 3 to display Hotel Information, it will first require the user to input checkin and checkout date. In this example, we input one day before the match as the checkin date, and one day after the match as the checkout date.
 

9.	Check Hotel Info.---Display Tables 
After Input the checkin and checkout dates, it automatically displays 3 tables about the hotel on the selected dates. (Price per night on the selected dates of some hotels is still to be determined. For those hotels, the price part is blank.)
•	Ten Cheapest Hotels
•	Ten Most Popular Hotels
•	Ten Hotels with Highest Ratings


10.	Check Past Matches and Performance 
The past matches and performance option show user the historic performance in years 2018 and 2019 for the team of that user selected. The output contains following two output -
•	Summary of wins and loses
•	Outcome of each and every match


11.	Loop Or Quit
After press enter key, the program back to the menu interface that can:
•	Quit program—Input 0
•	Back to the Match information Page that can display matchs of the selected team----Input -1
•	Back to the Team Selection Page that can select among 32 teams----Input -2
The program continues to loop until the user choose to quit the program.

 
Part 3 - Video
Link of the video demonstrating our project being run is below:
https://www.youtube.com/watch?v=siH1qrKyBBs&feature=youtu.be 


Part 4 - Group Members Information
Our group is made up by 4 students.<br>
1	Kartik Bansal<br>
2	Cyndi Wang<br>
3	Honda Zhang<br>
4	Georgia Fu<br>


