"""
Remote Button Press to Virtual Controller
"""
import time
import asyncio
from typing import Tuple
from evdev import UInput, ecodes, InputEvent, InputDevice

from structlog import get_logger

from remote_to_controller.config import set_config, Config
from remote_to_controller.models import MappingDefinition

log = get_logger()

EV_KEY = ecodes.ecodes["EV_KEY"]
LAST_PRESS_TIME = 0.0


def create_event_translation(
    mapping: MappingDefinition,
) -> Tuple[dict[int, int], dict[int, int]]:
    """
    Create a dictionary to translate remote values to gamepad event codes.
    """
    translations = {
        map.remote_value: getattr(ecodes, map.event_code) for map in mapping.mappings
    }

    gadget_translations = {
        map.remote_value: index for index, map in enumerate(mapping.mappings)
    }

    log.debug("Generated mappings", virtual=translations, gadget=gadget_translations)
    return translations, gadget_translations


def get_capabilities(mapping: MappingDefinition) -> dict[int, list[int]]:
    """
    Set the types of events (e.g., button presses, key presses) that the virtual gamepad
    """
    capabilities = {EV_KEY: []}
    for map_data in mapping.mappings:
        event_code_mapped = getattr(ecodes, map_data.event_code)
        if "BTN_" in map_data.event_code or "KEY_" in map_data.event_code:
            capabilities[EV_KEY].append(event_code_mapped)
    return capabilities


async def process_event(
    event: InputEvent, event_translation: dict[int, int]
) -> int | None:
    """
    Process button press events
    """
    global LAST_PRESS_TIME  # pylint: disable=global-statement

    log.info(
        "Received Event",
        event_code=event.code,
        event_type=event.type,
        event_value=event.value,
    )

    # Fetch the translated event (gamepad's button code)
    translated_event = event_translation.get(event.value)
    if translated_event is None:
        log.warning("Event value not mapped", event_value=event.value)
        return None

    current_time = time.time()
    # Check if the button was pressed within the last 500ms
    if current_time - LAST_PRESS_TIME < 0.2:
        log.info("Button pressed within 200ms. Skipping processing.")
        return None

    # Update last press time
    LAST_PRESS_TIME = current_time

    return translated_event


def create_virtual_gamepad(config: Config):
    """
    Create a virtual gamepad
    """
    capabilities = get_capabilities(config.mapping)
    virtual_gp = UInput(capabilities, name="VirtualGamepad")
    log.info("Virtual Gamepad Initialized")
    return virtual_gp


async def send_to_virtual(virtual_gp: UInput, translated_event: int):
    """
    Send the processed event to the virtual gamepad
    """
    log.debug(
        "Attempting to write button press to virtual gamepad",
        event_type=EV_KEY,
        translated_event=translated_event,
    )

    # Register the button press
    virtual_gp.write(EV_KEY, translated_event, 1)  # Button press
    virtual_gp.syn()
    log.info("Button Pressed", button=translated_event)

    log.debug(
        "Attempting to write button release to virtual gamepad",
        event_type=EV_KEY,
        translated_event=translated_event,
    )

    # Register the button release
    virtual_gp.write(EV_KEY, translated_event, 0)  # Button release
    virtual_gp.syn()
    log.info("Button Released", button=translated_event)


def bytes_to_binary_str(bytes_obj: bytearray) -> str:
    """
    Outputs the data to a binary strin
    """
    return "".join(f"{byte:08b}" for byte in bytes_obj)


