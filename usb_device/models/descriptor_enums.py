"""
Not Complete
Docs: https://usb.org/sites/default/files/hut1_4.pdf
"""

from enum import IntEnum


class HIDFieldType(IntEnum):
    """
    A descriptor has a set of field types that define what the values are

    https://usb.org/sites/default/files/hid1_11.pdf
    """

    # Main items
    INPUT = 0x81
    OUTPUT = 0x91
    FEATURE = 0xB1
    COLLECTION = 0xA1
    END_COLLECTION = 0xC0

    # Global items
    USAGE_PAGE = 0x05
    LOGICAL_MINIMUM = 0x15
    LOGICAL_MAXIMUM = 0x25
    PHYSICAL_MINIMUM = 0x35
    PHYSICAL_MAXIMUM = 0x45
    UNIT_EXPONENT = 0x55
    UNIT = 0x65
    REPORT_SIZE = 0x75
    REPORT_ID = 0x85
    REPORT_COUNT = 0x95
    PUSH = 0xA5
    POP = 0xB5

    # Local items
    USAGE = 0x09
    USAGE_MINIMUM = 0x19
    USAGE_MAXIMUM = 0x29
    DESIGNATOR_INDEX = 0x39
    DESIGNATOR_MINIMUM = 0x49
    DESIGNATOR_MAXIMUM = 0x59
    STRING_INDEX = 0x79
    STRING_MINIMUM = 0x89
    STRING_MAXIMUM = 0x99
    DELIMITER = 0xA9


class HIDCollectionType(IntEnum):
    """
    The types of collection
    Section: 6.2.2.6 Collection, End Collection Items
    https://usb.org/sites/default/files/hid1_11.pdf

    """

    PHYSICAL = 0x00
    APPLICATION = 0x01
    LOGICAL = 0x02
    REPORT = 0x03
    NAMED_ARRAY = 0x04
    USAGE_SWITCH = 0x05
    USAGE_MODIFIER = 0x06


class HIDInputType(IntEnum):
    """
    Enum representing HID input report field attributes.
    """

    # Main item tags
    DATA = 0x00
    CONSTANT = 0x01
    ARRAY = 0x00
    VARIABLE = 0x02
    ABSOLUTE = 0x00
    RELATIVE = 0x04
    NO_WRAP = 0x00
    WRAP = 0x08
    LINEAR = 0x00
    NON_LINEAR = 0x10
    PREFERRED_STATE = 0x00
    NO_PREFERRED = 0x20
    NO_NULL_POSITION = 0x00
    NULL_STATE = 0x40
    NON_VOLATILE = 0x00
    VOLATILE = 0x80
    BIT_FIELD = 0x00
    BUFFERED_BYTES = 0x100

    # Combinations
    DATA_VARIABLE_ABSOLUTE = DATA | VARIABLE | ABSOLUTE
    DATA_VARIABLE_RELATIVE = DATA | VARIABLE | RELATIVE
    DATA_ARRAY_ABSOLUTE = DATA | ARRAY | ABSOLUTE
    CONSTANT_ARRAY_ABSOLUTE = CONSTANT | ARRAY | ABSOLUTE
    CONSTANT_VARIABLE_ABSOLUTE = CONSTANT | VARIABLE | ABSOLUTE
