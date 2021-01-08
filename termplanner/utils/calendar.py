from calendar import LocaleHTMLCalendar
from datetime import date


class Calendar(LocaleHTMLCalendar):
    def __init__(self, year=None, month=None, locale="de_DE"):
        self.year = year
        self.month = month
        self.locale = locale
        super(Calendar, self).__init__(locale=self.locale)

    # formats a day as a td
    # filter events by day
    def formatday(self, day, events):
        events_per_day = events.filter(start_date__day=day)
        d = ""
        for event in events_per_day:
            d += (
                f"<li><a href='{event.get_absolute_url()}'>"
                f"{event.semestermodule.module.short_title} - {event.title}</a> </li>"
            )

        if day != 0:
            if date(self.year, self.month, day) == date.today():
                return f"<td class='table-info'><span class='date'>{day}</span><ul> {d} </ul></td>"
            else:
                return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return "<td></td>"

    # formats a week as a tr
    def formatweek(self, theweek, events):
        week = ""
        for d, weekday in theweek:
            week += self.formatday(d, events)
        return f"<tr> {week} </tr>"

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, withyear=True, events=None):

        events = events.filter(start_date__year=self.year, start_date__month=self.month)

        cal = '<table border="0" cellpadding="0" cellspacing="0" class="table calendar">\n'
        cal += f"{self.formatmonthname(self.year, self.month, withyear=withyear)}\n"
        cal += f"{self.formatweekheader()}\n"
        for week in self.monthdays2calendar(self.year, self.month):
            cal += f"{self.formatweek(week, events)}\n"
        cal += "</table>"
        return cal
