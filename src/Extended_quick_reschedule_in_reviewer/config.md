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
- `focus_lineedit`: button that resets the focus to the area where you input the
  digits
- `relearn_key`: this reschedules a card as new
- `one_more_day`, `one_less_day` : increase/decrease value in lineedit by one
  day
- `quick_buttons`:
    - `key`: shortcut in the reschedule dialog
    - `label` : text that's on the button 
    - `ivl`: new interval. If you set in the ReMemorize settings fuzz_days to true, this value will be modified. 
  rescheduled with the same interval use the same number twice
- `secondary_accept_1`, `secondary_accept_2`: keys that close the dialog and
  apply the number you entered into the text/linedit field. The motivation for
  these options is that this allows you to reschedule without the need to press
  Enter (or Tab-Space), i.e. you can quickly use the add-on with just the left
  hand. 
- `show_tooltip`: whether you want feedback after rescheduling



