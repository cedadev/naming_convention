import re
import json
import re
from typing import DefaultDict
import datetime
import sys
import time


class NameConvention:

    convertions = {"i": int, "s": str, "d": datetime, "u": str.upper, "l": str.lower}    

    datetime_patterns = [
        ("date", "\d{8}"),
        ("year", "\d{4}"),
        ("month", "\d{2}"),
        ("day", "\d{2}"),
        ("jday", "\d{3}"),
        ("time", "\d{6}"),
        ("hour", "\d{2}"),
        ("minute", "\d{2}"),
        ("second", "\d{2}"),
    ]

    def __init__(self, pattern, combine_datetime=True) -> None:
        self.orig_pattern = pattern
        self.regex = None
        self.make_regex()
        self.combine_datetime = combine_datetime 

    def make_regex(self):
        regex = self.orig_pattern
        # regex for any number of subdirs 
        regex = regex.replace("/.../", "(/.*/?)")
        regex = self.label_patterns(regex)
        regex = self.transform_special_chars(regex)
        self.regex = re.compile(regex)
        print(self.regex.pattern)

    @staticmethod
    def label_patterns(regex):
        """Transform labelled patterns like"<inst>" to regex patterns like  "(?P<inst>[^/_]+)". """

        while True:
            m = re.search(r"(?<!\(\?P)(?P<sep1>[^P\(\)])?<(?P<to_replace>(?P<label>\w+)(:(?P<length>\d+)(?P<convertion>.)?)?)>[\[\]]?(?P<sep2>[^\[\]\(\)])?", regex)
            if not m:
                break
            sep1 = m.group("sep1")
            sep2 = m.group("sep2")
            label = m.group("label")
            length = m.group("length")
            to_replace = m.group("to_replace")

            # check for date or time special labels
            datetime_label_pattern = None
            for datetime_label, datetime_pattern in NameConvention.datetime_patterns:
                if label.endswith(datetime_label):
                    datetime_label_pattern = datetime_pattern

            if datetime_label_pattern:
                label_pattern = datetime_label_pattern
            elif length:
                label_pattern = ".{" + length + "}"
            else:
                chars = "/"
                if sep1 and sep1 != "-" and sep1 not in chars:
                    chars += sep1 
                if sep2 and sep2 != "-" and sep2 not in chars:
                    chars += sep2 
                if sep1 == "-" or sep2 == "-":
                    chars += "-"
                label_pattern = f"[^{chars}]+"

            regex = regex.replace(f"<{to_replace}>", f"(?P<{label}>{label_pattern})", 1)
            print(regex, label_pattern)
        return regex

    @staticmethod
    def transform_special_chars(regex):
        """replace all dots and square brackets if not in parenthises. "." => "\." and "[...]" to "(...)?" """
        bracket_depth = 0
        new_regex = ''
        escape = False
        for c in regex:
            if c == "(" and not escape:
                bracket_depth += 1
            if c == ")" and not escape:
                bracket_depth -= 1
            if c == "." and not escape and bracket_depth == 0:
                c = "\."
            if c == "[" and not escape and bracket_depth == 0:
                c = "("
            if c == "]" and not escape and bracket_depth == 0:
                c = ")?"    
            if c == "\\":
                escape = True
            else:
                escape = False              
            new_regex += c
        return new_regex

    
    def analyses(self, path):
        result_dict = self.search(path)
        if self.combine_datetime:
            self.

    def search(self, path):
        m = self.regex.search(path)
        if m:
            return m.groupdict()
        return {}

def make_datetime(datestr, date_format):
    try: 
        return datetime.datetime.strptime(datestr, date_format).isoformat()  
    except ValueError:
        return None



def datetime_tidy2(d, prefix=""):
    """
    useful combos 

    

    date time (no year month, day jday, hour minute or second)
    date (no year, month jday or day)
    year jday (no day jday or month)
    hour (no time)
    hour minute (no time)
    hour minute second (no time)
    year (no date) 
    year month (no date) 
    year month day (no date) 



    ("date", "\d{8}"),
    ("year", "\d{4}"),
        ("month", "\d{2}"),
        ("day", "\d{2}"),
        ("jday", "\d{3}"),
        ("time", "\d{6}"),
        ("hour", "\d{2}"),
        ("minute", "\d{2}"),
        ("second", "\d{2}"),

"""

    date = d.get(prefix + "date")
    year = d.get(prefix + "year")
    month = d.get(prefix + "month")
    day = d.get(prefix + "day")
    jday = d.get(prefix + "jday")
    time = d.get(prefix + "time")
    hour = d.get(prefix + "hour")
    minute = d.get(prefix + "minute")
    second = d.get(prefix + "second")
    use_date_field = date and not (day or month or year or jday)
    use_jday_field = year and jday and not (date or month or day)
    use_year_field = year and (not date or jday)
    ambiguous_date_fields = not (use_date_field or use_jday_field or use_year_field)
    ambiguous_time_fields = time and (hour or minute or second)

    if ambiguous_date_fields: 
        raise ValueError("Ambiguous date fields. Date and day, month, year or jday fields detected.") 
    if ambiguous_time_fields: 
        raise ValueError("Ambiguous time fields. Time and hour, minute, or seconds fields detected.") 
    
    if use_date_field:
        year = int(date[0:4]) 
        month = int(date[4:6])
        day = int(date[6:8])
        date = datetime.date(year, month, day)
    elif use_jday_field:
        year = int(year)
        jday = int(jday)
        dt0 = datetime.date(year, 1, 1) 
        date = datetime.date.fromordinal(dt0.toordinal() - 1 + jday)
    else:
        year = int(year)
        if month: 
            month = int(month)
        else:
            month = 0
        if day: 
            day = int(day)
        else:
            day = 0
        date = datetime.date(year, month, day)
 
    if time: 
        hour = int(time[0:2]) 
        minute = int(time[2:4])
        second = int(time[4:6])
    else: 
        hour = int(hour) 
        if minute: 
            minute = int(minute)
        else:
            minute = 0
        if second: 
            second = int(second)
        else:
            second = 0
    time = datetime.time(hour, minute, second)   

    d["datetime"] = datetime.datetime.combine(date, time)

    # remove old time keys
    for key in "year", "month", "day", "hour", "min", "second", "time", "date":
        key = prefix + key
        if key in d: del d[key]

    return d   



def datetime_tidy(d):
    year = d.get("year")
    year2 = d.get("year2")
    if year2 is not None: 
        year2 = int(year2)
        if year2 < 30: year = str(year2 + 2000)
        else: year = str(year2 + 1900)
    month = d.get("month")
    day = d.get("day")
    hour = d.get("hour")
    minute = d.get("min")
    second = d.get("second")
    
    dt = make_datetime(f"{year}{month}{day}{hour}{minute}{second}", "%Y%m%d%H%M%S")
    if dt is None: dt = make_datetime(f"{year}{month}{day}{hour}{minute}", "%Y%m%d%H%M")
    if dt is None: dt = make_datetime(f"{year}{month}{day}{hour}", "%Y%m%d%H")
    if dt is None: dt = make_datetime(f"{year}{month}{day}", "%Y%m%d")
    if dt is not None:
        d["datetime"] = dt
    
    for key in "year", "month", "day", "hour", "min", "second":
        if key in d: del d[key]

    return d   

