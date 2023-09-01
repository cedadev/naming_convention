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
        self.datetime_prefixes = set()
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

    def label_patterns(self, regex):
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
                    prefix = label[:-len(datetime_label)]
                    self.datetime_prefixes.add(prefix)

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

            regex = regex.replace(f"<{to_replace}>", f"__REPLACE__")
            print(regex)
            regex = regex.replace(f"__REPLACE__", f"(?P<{label}>{label_pattern})", 1)
            #regex = re.sub("(?<!P)<{to_replace}>", f"(?P={label})", regex)
            regex = regex.replace(f"__REPLACE__", f"(?P={label})")
            print(regex, label_pattern)
            time.sleep(0.05)
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
            for prefix in self.datetime_prefixes:
                result_dict = consolidate_datetime(result_dict, prefix=prefix)
                print(result_dict)
        return result_dict

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




def consolidate_datetime(d, prefix=""):
    """Consolidate the date fields in a dictionary by creating a single datetime field"""

    # Date elements
    date = d.get(prefix + "date")
    year = d.get(prefix + "year")
    month = d.get(prefix + "month")
    day = d.get(prefix + "day")
    jday = d.get(prefix + "jday")

    date_date = None
    jday_date = None
    day_date = None
    if date:
        date_date = datetime.date(int(date[0:4]), int(date[4:6]), int(date[6:8]))
    if jday and year:
        dt0 = datetime.date(int(year), 1, 1) 
        jday_date = datetime.date.fromordinal(dt0.toordinal() - 1 + int(jday))
    if day and month and year:
        day_date = datetime.date(int(year), int(month), int(day))    
    elif year and month:
        day_date = datetime.date(int(year), int(month), 1)
    elif year:
        day_date = datetime.date(int(year), 1, 1)
    
    if date_date and jday_date and date_date != jday_date: 
        raise ValueError("Date field inconsistent with jday and year fields.")
    if date_date and day_date and date_date != day_date: 
        raise ValueError("Date field inconsistent with day, month and year fields.")
    if jday_date and day_date and day_date != jday_date: 
        raise ValueError("Day, month, year fields inconsistent with jday and year fields.")

    if date_date: 
        date = date_date
    elif day_date:
        date = day_date
    elif jday_date:
        date = jday_date
    else:
        # return dict unalltered
        return d

    # time elements
    time = d.get(prefix + "time")
    hour = d.get(prefix + "hour")
    minute = d.get(prefix + "minute")
    second = d.get(prefix + "second")

    time_time = None
    hour_time = None
    if time:
        time_time = datetime.time(int(date[0:2]), int(date[2:4]), int(date[4:6]))
    if hour and minute and second:
        hour_time = datetime.time(int(hour), int(minute), int(second))    
    elif hour and minute:
        hour_time = datetime.time(int(hour), int(minute), 0)
    elif hour:
        hour_time = datetime.time(int(hour), 0, 0)
    
    if time_time and hour_time and hour_time != time_time: 
        raise ValueError("Time field inconsistent with hour, minute and seconds fields.")

    if time_time: 
        d[prefix + "datetime"] = datetime.datetime.combine(date, time_time)
    elif hour_time:
        d[prefix + "datetime"] = datetime.datetime.combine(date, hour_time)
    else:
        # return dict unalltered
        d[prefix + "datetime"] = datetime.datetime.combine(date, datetime.time())

    # remove old time keys
    for key in ("year", "month", "day", "hour", "minute", "second", "time", "date", "jday"):
        key = prefix + key
        if key in d: del d[key]

    return d   

