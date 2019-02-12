# -*- coding: utf-8 -*-

"""
- this add-on is just a nicer skin for some function of
   ReMemorize, Copyright (C) 2018 lovac42
   https://ankiweb.net/shared/info/323586997
   
- this add-on Copyright (C) 2018, 2019 ignd

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.



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
from anki.hooks import addHook, runHook
from anki.utils import intTime

if ANKI21:
    from PyQt5.QtCore import Qt
    from PyQt5.QtCore import QTimer
else:
    from PyQt4.QtCore import Qt
    from PyQt4.QtCore import QTimer



from . import mydialog
from . import verify



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
    print(co)


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

    if m.exec_():  # True if dialog is accepted, https://stackoverflow.com/a/11553456
        if m.days == 0:
            runHook("ReMemorize.forget", card) 
        elif m.days < 0:
            runHook("ReMemorize.changeDue", card, abs(m.days))
        elif m.days > 0:
            runHook("ReMemorize.reschedule", card, m.days)                   
        if co['show_tooltip']:
            tooltip('card rescheduled with interval of about %d days (small randomization may apply)' %abs(m.days))
        mw.reviewer._answeredIds.append(card.id)
        mw.autosave()
        mw.reset()
    else:
        tooltip('declined')


