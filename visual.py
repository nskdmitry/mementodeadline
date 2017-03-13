# Memonto Deadline. GUI interface module
from tkinter import *
import memories, os, deadline, pdb

#
# Implements
#

def openList(listName):
    def openOnNotepad():
        os.system('notepad '+listName+'.txt')
    return openOnNotepad

def event_line(item):
    return "%s %s (%s). %s Готов на %d из 100." % (item['name'],
                 'через ' + str(item['time'].days) + ' дней' if item['time'].days > 4 else 'через ' + str(item['time'].days) + ' дня' if item['time'].days > 1 else 'завтра' if item['time'].days == 1 else 'уже сегодня' if item['time'].days == 0 else 'было ' + str(item['time'].days) + 'назад',
                 item['date'].strftime(deadline.date_format),
                 str(item['years']) + ' лет этому событию.' if item['regulary'] else 'Смотри, не опоздай!',
                 item['compleaty'])

#
#  GUI constructors
#

# Option dialog functional constructor
def setOption(param, opt):
    def optionWindow():
        dialog = Tk()
        dialog.title("Настроить " + param)
        dialog.wm_geometry("280x140")
        parameter = IntVar() if type(opt) == int else BooleanVar()
        parameter.set(opt)
        
        def dialog_cancel():
            memories.OPTIONS[param] = opt
            dialog.destroy()

        def dialog_ok():
            memories.OPTIONS[param] = parameter.get()
            dialog.destroy()
        
        Label(dialog, text=param).pack()
        if type(opt) == int:
            Scale(dialog,
                  from_=1, to=memories.MAX_INTEGER_PARAMETER_VALUE,
                  variable=parameter,
                  orient=tkinter.HORIZONTAL).pack(side = TOP)
        elif type(opt) == bool:
            Checkbutton(dialog, variable=parameter).pack(side = TOP)
        okSet = Button(dialog, text="OK", command=dialog_ok)
        oldSet = Button(dialog, text="Cancel", command=dialog_cancel)
        okSet.pack(side = RIGHT)
        oldSet.pack(side = RIGHT)
        
        dialog.mainloop()

        memories.OPTIONS[param] = parameter.get()
    return optionWindow

#
# Main (Alarm!) window/dialog
#
def alarm_dialog(events):
    info = map(event_line, events)
    
    alarmW = Tk()
    alarmW.wm_geometry("%dx%d+%d+%d" % (640, 130, 50, 100))
    alarmW.title("Memento Deadline")

    index = 0
    compleate = IntVar()
    compleate.set(events[index]['compleaty'])

    def update_scale(event):
        w = event.widget
        i = w.curselection()
        if len(i) == 1:
            if i[0] >= 0:
                index = i[0]
            #print(i, index)
            compleate.set(events[index]['compleaty'])

    def focus_out(event):
        print(index, compleate.get(), events[index]['compleaty'])
    
    # [File Options]
    mainMenu = Menu(alarmW)
    alarmW.config(menu=mainMenu)

    # [File] -> [Regulary... Eventy... Close]
    fileMenu = Menu(alarmW)
    fileMenu.add_command(label="Даты", command=openList('Regulary'))
    fileMenu.add_command(label="События", command=openList('Eventualy'))
    fileMenu.add_separator()
    fileMenu.add_command(label="Закрыть", command=alarmW.destroy)

    # [Options] -> [Notify_for_month Items_watch_M]
    optionMenu = Menu(alarmW)
    for (optname, optval) in memories.OPTIONS.items():
        integer = str(optval)
        optionMenu.add_command(label=optname+': '+integer, command=setOption(optname, optval))

    # Construct menu
    mainMenu.add_cascade(label="Файл", menu=fileMenu)
    mainMenu.add_cascade(label="Настройки", menu=optionMenu)

    # Event list
    scrollItems = Scrollbar(alarmW)
    scrollMessage = Scrollbar(alarmW)
    tasks = Listbox(alarmW,
                    width=200, height=memories.OPTIONS['ItemsWatch'],
                    xscrollcommand=scrollMessage.set,
                    yscrollcommand=scrollItems)
    for i, line in enumerate(info):
        tasks.insert(i, line)
    tasks.pack()
    tasks.bind("<<ListboxSelect>>", update_scale)
    tasks.bind("<<ListboxFocusOut>>", focus_out)

    def set_compleaty(event):
        sel = tasks.curselection()
        #print(index)
        if len(sel) == 0 and index < 0:
            return
        
        i = index if len(sel) == 0 else sel[0] if sel[0] >= 0 else index
        if i < 0:
            return
        events[i]['compleaty'] = compleate.get()
        tasks.delete(i)

        ev = events[i]
        line = event_line(ev)
        tasks.insert(i, line)

    #Scale of compleaty
    Label(alarmW, text="Готовность: ").pack(side = LEFT)
    scale_compleate = Scale(alarmW, from_=0, to=100,
                           variable=compleate,
                           orient=HORIZONTAL,
                           command=set_compleaty,
                           length=200)
    scale_compleate.pack(side = TOP)
    
    return alarmW
