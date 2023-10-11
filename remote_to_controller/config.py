"""
Config Parsing
"""
import argparse

from pydantic import BaseModel, Field
from structlog import get_logger
from evdev import InputDevice

from remote_to_controller.device import get_device
from remote_to_controller.check_uinput import can_write_to_uinput
from remote_to_controller.check_gadget import check_kernel_modules
from remote_to_controller.mapping import get_mapping
from remote_to_controller.models import MappingDefinition, GadgetConfig
from remote_to_controller.input_capabilities import get_gadget_config

log = get_logger()


class Config(BaseModel, arbitrary_types_allowed=True):
    """
    Config Vars
    """

    device: InputDevice
    mapping: MappingDefinition
    button_hold_time: float = Field(
        description="Seconds wait between checking if button is still pressed"
    )
    gamepad: GadgetConfig


def parse_arguments():
    """
    Parse command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Work with a specified input device.")
    parser.add_argument(
        "--device",
        required=False,
        help="Path to the input device, e.g., /dev/input/eventX",
    )
    parser.add_argument(
        "--mapping-file",
        required=False,
        help="Filename of the Mapping yaml in the mappings directory",
    )
    parser.add_argument(
        "--button-hold-time",
        required=False,
        default=0.5,
        type=float,
        help="How long between checking if the button is still being held in",
    )
    parser.add_argument(
        "--gamepad-type",
        required=False,
        default="virtual",
        type=str,
        help="virtual gamepad for running on a local system. gadget for using usb host mode",
    )
    parser.add_argument(
        "--hid-endpoint",
        required=False,
        default="/dev/hidg0",
        type=str,
        help="The hid gadget endpoint",
    )
    parsed_args = parser.parse_args()

    return parsed_args


def set_config() -> Config:
    """
    Get and Set the config
    """
    parsed_args = parse_arguments()
    if check_kernel_modules():
        log.info("USB Mode Available")
    if can_write_to_uinput():
        log.info("Can write to /dev/uinput")
    mapping = get_mapping(parsed_args)
    device = get_device(parsed_args, mapping)
    gamepad = get_gadget_config(parsed_args)
    return Config(
        device=device,
        mapping=mapping,
        button_hold_time=parsed_args.button_hold_time,
        gamepad=gamepad,
    )
