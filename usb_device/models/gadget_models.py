"""
Pydantic Models
"""
from enum import IntEnum

from typing import Optional

from pydantic import BaseModel, Field


class HIDSubclass(IntEnum):
    """
    From the USB HID Specs
    Section 4.2
    The spec says reserved are values 3-255
    It's for BIOS support so can be set to 0
    """

    NONE = 0
    BOOT_INTERFACE = 1
    RESERVED = 3


class HIDProtocol(IntEnum):
    """
    From the USB HID Specs 1.1
    Section 4.3
    The spec says reserved are values 3-255
    Use NONE for non keyboard and mouse
    """

    NONE = 0
    KEYBOARD = 1
    MOUSE = 2
    RESERVED = 3


class HIDFunction(BaseModel):
    """
    Functions folder
    """

    name: str = Field(
        default="usb0",
        description="The name of the folder, for hid functions it starts with hid.",
    )
    subclass: HIDSubclass
    protocol: HIDProtocol
    report_length: str
    report_desc: bytes = Field(
        description="The USB HID Descriptor",
    )


class GadgetLocaleValues(BaseModel):
    """
    Text Strings to identify the device
    """

    serialnumber: str
    product: str
    manufacturer: str


class GadgetLocale(BaseModel):
    """
    Localised Text Strings to identify the device
    The default is en-us
    """

    language: str = Field(
        default="0x409",
        description="The language identifier for the strings, 0x409 is en-us",
    )
    strings: GadgetLocaleValues


class GadgetSpec(BaseModel):
    """
    The base directory configuration values
    /sys/kernel/config/<gadget_name>/
    """

    # Required
    idVendor: str = Field(
        ..., description="16-bit number assigned by USB-IF to the vendor."
    )
    idProduct: str = Field(
        ..., description="16-bit number assigned by vendor to product."
    )
    # Optional
    bcdUSB: str | None = Field(
        default=None,
        description="Binary-coded decimal indicating supported USB version.",
    )
    bcdDevice: str | None = Field(
        default=None,
        description="Binary-coded decimal indicating device-defined version number.",
    )
    bDeviceClass: str | None = Field(default=None, description="USB class code.")
    bDeviceSubClass: str | None = Field(
        default=None, description="USB subclass code for the device."
    )
    bDeviceProtocol: str | None = Field(
        default=None, description="Protocol code for the device."
    )
    bMaxPacketSize0: str | None = Field(
        default=None,
        description="Maximum packet size for endpoint zero. (For full-speed and lower)",
    )
    bmAttributes: str | None = Field(
        default=None, description="Bitmap defining how the device behaves on power."
    )
    bSelfPowered: str | None = Field(
        default=None, description="If the device is self-powered."
    )
    bRemoteWakeup: str | None = Field(
        default=None, description="If the device supports remote wakeup."
    )
    use_vbus_for_power: str | None = Field(
        default=None,
        description="Use VBUS to detect USB power instead of separate supply.",
    )
    max_power: str | None = Field(
        default=None,
        description="Maximum power consumption from USB bus in 2 mA units.",
    )
    os_desc_use: str | None = Field(
        default=None, description="If OS descriptors should be used."
    )
    os_desc_b_vendor_code: str | None = Field(
        default=None,
        description="Vendor code to retrieve Microsoft OS 2.0 descriptors.",
    )
    os_desc_qw_sign: str | None = Field(
        default=None, description="Microsoft OS 2.0 descriptor's signature string."
    )
    UDC: str | None = Field(
        default=None,
        description="Which UDC this gadget should bind to. Setting this activates the gadget.",
    )
    bNumConfigurations: str | None = Field(
        default=None, description="Number of configurations the gadget supports."
    )


class USBGadgetModel(BaseModel):
    """
    libcomposite configfs
    https://github.com/torvalds/linux/tree/master/drivers/usb/gadget


    """

    spec: GadgetSpec = Field(..., description="The base configuration of the device")
    strings: list[GadgetLocale] = Field(
        ..., description="Localisation Strings for the device such as name, manufactor"
    )
    functions: list[HIDFunction] = Field(..., description="The HID Functions")


class USBConfigDescriptor(BaseModel):
    """
    Represents a USB Configuration Descriptor
    Providing information about a USB device's configuration and power requirements.
    """

    bLength: int = Field(description="Total length of this configuration descriptor.")
    bDescriptorType: int = Field(
        description="Type of descriptor (configuration descriptor)."
    )
    wTotalLength: int = Field(
        description="Total length of data returned for this configuration."
    )
    bNumInterfaces: int = Field(
        description="Number of interfaces supported by this configuration."
    )
    bConfigurationValue: int = Field(description="Value to select this configuration.")
    iConfiguration: int = Field(
        description="Index of a string descriptor describing this configuration."
    )
    bmAttributes: int = Field(description="Configuration characteristics.")
    MaxPower: str = Field(
        description="Maximum power consumption of this configuration in 2 mA units (bMaxPower in USB spec)."
    )


class USBFunctionModel(BaseModel):
    """
    USB function attributes based on libcomposite's function attributes.
    """

    # Required
    name: str = Field(description="Name of the USB function.")

    # Optional
    protocols: str | None = Field(
        default=None, description="USB protocols supported by the function."
    )
    subclass: str | None = Field(
        default=None, description="USB subclass code for the function."
    )
    protocol: str | None = Field(
        default=None, description="USB protocol code for the function."
    )
    max_speed: str | None = Field(
        default=None, description="Maximum USB speed supported by the function."
    )
    number: str | None = Field(
        default=None, description="USB function number for composite devices."
    )
    driver: str | None = Field(default=None, description="Function driver name.")
    functions: str | None = Field(
        default=None, description="List of USB functions for composite devices."
    )
    configs: str | None = Field(
        default=None, description="List of USB configurations for composite devices."
    )


class HIDFunctionModel(USBFunctionModel):
    protocol: Optional[str] = Field(
        default=None, description="The HID protocol version (e.g., '0x01')."
    )
    subclass: Optional[str] = Field(
        default=None, description="The HID subclass (e.g., '0x01')."
    )
    bcdHID: Optional[str] = Field(
        default=None, description="The HID specification version (e.g., '0x0110')."
    )
    report_length: Optional[str] = Field(
        default=None, description="The length of the HID report descriptor."
    )
    report_desc: Optional[str] = Field(
        default=None, description="The HID report descriptor in hexadecimal format."
    )
