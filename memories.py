# Memento Deadline. Options, constance and shared variables
from datetime import timedelta

MAX_INTEGER_PARAMETER_VALUE = 30

OPTIONS = {'NotifyDays': 30, 'ItemsWatch': 5}

PERIOD = { 'none': timedelta(days=0), 'day': timedelta(days=1), 'weak': timedelta(days=7), 'month': timedelta(days=30), 'year': timedelta(days=365) }

# Списки, совпадающие с файлами. Storable - файл переписывается с этого списка
# <listName>: (<period>, <filePath>, <storable>)
FILES = {
      'Dates': (PERIOD['year'], 'info/Dates.txt', True),
      'Events': (PERIOD['none'], 'info/Events.txt', False),
      'Cargo': (PERIOD['none'], 'info/DeathCargo.txt', False),
      'Usualy': (PERIOD['day'], 'info/Usealy.txt', True)
    }

# Списки, полученные путём обработки другого списка указанной функцией-извлекателем
# <listName>: (<extractorName>, <storable>, <saveInFile>, <listDisplayName>, <period>, <append?>)
LISTS = {
      'Nears': ('near_dates', True, FILES['Dates'][1], 'Даты', PERIOD['year'], True),
      'Actual': ('actual_events', True, FILES['Events'][1], 'Ожидается', PERIOD['none'], True),
      'Elapsed': ('elapsed_events', False, '', 'Прошедшие', PERIOD['none'], False),
      'Cargo': ('death_cargo', True, FILES['Cargo'][1], 'Мёртвый груз', PERIOD['none'], False),
      'Everyday': ('usualy_work', True, FILES['Usualy'][1], 'Ежедневные дела', PERIOD['day'], True),
      'Everyweak': ('usualy_word', True, FILES['Usualy'][1], 'Еженедельные дела', PERIOD['weak'], True),
      'Everymonth': ('usualy_word', True, FILES['Usualy'][1], 'Ежемесячные дела', PERIOD['month'], True)
    }
