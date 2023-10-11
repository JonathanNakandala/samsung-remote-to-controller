"""
Input Device Selection
"""
import sys
import argparse

from structlog import get_logger
from evdev import list_devices, InputDevice
from remote_to_controller.console import get_user_selection
from remote_to_controller.models import Event, MappingDefinition
from remote_to_controller.input_capabilities import event_code_from_string

log = get_logger()


def select_device(event_mapping: Event) -> str:
    """
    Device Selection for Input based on specified event type and event code
    """
    devices = list_devices()

    if not devices:
        log.critical("No input devices found.")
        sys.exit()

    # Convert the event type and code strings to their corresponding integer values
    desired_event_type_code = event_code_from_string(event_mapping.type)
    desired_event_code_code = event_code_from_string(event_mapping.code)

    # Filter devices by the desired event type and event code
    devices = [
        dev_path
        for dev_path in devices
        if desired_event_type_code in InputDevice(dev_path).capabilities()
        and desired_event_code_code
        in InputDevice(dev_path).capabilities().get(desired_event_type_code, [])  # type: ignore
    ]

    if not devices:
        log.critical(
            "No devices supporting events found.",
            event=event_mapping,
        )
        sys.exit()

    device_list = [
        {"Device Path": dev_path, "Device Name": InputDevice(dev_path).name}
        for dev_path in devices
    ]

    device_list.sort(key=lambda x: int(x["Device Path"].split("event")[-1]))

    selected_device = get_user_selection(device_list)

    return selected_device["Device Path"]


def get_device(
    parsed_args: argparse.Namespace, mapping: MappingDefinition
) -> InputDevice:
    """
    Get Mappings from arg or let user select
    """
    if parsed_args.device:
        device_path = parsed_args.device
    else:
        device_path = select_device(mapping.event)

    try:
        return InputDevice(device_path)
    except FileNotFoundError:
        log.critical("Could not find device", path=device_path)
        sys.exit()
