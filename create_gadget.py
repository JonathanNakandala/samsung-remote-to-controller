"""
Create a USB Gamepad Device
"""
from structlog import get_logger


from usb_device import USBGadget, models, create_gamepad_descriptor

log = get_logger()


def calculate_report_length(descriptor: bytes) -> int:
    """
    We need to define the length of the reports that get sent with the button press data
    """
    total_bits = 0
    descriptor_length = len(descriptor)
    i = 0

    report_size = 0
    while i < descriptor_length:
        # Check if current byte matches REPORT_SIZE
        if descriptor[i] == models.HIDFieldType.REPORT_SIZE.value:
            # Move to next byte to get the size value
            i += 1
            report_size = descriptor[i]  # This gives the size in bits
        elif descriptor[i] == models.HIDFieldType.REPORT_COUNT.value:
            # Move to next byte to get the count value
            i += 1
            report_count = descriptor[i]

            # Accumulate total bits
            total_bits += report_size * report_count
        i += 1

    # Convert total bits to bytes
    total_bytes = total_bits // 8
    return total_bytes


def setup_gamepad_gadget(descriptor):
    """
    Create a gamepad gadet to be used in USB host mode
    This will setup /dev/hidg0 as device to send data to

    """
    report_length = calculate_report_length(descriptor)
    log.info("Report length", length=report_length)
    joystick_model = models.USBGadgetModel(
        spec=models.GadgetSpec(
            idVendor="0x1d6b",
            idProduct="0x0104",
            bcdDevice="0x0100",
            bcdUSB="0x0200",
            bDeviceClass="0x00",
            bDeviceSubClass="0x00",
            bDeviceProtocol="0x00",
        ),
        strings=[
            models.GadgetLocale(
                strings=models.GadgetLocaleValues(
                    product="BananaPI Gamepad",
                    manufacturer="HomeMade",
                    serialnumber="12345",
                )
            )
        ],
        functions=[
            models.HIDFunction(
                subclass=models.HIDSubclass.NONE,
                protocol=models.HIDProtocol.NONE,
                report_length=str(report_length),
                report_desc=descriptor,
            )
        ],
    )
    # Create a new USBGadget instance
    joystick_gadget = USBGadget(gadget_name="my_gamepad", model=joystick_model)

    # Create the gadget directory in sysfs
    joystick_gadget.activate()


descriptors = create_gamepad_descriptor(24)
# Run the function to set up the gadget
setup_gamepad_gadget(descriptors)
