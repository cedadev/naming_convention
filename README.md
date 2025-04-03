
a nameing convention is a thing a little like a regex or a glob with named components 

```python
nc = NameConvention("/badc/acsoe/data/<instrument>/.../<project>_<site>-YYYYMMDD.dat")
```

The end of the pattern is implied as the end of the string ($)
<instrument> is mapped to (?P<instrument>[^/]+)
... is any intermediate string .* 
<project> is mapped to  (?P<project>[^/_]+)
<site> is mapped to (?P<site>[^_-])
YYYYMMDD is mapped to (?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2})

The result as regex is:
"/badc/acsoe/data/(?P<instrument>[^/]+)(.*)?/(?P<project>[^/_]+)_(?P<site>[^_-])-(?P<year>\d{4})(?P<month>\d{2})(?P<day>\d{2}).dat

Use the nameing convention like a compiled regex

m = nc.search("string to search")

As dict:

```python
nc.components("/badc/acsoe/data/sky_cam/.../TEX_chilbolton-20021225.dat")
# returns components as dict
{"instrument": "sky_cam",
 "project": TEX,
 "site": "chilbolton",
 "datetime": DateTime("20021225")}
```

 optional field have square brakets []

nc = NameConvention("/data/<instrument>[_<model>]_YYYYMMDD.dat")

[_<model>] mapps to (_(?P<model>[^_]))?

Fixed length fields

```python
nc = NameConvention("_<version:8><level:3><exp:4>.dat")

nc.components("dsfsdfhsdf_20180123L23TEX2.dat")

# returns components as dict
{"version": "20180123",
 "level": "L23",
 "exp": "TEX2"}
```


## Using regex in a naming convention
 - A regex pattern in a nameing convention pattern should be respected as much as possible. 
 - Any thing in parenthisis are plain regex and not preprocessed. 
 - As square brackets are used to indicate an optional component. Parenthisis must be used if this is to be interpreted as a 
   plain regex.

These are ok:
nc = NameConvention("<prod>_(?P<term>(T4|WS|aabc))_XXXX.dat")

nc = NameConvention("<prod>_([a-f]{4})_XXXX.dat")

nc = NameConvention("<prod>_\d{4}_XXXX.dat")

This is not ok

nc = NameConvention("<prod>_[a-f]{4}_XXXX.dat")

## methods

components: return a dict of components
search: like re serch




## dates and times

YYYY/MM/DD is easy to understand but can be a bit ambiguous. What if there are 2 dates, a processed date and an indicative date? 
It would be good to encode both times as datetime objects.  

recogognis special date and time labels.
 - date - the 8 digit date YYYYMMDD
 - year - the 4 digit year
 - month - the 2 digit month
 - day - the 2 digit day of month
 - jday - the 3 digit day of year
 - time - the 6 digit time HHMMSS
 - hour - the 2 digit hour
 - minute - the 2 digit time
 - second - the 2 digit second

By default these are combined into a single `datetime` field. 

Additionally if a label is suffixed any of these then these are combined into a single field 
<prod_date><prod_time> => `prod_datetime`  

