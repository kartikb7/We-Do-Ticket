import requests
import urllib.request
from bs4 import BeautifulSoup
import csv
import random
import time

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:20.0) Gecko/20100101 Firefox/20.0'}
request1 = requests.get("https://www.vividseats.com/nfl/?utm_source=google&utm_medium=cpc&utm_"
                        "campaign=NFL+Football&utm_term=nfl+ticket+exchange&vkid=15941722&gclid="
                        "CjwKCAjw2qHsBRAGEiwAMbPoDCuchV4uFGCefcG1aIB0QgjkStoc2cQ1HB5ath499SYP82i3"
                        "Pqb0ahoCK-4QAvD_BwE", headers = headers)
ticket = BeautifulSoup(request1.text, "lxml")

tempList = ticket.findAll("a", {"class": "vdp-type-link--block"})

listOfWebPage = []
for i in tempList:
    k = "https://www.vividseats.com" + str(i)[38:-4]
    listOfWebPage.append(k)

listOfWebPage = listOfWebPage[:32]

tempStorePage = []
for i in listOfWebPage:
    tempStorePage.append(i.split(">"))

cleanedWebPage = []
for i in tempStorePage:
    cleanedWebPage.append(i[0][:-1])

try:
  arrayOfMatch = [["Match", "Team A", "Team B", "Date", "Time", "Stadium", "Address", "City", "State", "Post Code", "Price", "URL"]]

  # go through cleaned web pag list
  for k in range (0, len(cleanedWebPage)):

      request2 = requests.get(cleanedWebPage[k], headers = headers)
      ticket = BeautifulSoup(request2.text, "lxml")
      # find match information
      tempList = ticket.findAll("script", {"type": "application/ld+json"})
      info = str(tempList[1]).split(",")
      # create a list of individual match
      for i in range(0, int(len(info)/30)):
          array = []
          match_title = info[2+i*30][8:-1]
          # get rid of unnecessary "()"
          if match_title[-1] == ")":
              item = match_title.find("(")
              match_title = match_title[:item]
          array.append(match_title)
          array.append((array[0].split(" at "))[0])
          array.append((array[0].split(" at "))[1])
          array.append(info[5+i*30][13:23])
          array.append(info[5+i*30][24:29])
          array.append(info[16+i*30][8:-1])
          array.append(info[18+i*30][17:-1])
          array.append(info[21+i*30][19:-1])
          array.append(info[22+i*30][17:19])
          array.append(info[20+i*30][14:19])
          array.append(int(info[29+i*30][8:-2].split(".")[0]))
          array.append(info[25+i*30][7:-1])
          # append individual match to the big array
          arrayOfMatch.append(array)

  # wait to avoid robot detection
      num = random.randrange(10, 20, 1)
      time.sleep(num)

except:
    print("Blocked by the website")

# write into csv file
file = open("dis.csv", "a")
wr = csv.writer(file, dialect='excel')
for i in arrayOfMatch:
    wr.writerow(i)

file.close()


