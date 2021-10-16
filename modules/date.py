import typing
import calendar
import datetime


class Module:
    def __init__(self) -> None:
        self.name = "date"
        self.keywords = [
            "date",
            "day", "month", "year",
            "days", "months", "years",
            "th", "st", "nd", "rd",
            "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday",
            "mon", "tue", "wed", "thu", "fri", "sat", "sun",
            "january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november", "december",
            "jan", "feb", "mar", "apr", "jun", "jul", "aug", "sep", "oct", "nov", "dec",
            "today", "tomorrow", "yesterday",
            "leap"
        ]

    def run(self, command: typing.List[str]) -> str:
        months = {
            "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6, "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
            "january": 1, "february": 2, "march": 3, "april": 4, "may": 5, "june": 6, "july": 7, "august": 8, "september": 9, "october": 10, "november": 11, "december": 12
        }
        monthlist = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        days = {
            "mon": 1, "tue": 2, "wed": 3, "thu": 4, "fri": 5, "sat": 6, "sun": 7,
            "monday": 1, "tuesday": 2, "wednesday": 3, "thursday": 4, "friday": 5, "saturday": 6, "sunday": 7
        }
        daylist = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        now = datetime.datetime.now()

        for n, word in enumerate(command):
            for smonth in list(months.keys())[:12]:
                if word.startswith(smonth) and len(word) > 3:
                    for lmonth in list(months.keys())[12:]:
                        if lmonth.startswith(word):
                            command[n] = lmonth
                            break

        """
        what day was
        how long until
        """
        day = now.day
        if 4 <= day <= 20 or 24 <= day <= 30:
            suffix = "th"
        else:
            suffix = ["st", "nd", "rd"][day % 10 - 1]

        if "today" in command or "now" in command or "is" and "it" in command:  # what day is it
            if "year" in command:
                return f"It is currently {now.year}"
            elif "month" in command:
                return f"It is currently {monthlist[now.month]}"
            elif "day" in command:
                return f"It is currently {daylist[day % 7]} the {day}{suffix} of {monthlist[now.month]}"
            else:
                return f"It is {daylist[now.weekday() % 7]} the {day}{suffix} of {monthlist[now.month - 1]}, {now.year}"

        elif "tomorrow" in command:  # what day is it tomorrow
            tomorrow = now + datetime.timedelta(days=1)
            if 4 <= tomorrow.day <= 20 or 24 <= tomorrow.day <= 30:
                suffix = "th"
            else:
                suffix = ["st", "nd", "rd"][tomorrow.day % 10 - 1]
            return f"Tomorrow will be {daylist[tomorrow.weekday() % 7]} the {tomorrow.day}{suffix} of {monthlist[tomorrow.month - 1]}, {tomorrow.year}"

        elif "yesterday" in command:  # what day was it yesterday
            yesterday = now - datetime.timedelta(days=1)
            if 4 <= yesterday.day <= 20 or 24 <= yesterday.day <= 30:
                suffix = "th"
            else:
                suffix = ["st", "nd", "rd"][yesterday.day % 10 - 1]
            return f"Yesterday was {daylist[yesterday.weekday() % 7]} the {yesterday.day}{suffix} of {monthlist[yesterday.month - 1]}, {yesterday.year}"

        elif "days" in command:
            if "in" in command:  # how many days in month/year
                if "this" in command:  # how many days in month
                    return f"There are {calendar.monthrange(now.year, now.month)[1]} days in {monthlist[now.month - 1]}"
                for month in months.keys():
                    year = now.year
                    empty = True
                    for word in command:
                        if word.isdigit():
                            if 999 <= int(word) <= 99999:
                                year = int(word)
                                empty = False
                                break
                    if month in command:
                        return f"There are {calendar.monthrange(year, months[month])[1]} days in {monthlist[months[month] - 1]} {year}"
                    elif "year" in command and "this" in command:  # how many days in this year
                        return f"There are {'366' if calendar.isleap(year) else '365'} days in {year}"
                    elif year and not empty:
                        return f"There {'were' if year <= now.year else 'will be'} {'366' if calendar.isleap(year) else '365'} days in {year}"

            elif "was" in command or "what" in command or "were" in command:  # what day was monday
                pass  # TODO

        elif "leap" in command:
            for word in command:
                if word.isdigit():
                    if 999 <= int(word) <= 99999:
                        year = int(word)
                        break
            else:
                year = now.year
            return f"{year} {'is' if year == now.year else ('was' if year < now.year else 'will')}{'' if calendar.isleap(year) else ' not'}" + \
                   f" {'be ' if year > now.year else ''}a leap year"

    def enter(self, query, window) -> bool:
        return False
