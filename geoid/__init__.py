""" CLasses for working with census Geoids

"""

__version__ = '0.0.12'
__author__ = 'eric@civicknowledge.com'

import inspect
import sys

import six

names = {  # (summary level value, base 10 chars,  Base 62 chars, prefix fields)
    'us': 10,
    'region': 20,
    'division': 30,
    'state': 40,
    'county': 50,
    'cosub': 60,
    'place': 160,
    'ua': 400,
    'tract': 140,
    'blockgroup': 150,
    'block': 101,
    'sdelm': 950,
    'sdsec': 960,
    'sduni': 970,
    'zcta': 860,
    'zip': 1200,

    # Other Levels that don't have proper names yet.
    'state_aianhh': 260,
    'necta_nectadiv_state_county_cousub': 358,
    'state_sldl': 620,
    'state_aianhh_place': 269,
    'aianhh_state_county': 270,
    'state_cbsa_metdiv': 323,
    'state_sldu': 610,
    'state_aianhh280': 280,
    'state_place_county': 155,
    'aianhh_aitsce_state': 290,
    'state_aianhh_aihhtli': 283,
    'state_cdcurr_aianhh': 550,
    'state_concit': 170,
    'state_concit_place': 172,
    'state_aianhh_aihhtli286': 286,
    'cbsa': 310,
    'cbsa_state': 311,
    'cbsa_state_place': 312,
    'cbsa_state_county': 313,
    'cbsa_metdiv': 314,
    'cbsa_metdiv_state': 315,
    'state_cbsa': 320,
    'state_cbsa_place': 321,
    'state_cbsa_county': 322,
    'state_county_cousub_submcd': 67,
    'state_cbsa_metdiv_county': 324,
    'state_county_cousub_place': 70,
    'necta_state_county': 353,
    'state_puma5': 795,
    'csa': 330,
    'csa_state': 331,
    'csa_cbsa': 332,
    'csa_cbsa_state': 333,
    'cnecta': 335,
    'state_county_cousub_place_tract': 80,
    'cnecta_necta': 337,
    'cnecta_necta_state': 338,
    'state_csa': 340,
    'state_csa_cbsa': 341,
    'state_cnecta': 345,
    'state_cnecta_necta': 346,
    'necta': 350,
    'necta_state': 351,
    'necta_state_place': 352,
    'cnecta_state': 336,
    'necta_state_county_cousub': 354,
    'necta_nectadiv': 355,
    'necta_nectadiv_state': 356,
    'state_anrc': 230,
    'necta_nectadiv_state_county': 357,
    'state_necta': 360,
    'cbsa_metdiv_state_county': 316,
    'state_necta_county': 362,
    'state_necta_county_cousub': 363,
    'state_necta_nectadiv': 364,
    'state_necta_nectadiv_county': 365,
    'state_necta_nectadiv_county_cousub': 366,
    'state_sldu_county': 612,
    'state_cdcurr': 500,
    'state_cdcurr_county': 510,
    'state_necta_place': 361,
    'aianhh': 250,
    'aianhh_aitsce': 251,
    'aianhh_aihhtli': 252,
    'state_sldl_county': 622,
    'aianhh_aihhtli254': 254

}


# Lengths in number of decimal digits.
# Note: It's ok to keep string as value - is such case string template will be used instead of int template.

lengths = {
    'aianhh': 4,  # American Indian Area/Alaska Native Area/ Hawaiian Home Land (Census)
    'aihhtli': '1',  # American Indian Trust Land/ Hawaiian Home Land Indicator
    'aitsce': 3,  # American Indian Tribal Subdivision (Census)
    'anrc': 5,  # Alaska Native Regional Corporation (FIPS)
    'blkgrp': 1,  # Block Group
    'blockgroup': 1,  # Block Group
    'block': 4,  # Block
    'cbsa': 5,  # Metropolitan and Micropolitan Statistical Area
    'cdcurr': 2,  # Current Congressional District ***
    'cnecta': 3,  # New England City and Town Combined Statistical Area
    'concit': 5,  # Consolidated City
    'county': 3,  # County of current residence
    'cousub': 5,  # County Subdivision (FIPS)
    'cosub': 5,  # County Subdivision (FIPS)
    'csa': 3,  # Combined Statistical Area
    'division': 1,  # Census Division
    'metdiv': 5,  # Metropolitan Statistical Area- Metropolitan Division
    'necta': 5,  # New England City and Town Area
    'nectadiv': 5,  # New England City and Town Area Division
    'place': 5,  # Place (FIPS Code)
    'puma5': 5,  # Public Use Microdata Area 5% File
    'region': 1,  # Census Region
    'sdelm': 5,  # State-School District (Elementary)
    'sdsec': 5,  # State-School District (Secondary)
    'sduni': 5,  # State-School District (Unified)
    'sldl': 3,  # State Legislative District Lower
    'sldu': '3',  # State Legislative District Upper
    'state': 2,  # State (FIPS Code)
    'submcd': 5,  # Subminor Civil Division (FIPS)
    'tract': 6,  # Census Tract
    'ua': 5,  # Urban Area
    'ur': 1,  # Urban/Rural
    'us': 0,
    'zcta': 5,
    # Nonstandard
    'zip': 5,
}

