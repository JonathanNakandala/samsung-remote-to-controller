import time
import random

HID_DEVICE_PATH = "/dev/hidg0"


def send_hid_report(buttons_state):
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

    with open(HID_DEVICE_PATH, "wb") as hid_device:
        hid_device.write(report_bytes)


def send_static_report():
    # A report with report ID and where no button is pressed
    report_bytes = bytearray([0x01, 0x00, 0x00, 0x00])

    with open(HID_DEVICE_PATH, "wb") as hid_device:
        hid_device.write(report_bytes)


def main():
    while True:
        # Generate a random button state (24 buttons, randomly pressed or not)
        random_button_states = [random.choice([True, False]) for _ in range(24)]
        send_hid_report(random_button_states)
        time.sleep(0.01)

        # Release all buttons
        # send_static_report()
        time.sleep(0.1)


if __name__ == "__main__":
    main()
