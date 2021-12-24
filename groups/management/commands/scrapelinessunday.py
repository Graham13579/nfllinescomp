from groups.models import Game
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help="Gets the games for the week"

    def handle(self,*args,**options):
        r=requests.get("http://www.footballlocks.com/nfl_odds.shtml")
        c=r.content
        soup=BeautifulSoup(c,'html.parser')
        nonBreakSpace = u'\xa0'

        name_translation={'Green Bay':'Green Bay Packers','Philadelphia':'Philadelphia Eagles','Buffalo':'Buffalo Bills','Tampa Bay':'Tampa Bay Buccaneers','Chicago':'Chicago Bears','Atlanta':'Atlanta Falcons','Carolina':'Carolina Panthers','Kansas City':'Kansas City Chiefs','Las Vegas':'Las Vegas Raiders','New England':'New England Patriots','Denver':'Denver Broncos','LA Rams':'Los Angeles Rams','Washington':'Washington Football Team','Houston':'Houston Texans','Jacksonville':'Jacksonville Jaguars','Tennessee':'Tennessee Titans','Arizona':'Arizona Cardinals','NY Jets':'New York Jets','Pittsburgh':'Pittsburgh Steelers','Baltimore':'Baltimore Ravens','Cincinnati':'Cincinnati Bengals','San Francisco':'San Francisco 49ers','Miami':'Miami Dolphins','Dallas':'Dallas Cowboys','NY Giants':'New York Giants','Indianapolis':'Indianapolis Colts','Cleveland':'Cleveland Browns','Seattle':'Seattle Seahawks','Minnesota':'Minnesota Vikings','New Orleans':'New Orleans Saints','LA Chargers':'Los Angeles Chargers','Detroit':'Detroit Lions'}

        all=soup.find('table',{'cols':'6'}).find_all('tr')[2:]
        for item in all:
            if item.find('td',{'width':'19%'}):
                continue
            favorite=item.find_all('td')[1].text.replace('At ','')
            if item.find_all('td')[2].text.replace(nonBreakSpace,'').replace('-','') != 'PK':
                line=float(item.find_all('td')[2].text.replace(nonBreakSpace,'').replace('-',''))
            else:
                line=float(0)
            underdog=item.find_all('td')[3].text.replace('At ','')

            try:
                Game.objects.create(favorite=name_translation[favorite],line=line,underdog=name_translation[underdog],gamedate='sunday')
            except:
                pass