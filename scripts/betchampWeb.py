from bs4 import BeautifulSoup
import requests
from datetime import date, timedelta, datetime
import sys
import getopt

# FOR THE WEBSITE (NO ACCURACY, NO JSON)

class Game():
    def __init__(self, teams, date, url):
        self.game = teams
        self.gameDate = date
        self.url = url
        self.stats()
        
        
    def stats(self):
        gameStats=getStats(self.url)
        if gameStats != None:
            self.faceOff_numTips = gameStats[0]
            self.probHome = gameStats[1]
            self.probDraw = gameStats[2]
            self.probAway = gameStats[3]
            self.oddHome = gameStats[4]
            self.oddDraw = gameStats[5]
            self.oddAway = gameStats[6]
            self.toWin = gameStats[7]
            self.gameLeague = gameStats[8]

def getWebsite(website):
    soup = BeautifulSoup(requests.get(website).text, 'lxml')

    return soup

def run(days):
    data = date.today()
    for ii in range(days+1):
        i = 1
        data2= data + timedelta(ii)
        while True:
            website = f"https://www.academiadasapostas.com/tips/listing/{data2}/page/{i}"
            soup = getWebsite(website)
            listTips = [tips.find('div') for tips in soup.find_all('div', class_="tip")]
            if not len(listTips):
                break
            
            getGameInfo(listTips)
            i+=1

def getGameInfo(listTips):
    for tip in listTips:
        tipData=tip.find('img').find_next_siblings()
        teams = tipData[0].text.replace('\n','')
        date = tipData[1].text
        url = tipData[2]['href']
        if 'x' in teams:
            Game(teams, date, url)


def getStats(url):
    gameWebsite = getWebsite(url)

    headbar = gameWebsite.find('div', class_='breadcrumbs')
    lista = [listItem.a.span.text for listItem in headbar.find_all('li')]
    gameLeague = lista[2]

    tab_content = gameWebsite.find('div', class_="tab_content")
    if tab_content:
        market0 = tab_content.find('div', id = "market0")
    else:
        return None

    if market0:
        faceOff_numTips = int(market0.find('span', class_="tipsred").text) #number of tips made on face off 1x2
        faceOff_container = market0.find_all('tr', class_="even")
        faceOffStats= [stat.find_all('td')  for stat in faceOff_container]

        probHome = faceOffStats[0][1].text
        probDraw = faceOffStats[1][1].text
        probAway = faceOffStats[2][1].text

        probHome = int(probHome.split('%')[0])
        probDraw = int(probDraw.split('%')[0])
        probAway = int(probAway.split('%')[0])

        if probHome > probDraw and probHome > probAway:
            toWin = 'Home'
        elif probDraw > probHome and probDraw > probAway:
            toWin = 'Draw'
        elif probAway > probHome and probAway > probDraw:
            toWin = 'Away'
        else:
            toWin = 'Inconclusive'

        try:
            oddHome = float(faceOffStats[0][3].span.text)
            oddDraw = float(faceOffStats[1][3].span.text)
            oddAway = float(faceOffStats[2][3].span.text)
        except :
            oddHome = 0
            oddDraw = 0
            oddAway = 0
    else:
        return None
    
    return faceOff_numTips, probHome, probDraw, probAway, oddHome, oddDraw, oddAway, toWin, gameLeague

if __name__ == "__main__":
    timestart = datetime.now()
    run(0)
    print("main", datetime.now()-timestart)