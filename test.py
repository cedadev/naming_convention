import unittest
import nameing_convention


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
        
if __name__ == '__main__':
    unittest.main()