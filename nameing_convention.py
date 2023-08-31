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
            for datetime_label, datetime_pattern in self.datetime_patterns:
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

            regex = regex.replace(f"<{to_replace}>", f"(?P<{label}>{label_pattern})")
            print(regex, label_pattern)
            time.sleep(0.3)



        # replace all dots and square brackets if not in parenthises.
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
            
        regex = new_regex

        self.regex = re.compile(new_regex)
        print(self.regex.pattern)
        self.regex.pattern
  
    
    def analyses(self, path):
        m = self.regex.search(path)
        if m:
            return m.groupdict()
        return None

def make_datetime(datestr, date_format):
    try: 
        return datetime.datetime.strptime(datestr, date_format).isoformat()  
    except ValueError:
        return None



def datetime_tidy2(d):
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

