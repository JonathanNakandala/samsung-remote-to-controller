"""
Functions to configure a device to act as a USB Game Controller
This requires hardware support in the device to be able to act as a USB device rather than a host
"""
from structlog import get_logger

log = get_logger()


def load_modules_list() -> str:
    """
    Load Kernel Modules list
    """
    try:
        with open("/proc/modules", "r", encoding="utf-8") as proc_modules:
            return proc_modules.read()
    except (FileNotFoundError, IOError, PermissionError):
        log.error("Unable to read /proc/modules", exc_info=True)
        raise


def check_kernel_modules() -> bool:
    """
    Check if the required kernel modules for USB devices are loaded
    """
    modules_to_check = ["g_hid", "libcomposite"]
    modules_list = load_modules_list()

    not_loaded_modules = []
    for module in modules_to_check:
        if module not in modules_list:
            not_loaded_modules.append(module)

    if not not_loaded_modules:
        log.info("All required kernel modules are loaded.")
        return True

    missing_modules = ", ".join(not_loaded_modules)
    log.warning(
        f"Kernel module(s) {missing_modules} are not loaded can't act as usb gadget"
    )
    return False
