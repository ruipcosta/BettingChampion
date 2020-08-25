# Betting Champion

Web scrapping football matches for statistics from academiadasapostas.com

The code developed access the website were multiples users share their thoughts on the outcome of the match. The code then writes to a json file some information about the game such all the game info (teams, league/competition, date), the number of people who made their assumption, the stats (win Home, draw, win Away) as well as the market odds (may vary based on the house).

# Running
Code developed in a virtual environment, all the requirements are in the requirements.txt
To initialize virtualenv with all the requirements run:

```bash
virtualenv env && source env/bin/activate && pip install -r requirements.txt
```