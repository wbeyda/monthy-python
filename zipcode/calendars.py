from calendar import LocaleHTMLCalendar, month_name, monthrange
from datetime import date


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

def contractor_calendar(queryset):
    for s in queryset:   
        eventdict = {}  
        conevents = s.contractorschedule_set.all() 
        counter = conevents.count() #2
        n = 1
        for i in conevents:
            y,m = i.start_date.year,i.start_date.month
            event = "<ul><li>" + i.start_date.strftime("%I:%M")+" "+ i.title +" "+ i.end_date.strftime("%I:%M") +"</li></ul>"
            #loop through the days of the month
            for j in range(1,monthrange(y,m)[1]+1): #1-31                           
                if i.start_date.day == j and j not in eventdict:
                    eventdict[j] = event
                elif j not in eventdict:
                    eventdict[j] = None
                #add to a day with an event
                if i.start_date.day == j and eventdict[j] != "" and eventdict[j] is not None and eventdict[j] != event:
                    eventdict[j] += event
                #change day from none to event 
                if i.start_date.day == j and eventdict[j] is None:
                    eventdict[j] = event
                if j == monthrange(y,m)[1] and n == counter:
                    htmlcalendar = GenericCalendar(y,m).formatmonth(y,m, eventdict)
                elif j == monthrange(y,m)[1] and n != counter:
                     n+=1
    return htmlcalendar

