"""
Configure a USB Port to be a USB device when connected to another computer
"""
import os
from pathlib import Path

from structlog import get_logger
from .models import (
    USBGadgetModel,
    GadgetLocale,
    HIDFunction,
)

log = get_logger()


class USBGadget:
    """
    Represents a USB gadget using the libcomposite framework.
    """

    BASE_PATH = Path("/sys/kernel/config/usb_gadget/")

    def __init__(self, gadget_name: str, model: USBGadgetModel):
        self.gadget_name = gadget_name
        self.path = self.BASE_PATH / gadget_name
        self.model = model

        self.create()
        self.setup_from_model()

    def _get_attr_path(self, attribute: str, path: Path | None = None) -> Path:
        """
        Determines the attribute path.
        """
        return self.path / attribute if path is None else path / attribute

    def _write_value(
        self,
        attribute: str,
        value: str | bytes,
        path=None,
    ):
        """
        Writes a value to a specific attribute.
        """
        attr_path = self._get_attr_path(attribute, path)
        try:
            mode = "wb" if type(value) == bytes else "w"
            with attr_path.open(mode) as f:
                f.write(value)
                log.info("Wrote value to attribute", attribute=attribute, value=value)
        except (FileNotFoundError, PermissionError, OSError) as e:
            error_msg = None
            match e:
                case FileNotFoundError():
                    error_msg = "Attribute file not found"
                case PermissionError():
                    error_msg = "Permission denied for attribute"
                case OSError() as os_error:
                    error_msg = f"Error writing to attribute, error={str(os_error)}"
                case _:
                    error_msg = "Unknown error"

            if error_msg:
                log.error(error_msg, attribute_path=attr_path, exc_info=True)
            raise

    def _setup_specification(self, spec):
        for field, value in spec.model_dump().items():
            if value:
                self._write_value(field, value)

    def _setup_localisation(self, strings):
        for locale in strings:
            strings_path = self.path / f"strings/{locale.language}"
            strings_path.mkdir(parents=True, exist_ok=True)
            for field, value in locale.strings.model_dump().items():
                if value:
                    self._write_value(field, value, strings_path)

    def _setup_hid_functions(self, hid_functions: list[HIDFunction]):
        """
        Sets up the HID function for the gadget.
        """
        for hid_function in hid_functions:
            hid_function_path = self.path / f"functions/hid.{hid_function.name}"
            if not hid_function_path.exists():
                hid_function_path.mkdir()
                log.info(
                    "Created HID function directory in sysfs",
                    path=str(hid_function_path),
                )
            else:
                log.warning(
                    "HID function directory already exists", path=str(hid_function_path)
                )

            self._write_value(
                "protocol", str(hid_function.protocol.value), hid_function_path
            )
            self._write_value(
                "subclass", str(hid_function.subclass.value), hid_function_path
            )
            self._write_value(
                "report_length", str(hid_function.report_length), hid_function_path
            )
            self._write_value(
                "report_desc", hid_function.report_desc, hid_function_path
            )

    def _setup_config_strings(self, config_path: Path, locale: GadgetLocale):
        """
        Sets up the localized strings for the configuration.
        """
        strings_path = config_path / f"strings/{locale.language}"
        strings_path.mkdir(parents=True, exist_ok=True)
        for field, value in locale.strings.model_dump().items():
            if value:
                self._write_value(field, value, strings_path)

    def _link_function_to_config(self, function_name: str, config_name: str):
        """
        Links a function to a configuration.
        """
        function_path = self.path / f"functions/{function_name}"
        config_path = self.path / f"configs/{config_name}"

        link_path = config_path / function_name
        if not link_path.exists():
            link_path.symlink_to(function_path)
            log.info(f"Linked {function_name} to {config_name}")
        else:
            log.warning(f"{function_name} already linked to {config_name}")

    def _setup_configuration(
        self, config_name: str, max_power: int, locale: GadgetLocale
    ):
        """
        Sets up the configuration for the gadget.
        """
        config_path = self.path / f"configs/{config_name}"
        if not config_path.exists():
            config_path.mkdir()
            log.info("Created configuration directory in sysfs", path=str(config_path))
        else:
            log.warning("Configuration directory already exists", path=str(config_path))

        self._write_value("bmAttributes", "0x80", config_path)
        self._write_value("MaxPower", str(max_power), config_path)

        # Set up localized strings for the configuration
        # self._setup_config_strings(config_path, locale)

    def setup_from_model(self):
        """
        Set up the gadget using values from the model.
        """
        log.info(
            "Setting up USB Gadget Device Specification", gadget_name=self.gadget_name
        )
        self._setup_specification(self.model.spec)

        log.info("Setting up Localisation Strings", gadget_name=self.gadget_name)
        self._setup_localisation(self.model.strings)

        log.info("Configuring HID Function")
        self._setup_hid_functions(self.model.functions)

        log.info("Configuring Gadget Configuration")
        config_name = "c.1"
        max_power = 100
        self._setup_configuration(config_name, max_power, self.model.strings[0])

        function_name = f"hid.{self.model.functions[0].name}"
        self._link_function_to_config(function_name, config_name)

    def create(self):
        """
        Creates the gadget directory in sysfs.
        """

        try:
            if not self.path.exists():
                self.path.mkdir()
                log.info("Created gadget directory in sysfs", path=str(self.path))
            else:
                log.warning("Gadget directory already exists", path=str(self.path))
        except (PermissionError, IsADirectoryError, OSError) as e:
            error_msg = None
            match e:
                case PermissionError():
                    error_msg = "Permission denied for creating gadget directory"
                case IsADirectoryError():
                    error_msg = "A directory already exists with the given gadget name"
                case OSError() as os_error:
                    error_msg = (
                        f"Error creating gadget directory, error={str(os_error)}"
                    )
                case _:
                    error_msg = "Unknown error"

            if error_msg:
                log.error(error_msg, path=str(self.path), exc_info=True)
            raise

    def activate(self):
        """
        Activates the USB gadget by writing the contents of /sys/class/udc
        to a file named UDC within the gadget directory.
        """
        try:
            # Use os.listdir() to get the contents of the directory
            udc_list = os.listdir("/sys/class/udc")

            # Convert the list to a string, separated by newlines
            udc_str = "\n".join(udc_list)

            # Write the string to UDC file in the gadget directory
            udc_path = self.path / "UDC"
            with udc_path.open("w") as f:
                f.write(udc_str)
                log.info(f"Wrote '{udc_str}' to {udc_path}")

        except (FileNotFoundError, PermissionError, OSError) as e:
            log.error(f"Error during gadget activation: {e}", exc_info=True)
            raise

    def remove(self):
        """
        Removes the gadget directory from sysfs.
        """
        try:
            if self.path.exists():
                self.path.rmdir()
                log.info("Removed gadget directory from sysfs", path=str(self.path))
            else:
                log.warning("Gadget directory does not exist", path=str(self.path))
        except PermissionError:
            log.error(
                "Permission denied for removing gadget directory",
                path=str(self.path),
                exc_info=True,
            )
            raise
        except OSError as os_error:
            log.error(
                "Error removing gadget directory",
                path=str(self.path),
                error=str(os_error),
                exc_info=True,
            )
            raise
