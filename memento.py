
# Memento Deadline.
# Author: Mironenko D., 2017.
import memories, deadline, tkinter, visual, pdb

full = deadline.upload_all_dates()
actual = deadline.near_dates(full, memories.OPTIONS['NotifyDays'])

#pdb.set_trace()

if len(actual) > 0:
    alarm = visual.alarm_dialog(actual)
    alarm.mainloop()
    
    deadline.update_events(full)
