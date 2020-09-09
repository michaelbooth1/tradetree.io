from DraftPick import DraftPick
from random import randint


def checkIfDraftPick(self, item, team):
    for i in item:
        if isinstance(i, str) and 'round pick' in i:
            splitPick = i.split()
            if 'conditional' in splitPick:
                pickUUID = '.'.join([splitPick[0], splitPick[2], team[0]])
                pick = DraftPick(pickUUID, splitPick[0], splitPick[2], team[0], True)
            else:
                pickUUID = '.'.join([splitPick[0], splitPick[1], team[0]])
                pick = DraftPick(pickUUID, splitPick[0], splitPick[1],team[0], False)
            item[item.index(i)] = pick

    return item


class Trade:
    def __init__(self, tradeId, sTeam, rTeam, date, sItems, rItems):
        self.tradeId = tradeId
        self.sTeam = rTeam
        self.rTeam = sTeam
        self.date = date
        self.sItems = checkIfDraftPick(self, sItems, self.sTeam)
        self.rItems = checkIfDraftPick(self, rItems, self.rTeam)





