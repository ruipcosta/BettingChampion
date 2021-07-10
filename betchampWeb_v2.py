import django
from bs4 import BeautifulSoup
import requests
from datetime import date, timedelta, datetime
from django.conf import settings
import os
import sys

sys.path.append("C:/Users/rcost/Documents/Projects/BettingChampion")
os.environ['DJANGO_SETTINGS_MODULE'] = 'bettingchampion.settings'

# FOR THE WEBSITE (NO ACCURACY, NO JSON)


# class Game():
#     def __init__(self, gameInfo, gameStats):
#         self.home = gameInfo[0][0]
#         self.away = gameInfo[0][1]
#         self.gameDate = gameInfo[1]
#         self.url = gameInfo[2]
#         self.faceOff_numTips = gameStats[0]
#         self.probHome = gameStats[1]
#         self.probDraw = gameStats[2]
#         self.probAway = gameStats[3]
#         self.toWin = gameStats[4]
#         self.gameLeague = gameStats[5]


def write2Db(gameInfo, gameStats):
    from games.models import AcademiaGame
    obj = AcademiaGame.objects.update_or_create(home=gameInfo[0][0], away=gameInfo[0][1],
                                                date=gameInfo[1], gameLeague=gameStats[5],
                                                numberTips=gameStats[0], ProbHome=gameStats[1],
                                                ProbDraw=gameStats[2], ProbAway=gameStats[3], ToWin=gameStats[4])
    obj.save()


def run(days):
    time = date.today()
    for ii in range(days+1):
        i = 1
        deltaTime = time + timedelta(ii)
        while True:
            website = f"https://www.academiadasapostas.com/tips/listing/{deltaTime}/page/{i}"
            soup = BeautifulSoup(requests.get(website).text, 'lxml')
            tips = soup.find_all('div', class_="tip")

            if not len(tips):
                break

            for tip in tips:
                getGameInfo(tip)

            i += 1


def getGameInfo(tip):

    tipData = tip.find('img').find_next_siblings()
    teams = tipData[0].text
    date = tipData[1].text
    try:
        url = tipData[2]['href']
    except:
        return
    if '\nx\n' in teams:
        teams = teams.split('\nx\n')
        teams = [teams[0].replace('\n', ''), teams[1].replace('\n', '')]
        gameInfo = [teams, date, url]
        gameStats = getStats(url)

        if gameStats != None:
            write2Db(gameInfo, gameStats)


def getStats(url):
    gameWebsite = BeautifulSoup(requests.get(url).text, 'lxml')

    headbar = gameWebsite.find('div', class_='breadcrumbs')
    lista = [listItem.a.span.text for listItem in headbar.find_all('li')]
    gameLeague = lista[2]

    tab_content = gameWebsite.find('div', class_="tab_content")
    if tab_content:
        market0 = tab_content.find('div', id="market0")
    else:
        return None

    if market0:
        # number of tips made on face off 1x2
        faceOff_numTips = int(market0.find('span', class_="tipsred").text)
        faceOff_container = market0.find_all('tr', class_="even")
        faceOffStats = [stat.find_all('td') for stat in faceOff_container]

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

    gameStats = [faceOff_numTips, probHome,
                 probDraw, probAway, toWin, gameLeague]
    return gameStats


if __name__ == "__main__":
    django.setup()
    timestart = datetime.now()
    run(0)
    print("main", datetime.now()-timestart)
