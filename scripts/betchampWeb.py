from bs4 import BeautifulSoup
import requests
from datetime import date, timedelta, datetime
import sys
import getopt
import json

# FOR THE WEBSITE (NO ACCURACY, NO JSON)

class Game():
    def __init__(self, gameInfo, gameStats):
        self.home = gameInfo[0][0]
        self.away = gameInfo[0][1]
        self.gameDate = gameInfo[1]
        self.url = gameInfo[2]
        self.faceOff_numTips = gameStats[0]
        self.probHome = gameStats[1]
        self.probDraw = gameStats[2]
        self.probAway = gameStats[3]
        self.toWin = gameStats[4]
        self.gameLeague = gameStats[5]

def getWebsite(website):
    soup = BeautifulSoup(requests.get(website).text, 'lxml')

    return soup

def writeJSON(data, game):
    data['Games'].append({
            'home': game.home,
            'away': game.away,
            'date': game.gameDate,
            'gameLeague': game.gameLeague,
            'numberTips': game.faceOff_numTips,
            'ProbHome': game.probHome,
            'ProbDraw': game.probDraw,
            'ProbAway': game.probAway,
            'ToWin': game.toWin
        })
    return data

def createJSON():
    data = dict()
    data['Meta']={
        'Time':  datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    data['Games']=[]
    return data

def run(days):
    jsonFile=createJSON()
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
            
            jsonFile=getGameInfo(listTips, jsonFile)
            i+=1
    # jsonFile = json.dumps(jsonFile,ensure_ascii=False)
    return jsonFile

def getGameInfo(listTips, jsonFile):
    for tip in listTips[0]:
        tipData=tip.find('img').find_next_siblings()
        teams = tipData[0].text
        date = tipData[1].text
        try: url = tipData[2]['href']
        except: continue
        if '\nx\n' in teams:
            teams = teams.split('\nx\n')
            teams=[teams[0].replace('\n',''),teams[1].replace('\n','')]
            gameInfo=[teams,date,url]
            gameStats = getStats(url)
            if gameStats != None:
                match=Game(gameInfo,gameStats)
                jsonFile= writeJSON(jsonFile,match)
    return jsonFile

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
    else:
        return None
    
    gameStats=[faceOff_numTips, probHome, probDraw, probAway, toWin, gameLeague]
    return gameStats

if __name__ == "__main__":
    timestart = datetime.now()
    run(0)
    print("main", datetime.now()-timestart)