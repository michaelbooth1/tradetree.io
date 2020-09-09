from urllib import request
from Database import get_database
from bs4 import BeautifulSoup
import json
import requests

BASE_URL = 'https://statsapi.web.nhl.com/api/v1/'
TEAMS_ENDPOINT = 'teams/'
ROSTER_ENDPOINT = 'roster'
WIKI_URL = 'https://en.wikipedia.org/wiki/2019_NHL_Entry_Draft'
DB = get_database()
NHL_TEAMS = "AnaheimDucks,\
ArizonaCoyotes,\
BostonBruins,\
BuffaloSabres,\
CalgaryFlames,\
CarolinaHurricanes,\
ChicagoBlackhawks,\
ColoradoAvalanche,\
ColumbusBlue Jackets,\
DallasStars,\
DetroitRedWings,\
EdmontonOilers,\
FloridaPanthers,\
LosAngelesKings,\
MinnesotaWild,\
MontrealCanadiens,\
NashvillePredators,\
NewJerseyDevils,\
NewYorkIslanders,\
NewYorkRangers,\
OttawaSenators,\
PhiladelphiaFlyers,\
PittsburghPenguins,\
San JoseSharks,\
St.LouisBlues,\
Tampa BayLightning,\
TorontoMapleLeafs,\
VancouverCanucks,\
VegasGoldenKnights,\
WashingtonCapitals,\
WinnipegJets"

def universalGet(*args):
    xData = request.urlopen(''.join(args))
    xResponse = json.loads(xData.read().decode('utf-8'))
    return xResponse

def addTeams():
    teamsResponse = universalGet(BASE_URL,TEAMS_ENDPOINT)

    for item in teamsResponse['teams']:
        write = DB.collection(u'teams').document(item['abbreviation'])
        write.set({
            u'id': item['id'],
            u'link': item['link'],
            u'name': item['name'],
        })

def getTeamIDs():
    teams_docs = DB.collection(u'teams').stream()
    teams = []
    for doc in teams_docs:
        row = doc.to_dict()
        teams.append(str(row['id']) + '/')
    return teams

TEAM_IDs = None #getTeamIDs()

def addPlayers():
    for teamID in TEAM_IDs:
        playerResponse = universalGet(BASE_URL + TEAMS_ENDPOINT + teamID + ROSTER_ENDPOINT)

        for player in playerResponse['roster']:
            write = DB.collection(u'players').document(''.join(player['person']['fullName'].split()))
            write.set({
                u'id': player['person']['id'],
                u'link': player['person']['link'],
                u'fullName': player['person']['fullName'],
                u'teamId': teamID,
            })

response = requests.get(WIKI_URL)
soup = BeautifulSoup(response.content, 'html.parser')
table = soup.find('th', style='background:#ddf; width:34.0%;').find_parents('tbody')



