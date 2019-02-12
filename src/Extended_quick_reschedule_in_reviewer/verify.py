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
    "quick_button_1_key" : "t",
    "quick_button_2_key" : "g",
    "quick_button_3_key" : "b",
    "relearn_key" : "f",
    "secondary_accept_1": "e",
    "secondary_accept_2": "space"
}

default_button_ivls = {
    "quick_button_1_lower":7,
    "quick_button_1_upper":7,
    "quick_button_2_lower":28,
    "quick_button_2_upper":32,
    "quick_button_3_lower":330,
    "quick_button_3_upper":390
}


def list_to_multiline_string(list_):
    out = ""
    for i in list_:
        out += "- " + i + '\n'
    return(out)




def warn_about_illegal_settings(illegal_list):
    if illegal_list:
        msg = 'Add-on Extended Quick Reschedule in Reviewer \n' + \
                'Invalid settings were detected for these settings:  \n\n' + \
                list_to_multiline_string(illegal_list) + \
                '\nThese settings are ignored and the default values are applied. \n' + \
                'Please adjust the config.\n\n' + \
                'Hint: For technical reasons this add-on only accepts ASCII\n' + \
                'characters, numbers and some additional keys (like Fn-keys,\n' + \
                'space,..) as shortcuts. No unicode.\n\n\n'

        if any('invalid date' in s for s in illegal_list) or any('nonexistend deck' in s for s in illegal_list):
            msg += 'If you use a version from before 2018-11-22: More recent\n' +\
                'versions of this add-on verify the deck names in\n' + \
                '"final_latest_date" so that a typo doesn\'t disable the\n' + \
                'exam mode silently. Old versions of this add-on had \n' + \
                'some deck names set as examples. These examples will throw \n' + \
                'an error now. To remove the values for "final_latest_date" \n' + \
                'you need to change your settings once.\n'

            if version.startswith("2.1."):
                msg += 'Go to Tools>Add-ons, select the add-on and click on "Config", \n' + \
                'to disable the exam mode set: \n' + \
                '    "final_latest_date": false,   \n' +\
                'After this go to the Deck overview and only then resume your \n' + \
                'reviews.'
            else:
                msg += 'Open the add-on folder and edit the file "config.json" in the\n' +\
                'folder "Extended_quick_reschedule_in_reviewer" with a text \n' + \
                'editor. To disable the exam mode set \n ' + \
                '    "final_latest_date": false,   '
                msg += '\n\nRestart Anki after changing the settings.' 
        showInfo(msg,parent=False, help="", type="info", 
        title="Anki Add-on: Extended quick reschedule in reviewer config") 


def validate_yyyymmdd(date_text):    #https://stackoverflow.com/a/16870699
    try:
        datetime.datetime.strptime(date_text, '%Y-%m-%d')
    except ValueError:
        return False
    else:
        return True 


def process_dict(dict_):
    dlist = [x['name'] for x in mw.col.decks.all()]
    out = []
    if not isinstance(dict_, dict):
        out.append('final_latest_date--not_a_dictionary')
    else:
        for k,v in dict_.items():
            if not validate_yyyymmdd(v):
                out.append('invalid date: "%s"' % v)
            if not k in dlist:
                out.append('nonexistend deck: "%s"' % k)
    return out


def verify_config(cfg):
    illegal_list = []
    for k,v in cfg.items():
        if (k in default_values) and (v.title() not in valid_qt_keys):
            cfg[k] = default_values[k]
            illegal_list.append(k)

    for e in ["add_entry_to_context_menu", "add_num_area_to_dialog","add_quick_buttons_to_dialog",
            "revlog_rescheduled","show_tooltip","upper_auto_correct_accept"]:
        if not isinstance(cfg[e], bool):
            illegal_list.append(e)

    if cfg["final_latest_date"]:  
        ret = process_dict(cfg["final_latest_date"])
        if ret:
            for i in ret:
                illegal_list.append(i)

    for k,v in cfg.items():
        if k in default_button_ivls:
            if not isinstance(v, int):
                cfg[k] = default_button_ivls[k] 
                illegal_list.append(k)

    if cfg["quick_button_1_lower"] > cfg["quick_button_1_upper"]:
        illegal_list.append("quick_button_1_lower is greater than quick_button_1_upper")  
        cfg["quick_button_1_lower"] = default_button_ivls["quick_button_1_lower"]
        cfg["quick_button_1_upper"] = default_button_ivls["quick_button_1_upper"]

    if cfg["quick_button_2_lower"] > cfg["quick_button_2_upper"]:
        illegal_list.append("quick_button_2_lower is greater than quick_button_2_upper")       
        cfg["quick_button_2_lower"] = default_button_ivls["quick_button_2_lower"]
        cfg["quick_button_2_upper"] = default_button_ivls["quick_button_2_upper"]

    if cfg["quick_button_3_lower"] > cfg["quick_button_3_upper"]:
        illegal_list.append("quick_button_3_lower is greater than quick_button_3_upper")        
        cfg["quick_button_3_lower"] = default_button_ivls["quick_button_3_lower"]
        cfg["quick_button_3_upper"] = default_button_ivls["quick_button_3_upper"]

    warn_about_illegal_settings(illegal_list)

    cfg['access_dialog_from_reviewer']  = str(cfg["access_dialog_from_reviewer"])
    cfg['focus_lineedit']               = str(cfg["focus_lineedit"])
    cfg['one_more_day']                 = str(cfg["one_more_day"])
    cfg['one_less_day']                 = str(cfg["one_less_day"])
    cfg['qb1_key']                      = str(cfg["quick_button_1_key"])
    cfg['qb2_key']                      = str(cfg["quick_button_2_key"])
    cfg['qb3_key']                      = str(cfg["quick_button_3_key"])
    cfg['relearn_key']                  = str(cfg["relearn_key"])
    cfg['secondary_accept_1']           = str(cfg["secondary_accept_1"])
    cfg['secondary_accept_2']           = str(cfg["secondary_accept_2"])

    return cfg
