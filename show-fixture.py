import requests
from bs4 import BeautifulSoup

from tabulate import tabulate

import math
import sys
import json

# print help if user has wrong input
def usage():
  print("Usage:")
  print("python sc.py [option]")
  print("----------------------")
  print("    pl : show premier league standing")
  print("    sa : show seri A standing")
  print("    bu : show germany bundesliga standing")
  print("    lu : show france league 1 standing")
  print("    ll : show Spanish laliga standing")
  print("    ch : show england championShip standing")

#################################
# return exact url
def league(i):
        switcher={
               'pl' : 'https://www.eurosport.com/football/premier-league/calendar-result.shtml',
               'sa' : "https://www.eurosport.com/football/serie-a/calendar-result.shtml",
               'll' : 'https://www.eurosport.com/football/liga/calendar-result.shtml',
               'bu' : 'https://www.eurosport.com/football/bundesliga/calendar-result.shtml',
               'lu' : 'https://www.eurosport.com/football/ligue-1/calendar-result.shtml',
               'ch' : 'https://www.eurosport.com/football/championship/calendar-result.shtml'
             }
        return switcher.get(i,"Invalid option")

# check if input length was too many or too few
if len(sys.argv) < 2 or len(sys.argv) > 2:
  usage()
  sys.exit()

loc = requests.get("http://ipinfo.io")

jloc = json.loads(loc.text)
# checkif input league was in var
le = league(sys.argv[1])
if le != "Invalid option":
  # get full page With requests library
  page = requests.get(le)
  # parse html web page with BeautifulSoup
  soup= BeautifulSoup(page.content, 'html.parser')
  # extract match part from whole web page
  match = soup.find("div", class_="ajax-container")
  
  # extract div tage for iteration over it
  div = match.find_all("div")
  # fir seek position in list
  counter = 0
  # vars for sort data ti show with tabulate
  row= []
  inner = []
  headers = ["home", "S/T", "S/L", "away"]
  date = [] 
  scores = []
  team_name = []
  tages = []
  #iteration over div tages
  for m in div:
    if m.get("class")[0] == "date-caption" or m.get("class")[0] == "team__name" :
      tages.append(m.get("class")[0])
      if m.get("class")[0] == 'date-caption':
        date.append(m.text)
      if m.get("class")[0] == 'team__name':
        team_name.append(m.find("span", class_="team__label").text)
    if m.get("class")[0] == "match__score-text" or m.get("class")[0] == "match__time":
      scores.append(m.text)
      if m.get("class")[0] == "match__time":
        scores.append("{}/{}".format (jloc["country"],jloc["city"]))
  
  match_score = []
  
  for i in range(0, len(team_name)):
    if i < len(scores):
      match_score.append(scores[i])
    else:
      match_score.append("N/A")
  index = []
  
  #import pdb; pdb.set_trace()
  for i in range(0,len(tages)):
    if tages[i]== 'date-caption':
      index.append(i)
  index.append(len(tages))
  
  for d in range(0,len(index)-1):
    cm = math.ceil((index[d+1] - index[d]-1)/2)
    for c in range(0,int(cm)):
      inner.append([team_name[counter],match_score[counter],match_score[counter+1] ,team_name[counter+1]])
      counter = counter + 2
    row.append(inner)
    inner = []
  for r in row:
    print("\t\t",date.pop(0))
    print(tabulate(r,headers,tablefmt="fancy-grid"))