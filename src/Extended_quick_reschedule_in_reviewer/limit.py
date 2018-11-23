# -*- coding: utf-8 -*-
#License: AGPLv3

import datetime

from aqt import mw


def deadline_for_did(didlist, deadlinelist):
    latest = False  
    for did in didlist:
        parent_ids = [x['id'] for x in mw.col.decks.parents(did)] 
        relevant_ids = [did] + parent_ids 
        for i in relevant_ids:
            d = mw.col.decks.get(i)
            if isinstance(deadlinelist, dict):
                if d['name'] in deadlinelist:
                    thismaxdate = datetime.datetime.strptime(deadlinelist[d['name']],'%Y-%m-%d') 
                    if latest == False:
                        latest = thismaxdate
                    elif thismaxdate < latest:
                        latest = thismaxdate
    return latest


def upper_under_exam_date_or_deck_maxIvl(card,deadlinelist,upper):
    decks = mw.col.decks
    if card.odid:    
        latestAsDTO = deadline_for_did([card.did,card.odid],deadlinelist)
    else:
        latestAsDTO = deadline_for_did([card.did],deadlinelist)

    if latestAsDTO:
        return (latestAsDTO - datetime.datetime.now()).days + 1    #+1 to also include the last day
    else:
        if card.odid:
            conf = decks.confForDid(card.odid)
        else:
            conf = decks.confForDid(card.did)
        return conf['rev']['maxIvl']    
