from usb_device import (
    USBGadget,
    models,
    create_gamepad_descriptor,
)


def setup_rpi_joystick_gadget(descriptor):
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
                    product="My Controller",
                    manufacturer="HomeMade",
                    serialnumber="12345",
                )
            )
        ],
        functions=[
            models.HIDFunction(
                subclass=models.HIDSubclass.NONE,
                protocol=models.HIDProtocol.NONE,
                report_length=str(len(descriptor)),
                report_desc=descriptor,
            )
        ],
    )
    # Create a new USBGadget instance
    joystick_gadget = USBGadget("32_buttons_rpi_joystick5", joystick_model)

    # Create the gadget directory in sysfs
    joystick_gadget.activate()


descriptor = create_gamepad_descriptor(18)
# Run the function to set up the gadget
setup_rpi_joystick_gadget(descriptor)
