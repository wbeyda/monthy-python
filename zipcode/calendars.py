from calendar import LocaleHTMLCalendar, month_name, monthrange
import datetime
from datetime import date
from collections import defaultdict


class GenericCalendar(LocaleHTMLCalendar):
        def __init__(self, year, month):
                super(GenericCalendar, self).__init__()
                self.yr = year
                self.mo = month

        def formatday(self, day, weekday, event):
                if day == 0:
                        return '<td class="noday">&nbsp;</td>' # day outside month
                elif day != 0 and event[0][day] != None:
                        return '<td class="%s">%d %s</td>' % (self.cssclasses[weekday], day, event[0][day])
                elif day !=0 and event[0][day] == None:
                        return '<td class="%s">%d %s</td>' % (self.cssclasses[weekday], day, "")

        def formatweek(self, theweek, *event):                                                                      
                if len(event) == 0:                                                                                         
                        s = ''.join(self.formatday(d, wd, event) for (d, wd) in theweek)                                               
                else:                                                                                                       
                        s = ''.join(self.formatday(d, wd, event) for (d, wd) in theweek)                                       
                return '<tr>%s</tr>' % s

        def formatmonth(self, theyear, themonth, event, withyear=True):
                v = []
                a = v.append
                a('<table border="0" cellpadding="0" cellspacing="0" class="month">')
                a('\n')
                a(self.formatmonthname(theyear, themonth, withyear=withyear))
                a('\n')
                a(self.formatweekheader())
                a('\n')
                for week in self.monthdays2calendar(theyear, themonth):
                        a(self.formatweek(week, event))
                        a('\n')
                a('</table>')
                a('\n')
                return ''.join(v)

def last_day_of_month(date):
    if date.month == 12:
        return date.replace(day=31, hour=23, minute=59, second=59)
    return date.replace(month=date.month+1, day=1, hour=23, minute=59, second=59) - datetime.timedelta(days=1)

def first_day_of_month(date):
    return date.replace(day=1, hour=0, minute=0, second=0)

def contractor_calendar(queryset):
    for s in queryset:   
        eventdict = defaultdict(str)  
        conevents = s.contractorschedule_set.all().exclude(start_date__gt=last_day_of_month(datetime.datetime.today())) \
                                                  .exclude(start_date__lt=first_day_of_month(datetime.datetime.today())) 
        if conevents.exists():
            counter = conevents.count() #2
            n = 1
            for i in conevents:
                y,m = i.start_date.year,i.start_date.month
                event = "<ul class=\"calendar-event\"><li style=\"background-color:#"+ i.background_color +"\">" +\
                         i.start_date.strftime("%I:%M")+" "+ i.title +" "+ i.end_date.strftime("%I:%M") +"</li></ul>"
                #loop through the days of the month
                if i.start_date.day != i.end_date.day or i.start_date.month != i.end_date.month:
                    if i.start_date.month != i.end_date.month:
                        chunkofdays = range(i.start_date.day, monthrange(y,m)[1]+1)
                    else:
                        chunkofdays = range(i.start_date.day, i.end_date.day+1)
                    for days in chunkofdays:
                        if days == chunkofdays[-1]:
                            eventend = "<ul class=\"calendar-event\"><li style=\"background-color:#"+ i.background_color +"\">"  +\
                                         i.start_date.strftime("%I:%M")+" "+ i.title +" "+ i.end_date.strftime("%I:%M") +"</li></ul>"
                            eventdict[days] += eventend 
                        else: 
                            eventstart = "<ul class=\"calendar-event\"><li style=\"background-color:#"+ i.background_color +"\">" +\
                                         i.start_date.strftime("%I:%M")+" "+ i.title + "</li></ul>"
                            eventdict[days] += eventstart
                for j in range(1,monthrange(y,m)[1]+1): #1-31                           
                    
                    if i.start_date.day == j and j not in eventdict:
                        eventdict[j] = event
                    #add to a day with an event
                    if i.start_date.day == j and eventdict[j] != "" and eventdict[j] is not None and eventdict[j] != event and i.is_chunk != True:
                        eventdict[j] += event
                    
                    #change day from none to event 
                    if i.start_date.day == j and eventdict[j] is None:
                        eventdict[j] = event
                    
                    if j == monthrange(y,m)[1] and n == counter:
                        htmlcalendar = GenericCalendar(y,m).formatmonth(y,m, eventdict)
                    elif j == monthrange(y,m)[1] and n != counter:
                        n+=1
            return htmlcalendar

        else:
            todaysdate = date.today()
            y,m = todaysdate.year, todaysdate.month
            htmlcalendar = LocaleHTMLCalendar().formatmonth(y,m)
            return htmlcalendar 


def next_last_month_contractor_calendar(queryset):
    counter = len(queryset)
    eventdict = defaultdict(str) 
    n = 1
    for i in queryset:   
        y,m = i.start_date.year,i.start_date.month
        event = "<ul class=\"calendar-event\" ><li style=\"background-color:#"+ i.background_color +"\">" +\
                 i.start_date.strftime("%I:%M")+" "+ i.title +" "+ i.end_date.strftime("%I:%M") +"</li></ul>"
        #loop through the days of the month
        if i.start_date.day != i.end_date.day or i.start_date.month != i.start_date.month:
                if i.start_date.month != i.end_date.month:
                    chunkofdays = range(i.start_date.day, monthrange(y,m)[1]+1)
                else:
                    chunkofdays = range(i.start_date.day, i.end_date.day+1)
                print("this is a chunk", i.start_date, i.end_date)
                for days in chunkofdays:
                    if days == chunkofdays[-1]:
                        eventend = "<ul class=\"calendar-event\" ><li style=\"background-color:#"+ i.background_color +"\">"  +\
                                     i.start_date.strftime("%I:%M")+" "+ i.title +" "+ i.end_date.strftime("%I:%M") +"</li></ul>"
                        eventdict[days] += eventend
                    else: 
                        eventstart = "<ul class=\"calendar-event\" ><li style=\"background-color:#"+ i.background_color +"\">" +\
                                     i.start_date.strftime("%I:%M")+" "+ i.title + "</li></ul>"
                        eventdict[days] += eventstart
        for j in range(1,monthrange(y,m)[1]+1): #1-31                           
            if i.start_date.day == j and j not in eventdict:
                eventdict[j] = event
            #add to a day with an event
            if i.start_date.day == j and eventdict[j] != "" and eventdict[j] != event and i.is_chunk != True:
                eventdict[j] += event
            if j == monthrange(y,m)[1] and n == counter:
                htmlcalendar = GenericCalendar(y,m).formatmonth(y,m, eventdict)
            elif j == monthrange(y,m)[1] and n != counter:
                n+=1
    return htmlcalendar