async def write_hid_report_to_device(hid_endpoint, buttons_state):
    """
    Send HID report to the device endpoint.

    :param buttons_state: A list of 24 booleans, where each boolean represents
                          the state of a button (True=pressed, False=not pressed).
    """
    if len(buttons_state) != 24:
        raise ValueError("Expected 24 button states")

    # Report ID
    report_bytes = bytearray([0x01])

    # Convert the button states to a 3-byte report
    current_byte = 0x00
    for i, button in enumerate(buttons_state):
        if button:
            current_byte |= 1 << (i % 8)

        # Every 8 buttons, append the current byte to report_bytes and reset current_byte
        if (i + 1) % 8 == 0:
            report_bytes.append(current_byte)
            current_byte = 0x00

    # Fill in the remaining bytes (if any)
    while len(report_bytes) < 4:
        report_bytes.append(0x00)
    # Report for all buttons released
    release_report_bytes = bytearray([0x01, 0x00, 0x00, 0x00])
    try:
        with open(hid_endpoint, "wb") as hid_device:
            # Write the button press report
            hid_device.write(report_bytes)
            log.info(
                "Sent button press to gadget with result",
                endpoint=hid_endpoint,
                data=bytes_to_binary_str(report_bytes),
            )
    except (FileNotFoundError, OSError, PermissionError, ValueError, IOError):
        log.error("Error while sending to gadget", exc_info=True)
        # Short delay before releasing the button
        # To ensure the press is registered.
    await asyncio.sleep(0.2)
    try:
        with open(hid_endpoint, "wb") as hid_device:
            # Write the button release report
            hid_device.write(release_report_bytes)
            log.info(
                "Sent button release to gadget with result",
                endpoint=hid_endpoint,
                data=bytes_to_binary_str(release_report_bytes),
            )

    except (FileNotFoundError, OSError, PermissionError, ValueError, IOError):
        log.error("Error while sending to gadget", exc_info=True)


async def send_to_gadget(hid_endpoint, translated_event: int):
    """
    Send the processed event to the external gadget.
    """
    if not 0 <= translated_event < 24:
        raise ValueError("Position must be between 0 and 23 inclusive.")

    buttons_state = [False] * 24
    buttons_state[translated_event] = True
    await write_hid_report_to_device(hid_endpoint, buttons_state)


def device_available(config: Config) -> bool:
    """
    Check to see if configured deevice is available
    """
    try:
        device = InputDevice(config.device.path)
        device.close()
        return True
    except OSError:
        return False


RECHECK_DELAY = 10


async def watch_device(config: Config):
    """
    Read events and process
    """
    virtual_translation, gadget_translation = create_event_translation(config.mapping)

    while True:
        try:
            match config.gamepad.gamepad_type:
                case "virtual":
                    virtual_gp = create_virtual_gamepad(config)
                    try:
                        async for event in config.device.async_read_loop():
                            if event.type == getattr(ecodes, config.mapping.event.type):
                                processed_event = await process_event(
                                    event, virtual_translation
                                )
                                if processed_event is not None:
                                    await send_to_virtual(virtual_gp, processed_event)
                                await asyncio.sleep(0.1)
                    finally:
                        virtual_gp.close()
                        log.info("Virtual Gamepad Closed")

                case "gadget":
                    try:
                        async for event in config.device.async_read_loop():
                            if event.type == getattr(ecodes, config.mapping.event.type):
                                processed_event = await process_event(
                                    event, gadget_translation
                                )
                                if processed_event is not None:
                                    await send_to_gadget(
                                        config.gamepad.hid_endpoint, processed_event
                                    )
                                await asyncio.sleep(0.1)
                    finally:
                        log.info("Ending gadget")

                case _:
                    raise ValueError("Unsupported gamepad type")

        except OSError:
            log.warning("Device disconnected, waiting for it to become available...")
            while not device_available(config.device.path):
                await asyncio.sleep(RECHECK_DELAY)
            log.info("Device reconnected, resuming...")


def main():
    """
    Entrypoint
    """

    config = set_config()
    log.info("Samsung Report to Virtual Gamepad", config=config)
    # virtual_gamepad(config)
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(watch_device(config))
    except KeyboardInterrupt:
        pass
    finally:
        loop.close()


if __name__ == "__main__":
    main()
