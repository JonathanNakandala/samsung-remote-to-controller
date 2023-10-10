# Samsung Remote Control to Game Controller

Samsung remote controllers can be paired via bluetooth ble

This software maps the input device created automatically by Linux using the HID profile in BLE.

Then it creates a virtual gamepad using evdev that can then be used for example with Stepmania / Outfox as a controller to select songs.

If the device supports having a usb port act as a device then it's possible to have it emulate a device.



## How to Run

```
poetry run remote_to_controller
```


## Paring the remote control

Run:

```
bluetoothctl
```

Start scanning for BLE devices

```
scan le
```

Pair your device
```
pair <MAC Address>
```

Then check dmesg to see if the device has been set up as input devices:
```
sudo dmesg -w
```

```
[  243.694987] input: Smart Control 2016 Keyboard as /devices/virtual/misc/uhid/0005:0000:0000.0002/input/input4
[  243.695891] input: Smart Control 2016 Mouse as /devices/virtual/misc/uhid/0005:0000:0000.0002/input/input5
[  243.696344] input: Smart Control 2016 as /devices/virtual/misc/uhid/0005:0000:0000.0002/input/input6
[  243.696715] input: Smart Control 2016 as /devices/virtual/misc/uhid/0005:0000:0000.0002/input/input7
```

The Samsung remote control appears as multiple devices so you need to determine which one receives button inputs

Check dmesg to ensure that the device has been found


### Act as a USB Gamepad

Rather than a virtual gamepad, if you want to connect a SBC to another computer and have it appear as a gamepad.

First ensure that your device supports USB Device / Peripheral / Gadget mode

It may need to be enabled, and it may only work on a specific port. 


#### Setup

##### Kernel Modules
We need to load the kernel modules to support running as a USB device:

- libcomposite
    - Allows defining, activate, and manage a gadget configuration from user-space
- g_hid
    - Allows the device to act as a USB HID device when connected to another device

https://www.kernel.org/doc/html/v6.1/driver-api/usb/gadget.html

https://www.kernel.org/doc/Documentation/usb/gadget_hid.txt


We can use modules-load.d to configure kernel modules to load at boot:

https://www.freedesktop.org/software/systemd/man/modules-load.d.html

```
sudo nano /etc/modules-load.d/usb_gadget.conf
```

Inside the file we list the modules one per line

```
libcomposite
g_hid
```


### Configure permissions

Create:
```
sudo nano /etc/udev/rules.d/99-usb-gadget.rules
```

```
SUBSYSTEM=="usb_gadget", ACTION=="add|change", ATTRS{idVendor}=="0x1d6b", ATTRS{idProduct}=="0x0105", GROUP="input", MODE="0660"
```

You can try reloading live, but it seems it sometimes requires a reboot to actually work
```
sudo udevadm control --reload-rules
sudo udevadm trigger

```

## Troubleshooting

### `evdev.uinput.UInputError: "/dev/uinput" cannot be opened for writing`

Create a a file with a rule in /dev/dev/rules.d

This will allow the input group access to /dev/uinput`

```
KERNEL=="uinput", SUBSYSTEM=="misc", OPTIONS+="static_node=uinput", TAG+="uaccess", GROUP="input", MODE="0660"
```

And ensure that the current user is part of the input group by running:

```
groups
```

Then reboot the device

Afterwards we can check the permissions have been applied:

```
stat /dev/uinput
```

And it should return something like:

```
  File: /dev/uinput
  Size: 0               Blocks: 0          IO Block: 4096   character special file
Device: 5h/5d   Inode: 358         Links: 1     Device type: a,df
Access: (0660/crw-rw----)  Uid: (    0/    root)   Gid: (  106/   input)
```

### Pairing Issues

#### Input devices not being created

Some bluetooth chip drivers seem to have issues pairing with the remote control.
