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


def set_report_id(number: int) -> list:
    """
    Generates a HID descriptor list to start a collection.

    This function begins a new collection in the HID descriptor. Collections allow
    grouping of related data inputs or outputs.
    """
    return [HIDFieldType.REPORT_ID, number]


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

    return descriptor


def end_collection() -> list:
    """
    End an opened collection
    """
    descriptor = [HIDFieldType.END_COLLECTION]
    return descriptor


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


def physical_minimum_maximum(min_value: int, max_value: int) -> list:
    """
    The min and max values of the button, axis etc
    """
    return [
        HIDFieldType.PHYSICAL_MINIMUM,
        min_value,
        HIDFieldType.PHYSICAL_MAXIMUM,
        max_value,
    ]


def report_size_count(size: int, count: int) -> list:
    """
    The size of the report and the count of how many to report
    """
    return [HIDFieldType.REPORT_SIZE, size, HIDFieldType.REPORT_COUNT, count]


def define_input_type(input_type: HIDInputType) -> list[int]:
    """
    Generates the descriptor bytes for the specified HID input type.
    """
    return [HIDFieldType.INPUT, input_type]


def usage_minimum_maximum(min_value: int, max_value: int) -> list:
    """
    The amount of of the item
    """
    return [
        HIDFieldType.USAGE_MINIMUM,
        min_value,
        HIDFieldType.USAGE_MAXIMUM,
        max_value,
    ]


def unit_and_exponent(unit: int, exponent: int):
    """
    Unit and exponent
    """

    return [
        HIDFieldType.UNIT,
        unit,
        HIDFieldType.UNIT_EXPONENT,
        exponent,
    ]


def define_digital_buttons(num_buttons: int) -> list[int]:
    """
    Generates a HID descriptor list for button controls.

    This function creates a descriptor for a range of button usages, from button 1
    to the specified maximum number of buttons. The buttons are defined as single-bit
    digital inputs with a logical range of 0 to 1.
    """
    return (
        (
            [
                HIDFieldType.USAGE_PAGE,
                HIDUsagePage.BUTTON,
            ]
        )
        + usage_minimum_maximum(1, num_buttons)
        + logical_minimum_maximum(0, 1)
        + physical_minimum_maximum(0, 1)
        + unit_and_exponent(0, 0)
        + report_size_count(1, num_buttons)
        + define_input_type(HIDInputType.VARIABLE)
    )


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
        + set_report_id(1)
        + start_collection(HIDCollectionType.PHYSICAL)
        # Define buttons
        + define_digital_buttons(num_buttons)
        + end_collection()
        + end_collection()
    )
    values = bytes(enum_to_values(descriptor))
    log.info("Generated Descriptor", descriptor=descriptor, values=values.hex())
    return values
