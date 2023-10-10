"""
HID Usage Controls
"""

from enum import IntEnum


class HIDUsagePage(IntEnum):
    """
    Section 3: Usage Pages
    0x00 is undefined
    """

    GENERIC_DESKTOP = 0x01
    SIMULATION_CONTROLS = 0x02
    VR_CONTROLS = 0x03
    SPORT_CONTROLS = 0x04
    GAME_CONTROLS = 0x05
    GENERIC_DEVICE = 0x06
    KEYBOARD_KEYPAD = 0x07
    LED = 0x08
    BUTTON = 0x09


class HIDPageGenericDesktop(IntEnum):
    """
    Section 4: Generic Desktop Page 0x01


    0x00 is undefined
    0x03 is reserved
    """

    POINTER = 0x01
    MOUSE = 0x02
    JOYSTICK = 0x04
    GAMEPAD = 0x05
    KEYBOARD = 0x06
    KEYPAD = 0x07
    MULTI_AXIS_CONTROLLER = 0x08
    TABLET_PC_SYSTEM_CONTROLS = 0x09
    WATER_COOLING_DEVICE = 0x0A
    COMPUTER_CHASSIS_DEVICE = 0x0B
    WIRELESS_RADIO_CONTROLS = 0x0C
    PORTABLE_DEVICE_CONTROL = 0x0D
    SYSTEM_MULTI_AXIS_CONTROLLER = 0x0E
    SPATIAL_CONTROLLER = 0x0F
    ASSISTIVE_CONTROL = 0x10
    DEVICE_DOCK = 0x11
    DOCKABLE_DEVICE = 0x12
    CALL_STATE_MGMT_CONTROL = 0x13
    COUNTED_BUFFER = 0x3A
    SYSTEM_CONTROL = 0x80
    THUMBSTICK = 0x96
    SENSOR_ZONE = 0xC0
    CHASSIS_ENCLOSURE = 0xC5


class HIDPageSimulation(IntEnum):
    """

    Section 5: Simulation Controls Page 0x02
    """

    FLIGHT_SIMULATION_DEVICE = 0x01
    AUTOMOBILE_SIMULATION_DEVICE = 0x02
    TANK_SIMULATION_DEVICE = 0x03
    SPACESHIP_SIMULATION_DEVICE = 0x04
    SUBMARINE_SIMULATION_DEVICE = 0x05
    SAILING_SIMULATION_DEVICE = 0x06
    MOTORCYCLE_SIMULATION_DEVICE = 0x07
    SPORTS_SIMULATION_DEVICE = 0x08
    AIRPLANE_SIMULATION_DEVICE = 0x09
    HELICOPTER_SIMULATION_DEVICE = 0x0A
    MAGIC_CARPET_SIMULATION_DEVICE = 0x0B
    BICYCLE_SIMULATION_DEVICE = 0x0C
    FLIGHT_CONTROL_STICK = 0x20
    FLIGHT_STICK = 0x21
    CYCLIC_CONTROL = 0x22
    CYCLIC_TRIM = 0x23
    FLIGHT_YOKE = 0x24
    TRACK_CONTROL = 0x25


class HIDPageVR(IntEnum):
    """
    Section 6: VR Controls Page 0x03
    """

    BELT = 0x01
    BODY_SUIT = 0x02
    FLEXOR = 0x03
    GLOVE = 0x04
    HEAD_TRACKER = 0x05
    HEAD_MOUNTED_DISPLAY = 0x06
    HAND_TRACKER = 0x07
    OCULOMETER = 0x08
    VEST = 0x09
    ANIMATRONIC_DEVICE = 0x0A
    STEREO_ENABLE = 0x20
    DISPLAY_ENABLE = 0x21


class HIDPageSport(IntEnum):
    """
    INCOMPLETE
    Section 7: Sport Controls Page (0x04)
    """

    BASEBALL_BAT = 0x01
    GOLF_CLUB = 0x02
    ROWING_MACHINE = 0x03
    THREADMILL = 0x04
    STICK_TYPE = 0x28

class HIDPageGameControls(IntEnum):
    """
    INCOMPLETE
    Section 8: Game Controls Page 0x05
    """

    THREE_D_GAME_CONTROLLER = 0x01
    PINBALL_DEVICE = 0x02
    POINT_OF_VIEW = 0x20


class HIDPageGeneric(IntEnum):
    """
    INCOMPLETE
    Section 9: Generic Device Controls Page (0x06)
    """

    BACKGROUND_NON_USER_CONTROLS = 0x01
    BATTERY_STRENGTH = 0x20
    SOFTWARE_VERSION = 0x2A
    PROTOCOL_VERSION = 0x2B
    HARDWARE_VERSION = 0x2C


class HIDPageKeyboard(IntEnum):
    """
    INCOMPLETE
    Section 10: Keyboard/Keypad Page (0x07)
    """

    KEYBOARD_A = 0x04
    KEYBOARD_F1 = 0x3A
    KEYBOARD_ENTER = 0x28
    KEYPAD_ENTER = 0x58


class HIDPageLED(IntEnum):
    """
    INCOMPLETE
    Section 11: LED Page (0x08)
    """

    NUM_LOCK = 0x01
    POWER = 0x06
    ERROR = 0x39
    PLAYER_INDICATOR = 0x60


class HIDPageButton(IntEnum):
    """
    INCOMPLETE
    Section 12: Button Page (0x09)
    """

    BUTTON_OFF = 0x00
    BUTTON_1 = 0x01
    BUTTON_2 = 0x02
    BUTTON_3 = 0x03
