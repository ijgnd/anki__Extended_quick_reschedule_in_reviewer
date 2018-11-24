# -*- coding: utf-8 -*-

"""
- License: AGPLv3
- some important/core functions are taken/modified from ReMemorize, https://ankiweb.net/shared/info/323586997
  Copyright (C) 2018 lovac42
  see the lines below "code taken from"
- this add-on is  mostly a nicer skin for some of the functions from ReMemorize

configuration is set in the file config.json
"""

import os
import datetime
import json
import random
import time
from heapq import *
from codecs import open

from anki import version
ANKI21 = version.startswith("2.1.")

from aqt import mw
from aqt.qt import *
from aqt.utils import tooltip, showInfo
from aqt.reviewer import Reviewer
from anki.hooks import addHook, remHook
from anki.utils import intTime

if ANKI21:
    from PyQt5.QtCore import Qt
    from PyQt5.QtCore import QTimer
else:
    from PyQt4.QtCore import Qt
    from PyQt4.QtCore import QTimer



from . import mydialog
from . import verify
from . import rememorize
from . import utils
from . import limit


#this weird layout to load shortcut/context menu so that is runs only after checking all
#user settings once the profile has loaded

if not ANKI21:
    origKeyHandler = Reviewer._keyHandler
def addShortcuts20(self, evt):
    k = unicode(evt.text())
    if k == co['access_dialog_from_reviewer']:
        #mw.checkpoint(_("Reschedule card"))
        promptNewInterval()
        #mw.reset()
    else:
        origKeyHandler(self, evt)


def reviewerContextMenu20(self, m):
    #self is Reviewer
    a = m.addAction('reschedule')
    a.connect(a, SIGNAL("triggered()"),lambda s=self: promptNewInterval())



def addShortcuts21(shortcuts):
    additions = (
        (co['access_dialog_from_reviewer'], promptNewInterval),
    )
    shortcuts += additions


def reviewerContextMenu21(view, menu):
    if mw.state != "review":
        return
    self = mw.reviewer
    opts = [
        [_("reschedule"), "", promptNewInterval],
    ]
    self._addMenuItems(menu, [None, ])
    self._addMenuItems(menu, opts)



def entry_for_21__contextmenu_shortcut():
    addHook("reviewStateShortcuts", addShortcuts21)
    if co['add_entry_to_context_menu']:
        addHook('AnkiWebView.contextMenuEvent', reviewerContextMenu21)


def entry_for_20__contextmenu_shortcut():
    Reviewer._keyHandler = addShortcuts20
    if co['add_entry_to_context_menu']:
        addHook("AnkiWebView.contextMenuEvent", reviewerContextMenu20)



def reload_config(config):
    global co
    co = verify.verify_config(config)


def load_config(config):
    addHook('profileLoaded', lambda: reload_config(config))

    if ANKI21:
        addHook('profileLoaded', entry_for_21__contextmenu_shortcut)
    else:
        addHook('profileLoaded', entry_for_20__contextmenu_shortcut)


if ANKI21:
    load_config(mw.addonManager.getConfig(__name__))
    mw.addonManager.setConfigUpdatedAction(__name__,reload_config) 

else:
    moduleDir, _ = os.path.split(__file__)
    path = os.path.join(moduleDir, 'config.json')
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            data=f.read()
        try:
            load_config(json.loads(data))
        except:
            showInfo('Add-on Extended Quick Reschedule in Reviewer:\n\n' + 
                    'config file is not a valid json file. Edit your\n' + 
                    '"config.json" and restart.\n\n' +
                    'Maybe these hints are useful for you:\n' +
                    '- In json there may NOT be a comma behind the last entry.\n' + 
                    '- Keys and values are separated by ":".\n' + 
                    '- true and false are lower case.\n'
                    '- everything apart from true, false, and numbers \n' + 
                    '  must be surrounded with "".\n\n' +
                    'Your config.json is ignored. Loading default config ...'
                    )
            path = os.path.join(moduleDir, 'backup_config_for_20.json')
            with open(path, 'r', encoding='utf-8') as f:
                data=f.read()
            load_config(json.loads(data))




def promptNewInterval():
    card = mw.reviewer.card
    m=mydialog.MultiPrompt(co)

    m.setFixedSize(739, 68)  # m.setFixedSize(m.size())
    if co['add_num_area_to_dialog'] or co['add_quick_buttons_to_dialog']:
        m.setFixedSize(739, 330)
    if m.exec_():  # True if dialog is accepted, https://stackoverflow.com/a/11553456
        if m.lower == 0 and m.upper == 0:
            mw.col.sched.forgetCards([card.id])
            if co['show_tooltip']:
                tooltip('card reset')
        else:
            if m.upper > limit.upper_under_exam_date_or_deck_maxIvl(card,co['final_latest_date'],m.upper):
                m.upper = limit.upper_under_exam_date_or_deck_maxIvl(card,co['final_latest_date'],m.upper)
                m.lower = max(int(round(m.upper  * (100.0-co['upper_auto_correct_fuzz_in_percent'])/100)),1)
            if co['revlog_rescheduled']:
                rememorize.updateStats(card)
            ivl = utils.customReschedCards( [card.id], m.lower, m.upper )
            if co['show_tooltip']:
                tooltip('card rescheduled with interval of %d' %ivl)
            mw.reviewer._answeredIds.append(card.id)
            mw.autosave()
        mw.reset()
    else:
        tooltip('declined')


