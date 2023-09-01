import unittest
import nameing_convention
import datetime

class TestNameingConvention(unittest.TestCase):


    def test_acsoe_regex(self):
        pattern = "/badc/acsoe/data/<instrument>/.../<project>_<site>-<date>.dat"
        right_regex_pattern = "/badc/acsoe/data/(?P<instrument>[^/]+)(/.*/?)(?P<project>[^/_]+)_(?P<site>[^/_-]+)-(?P<date>\d{8})\.dat"
        nc = nameing_convention.NameConvention(pattern)
        self.assertEqual(nc.regex.pattern, right_regex_pattern)
        
    def test_optional_regex(self):
        pattern = "/data/<instrument>[_<model>]_<date>.dat"
        right_regex_pattern = "/data/(?P<instrument>[^/_]+)(_(?P<model>[^/_]+))?_(?P<date>\d{8})\.dat"
        nc = nameing_convention.NameConvention(pattern)
        self.assertEqual(nc.regex.pattern, right_regex_pattern)
        
    def test_fixedlen_regex(self):
        pattern = "_<version:8><level:3><exp:4>.dat"
        right_regex_pattern = "_(?P<version>.{8})(?P<level>.{3})(?P<exp>.{4})\.dat"
        nc = nameing_convention.NameConvention(pattern)
        self.assertEqual(nc.regex.pattern, right_regex_pattern)
        
    def test_regex_in_pattern_regex(self):
        pattern = "<prod>_(?P<term>(T4|WS|aabc))_XX\.XX-([a-f]{4}).dat"
        right_regex_pattern = "(?P<prod>[^/_]+)_(?P<term>(T4|WS|aabc))_XX\.XX-([a-f]{4})\.dat"
        nc = nameing_convention.NameConvention(pattern)
        self.assertEqual(nc.regex.pattern, right_regex_pattern)
        
    def test_time_regex(self):
        pattern = "/badc/acsoe/data/<instrument>/.../<project>_<site>-<hour><minute>.dat"
        right_regex_pattern = "/badc/acsoe/data/(?P<instrument>[^/]+)(/.*/?)(?P<project>[^/_]+)_(?P<site>[^/_-]+)-(?P<hour>\d{2})(?P<minute>\d{2})\.dat"
        nc = nameing_convention.NameConvention(pattern)
        self.assertEqual(nc.regex.pattern, right_regex_pattern)

    def test_time_prefix_regex(self):
        pattern = "/badc/acsoe/data/<instrument>/.../<project>_<site>-<proc_hour><proc_minute>.dat"
        right_regex_pattern = "/badc/acsoe/data/(?P<instrument>[^/]+)(/.*/?)(?P<project>[^/_]+)_(?P<site>[^/_-]+)-(?P<proc_hour>\d{2})(?P<proc_minute>\d{2})\.dat"
        nc = nameing_convention.NameConvention(pattern)
        self.assertEqual(nc.regex.pattern, right_regex_pattern)

    def test_acsoe_analyses(self):
        pattern = "/badc/acsoe/data/<instrument>/<project>_<site>-<date>.dat"
        right_regex_pattern = "/badc/acsoe/data/(?P<instrument>[^/]+)/(?P<project>[^/_]+)_(?P<site>[^/_-]+)-(?P<date>\d{8})\.dat"
        path = "/badc/acsoe/data/inst234/projXXX_RAL.3-20230823.dat"
        result = {'instrument': 'inst234', 'project': 'projXXX', 'site': 'RAL.3', 
                  'datetime': datetime.datetime(2023, 8, 23, 0, 0)}
        nc = nameing_convention.NameConvention(pattern)
        self.assertEqual(nc.analyses(path), result)


    def test_time_prefix_anal(self):
        pattern = "<proc_date>/<project>_<site>-<proc_hour><proc_minute>.dat"
        path = "/badc/acsoe/20230131/inst234_RAL.3-1721.dat"
        result = {'project': 'inst234', 'site': 'RAL.3', 
                  'proc_datetime': datetime.datetime(2023, 1, 31, 17, 21)}
        nc = nameing_convention.NameConvention(pattern)
        self.assertEqual(nc.analyses(path), result)


    def test_time_prefix2_anal(self):
        pattern = "<proc_date>/<project>_<site>_<date>-<proc_hour><proc_minute>.dat"
        path = "/badc/acsoe/20230131/inst234_RAL.3_20220819-1721.dat"
        result = {'project': 'inst234', 'site': 'RAL.3', 
                  'datetime': datetime.datetime(2022, 8, 19),
                  'proc_datetime': datetime.datetime(2023, 1, 31, 17, 21)}
        nc = nameing_convention.NameConvention(pattern)
        print(nc.datetime_prefixes)
        self.assertEqual(nc.analyses(path), result)


#    def test_repeat_label_regex(self):
#        pattern = "<inst>/<project>_<inst>.dat"
#        right_regex_pattern = "(?P<inst>[^/]+)(?P<project>[^/_]+)_(?P<inst2>[^/_.]+)\.dat"
#        nc = nameing_convention.NameConvention(pattern)
#        self.assertEqual(nc.regex.pattern, right_regex_pattern)   

if __name__ == '__main__':
    unittest.main()