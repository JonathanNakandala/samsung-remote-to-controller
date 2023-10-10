"""
USB HID Descriptor Creation
"""
from enum import IntEnum

from structlog import get_logger

from .models import USAGE_PAGE_TO_USAGES, HIDUsagePage, HIDPageGenericDesktop
from .models import (
    HIDFieldType,
    HIDCollectionType,
    HIDInputType,
)

log = get_logger()


def enum_to_values(items: list) -> list[int]:
    """
    Converts all any IntEnum instances into their values
    """
    return [item.value if isinstance(item, IntEnum) else item for item in items]


def set_usage(usage_page: HIDUsagePage, usage_definition) -> list:
    """
    Generates a HID descriptor list for usage page and usage.

    The initial part of the HID descriptor giving type of device and its functionalities.
    """

    mapping = USAGE_PAGE_TO_USAGES.get(usage_page)

    log.debug(
        "Mapping usage definition",
        page=usage_page,
        definition=usage_definition,
        mapping=mapping,
    )
    usage = [
        HIDFieldType.USAGE_PAGE,
        usage_page,
        HIDFieldType.USAGE,
        usage_definition,
    ]
    log.info("Generated usage block", block=usage)
    return usage


def start_collection(collection_type: HIDCollectionType) -> list:
    """
    Generates a HID descriptor list to start a collection.

    This function begins a new collection in the HID descriptor. Collections allow
    grouping of related data inputs or outputs.
    """
    return [HIDFieldType.COLLECTION, collection_type]


def create_collection(
    usage_page: HIDUsagePage,
    usage: HIDPageGenericDesktop,
    collection_type: HIDCollectionType,
) -> list[int]:
    """
    Generates a HID collection descriptor based on the given parameters.

    The function constructs a list of bytes for a HID collection descriptor using
    the specified usage page, usage, and collection type. The descriptor allows
    the configuration of HID devices, ensuring proper communication between
    the device and the host.
    """

    descriptor = [
        HIDFieldType.USAGE_PAGE,
        usage_page,
        HIDFieldType.USAGE,
        usage,
        HIDFieldType.COLLECTION,
        collection_type,
    ]

    return enum_to_values(descriptor)


def end_collection() -> list[int]:
    """
    End an opened collection
    """
    descriptor = [HIDFieldType.END_COLLECTION]
    return enum_to_values(descriptor)


def logical_minimum_maximum(min_value: int, max_value: int) -> list:
    """
    The min and max values of the button, axis etc
    """
    return [
        HIDFieldType.LOGICAL_MINIMUM,
        min_value,
        HIDFieldType.LOGICAL_MAXIMUM,
        max_value,
    ]


def define_axis(axis: int) -> list:
    return [HIDFieldType.USAGE, axis]


def report_size_count(size: int, count: int) -> list:
    return [HIDFieldType.REPORT_SIZE, size, HIDFieldType.REPORT_COUNT, count]


def input_data_variable_absolute() -> list:
    return [HIDFieldType.INPUT, 0x02]


def define_digital_buttons(num_buttons: int) -> list[int]:
    """
    Generates a HID descriptor list for button controls.

    This function creates a descriptor for a range of button usages, from button 1
    to the specified maximum number of buttons. The buttons are defined as single-bit
    digital inputs with a logical range of 0 to 1.
    """
    return [
        HIDFieldType.USAGE_PAGE,
        HIDUsagePage.BUTTON,
        HIDFieldType.USAGE_MINIMUM,
        1,
        HIDFieldType.USAGE_MAXIMUM,
        num_buttons,
        HIDFieldType.LOGICAL_MINIMUM,
        0,
        HIDFieldType.LOGICAL_MAXIMUM,
        1,
        HIDFieldType.REPORT_COUNT,
        num_buttons,
        HIDFieldType.REPORT_SIZE,
        0x01,  # Report Size (1 bit)
        HIDFieldType.INPUT,
        HIDInputType.DATA_VARIABLE_ABSOLUTE,  # Input (Data, Variable, Absolute)
    ]


def create_joystick_descriptor(num_buttons: int) -> bytes:
    """
    Create a Joystick
    """
    if num_buttons < 1 or num_buttons > 255:
        raise ValueError("Number of buttons should be between 1 and 255.")

    descriptor_bytes = (
        set_usage(HIDUsagePage.GENERIC_DESKTOP, HIDPageGenericDesktop.JOYSTICK)
        + start_collection(HIDCollectionType.APPLICATION)
        + logical_minimum_maximum(0x0, 0x1)
        + define_axis(0x30)  # Usage (X)
        + define_axis(0x31)  # Usage (Y)
        + report_size_count(
            0x08, 0x02
        )  # Report Size of 8 bits and Report Count of 2 axes
        + input_data_variable_absolute()
        + end_collection()
        + define_digital_buttons(num_buttons)
        + end_collection()
    )

    return bytes(enum_to_values(descriptor_bytes))


def define_input_type(input_type: HIDInputType) -> list[int]:
    """
    Generates the descriptor bytes for the specified HID input type.
    """
    return [HIDFieldType.INPUT.value, input_type.value]


def create_gamepad_descriptor(num_buttons: int) -> bytes:
    """
    Generates a HID gamepad descriptor for a specified number of buttons.
    """
    if num_buttons < 1 or num_buttons > 255:
        raise ValueError("Number of buttons should be between 1 and 255.")

    descriptor = (
        # Define the gamepad collection
        set_usage(HIDUsagePage.GENERIC_DESKTOP, HIDPageGenericDesktop.GAMEPAD)
        + start_collection(HIDCollectionType.APPLICATION)
        # Define buttons
        + set_usage(HIDUsagePage.BUTTON, 1)
        + define_digital_buttons(num_buttons)
        + define_input_type(HIDInputType.DATA_VARIABLE_ABSOLUTE)
        + end_collection()
    )
    values = enum_to_values(descriptor)
    print(values)
    return bytes(values)
