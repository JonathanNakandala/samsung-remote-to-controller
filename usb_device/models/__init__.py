"""
Exported Models
"""
from enum import IntEnum

from .gadget_models import (
    HIDSubclass,
    HIDProtocol,
    GadgetLocaleValues,
    GadgetLocale,
    GadgetSpec,
    USBGadgetModel,
    USBConfigDescriptor,
    USBFunctionModel,
    HIDFunctionModel,
    HIDFunction,
    GadgetLocale,
)
from .descriptor_usage_page import (
    HIDUsagePage,
    HIDPageGenericDesktop,
    HIDPageGameControls,
    HIDPageGeneric,
    HIDPageKeyboard,
    HIDPageLED,
    HIDPageButton,
    HIDPageSimulation,
    HIDPageVR,
    HIDPageSport,
)

from .descriptor_enums import (
    HIDFieldType,
    HIDCollectionType,
    HIDInputType,
)

USAGE_PAGE_TO_USAGES = {
    HIDUsagePage.GENERIC_DESKTOP: HIDPageGenericDesktop,
    HIDUsagePage.SIMULATION_CONTROLS: HIDPageSimulation,
    HIDUsagePage.VR_CONTROLS: HIDPageVR,
    HIDUsagePage.SPORT_CONTROLS: HIDPageSport,
    HIDUsagePage.GAME_CONTROLS: HIDPageGameControls,
    HIDUsagePage.GENERIC_DEVICE: HIDPageGeneric,
    HIDUsagePage.KEYBOARD_KEYPAD: HIDPageKeyboard,
    HIDUsagePage.LED: HIDPageLED,
    HIDUsagePage.BUTTON: HIDPageButton,
}
