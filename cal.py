import icalendar
from datetime import *
from dateutil.rrule import *
from dateutil.tz import UTC

def parse_recurrences(recur_rule, start, exclusions):
    """ Find all reoccuring events """
    rules = rruleset()
    first_rule = rrulestr(recur_rule, dtstart=start)
    rules.rrule(first_rule)
    if exclusions:
        for xdt in exclusions.dts:
            try:
                rules.exdate(xdt.dt)
            except AttributeError:
                pass
    now = datetime.now(timezone.utc)
    this_year = now + timedelta(days=60)
    dates = []
    for rule in rules.between(now, this_year):
        dates.append(rule.strftime("%D %H:%M UTC "))
    return dates

icalfile = open('calendar.ics', 'rb')
gcal = icalendar.Calendar.from_ical(icalfile.read())
for component in gcal.walk():
    if component.name == "VEVENT":
        summary = component.get('summary')
        # description = component.get('description')
        description = "HELLO"
        location = component.get('location')
        startdt = component.get('dtstart').dt
        enddt = component.get('dtend').dt
        exdate = component.get('exdate')
        if component.get('rrule'):
            reoccur = component.get('rrule').to_ical().decode('utf-8')
            # for item in parse_recurrences(reoccur, startdt, exdate):
                # print("{0} {1}: {2} - {3}\n".format(item, summary, description, location))
        else:
            print("{0}-{1} {2}: {3} - {4}\n".format(startdt.strftime("%D %H:%M UTC"), enddt.strftime("%D %H:%M UTC"), summary, description, location))
icalfile.close()