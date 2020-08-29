from bs4 import BeautifulSoup
import requests
import json
from datetime import date, timedelta


days = 30
    
def getWebsite(website):
    source = requests.get(website).text
    soup = BeautifulSoup(source, 'lxml')

    return soup

def writeJson(data, game):
    data['Games'].append({
        'game': game.game,
        'date': game.gameDate,
        'gameLeague': game.gameLeague,
        'NumberTips': game.faceOff_numTips,
        'ProbHome': game.probHome,
        'OddHome': game.oddHome,
        'ProbDraw': game.probDraw,
        'OddDraw': game.oddDraw,
        'ProbAway': game.probAway,
        'OddAway': game.oddAway
    })

    return data

def getGameUrls(urls):
    data = date.today()

    for ii in range(days):
        i = 1
        data2= data - timedelta(2)-timedelta(ii)
        while True:
            website = f"https://www.academiadasapostas.com/tips/listing/{data2}/page/{i}"
            soup = getWebsite(website)
            listTips = [tips.find('div') for tips in soup.find_all('div', class_="tip")]
            if not len(listTips):
                break
            
            for tip in listTips:
                urls.append(tip.find('a')['href'])
            i+=1
        
    return urls


class game():
    
    def __init__(self,url):
        self.url = url

        if self.url != '':
            gameWebsite = getWebsite(self.url)
            self.getGameInfo(gameWebsite)
            self.getStats(gameWebsite)        


    def getGameInfo(self, gameWebsite):
        headbar = gameWebsite.find('div', class_='breadcrumbs')
        lista = [listItem.a.span.text for listItem in headbar.find_all('li')]
        self.game = lista[3]
        self.gameLeague = lista[2]

        gameData = gameWebsite.find('td', class_="stats-game-head-date")
        gameStatus = [listItem.text for listItem in gameData.find_all('li') if len(listItem.text) > 1]
        self.finalScore = gameStatus[0] # ' - ' for scheduled games
        if gameStatus[1].find('(') != -1:
            self.gameStatus = gameStatus[2] # game ' Terminado ' or ' Agendado ' or real time score
            ii = 3
        else:
            self.gameStatus = gameStatus[1]
            ii = 2

        if len(gameStatus[ii])<26:
            self.gameDate = gameStatus[ii]
        else:
            self.gameDate = gameStatus[ii+1]


        if self.gameStatus == ' Terminado ':
            if int(self.finalScore.split('-')[0]) > int(self.finalScore.split('-')[1]):
                self.won = 'Home'
            elif int(self.finalScore.split('-')[0]) == int(self.finalScore.split('-')[1]):
                self.won = 'Draw'
            else:
                self.won = 'Away'
            
    def getStats(self,gameWebsite):
        
        tab_content = gameWebsite.find('div', class_="tab_content")
        if tab_content:
            market0 = tab_content.find('div', id = "market0")
        else:
            market0 = None
        if market0:
            self.faceOff_numTips = market0.find('span', class_="tipsred").text #number of tips made on face off 1x2
            faceOff_container = market0.find_all('tr', class_="even")
            faceOffStats= [stat.find_all('td')  for stat in faceOff_container]

            self.probHome = faceOffStats[0][1].text
            self.probDraw = faceOffStats[1][1].text
            self.probAway = faceOffStats[2][1].text

            probHome = int(self.probHome.split('%')[0])
            probDraw = int(self.probDraw.split('%')[0])
            probAway = int(self.probAway.split('%')[0])

            if probHome > probDraw and probHome > probAway:
                self.toWin = 'Home'
            elif probDraw > probHome and probDraw > probAway:
                self.toWin = 'Draw'
            else:
                self.toWin = 'Away'

            try:
                self.oddHome = faceOffStats[0][3].span.text
                self.oddDraw = faceOffStats[1][3].span.text
                self.oddAway = faceOffStats[2][3].span.text
            except :
                self.oddHome = "-"
                self.oddDraw = "-"
                self.oddAway = "-"
        
if __name__ == "__main__":
    
    data = {}
    data['Games'] = []
    matches = []
    urls = getGameUrls(matches)
    counter = 0
    rightCounter = 0

    for url in urls:
        gamez = game(url)
        try:
            gamez.faceOff_numTips
        except :
            continue
        data = writeJson(data, gamez)
        try: 
            gamez.won
        except :
            continue
        
        if int(gamez.faceOff_numTips) > 10:
            if gamez.toWin == gamez.won:
                rightCounter += 1

            counter += 1
        


    
    print(f'{counter} games played, {rightCounter} guesses right. {(rightCounter/counter)*100}% accuracy.')


    
    # with open('data.txt', 'w', encoding='utf8') as outfile:
    #       json.dump(data, outfile, indent=2, ensure_ascii=False)

    