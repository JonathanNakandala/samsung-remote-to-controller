"""
Input Device Selection
"""
import sys
import argparse

from structlog import get_logger
from evdev import list_devices, InputDevice
from remote_to_controller.console import get_user_selection


log = get_logger()


def select_device() -> str:
    """
    Device Selection for Input
    """
    devices = list_devices()

    if not devices:
        log.critical("No input devices found.")
        sys.exit()

    device_list = [
        {"Device Path": dev_path, "Device Name": InputDevice(dev_path).name}
        for dev_path in devices
    ]

    device_list.sort(key=lambda x: int(x["Device Path"].split("event")[-1]))

    selected_device = get_user_selection(device_list)

    return selected_device["Device Path"]


def get_device(parsed_args: argparse.Namespace) -> InputDevice:
    """
    Get Mappings from arg or let user select
    """
    if parsed_args.device:
        device_path = parsed_args.device
    device_path = select_device()
    try:
        return InputDevice(device_path)
    except FileNotFoundError:
        log.critical("Could not find device", path=device_path)
        sys.exit()
