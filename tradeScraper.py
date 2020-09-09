import requests
from bs4 import BeautifulSoup
from Trade import Trade
from DraftPick import DraftPick
from Database import get_database

URL_ID = 1
tradeList = []
ID = 0
BASE_YEAR = 2010
DB = get_database()
indexId = 0
pickIndexId = 0

while BASE_YEAR != 2020:
    while True:
        URL = 'http://www.nhltradetracker.com/user/trade_list_by_season/' + str(BASE_YEAR) + ''.join(["-", str(int(str(BASE_YEAR)[2:]) + 1) ,"/"]) + str(URL_ID)
        response = requests.get(URL)
        soup = BeautifulSoup(response.content, 'html.parser')

        findTradeItems = soup.findAll('td', width='75%')
        findDate = soup.findAll('td', width='20%')
        findTeams = soup.findAll('td', width='40%')

        if len(findDate) == 0:
            break

        teams = []
        dates = []
        items = []

        for i in findTradeItems:
            toAppend = []
            for item in i.findAll('span'):
                toAppend.append(item.text.strip())
            items.append(toAppend)

        for d in findDate:
            dates.append([d.text]) if d.text != 'Date' else None

        for t in findTeams:
            teams.append([' '.join((t.text.split())[:-1])]) if not t.has_attr('valign') else None

        for x in range(len(dates)):
            tradeList.append(Trade(ID, teams[x * 2], teams[x * 2 + 1], dates[x], items[x * 2], items[x * 2 + 1],))
            ID += 1

        URL_ID += 1

    URL_ID = 1
    BASE_YEAR += 1

for trade in tradeList:

    for x in trade.sItems:
        write = DB.collection(u'trades').document(str(indexId))
        write.set({
            u'id': trade.tradeId,
            u'sendingTeam': trade.sTeam,
            u'receivingTeam': trade.rTeam,
            u'date': trade.date,
            u'item': x.draftId if isinstance(x, DraftPick) else x
        })
        if isinstance(x, DraftPick):
            write = DB.collection(u'picks').document(str(pickIndexId))
            write.set({
                u'id': x.draftId,
                u'year': x.year,
                u'round': x.round,
                u'team': x.team,
                u'conditional': x.conditional
            })
            pickIndexId += 1
        indexId += 1

    for y in trade.rItems:
        write = DB.collection(u'trades').document(str(indexId))
        write.set({
            u'id': trade.tradeId,
            u'sendingTeam': trade.rTeam,
            u'receivingTeam': trade.sTeam,
            u'date': trade.date,
            u'item': y.draftId if isinstance(y, DraftPick) else y
        })
        if isinstance(y, DraftPick):
            write = DB.collection(u'picks').document(str(pickIndexId))
            write.set({
                u'id': y.draftId,
                u'year': y.year,
                u'round': y.round,
                u'team': y.team,
                u'conditional': y.conditional
            })
            pickIndexId += 1
        indexId += 1