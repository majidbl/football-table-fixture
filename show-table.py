import requests
from bs4 import BeautifulSoup
import json
from tabulate import tabulate
import sys

def usage():
  print("Usage:")
  print("python sc.py [option]")
  print("----------------------")
  print("    pl : show premier league standing")
  print("    sa : show seri A standing")
  print("    bu : show germany bundesliga standing")
  print("    lu : show france league 1 standing")
  print("    ll : show Spanish laliga standing")
  print("    po : show portugal league standing")

#################################

def league(i):
        switcher={
                'pl':"https://supersport.com/football/premier-league/logs",
                'sa':'https://supersport.com/football/italy/logs',
                'll':'https://supersport.com/football/spain/logs',
               'lu':'https://supersport.com/football/france/logs',
               'bu':'https://supersport.com/football/germany/logs',
               'po':'https://supersport.com/football/portugal/logs'
               
             }
        return switcher.get(i,"Invalid option")



if len(sys.argv) < 2 or len(sys.argv) > 2:
  usage()
  sys.exit()

le = league(sys.argv[1])
if le != "Invalid option":
  page = requests.get(le)
  #print(page)
  soup = BeautifulSoup(page.content, 'html.parser')

  #print(soup)

  table = soup.find('football-home-logs')

  #print(table)
  js = json.loads(table["logs"])

  headers = ["#","Team", "PL" ,"W", "D", "L", "P"]
  data = []
  for t in js:
    for te in t["positions"]:
      #print("{}    {}    {}    {}".format (te["name"],te["won"],te["drew"], te["lost"]))
      data.append([te["position"],te["name"],te["played"],te["won"],te["drew"], te["lost"],te["points"]])

  print(tabulate(data, headers, tablefmt="github"))
