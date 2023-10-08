"""
Check if user is allowed to access /dev/uinput

"""
import os
import stat


def can_write_to_uinput() -> bool:
    """
    Check if /dev/uinput is writable
    Which is required for evdev by comparing current user's UID and GID
    """
    uid = os.getuid()
    gids = os.getgroups()
    uinput_stat = os.stat("/dev/uinput")

    mode = uinput_stat.st_mode

    # Check if the current user has write permissions
    if uid == uinput_stat.st_uid and mode & stat.S_IWUSR:
        return True

    # Check if one of the current user's groups has write permissions
    for gid in gids:
        if gid == uinput_stat.st_gid and mode & stat.S_IWGRP:
            return True

    # Check if others have write permissions
    if mode & stat.S_IWOTH:
        return True

    return False
