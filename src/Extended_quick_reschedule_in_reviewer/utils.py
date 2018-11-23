# -*- coding: utf-8 -*-

# taken from utils.py from 
    # Copyright: (C) 2018 Lovac42
    # Support: https://github.com/lovac42/ReMemorize
    # License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
# I only added the tooltip

from aqt import mw
from aqt.utils import tooltip
from anki.utils import intTime
import random, time


#from: anki.sched.Scheduler, removed resetting ease factor, added logs
def customReschedCards(ids, imin, imax, logging=True):
    # mw.checkpoint(_("Rescheduled")) #undo state, inc siblings

    d = []
    t = mw.col.sched.today
    mod = intTime()
    for id in ids:
        card=mw.col.getCard(id)
        mw.col.markReview(card) #undo, push each sibling onto the undo stack.

        r = random.randint(imin, imax)
        ivl = max(1, r)

        #initialize new cards, just in case.
        fct=2500 if card.factor==0 else max(1300,card.factor)
        d.append(dict(id=id, due=r+t, ivl=ivl, mod=mod, usn=mw.col.usn(), fact=fct))
        if logging:
            try:
                log(card,ivl,fct)
            except:
                time.sleep(0.01) # duplicate pk; retry in 10ms
                log(card,ivl,fct)

    mw.col.sched.remFromDyn(ids)
    mw.col.db.executemany("""
update cards set type=2,queue=2,ivl=:ivl,due=:due,odue=0,
usn=:usn,mod=:mod,factor=:fact where id=:id""", d)
    mw.col.log(ids)
    return ivl


#lastIvl = card.ivl
#ease=0, timeTaken=0
#custom log type: 4 = rescheduled
def log(card, ivl, fct=0):
    delay=getDelay(card)
    logId = intTime(1000)
    mw.col.db.execute(
        "insert into revlog values (?,?,?,0,?,?,?,0,4)",
        logId, card.id, mw.col.usn(),
        ivl, -delay or card.ivl or 1, fct or card.factor )

def getDelay(card):
    if card.queue not in (1,3): return 0
    conf=mw.col.sched._lrnConf(card)
    left=card.left%1000
    return mw.col.sched._delayForGrade(conf,left) 
