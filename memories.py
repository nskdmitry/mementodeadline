# Memento Deadline. Options, constance and shared variables
from datetime import timedelta

MAX_INTEGER_PARAMETER_VALUE = 30

OPTIONS = {'NotifyDays': 30, 'ItemsWatch': 5}

PERIOD = { 'none': timedelta(days=0), 'day': timedelta(days=1), 'weak': timedelta(days=7), 'month': timedelta(days=30), 'year': timedelta(days=365) }

# Списки, совпадающие с файлами. Storable - файл переписывается с этого списка целиком
# <listName>: (<period>, <filePath>, <storable>, <colorInListbox: #RRGGBB>, <Name>)
FILES = {
  'Events': (PERIOD['none'], 'info/Events.txt', False, "#8f0000", "События"),
  'Bithday': (PERIOD['year'], 'info/Bithdays.txt', True, "#00FF05", "Дни рождения"),
  'Dates': (PERIOD['year'], 'info/Dates.txt', True, "#5f5f5f", "Даты"),
  'Cargo': (PERIOD['none'], 'info/DeathCargo.txt', False, "#6f1f1f", "Мёртвый груз"),
  'Usualy': (PERIOD['day'], 'info/Usualy.txt', False, "#000500", "Повседневные дела"),
  'Elapsed': (PERIOD['none'], 'info/Elapsed.txt', True, "#afafaf", "Прошедшие")}

# Списки, полученные путём обработки другого списка указанной функцией-извлекателем
# <listName>: (<extractorName>, <storable?>, <file>, <listDisplayName>, <period>, <append?>, <colorInListbox: #RRGGBB>)
LISTS = {
  'Nears': ('near_dates', True, 'Dates', 'Даты', PERIOD['year'], True, "#1f001f"),
  'Actual': ('actual_events', True, 'Events', 'Ожидается', PERIOD['none'], True, "#6f0000"),
  'Bithday': ('near_dates', True, 'Bithday', 'Дни рождения', PERIOD['year'], False, "#002500"),
  'Elapsed': ('elapsed_events', False, 'Elapsed', 'Прошедшие', PERIOD['none'], False, "#ffffff"),
  'Cargo': ('death_cargo', True, 'Cargo', 'Мёртвый груз', PERIOD['none'], False, "#6f1f1f"),
  'Everyday': ('usualy_work', True, 'Usualy', 'Ежедневные дела', PERIOD['day'], True, "#00f500"),
  'Everyweak': ('usualy_work', True, 'Usualy', 'Еженедельные дела', PERIOD['weak'], True, "#005f00"),
  'Everymonth': ('usualy_work', True, 'Usualy', 'Ежемесячные дела', PERIOD['month'], True, "#004f00")}

