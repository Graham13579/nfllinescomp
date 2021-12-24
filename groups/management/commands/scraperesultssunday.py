from groups.models import Game,PlayerPick
import requests
from bs4 import BeautifulSoup
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help="Gets the games results"

    def handle(self,*args,**options):
        r=requests.get("https://www.msn.com/en-us/Sports/nfl/scores")
        c=r.content
        soup=BeautifulSoup(c,'html.parser')

        all=soup.find('div',{'class':'section nolivesection'}).find('table',{'class':'footballscorestable'}).find_all('tbody',{'class':'even rowlink'})
        for item in all:
            if item.find('td',{'class':'matchstatus paddingleft orangeText hidedownlevel size123 aligncenter'}).find('a').text == 'FINAL':
                try:
                    winner=item.find('td',{'class':'teamname teamlinedown alignright size234 winteamname'}).text
                    try:
                        try:
                            game=Game.objects.get(favorite=winner,gamedate='sunday')
                        except:
                            game=Game.objects.get(underdog=winner,gamedate='sunday')
                    except:
                        pass
                    winnerscore=item.find('td',{'class':'totalscore teamlinedown winningteam'}).text
                    loserscore=item.find('td',{'class':'totalscore teamlineup'}).text
                    game.winner=winner
                    game.winnerscore=int(winnerscore)
                    game.loserscore=int(loserscore)
                    game.scoredifferential=(int(winnerscore)-int(loserscore))
                    game.save()

                    playerpicks=PlayerPick.objects.filter(gamepicked__winner=game.winner).select_related('gamepicked')
                    for pick in playerpicks:
                        pick.player.score += pick.score_to_add()
                        pick.player.save()

                except:
                    winner=item.find('td',{'class':'teamname teamlineup alignright size234 winteamname'}).text
                    try:
                        try:
                            game=Game.objects.get(favorite=winner,gamedate='sunday')
                        except:
                            game=Game.objects.get(underdog=winner,gamedate='sunday')
                    except:
                        pass
                    winnerscore=item.find('td',{'class':'totalscore teamlineup winningteam'}).text
                    loserscore=item.find('td',{'class':'totalscore teamlinedown'}).text
                    game.winner=winner
                    game.winnerscore=int(winnerscore)
                    game.loserscore=int(loserscore)
                    game.scoredifferential=(int(winnerscore)-int(loserscore))
                    game.save()

                    playerpicks=PlayerPick.objects.filter(gamepicked__winner=game.winner).select_related('gamepicked')
                    for pick in playerpicks:
                        pick.player.score += pick.score_to_add()
                        pick.player.save()

        all=soup.find('div',{'class':'section nolivesection'}).find('table',{'class':'footballscorestable'}).find_all('tbody',{'class':'odd rowlink'})
        for item in all:
            if item.find('td',{'class':'matchstatus paddingleft orangeText hidedownlevel size123 aligncenter'}).find('a').text == 'FINAL':
                try:
                    winner=item.find('td',{'class':'teamname teamlinedown alignright size234 winteamname'}).text
                    try:
                        try:
                            game=Game.objects.get(favorite=winner,gamedate='sunday')
                        except:
                            game=Game.objects.get(underdog=winner,gamedate='sunday')
                    except:
                        pass
                    winnerscore=item.find('td',{'class':'totalscore teamlinedown winningteam'}).text
                    loserscore=item.find('td',{'class':'totalscore teamlineup'}).text
                    game.winner=winner
                    game.winnerscore=int(winnerscore)
                    game.loserscore=int(loserscore)
                    game.scoredifferential=(int(winnerscore)-int(loserscore))
                    game.save()

                    playerpicks=PlayerPick.objects.filter(gamepicked__winner=game.winner).select_related('gamepicked')
                    for pick in playerpicks:
                        pick.player.score += pick.score_to_add()
                        pick.player.save()

                except:
                    winner=item.find('td',{'class':'teamname teamlineup alignright size234 winteamname'}).text
                    try:
                        try:
                            game=Game.objects.get(favorite=winner,gamedate='sunday')
                        except:
                            game=Game.objects.get(underdog=winner,gamedate='sunday')
                    except:
                        pass
                    winnerscore=item.find('td',{'class':'totalscore teamlineup winningteam'}).text
                    loserscore=item.find('td',{'class':'totalscore teamlinedown'}).text
                    game.winner=winner
                    game.winnerscore=int(winnerscore)
                    game.loserscore=int(loserscore)
                    game.scoredifferential=(int(winnerscore)-int(loserscore))
                    game.save()

                    playerpicks=PlayerPick.objects.filter(gamepicked__winner=game.winner).select_related('gamepicked')
                    for pick in playerpicks:
                        pick.player.score += pick.score_to_add()
                        pick.player.save()