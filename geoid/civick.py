"""
The Civic Knowledge geoid, a gvid, is  very similar to the census versions, but
expresses numbers in base 62 and includes other important values. 
"""

from . import base62_encode, base62_decode, Geoid, make_classes
import sys

class GVid(Geoid):

    sl = None
    fmt = None

    class_map = {}
    sl_map = {}

    sl_width = 2
    sl_format = '{sl:0>2s}'
    elem_format = '{{{}:0>{}s}}'
    elem_str_format = '{{{}:s}}'
    sl_regex = '(?P<sl>.{2})'
    elem_regex = '(?P<{}>.{{{}}})'

    encode = base62_encode
    decode = base62_decode

    @classmethod
    def part_width(cls, dec_width):
        # Convert a decimal number of digits to a base 62 number of digits, via strings.
        # Maybe would be faster to use log()?
        return len(base62_encode(int('9'*int(dec_width))))

    @classmethod
    def class_factory(cls, name):

        def __init__(self, *args, **kwargs):
            cls.__init__(self, *args, **kwargs)

        return type(name, (cls,), {"__init__": __init__})

    def summarize(self):
        """Convert all of the values to their max values. This form is used to represent the summary level"""

        s = str(self.allval())

        return self.parse(s[:2]+ ''.join(['Z']*len(s[2:])))


make_classes(GVid, sys.modules[__name__])
