from datetime import date
import requests
import re
from xml.etree import ElementTree

# TODO: save checkpoints for easy updates

def main(): 
    for year in range(2011, date.today().year + 1):

        # TODO: start with 3 (March), not 4 (April) [FOR TESTING ONLY]
        for month in range(4, 11): 
            for day in range(1, num_days_in(month)+1):
                url = 'http://gd.mlb.com/components/game/mlb/year_{y}/month_{m:02d}/day_{d:02d}/'.format(y=year, m=month, d=day)
                games_index = requests.get(url).text
                games = re.findall(r'> (gid.*mlb.*mlb.*)/</a>', games_index)
                for game_id in games:
                    if month == 3 or (month == 4 and day < 10):
                        spring_check_url = "{url}{gid}/linescore.json".format(url=url, gid=game_id)
                        spring_check = requests.get(spring_check_url).text
                        if re.search(r'spring', spring_check):
                            continue
                    innings_url = "{url}{gid}/inning/".format(url=url, gid=game_id)
                    innings_index = requests.get(innings_url).text
                    innings = re.findall(r'(inning_[0-9]+)', innings_index)
                    for inning in innings:
                        inning_url = "{url}{inning}.xml".format(url=innings_url, inning=inning)
                        data = requests.get(inning_url)
                        xml = ElementTree.fromstring(data.content)
                        parse(xml)
                        exit(1)



def parse(inning):
    for half in inning:
        for atbat in half.findall('atbat'):
            print atbat.attrib
            
            for pitch in atbat.findall('pitch'):
                print atbat_action.attrib


def num_days_in(month):
    return {
        3: 31, 4: 30, 5: 31,
        6: 30, 7: 31, 8: 31,
        9: 30, 10: 31
    }[month]


if __name__ == '__main__':
    main()