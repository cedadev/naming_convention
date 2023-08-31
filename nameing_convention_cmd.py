

import click
import json
import re
from typing import DefaultDict
import datetime
import sys
from nameing_convention import run_regexs, datetime_tidy


@click.command()
@click.option('--filelist', help='file listing. Defaults to sdtin', type=click.File('r'), default=sys.stdin)
def main(filelist):
    argrigate = {}
    total_keys = 0

    number_of_keys = DefaultDict(int)
    little_info_list = []
    no_date = []
    values = DefaultDict(set)
    n = 0
    for line in filelist:
        n += 1
        path = line.strip()
        d = run_regexs(path)
        print(d)
        d = datetime_tidy(d)
        print(d)
        print(path, d)
        if "datetime" not in d:
            no_date.append(path)
        argrigate.update(d)
        nkeys = len(d.keys())
        total_keys += nkeys
        number_of_keys[nkeys] += 1
        if nkeys > 0 and nkeys < 4:
            little_info_list.append(path)
        for key in d:
            values[key].add(d[key])

    print()
    little_info_list.sort()
    print("Littel info paths")
    for path in little_info_list:
        print(path)
    print() 
#    print("no date paths")
#    for path in no_date:
#        print(path)
    print() 
    print(json.dumps(argrigate, indent=4))
    print(f"total keys: {total_keys}")
    print(f"files with x keys:")
    print(json.dumps(number_of_keys, indent=4)) 
    print()
    print(f"little info: {len(little_info_list)}/{n}")
    print(f"no date: {len(no_date)}/{n}")
#    print(values)

if __name__ == "__main__":
    main() 
