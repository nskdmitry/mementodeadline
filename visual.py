# Memonto Deadline. GUI interface module
from tkinter import *
from memories import *
import os, deadline, pdb

#
# Implements
#

def openList(listName):
  def openOnNotepad():
    os.system('notepad '+listName+'.txt')
  return openOnNotepad

def days_after(days):
  return str(days) + ' дней назад' if days > 4 else str(days) + ' дня назад' if days > 1 else 'вчера' if days == 1 else 'ещё успеешь' if days == 0 else days_after(-days)

def days_for_event(days):
  return 'через ' + str(days) + ' дней' if days > 4 else 'через ' + str(days) + ' дня' if days > 1 else 'завтра' if days == 1 else 'уже сегодня' if days == 0 else days_after(days)

PRINTABLE = {
  'Events': lambda item: "" if len(item) == 0 else "%s %s (%s). Смотри, не опоздай! Готов на %d из 100." % (item['name'],
           days_for_event(item['time'].days),
           item['date'].strftime(deadline.date_format),
           item['compleaty']),
  'Cargo': lambda item: "" if len(item) == 0 else "%s %s (%s) %d. Выполнено на %d из 100." % (item['name'],
           days_after(item['time'].days),
           item['date'].strftime(deadline.date_format),
		   item['years'],
           item['compleaty']),
  'Bithday': lambda item: "" if len(item) == 0 else "%s %s (%s). Исполняется %d лет. Готов на %d из 100." % (item['name'],
           days_for_event(item['time'].days),
           item['date'].strftime(deadline.date_format),
		   item['years'],
           item['compleaty']),
  'Dates': lambda item: "" if len(item) == 0 else "%s %s (%s). %d годовщина. Готов на %d из 100." % (item['name'],
           days_for_event(item['time'].days),
           item['date'].strftime(deadline.date_format),
		   item['years'],
           item['compleaty']),
  'Elapsed': lambda item: "" if len(item) == 0 else "%s %s (%s). Смотри, не опоздай! Готов на %d из 100." % (item['name'],
           days_for_event(item['time'].days),
           item['date'].strftime(deadline.date_format),
           item['compleaty']),
  'Usualy': lambda item: "" if len(item) == 0 else "Минимум раз за %s нужно %s." % (item["compleate"], item['name'])}
		   
#
# Widget classes of GUI
#

# List of event definitions
class DeadlineView(Listbox):
  def __init__(self, master, events, mainIndexVar, compleateIntVar):
    scrollItems = Scrollbar(master)
    scrollMessage = Scrollbar(master)
    Listbox.__init__(self, master=master, width=200, height=OPTIONS["ItemsWatch"], xscrollcommand=scrollMessage.set, yscrollcommand=scrollItems.set)
    self.index = mainIndexVar
    self.compleate = compleateIntVar
    self.events = events
		
    def update_scale(event):
      w = event.widget
      i = w.curselection()
      if len(i) == 1:
        if i[0] >= 0: self.index.set(i[0])
        self.compleate.set(events[self.index.get()]['compleaty'])
    self.bind("<<ListboxSelect>>", update_scale)

  # Unfiltration adding deadlines list to display
  def addItems(self, deadlines):
    if len(deadlines) == 0: return 0
	
    self.events += deadlines
    colorBack = "#ffffff"
    for record in deadlines:
      listName = record["category"]
      line = PRINTABLE[listName](record)
      if len(line) == 0: continue
	  
      if listName in FILES.keys(): colorBack = FILES[listName][3] 
      elif listName in LISTS.keys(): colorBack = LISTS[listName][6]
      else: return 0
	  
      self.insert(END, line)
      self.itemconfig(END, foreground=colorBack)

  # Filtration adding deadlines list to visual list box
  def upload_from_lists(self, deadlinesList, itemsLists = []):
    if len(itemsLists) == 0:
      itemsLists = LISTS.keys()
    #self.clear()
    for_display = list( filter(lambda item: item["category"] in itemsLists, deadlinesList) )
    self.addItems(for_display)

