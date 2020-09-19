from bs4 import BeautifulSoup
import requests
import json
from datetime import date, timedelta, datetime
import sys
import getopt
import pyfiglet


def usage():
    print("Betting Champiom")
    print()
    print("Usage: betchamp.py -d days")
    print("-a --accuracy             - Acurracy of the probabilities in the previous [days]")
    print("-n --NumTips              - Number of required tips to a game")
    print()
    print()
    print("Examples: ")
    print("betchamp.py -d 2")
    print("betchamp.py -d 2 -n 10")
    print("betchamp.py -d 5 -s")
    print("betchamp.py -d 5 -s -n 10")
    sys.exit(0)

def init():
    print(pyfiglet.figlet_format("Betting Champion  "))
    print()
    if not len(sys.argv[1:]):
        usage()
    
    try:
        opts, args = getopt.getopt(sys.argv[1:],"had:n:",["help","accuracy","NumTips"])
    except getopt.GetoptError as err:
        print(err)
        usage()
    
    if "-d" not in sys.argv:
        print("Days defalted to 0 (today)")

    for o,a in opts:
        if o in ("-h","--help"):
            usage()
        elif o in ("-a","--accuracy"):
            accuracy = True
            file = "FinishedGames.json"
        elif o in ("-n","--NumTips"):
            NumTips = int(a)
        elif o in ("-d"):
            days = int(a)
        else:
            assert False,"Unhandled Option"
    
    return days, file, NumTips, accuracy

def getWebsite(website):
    soup = BeautifulSoup(requests.get(website).text, 'lxml')

    return soup

def getGameUrls(days, accuracy):
    timestart = datetime.now()
    data = date.today()
    urls=[]

    for ii in range(days+1):
        i = 1
        if accuracy:
            data2= data - timedelta(ii)
        else:
            data2= data + timedelta(ii)

        while True:
            website = f"https://www.academiadasapostas.com/tips/listing/{data2}/page/{i}"
            soup = getWebsite(website)
            listTips = [tips.find('div') for tips in soup.find_all('div', class_="tip")]
            if not len(listTips):
                break
            
            for tip in listTips:
                urls.append(tip.find('a')['href'])
            i+=1
    print("getGameUrls", datetime.now()-timestart)
    return urls

def getGameInfo(gameWebsite):
    headbar = gameWebsite.find('div', class_='breadcrumbs')
    lista = [listItem.a.span.text for listItem in headbar.find_all('li')]
    game = lista[3]
    gameLeague = lista[2]
    gameData = gameWebsite.find('td', class_="stats-game-head-date")
    gameStatus = [listItem.text for listItem in gameData.find_all('li') if len(listItem.text) > 1]
    finalScore = gameStatus[0] # ' - ' for scheduled games

    if gameStatus[1].find('(') != -1:
        gameStatus = gameStatus[2] # game ' Terminado ' or ' Agendado ' or real time score
        ii = 3
    else:
        gameStatus = gameStatus[1]
        ii = 2
    if len(gameStatus[ii])<26:
        gameDate = gameStatus[ii]
    else:
        gameDate = gameStatus[ii+1]
    return finalScore, game, gameLeague, gameDate, gameStatus
    
def getStats(gameWebsite):
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
    
    return faceOff_numTips, probHome, probDraw, probAway, oddHome, oddDraw, oddAway, toWin


def writeJson(data, game, accuracy):

    if accuracy:
        try:
            game.won
        except:
            return
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
            'OddAway': game.oddAway,
            'ToWin': game.toWin,
            'Won': game.won,
            'FinalScore': game.finalScore
        })
    else:
        data['Games'].append({
            'game': game.game,
            'date': game.gameDate,
            'gameLeague': game.gameLeague,
            'numberTips': game.faceOff_numTips,
            'ProbHome': game.probHome,
            'OddHome': game.oddHome,
            'ProbDraw': game.probDraw,
            'OddDraw': game.oddDraw,
            'ProbAway': game.probAway,
            'OddAway': game.oddAway,
            'ToWin': game.toWin
        })
    

class game():
    
    def __init__(self, gameWebsite, gameInfo, gameStats):
        self.game = gameInfo[1]
        self.gameLeague = gameInfo[2]
        self.gameDate = gameInfo[3]
        self.gameStatus = gameInfo[4]
        self.faceOff_numTips = gameStats[0]
        self.probHome = gameStats[1]
        self.probDraw = gameStats[2]
        self.probAway = gameStats[3]
        self.oddHome = gameStats[4]
        self.oddDraw = gameStats[5]
        self.oddAway = gameStats[6]
        self.toWin = gameStats[7]

class finishedGame(game):
    
    def __init__(self, gameWebsite, gameInfo, gameStats):
        super().__init__(gameWebsite, gameInfo, gameStats)
        finalScore = gameInfo[0]
        finalScoreSplit = finalScore.split('-')

        if finalScoreSplit[0] != ' ':
            self.finalScore = finalScore
            if int(finalScoreSplit[0]) > int(finalScoreSplit[1]):
                self.won = 'Home'
            elif int(finalScoreSplit[0]) == int(finalScoreSplit[1]):
                self.won = 'Draw'
            else:
                self.won = 'Away'

def createJson(listUrl):
    data = dict()
    data['Meta']={
        'Time':  datetime.now().strftime("%Y-%m-%d %H:%M"),
        'NumberGames': len(listUrl)
    }
    data['Games']=[]
    return data



def run(listUrl, NumTips, accuracy):
    timestart = datetime.now()
    counter = 0
    for url in listUrl:
        gameWebsite = getWebsite(url)
        gameInfo = getGameInfo(gameWebsite)
        gameStats = getStats(gameWebsite)
        if gameStats:
            if gameInfo[4] == ' Terminado ' and gameStats[0] > NumTips and accuracy:
                finishedMatch = finishedGame(gameWebsite, gameInfo, gameStats)
                writeJson(data, finishedMatch, accuracy)
            elif gameInfo[4] == ' Agendado ' and gameStats[0] > NumTips and not accuracy:
                match = game(gameWebsite, gameInfo, gameStats)
                writeJson(data, match, accuracy)


        counter+=1
        # sys.stdout.write("\r%d out of %d games stats completed" % (counter,len(listUrl)))
        # sys.stdout.flush()
    print("run", datetime.now()-timestart)
    return data

def initialRun(days, accuracy):
    timestart = datetime.now()
    listUrl = getGameUrls(days, accuracy)
    data = createJson(listUrl)
    print("initialRun-",len(listUrl), datetime.now()-timestart)
    return listUrl, data

def main():
    timestart = datetime.now()
    accuracy = False
    NumTips = 0
    days = 0
    file = "games.json"
    global data
    # days, file, NumTips, accuracy = init()
    listUrl, data = initialRun(days, accuracy)

    data = run(listUrl, NumTips, accuracy)

    # with open(file, "w", encoding='utf8') as f:
    #     json.dump(data, f, indent=2, ensure_ascii=False, default=str)
    print("main", datetime.now()-timestart)
    # print("Statistics completed. Data file created")~
    return data


    

if __name__ == "__main__":
    
    main()