segments = {
    10: ['us'],  # United States
    20: ['region'],  # Region
    30: ['division'],  # Division
    40: ['state'],  # State
    50: ['state', 'county'],  # County
    60: ['state', 'county', 'cousub'],  # County Subdivision
    67: ['state', 'county', 'cousub', 'submcd'],  # State (Puerto Rico Only)-County-County Subdivision-Subbarrio
    70: ['state', 'county', 'cousub', 'place'],  # County Subdivision-Place/Remainder
    80: ['state', 'county', 'cousub', 'place', 'tract'],  # County Subdivision-Place/Remainder-Census Tract
    101: ['state', 'county', 'tract', 'block'],
    140: ['state', 'county', 'tract'],  # Census Tract
    150: ['state', 'county', 'tract', 'blockgroup'],  # Census Tract-Block Group
    155: ['state', 'place', 'county'],  # Place-County
    160: ['state', 'place'],  # Place
    170: ['state', 'concit'],  # Consolidated City
    172: ['state', 'concit', 'place'],  # Consolidated City-Place Within Consolidated City
    230: ['state', 'anrc'],  # State-Alaska Native Regional Corporation
    250: ['aianhh'],  # American Indian Area/Alaska Native Area/Hawaiian Home Land
    251: ['aianhh', 'aitsce'],  # American Indian Area/Alaska NativeArea/HawaiianHomeLand-Tribal Subdivision/Remainder
    252: ['aianhh', 'aihhtli'],  # American Indian Area/Alaska Native Area (Reservation or Statistical Entity Only)4
    254: ['aianhh', 'aihhtli'],  # American Indian Area (Off-Reservation Trust Land Only)/Hawaiian Home Land
    260: ['state', 'aianhh'],  # American Indian Area/Alaska Native Area/Hawaiian Home Land-State
    269: ['state', 'aianhh', 'place'],  # American Indian Area/Alaska Native Area/Hawaiian Home Land-Place-Remainder
    270: ['aianhh', 'state', 'county'],  # American Indian Area/Alaska Native Area/Hawaiian Home Land-State-County
    280: ['state', 'aianhh'],  # State-American Indian Area/Alaska Native Area/Hawaiian Home Land
    283: ['state', 'aianhh', 'aihhtli'],
    # State-American Indian Area/Alaska Native Area (Reservation or Statistical Entity Only)
    286: ['state', 'aianhh', 'aihhtli'],
    # State-American Indian Area (Off-Reservation Trust Land Only)/Hawaiian Home Land
    290: ['aianhh', 'aitsce', 'state'],
    # American Indian Area/Alaska Native Area/Hawaiian Home Land-Tribal Subdivision/Remainder-State
    310: ['cbsa'],  # CBSA
    311: ['cbsa', 'state'],  # CBSA-State-County
    312: ['cbsa', 'state', 'place'],  # CBSA-State-Principal City
    313: ['cbsa', 'state', 'county'],  # CBSA-State-County
    314: ['cbsa', 'metdiv'],  # Metropolitan Statistical Area/Metropolitan Division
    315: ['cbsa', 'metdiv', 'state'],  # Metropolitan Statistical Area/Metropolitan Division-State
    316: ['cbsa', 'metdiv', 'state', 'county'],  # Metropolitan Statistical Area/Metropolitan Division-State-County
    320: ['state', 'cbsa'],  # State- CBSA
    321: ['state', 'cbsa', 'place'],  # State- CBSA -Principal City
    322: ['state', 'cbsa', 'county'],  # State- CBSA -County
    323: ['state', 'cbsa', 'metdiv'],  # State- Metropolitan Statistical Area/Metropolitan Division
    324: ['state', 'cbsa', 'metdiv', 'county'],  # State- Metropolitan Statistical Area/Metropolitan Division-County
    330: ['csa'],  # Combined Statistical Area
    331: ['csa', 'state'],  # Combined Statistical Area-State
    332: ['csa', 'cbsa'],  # Combined Statistical Area-CBSA
    333: ['csa', 'cbsa', 'state'],  # Combined Statistical Area-CBSA-State
    335: ['cnecta'],  # Combined New England City and Town Area
    336: ['cnecta', 'state'],  # Combined New England City and Town Area -State
    337: ['cnecta', 'necta'],  # Combined New England City and Town Area -New England City and Town Area
    338: ['cnecta', 'necta', 'state'],  # Combined New England City and Town Area -New England City and Town Area-State
    340: ['state', 'csa'],  # State-Combined Statistical Area
    341: ['state', 'csa', 'cbsa'],  # State-Combined Statistical Area-CBSA
    345: ['state', 'cnecta'],  # State-Combined New England City and Town Area
    346: ['state', 'cnecta', 'necta'],  # State-Combined New England City and Town Area-New England City and Town Area
    350: ['necta'],  # New England City and Town Area
    351: ['necta', 'state'],  # New England City and Town Area-State
    352: ['necta', 'state', 'place'],  # New England City and Town Area-State-Principal City
    353: ['necta', 'state', 'county'],  # New England City and Town Area-State-County
    354: ['necta', 'state', 'county', 'cousub'],  # New England City and Town Area-State-County-County Subdivision
    355: ['necta', 'nectadiv'],  # New England City and Town Area (NECTA)-NECTA Division
    356: ['necta', 'nectadiv', 'state'],  # New England City and Town Area (NECTA)-NECTA Division-State
    357: ['necta', 'nectadiv', 'state', 'county'],  # New England City and Town Area (NECTA)-NECTA Division-State-County
    358: ['necta', 'nectadiv', 'state', 'county', 'cousub'],
    # New England City and Town Area (NECTA)-NECTA Division-State-County-County Subdivision
    360: ['state', 'necta'],  # State-New England City and Town Area
    361: ['state', 'necta', 'place'],  # State-New England City and Town Area-Principal City
    362: ['state', 'necta', 'county'],  # State-New England City and Town Area-County
    363: ['state', 'necta', 'county', 'cousub'],  # State-New England City and Town Area-County-County Subdivision
    364: ['state', 'necta', 'nectadiv'],  # State-New England City and Town Area (NECTA)-NECTA Division
    365: ['state', 'necta', 'nectadiv', 'county'],  # State-New England City and Town Area (NECTA)-NECTA Division-County
    366: ['state', 'necta', 'nectadiv', 'county', 'cousub'],
    # State-New England City and Town Area (NECTA)-NECTA Division-County-County Subdivision
    400: ['ua'],  # Urban Area
    500: ['state', 'cdcurr'],  # Congressional District
    510: ['state', 'cdcurr', 'county'],  #
    550: ['state', 'cdcurr', 'aianhh'],
    # Congressional District-American IndianArea/Alaska NativeArea/Hawaiian Home Land
    610: ['state', 'sldu'],  # State Senate District
    612: ['state', 'sldu', 'county'],  # State Senate District-County
    620: ['state', 'sldl'],  # State House District
    622: ['state', 'sldl', 'county'],  # State House District-County
    795: ['state', 'puma5'],  # State-Public Use MicroSample Area 5%
    860: ['zcta'],
    950: ['state', 'sdelm'],  # State-Elementary School District
    960: ['state', 'sdsec'],  # State-High School District
    970: ['state', 'sduni'],  # State-Unified School District
    # Nonstandard
    1200: ['zip']
}

