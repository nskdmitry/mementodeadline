# Memento Deadline. Deadlines + Input/Output.
import datetime, time, memories

current_day = datetime.date.today()
date_format = "%d.%m.%Y"
record_format = "%s\t%s\t%s\t%d"
now_it = datetime.timedelta(days=0)
date_period = datetime.timedelta(days=365)

def load_list(items, path, period = now_it):
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
                items.append({'date': dateOf,
                              'name': inf[1],
                              'note': inf[2],
                              'compleaty': int(inf[3]),
                              'regulary': period.days > 0,
                              'time': nextDate - current_day,
                              'years': (dateOf.year - current_day.year)})
    return items

def upload_all_dates():
    items = []
    f = open("Regulary.txt", "r")
    while True:
        line = f.readline()
        if not line: break
        inf = line.split("\t")
        if len(inf) == 4:
            dateOf = datetime.datetime.strptime(inf[0], date_format).date()
            # Calculate this deadline on this year
            nextDate = dateOf.replace(year=current_day.year)
            items.append({'date': dateOf,
                          'name': inf[1],
                          'note': inf[2],
                          'compleaty': int(inf[3]),
                          'regulary': True,
                          'time': nextDate - current_day,
                          'years': (dateOf.year - current_day.year)})
    f.close()

    f = open("Eventualy.txt", "r")
    while True:
        line = f.readline()
        if not line: break
        inf = line.split("\t")
        if len(inf) == 4:
            dateOf = datetime.datetime.strptime(inf[0], date_format).date()
            items.append({'date': dateOf,
                          'name': inf[1],
                          'note': inf[2],
                          'compleaty': int(inf[3]),
                          'regulary': False,
                          'time': dateOf - current_day,
                          'years': 0})
    f.close()
    
    return items

# Extract a events lists by catgory

def near_dates(full, time):
    dt = datetime.timedelta(days=time)
    return list(filter(lambda item: (item["time"] <= dt) and (item["time"] >= now_it), full))

def actual_events(full, period):
    return list(filter(lambda item: (not item["regulary"] and (item["time"] >= now_it)), full))

def regulary_events(full, period):
    return list(filter(lambda item: item["regulary"], full))

# exterminating from list data
def death_cargo(full, period):
    return list(filter(lambda item: not item["regulary"] and (item["time"] < now_it) and (item["compleaty"] < 100)))

def elapsed_events(full, period):
    return list(filter(lambda item: item["regulary"] and item["compleaty"] == 100 and item["time"] < now_it, full))

# Save and update events list

def save_list(events, path, period):
    periodical = (period.days > now_it.days)
    with open(path, 'w') as f:
        for item in events:
            if periodical and (item['time'].days > now_it.days):
                item['compleaty'] = 0
            line = record_format % (item['date'].strftime(date_format), item['name'], item['note'], item['compleaty']) + '\n'
            f.write(line)

def update_events(full):
    events = actual_events(full, memories.PERIOD['none'])
    dates = regulary_events(full, memories.PERIOD['none'])
    save_list(events, 'Eventualy.txt', now_it)
    save_list(dates, 'Regulary.txt', date_period)