# Option dialog functional constructor
class OptionDialog(Tk):
  def __init__(self, optName, optValue):
    Tk.__init__(self)
    self.title("Настроить " + optName)
    self.minsize(280, 140)
    parameter = IntVar() if type(optValue) == int else BooleanVar()
    parameter.set(optValue)
		
    def dialog_cancel():
      OPTIONS[optName] = optValue
      self.destroy()
    def dialog_ok():
      OPTIONS[optName] = parameter.get()
      self.destroy()
		
    Label(self, text=optName).pack()
    if type(optValue) == int:
      Scale(self,
            from_=1, to=MAX_INTEGER_PARAMETER_VALUE,
            variable=parameter,
            orient=HORIZONTAL).pack(side = TOP)
    elif type(opt) == bool:
      Checkbutton(self, variable=parameter).pack(side = TOP)
    Button(self, text="OK", command=dialog_ok).pack(side = RIGHT)
    Button(self, text="Cancel", command=dialog_cancel).pack(side = RIGHT)
        
    self.mainloop()
    OPTIONS[optName] = parameter.get()

# Edition dialog of deadline.
class DeadlineEditDialog():
  def __init__(self, deadlines, id=-1, list_define = 'Events'):
    caption = "Редактировать сроки " if id > 0 else "Новые сроки "
	
    edit = Tk()
    edit.wm_geometry("%dx%d+%d+%d" % (640, 130, 50, 100))
    edit.title(caption)
	
    self.endtime = deadline.default_deadline() if id < 0 else deadlines[list_define][id]
	
    Label(edit, text = 'Название').grid(column = 0, row = 0)
    naming = Entry(edit, width=100).grid(column = 0, row = 1)
    Label(edit, text = 'Срок/дата').grid(column = 0, row = 2)
    timepicker = Entry(edit, text="").grid(column = 0, row = 3)
    Label(edit, text = 'Тип').grid(column = 1, row = 2)
    fileList = Combobox(edit).grid(column = 1, row = 3)
    notepad = Text(edit, width=250).grid(column = 0, row = 4)
    Button(edit, text="OK").grid(column = 0, row = 5)
    Button(edit, text="Cancel").grid(column = 1, row = 5)

# Main ("Alarm!") window
class MainWindow(Tk):	
  def setOption(self, param, opt):
    def callDialog():
      OptionDialog(param, opt).mainloop()
    return callDialog

  def __init__(self, events = []):
    Tk.__init__(self)
    self.wm_geometry("%dx%d+%d+%d" % (640, 130, 50, 100))
    self.title("Memento Deadline")

    index = IntVar()
    index.set(0)
    compleate = IntVar()
    compleate.set(events[index.get()]['compleaty'] if len(events) > 0 else 0)
		
    # [File Options]
    mainMenu = Menu(self)
    self.config(menu=mainMenu)

    # [File] -> [Regulary... Eventy... Close]
    fileMenu = Menu(self)
    fileMenu.add_command(label="Даты", command=openList('Regulary'))
    fileMenu.add_command(label="События", command=openList('Eventualy'))
    fileMenu.add_separator()
    fileMenu.add_command(label="Закрыть", command=self.destroy)

    # [Options] -> [Notify_for_month Items_watch_M]
    optionMenu = Menu(self)
    #pdb.set_trace()
    for (optname, optval) in OPTIONS.items():
      integer = str(optval)
      optionMenu.add_command(label=optname+': '+integer, command=MainWindow.setOption(self, optname, optval))

    # Construct menu
    mainMenu.add_cascade(label="Файл", menu=fileMenu)
    #mainMenu.add_cascade(label="Настройки", menu=optionMenu)

    # Event list
    self.tasks = DeadlineView(self, events, index, compleate)
    self.tasks.pack()
    
    def set_compleaty(event):
      sel = self.tasks.curselection()
      if len(sel) == 0 and index.get() < 0: return
        
      i = index.get() if len(sel) == 0 else sel[0] if sel[0] >= 0 else index.get()
      if (i < 0) or (len(events) == 0):  return
      events[i]['compleaty'] = compleate.get()
      self.tasks.delete(i)

      eventIndex = i
      j = 0
      keyses = list(LISTS.keys())
      while eventIndex > len(LISTS[keyses[j]]):
        eventIndex -= len(LISTS[keyses[j]])
        j += 1
      print(self.tasks.events, "[", eventIndex, "]")
      ev = self.tasks.events[eventIndex]
      line = PRINTABLE[ev['category']](ev)
      self.tasks.insert(i, line)
		
    #Scale of compleaty
    Label(self, text="Готовность: ").pack(side = LEFT)
    self.scale_compleate = Scale(self, from_=0, to=100,
                           variable=compleate,
                           orient=HORIZONTAL,
                           command=set_compleaty,
                           length=200)
    self.scale_compleate.pack(side = TOP)

