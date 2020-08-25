from bs4 import BeautifulSoup
import requests
import json


    
def getWebsite(website):
    source = requests.get(website).text
    soup = BeautifulSoup(source, 'lxml')

    return soup

def writeJson(data, game):
    data['Games'].append({
        'game': game.game,
        'date': game.date,
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

    

class game():
    
    def __init__(self,tips):
        tip = tips.find('div')
        game = [lol.text  for lol in tip.find_all('li') if lol.text != '\n']
        self.game = game[0]+' '+game[1]+' '+game[2]
        self.gameLeague = tip.h3.text
        self.gameLeague = self.gameLeague.replace('\n','')
        self.date = tip.find('p').text
        self.url = tip.find('a')['href']

        self.getStats(self.url)




    def getStats(self,url):
        gameUrl = getWebsite(url)
        stats = gameUrl.find('div', class_="tab_content")
        faceOff = stats.find('div', id = "market0")
        self.faceOff_numTips = faceOff.find('span', class_="tipsred").text #number of tips made on face off 1x2
        faceOff_container = faceOff.find_all('tr', class_="even")
        faceOffStats=[]
        for stat in faceOff_container:
            faceOffStats.append(stat.find_all('td'))

        self.probHome = faceOffStats[0][1].text
        self.oddHome = faceOffStats[0][3].span.text

        self.probDraw = faceOffStats[1][1].text
        self.oddDraw = faceOffStats[1][3].span.text

        self.probAway = faceOffStats[2][1].text
        self.oddAway = faceOffStats[2][3].span.text


    

        
if __name__ == "__main__":
    website = 'https://www.academiadasapostas.com/tips/listing'
    
    soup = getWebsite(website)
    


    # game(soup.find('div', class_="tip"))
    data = {}
    data['Games'] = []
    for tips in soup.find_all('div', class_="tip"):
        gamez = game(tips)
        data = writeJson(data, gamez)
    
    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile, indent=3)

    