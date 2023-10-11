"""
The Samsung remote appears as 4 input Devices with two having the same name
So we need to search for the input device which has the capabilities that log the button presses
"""
import argparse

import evdev
from remote_to_controller.models import GadgetConfig


def event_code_from_string(event_string: str) -> int:
    """
    Convert a string like "EV_REL" to its corresponding integer value from evdev.ecodes.
    If the event_string is not valid, it returns None.
    """
    return getattr(evdev.ecodes, event_string)


def get_gadget_config(parsed_args: argparse.Namespace) -> GadgetConfig:
    """
    Gadget config
    """
    gamepad_type = parsed_args.gamepad_type
    hid_endpoint = parsed_args.hid_endpoint
    config = GadgetConfig(gamepad_type=gamepad_type, hid_endpoint=hid_endpoint)
    return config