plurals = {
    'county': 'counties',
    'place': 'places'
}


class NotASummaryName(Exception):
    """An argument was not one of the valid summary names"""


class ParseError(Exception):
    """Error parsing a geoid"""


def base62_encode(num):
    """Encode a number in Base X. WIth the built-in alphabet, its base 62

    `num`: The number to encode
    `alphabet`: The alphabet to use for encoding
    Stolen from: http://stackoverflow.com/a/1119769/1144479
    """

    num = int(num)

    alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    if (num == 0):
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        rem = num % base
        num = num // base
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)


def base62_decode(string):
    """Decode a Base X encoded string into the number

    Arguments:
    - `string`: The encoded string
    - `alphabet`: The alphabet to use for encoding
    Stolen from: http://stackoverflow.com/a/1119769/1144479
    """

    alphabet = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

    base = len(alphabet)
    strlen = len(string)
    num = 0

    idx = 0
    for char in string:
        power = (strlen - (idx + 1))
        num += alphabet.index(char) * (base ** power)
        idx += 1

    return int(num)


def augment(module_name, base_class):
    """Call the augment() method for all of the derived classes in the module """

    for name, cls in inspect.getmembers(sys.modules[module_name],
                                        lambda x : inspect.isclass(x) and  issubclass(x, base_class) ):
        if cls == base_class:
            continue

        cls.augment()


