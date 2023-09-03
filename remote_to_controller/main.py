"""
Remote Button Press to Virtual Controller
"""
import time
import asyncio
from evdev import UInput, ecodes, InputEvent

from structlog import get_logger

from remote_to_controller.config import set_config, Config
from remote_to_controller.models import MappingDefinition

log = get_logger()

EV_KEY = ecodes.ecodes["EV_KEY"]
LAST_PRESS_TIME = 0.0


def create_event_translation(mapping: MappingDefinition) -> dict[int, int]:
    """
    Create a dictionary to translate remote values to gamepad event codes.
    """
    translations = {
        map.remote_value: getattr(ecodes, map.event_code) for map in mapping.mappings
    }
    print(translations)
    return translations


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
    event: InputEvent, event_translation: dict[int, int], virtual_gp: UInput
):
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
    if translated_event is not None:
        current_time = time.time()

        # Check if the button was pressed within the last 500ms
        if current_time - LAST_PRESS_TIME < 0.2:
            log.info("Button pressed within 200ms. Skipping processing.")
            return

        log.debug(
            "Attempting to write button press to virtual gamepad",
            event_type=event.type,
            translated_event=translated_event,
        )

        # Register the button press
        virtual_gp.write(EV_KEY, translated_event, 1)  # Button press
        virtual_gp.syn()
        log.info("Button Pressed", button=event.code, remote_value=event.value)

        # Update last press time
        LAST_PRESS_TIME = current_time

        log.debug(
            "Attempting to write button release to virtual gamepad",
            event_type=event.type,
            translated_event=translated_event,
        )

        # Register the button release
        virtual_gp.write(EV_KEY, translated_event, 0)  # Button release
        virtual_gp.syn()
        log.info("Button Released", button=event.code)
    else:
        log.warning("Event value not mapped", event_value=event.value)


async def watch_device(config: Config):
    """
    Read events and process
    """
    event_translation = create_event_translation(config.mapping)
    capabilities = get_capabilities(config.mapping)
    virtual_gp = UInput(capabilities, name="VirtualGamepad")
    log.info("Virtual Gamepad Initialized")

    try:
        async for event in config.device.async_read_loop():
            if event.type == getattr(ecodes, config.mapping.event.type):
                await process_event(event, event_translation, virtual_gp)
                await asyncio.sleep(0.1)
    finally:
        virtual_gp.close()
        log.info("Virtual Gamepad Closed")


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
