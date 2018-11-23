# -*- coding: utf-8 -*-

# taken from rememorize.py
# Copyright: (C) 2018 Lovac42
# Support: https://github.com/lovac42/ReMemorize
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

from aqt import mw

def updateStats(card): #subtract count from new/rev queue
    if card.queue == 0:
        mw.col.sched._updateStats(card, 'new')
    else:
        mw.col.sched._updateStats(card, 'rev')  