def get_class(module, sl):

    for name, named_sl in names.items():
        if named_sl == sl:
            return getattr(module, name.capitalize())

    raise NotASummaryName("No class for summary_level {}".format(sl))


def make_classes(base_class, module):
    """Create derived classes and put them into the same module as the base class.

    This function is called at the end of each of the derived calss modules, acs, census, civik and tiger.
    It will create a set of new derived class in the module, one for each of the
    enries in the `summary_levels` dict.

    """
    from functools import partial

    for k in names:

        cls = base_class.class_factory(k.capitalize())

        cls.augment()

        setattr(module, k.capitalize(), cls)

    setattr(module, 'get_class', partial(get_class, module))


class Geoid(object):

    @classmethod
    def resolve_summary_level(cls, sl):
        try:
            return cls.sl_map[sl]
        except KeyError:
            return None

    @classmethod
    def make_format_string(cls, level):

        sl_num = names[level]

        segs = segments[sl_num]

        formats = []

        formats.append(cls.sl_format)

        for seg in segs:
            # Lengths dict may have strings to indicate string format usage.
            if int(lengths[seg]) <= 0:
                    continue

            if isinstance(lengths[seg], int):
                fmt = cls.elem_format
            else:
                fmt = cls.elem_str_format

            formats.append(fmt.format(seg, cls.part_width(lengths[seg])))

        return ''.join(formats)

    @classmethod
    def make_regex(cls, level):

        sl_num = names[level]

        segs = segments[sl_num]

        # Lengths dict may have strings to indicate string format usage.
        regexes = [cls.sl_regex] + [cls.elem_regex.format(seg, cls.part_width(lengths[seg]))
                                    for seg in segs if int(lengths[seg]) > 0]

        re_str = '^' + ''.join(regexes) + '$'

        return re_str

    @classmethod
    def augment(cls):
        """Augment the class with computed formats, regexes, and other things. This caches these values so
        they don't have to be created for every instance. """

        import re

        level_name = cls.__name__.lower()

        cls.sl = names[level_name]

        cls.class_map[cls.__name__.lower()] = cls

        cls.sl_map[cls.sl] = cls

        cls.fmt = cls.make_format_string(cls.__name__.lower())

        cls.regex_str = cls.make_regex(cls.__name__.lower())
        cls.regex = re.compile(cls.regex_str)

        # List of field names
        cls.level = level_name
        cls.fields = segments[cls.sl]

    @classmethod
    def get_class(cls, name_or_sl):
        """Return a derived class based on the class name or the summary_level"""
        try:
            return cls.sl_map[int(name_or_sl)]

        except TypeError as e:
            raise TypeError("Bad name or sl: {} : {}".format(name_or_sl, e))
        except ValueError:
            try:
                return cls.class_map[name_or_sl.lower()]
            except (KeyError, ValueError):
                raise NotASummaryName("Value '{}' is not a valid summary level".format(name_or_sl))

    def __init__(self, *args, **kwargs):

        # This is a bit unusual, because it means, that , unlike nornal
        # python args, a kwarg can overwrite a position arg.

        d = dict(zip(self.fields, args + ((0,) * 10)))  # Add enough zeros to set all fields to zero

        d.update(kwargs)

        for k, v in d.items():
            if k in self.fields:
                try:
                    setattr(self, k, v)
                except TypeError as e:
                    raise TypeError("Failed to convert '{}' ({}) for field '{}' in {}: {}"
                                    .format(v, type(v), k, type(self), e))
                except ValueError as e:
                    raise ValueError("Failed to convert '{}' ({}) for field '{}' in {}: {}"
                                     .format(v, type(v), k, type(self), e))

    def __str__(self):

        d = self.__dict__
        d['sl'] = self.sl

        try:
            fn = six.get_method_function(self.encode)
            kwargs = {k: fn(v) for k, v in d.items()}
            return self.fmt.format(**kwargs)
        except (ValueError, KeyError) as e:
            raise ValueError('Bad value in {} for {}: {}'.format(d, self.fmt, e))

    def __hash__(self):
        return hash(str(self))

    def __cmp__(self, other):
        return cmp(str(self), str(other))

    @classmethod
    def parse(cls, gvid):

        if not bool(gvid):
            return None

        try:
            if not cls.sl:
                # Civick and ACS include the SL, so can call from base type.
                if six.PY3:
                    fn = cls.decode
                else:
                    fn = cls.decode.__func__

                sl = fn(gvid[0:cls.sl_width])
            else:
                sl = cls.sl  # Otherwise must use derived class.
        except ValueError as e:
            raise ValueError("Failed to parse gvid '{}': {}".format(gvid, str(e)))

        cls = cls.sl_map[sl]

        m = cls.regex.match(gvid)

        if not m:
            raise ValueError("Failed to match '{}' to '{}' ".format(gvid, cls.regex_str))

        d = m.groupdict()

        if not d:
            return None

        if six.PY3:
            fn = cls.decode
        else:
            fn = cls.decode.__func__
        d = {k: fn(v) for k, v in d.items()}

        try:
            del d['sl']
        except KeyError:
            pass

        return cls(**d)

    def convert(self, root_cls):
        """Convert to another derived class. cls is the base class for the derived type,
        ie AcsGeoid, TigerGeoid, etc. """

        d = self.__dict__
        d['sl'] = self.sl

        try:
            cls = root_cls.get_class(root_cls.sl)
        except (AttributeError, TypeError):
            # Hopefully because root_cls is a module
            cls = root_cls.get_class(self.sl)

        return cls(**d)

    def promote(self, level=None):
        """Convert to the next higher level summary level"""

        if level is None:

            if len(self.fields) < 2:
                if self.level in ('region', 'division', 'state', 'ua'):
                    cls = self.get_class('us')
                else:
                    return None
            else:
                cls = self.get_class(self.fields[-2])
        else:
            cls = self.get_class(level)

        d = dict(self.__dict__.items())
        d['sl'] = self.sl

        return cls(**d)

    def summarize(self):
        """Convert all of the values to their max values. This form is used to represent the summary level"""

        raise NotImplementedError

    def allval(self):
        """Convert the last value to zero. This form represents the entire higher summary level at the granularity
        of the lower  summary level. For example, for a county, it means 'All counties in the state' """

        d = dict(self.__dict__.items())
        d['sl'] = self.sl

        d[self.level] = 0

        cls = self.get_class(self.sl)

        return cls(**d)

    @property
    def tuples(self):
        """Return tuples of field, value, in the order of the levels as they are defined """
        return [(field, getattr(self, field, None)) for field in self.fields]

    @property
    def is_summary(self):
        """Return True if this geoid is an summary -- all of the fields are 0"""

        return str(self) == str(self.summarize())

    @property
    def is_allval(self):
        """Return True if this geoid is an allval -- the last field is zero, but the first is not"""

        tups = self.tuples

        return tups[-1][1] == 0 and tups[0][1] != 0

    @property
    def level_plural(self):
        """Return the name of the level as a plural"""
        return plurals.get(self.level, self.level + "s")


def generate_all(sumlevel, d):
    """Generate a dict that includes all of the available geoid values, with keys
    for the most common names for those values. """

    from geoid.civick import GVid
    from geoid.tiger import TigerGeoid
    from geoid.acs import AcsGeoid

    sumlevel = int(sumlevel)

    d = dict(d.items())

    # Map common name variants
    if 'cousub' in d:
        d['cosub'] = d['cousub']
        del d['cousub']

    if 'blkgrp' in d:
        d['blockgroup'] = d['blkgrp']
        del d['blkgrp']

    if 'zcta5' in d:
        d['zcta'] = d['zcta5']
        del d['zcta5']

    gvid_class = GVid.resolve_summary_level(sumlevel)

    if not gvid_class:
        return {}

    geoidt_class = TigerGeoid.resolve_summary_level(sumlevel)
    geoid_class = AcsGeoid.resolve_summary_level(sumlevel)

    try:
        return dict(
            gvid=str(gvid_class(**d)),
            geoid=str(geoid_class(**d)),
            geoidt=str(geoidt_class(**d))
        )
    except:
        raise
