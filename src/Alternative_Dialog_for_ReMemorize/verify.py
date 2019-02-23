# -*- coding: utf-8 -*-

"""
- License: AGPLv3
"""

import datetime

from anki import version
from aqt import mw
from aqt.qt import *
from aqt.utils import showInfo
from anki.hooks import addHook, remHook



valid_qt_keys = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D",
"E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T",
"U", "V", "W", "X", "Y", "Z", "Space", "Tab","CapsLock","F1", "F2", "F3", "F4",
"F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12"]


default_values = {
    "access_dialog_from_reviewer": "g",
    "focus_lineedit": "r",
    "one_more_day": "f",
    "one_less_day" : "d",
    "relearn_key" : "a",
    "secondary_accept_1": "e",
    "secondary_accept_2": "space"
}


def list_to_multiline_string(list_):
    out = ""
    for i in list_:
        out += "- " + i + '\n'
    return(out)



def warn_about_illegal_settings(illegal_list):
    if illegal_list:
        msg = 'Add-on "Alternative Dialog for ReMemorize" \n' + \
                'Invalid settings were detected for these settings:  \n\n' + \
                list_to_multiline_string(illegal_list) + \
                '\nThese settings are ignored and the default values are applied. \n' + \
                'Please adjust the config.\n\n' + \
                'Hint: For technical reasons this add-on only accepts ASCII\n' + \
                'characters, numbers and some additional keys (like Fn-keys,\n' + \
                'space,..) as shortcuts. No unicode.\n\n\n'
        showInfo(msg,parent=False, help="", type="info", 
        title="Anki Add-on: Alternative Dialog for ReMemorize config") 



def verify_config(cfg):
    if cfg.get("quick_button_1_key") or cfg.get("upper_auto_correct_accept"):
        msg = "Reset the configuration of the add-on Alternative_Dialog_for_ReMemorize " + \
              '(previously named "Extended quick reschedule in reviewer") to the ' + \
              'default values. In the lower left of the config window for this add-on ' + \
              'click "Restore Defaults". \nThis is necessary because the recent update ' + \
              "of this add-on changed how it works. \nIf you don't reset and reapply " + \
              'your settings you might run into unexplainable errors. ' + \
              '\n\nFor additional information see https://ankiweb.net/shared/info/2107899486'
        showInfo(msg, title="Anki Add-on: Alternative Dialog for ReMemorize ")


    illegal_list = []
    for k,v in cfg.items():
        if (k in default_values) and (v.title() not in valid_qt_keys):
            cfg[k] = default_values[k]
            illegal_list.append(k)

    for e in ["add_entry_to_context_menu", "add_num_area_to_dialog","add_quick_buttons_to_dialog","show_tooltip",]:
        if not isinstance(cfg[e], bool):
            illegal_list.append(e)

    for e in cfg['quick_buttons']:
        if not isinstance(e['ivl'], int): 
            illegal_list.append('quick keys, label: "' + e['label'] + '", ivl: "' + e['ivl'] + '"')
        if e['key'].title() not in valid_qt_keys:
            illegal_list.append('quick keys, label: "' + e['label'] + '", key: "' + e['key'] + '"')
            e['key'] = ""  # disable so that it's not eval-ed

    warn_about_illegal_settings(illegal_list)

    cfg['access_dialog_from_reviewer']  = str(cfg["access_dialog_from_reviewer"])
    cfg['focus_lineedit']               = str(cfg["focus_lineedit"])
    cfg['one_more_day']                 = str(cfg["one_more_day"])
    cfg['one_less_day']                 = str(cfg["one_less_day"])
    cfg['relearn_key']                  = str(cfg["relearn_key"])
    cfg['secondary_accept_1']           = str(cfg["secondary_accept_1"])
    cfg['secondary_accept_2']           = str(cfg["secondary_accept_2"])

    return cfg





