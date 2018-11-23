Anki sorts the names of configuration options alphabetically. To get a proper
order some options got unusual names. Changes for `access_dialog_from_reviewer`
and `add_entry_to_context_menu` only take effect after a restart - the rest of
of the options is applied without a restart in 2.1. If you change the settings 
while reviewing you need to go back to the main screen and restart your reviews
for the changes to take effect.

When you make changes keep this in mind:

- everything apart from true, false, and numbers must be surrounded with "". 
- true and false must be lower case.
- for shortcuts only use letters, numbers and F-keys. Some of these may not
  work.

options:

- `access_dialog_from_reviewer` - key that needs to be pressed in the reviewer
  to open the reschedule dialog. You should only use a key that's not used by
  Anki for something different.
- `add_entry_to_context_menu`: if true, there's an entry in the context menu of
  the reviewer (the menu you see after you right click on the card)
- `add_num_area_to_dialog` if true, then touch-friendly buttons to enter the
  next interval are shown
- `add_quick_buttons_to_dialog`: if true, show buttons (and use shortcuts) to
  reschedule for a fixed period (see quick_button options below)
- `final_latest_date`: [beta] If you want to make sure that you don't accidently
  reschedule your card for a date that's too far in the future, e.g. if you have
  an exam. This setting works per deck. If you set here a deck that doesn't
  exist that setting will be ignored. If you use a filtered deck the limit of
  the source deck is also applied. Limits of parent decks are also applied. If
  you don't set a limit for a deck here the setting for Maximum Interval from
  your deck options is used (so that no invalid values can be written to the
  database). As a precaution I label this "beta - might not work" because no
  other Anki developer has verified the code yet. But it works for me. 
- `focus_lineedit`: button that resets the focus to the area where you input the
  digits
- `relearn_key`: this reschedules a card as new
- `one_more_day`, `one_less_day` : increase/decrease value in lineedit by one
  day
- `quick_button_1_key`, : shortcut in the reschedule dialog
- `quick_button_1_label` : text that's on the button 
- `quick_button_1_lower` : lower limit for new interval
- `quick_button_1_upper` : upper limit for new interval. If all cards should be
  rescheduled with the same interval use the same number twice
- `secondary_accept_1`, `secondary_accept_2`: keys that close the dialog and
  apply the number you entered into the text/linedit field. The motivation for
  these options is that this allows you to reschedule without the need to press
  Enter (or Tab-Space), i.e. you can quickly use the add-on with just the left
  hand. 
- `revlog_rescheduled` : whether an entry is added to the table of prior
  revisions of this card
- `show_tooltip`: whether you want feedback after rescheduling
- `upper_auto_correct_accept`: whether the setting from
  upper_auto_correct_fuzz_in_percent should be applied
- `upper_auto_correct_fuzz_in_percent`: When I set a date for a deck in
  final_latest_date I don't want all cards whose next due date is limited by
  final_latest_date to be shown on the date set in final_latest_date. Otherwise
  I might have many cards due on this one day. Instead I like to spread out the
  dates over a couple of days. The variable upper_auto_correct_fuzz_in_percent
  determines from which time span the the new capped interval will be chosen:
  zero means the review will be on the latest day possible, 100 means the review
  can be on any day between today and the latest day possible.


