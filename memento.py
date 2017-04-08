# Memento Deadline. Execution file.
# Author: Mironenko D., 2017.
import memories, deadline, tkinter, visual, pdb

full = deadline.upload_all_deadlines()
#actual = []
#for listName in full.keys():
#	actual += deadline.near_dates(full[listName], memories.OPTIONS['NotifyDays'])

if len(full) > 0:
  alarm = visual.MainWindow()
  #pdb.set_trace()
  alarm.tasks.upload_from_lists(full)
  alarm.mainloop()
	
  deadline.update_events(full)

