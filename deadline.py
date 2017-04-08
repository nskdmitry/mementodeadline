# Memento Deadline. Deadlines + Input/Output.
import datetime, time, memories, os, pdb, sys

current_day = datetime.date.today()
date_format = "%d.%m.%Y"
record_format = "%s\t%s\t%s\t%d"
now_it = datetime.timedelta(days=0)
date_period = datetime.timedelta(days=365)

CLASSIFICATOR = {
  
}

def default_deadline(is_turning = False, category = 'Actual'):
  return {
    'date': current_day,
    'name': 'New deadline',
    'note': 'Description of event',
    'compleaty': 0,
    'regulary': is_turning,
    'time': now_it,
    'years': 0,
    'category': category}

def set_category(category):
  def setter_category(deadline):
    return {
      'date': deadline['date'],
      'name': deadline['name'],
      'note': deadline['note'],
      'compleaty': deadline['compleaty'],
      'regulary': deadline['regulary'],
      'time': deadline['time'],
      'years': deadline['years'] if 'years' in deadline else 0,
      'category': category}
  return setter_category
	
def load_list(items, path, period = now_it, category = 'Actual'):
  if not os.path.exists(path):
    return items
    
  with open(path, "r") as f:
    while True:
      line = f.readline()
      if not line: break
      inf = line.split("\t")
      if len(inf) == 4:
        dateOf = datetime.datetime.strptime(inf[0], date_format).date()
        # Calculate this deadline on this year
        byYear = period.days // 365
        byMonth = (period.days - byYear * 365) // 30
        byDay = period.days - byYear * 365 - byMonth * 30
        nextDate = dateOf.replace(year= current_day.year if byYear > 0 else dateOf.year,
                                  month= current_day.month if byMonth > 0 else dateOf.month,
                                  day= current_day.day if byDay > 0 else dateOf.day)
        items.append({
		  'date': dateOf, 'name': inf[1], 'note': inf[2], 'category': category,
          'compleaty': int(inf[3]), 'regulary': period.days > 0,
          'time': nextDate - current_day, 'years': (dateOf.year - current_day.year)})
  items.sort(key=(lambda item: -item['time'].days))
  return items

def upload_deadlines(listName, deadlines):
  if listName in memories.FILES.keys():
    listDef = memories.FILES[listName]
    return load_list(deadlines, listDef[1], listDef[0], listName)
  elif listName in memories.LISTS.keys():
    listDef = memories.LISTS[listName]
    call = getattr(sys.modules[__name__], listDef[0])
    return call(deadlines, listDef[4], listName)
  return deadlines

def upload_all_deadlines(names = memories.LISTS.keys()):
  deadlines = []
  alls = {}
  for listName in memories.FILES:
    alls[listName] = upload_deadlines(listName, [])
  for listName in names:
    lyst = alls[listName] if listName in alls  else []
    listDef = memories.LISTS[listName]
    call = getattr(sys.modules[__name__], listDef[0])
    deadlines += list(map(set_category(listName), call(lyst, listDef[4].days)))
  return deadlines

# Extract a events lists by category

def near_dates(full, time):
  dt = datetime.timedelta(days=time)
  return list(filter(lambda item: (item["time"] <= dt) and (item["time"] >= now_it), full))

def actual_events(full, period):
  return list(filter(lambda item: (not item["regulary"] and (item["time"] >= now_it)), full))

def regulary_events(full, period):
  return list(filter(lambda item: item["regulary"], full))

# exterminating from list data
def death_cargo(full, period):
  return list(filter(lambda item: not item["regulary"] and (item["time"] < now_it) and (item["compleaty"] < 100), full))

def elapsed_events(full, period):
  return list(filter(lambda item: item["regulary"] and item["compleaty"] == 100 and item["time"] < now_it, full))

def usualy_work(full, period):
  return list(filter(lambda item: item["regulary"] and item["time"] >= now_it, full))
  
# Save and update events list

def save_list(events, path, period, append):
  periodical = (period.days > now_it.days)
  with open(path, 'w') if not append else open(path, 'a') as f:
    for item in events:
      if periodical and (item['time'].days > now_it.days):
        item['compleaty'] = 0
        line = record_format % (item['date'].strftime(date_format), item['name'], item['note'], item['compleaty']) + '\n'
        f.write(line)

def merge_deadline(cache, listName):
  category = memories.LISTS[listName]
  if not category[1]:
    return True
  stored = load_list([], category[2], category[4])
  exists_events = list(map(lambda item: item["name"], stored))
	
  for item in cache:
    inx = exists_events.index(item["name"])
    if inx > -1:
      stored[inx] = item
    elif category[5]:
      stored.insert(END, item)
	
    save_list(stored, category[2], category[4], False)
    return len(stored)

def save_deadlines(listName, deadlines):
  if listName in memories.FILES.keys():
    theList = memories.FILES[listName]
    if theList[2]:
      save_list(deadlines, theList[1], theList[0], True)
  elif listName in memories.LISTS.keys():
    merge_deadline(deadlines, memories.FILES[theList[2]][1], theList[4], theList[5])

def save_all_deadlines(listName, deadlinesDict):
  allLists = deadlinesDict.keys()
  for listName in allLists:
    save_deadlines(listName, deadlinesDict[listName])

def update_events(full):
  events = actual_events(full, memories.PERIOD['year'])
  dates = regulary_events(full, memories.PERIOD['none'])
  save_list(events, 'Eventualy.txt', now_it, False)
  save_list(dates, 'Regulary.txt', date_period, False)

