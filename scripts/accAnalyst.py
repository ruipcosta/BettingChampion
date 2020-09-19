import json
import sys

def main():
    
    try: 
        with open("FinishedGames.json", 'r', encoding='utf8') as f:
            data = json.load(f.read())
    except:
        print('Finished game data file not found')
        print('Please rerun betchamp.py and try again')
        sys.exit(0)

    




if __name__ == "__main__":
    main()
