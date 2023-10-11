# Samsung Remote Control to Game Controller

Samsung remote controllers can be paired via bluetooth ble

This software maps the input device created automatically by Linux using the HID profile in BLE.

Then it creates a virtual gamepad using evdev that can then be used for example with Stepmania / Outfox as a controller to select songs.

If the device supports having a usb port act as a device then it's possible to have it emulate a device.


## Samsung 2016 Remote Controller

When paired with a linux machine, 4 devices get created.

`evtest` can be used to to view the events

```
/dev/input/event3:      Smart Control 2016 Keyboard
/dev/input/event4:      Smart Control 2016 Mouse
/dev/input/event5:      Smart Control 2016
/dev/input/event6:      Smart Control 2016
```

In this case event5 is the one to use as you can see the event appear using evtest 

```
Input driver version is 1.0.1
Input device ID: bus 0x5 vendor 0x0 product 0x0 version 0x0
Input device name: "Smart Control 2016"
Supported events:
  Event type 0 (EV_SYN)
  Event type 2 (EV_REL)
    Event code 9 (REL_MISC)
Properties:
Testing ... (interrupt to exit)
Event: time 1697040408.261407, type 2 (EV_REL), code 9 (REL_MISC), value 96
Event: time 1697040408.261407, -------------- SYN_REPORT ------------
Event: time 1697040408.351591, type 2 (EV_REL), code 9 (REL_MISC), value 96
Event: time 1697040408.351591, -------------- SYN_REPORT ------------
```
<details>
  <summary>evtest info for other input devices</summary>
event6:

```
Input driver version is 1.0.1
Input device ID: bus 0x5 vendor 0x0 product 0x0 version 0x0
Input device name: "Smart Control 2016"
Supported events:
  Event type 0 (EV_SYN)
Key repeat handling:
  Repeat type 20 (EV_REP)
    Repeat code 0 (REP_DELAY)
      Value    250
    Repeat code 1 (REP_PERIOD)
      Value     33
Properties:
Testing ... (interrupt to exit)
```

event4:

```
Select the device event number [0-6]: 4
Input driver version is 1.0.1
Input device ID: bus 0x5 vendor 0x0 product 0x0 version 0x0
Input device name: "Smart Control 2016 Mouse"
Supported events:
  Event type 0 (EV_SYN)
  Event type 1 (EV_KEY)
    Event code 272 (BTN_LEFT)
    Event code 273 (BTN_RIGHT)
    Event code 274 (BTN_MIDDLE)
  Event type 2 (EV_REL)
    Event code 0 (REL_X)
    Event code 1 (REL_Y)
  Event type 4 (EV_MSC)
    Event code 4 (MSC_SCAN)
```

event3

```
Select the device event number [0-6]: 3
Input driver version is 1.0.1
Input device ID: bus 0x5 vendor 0x0 product 0x0 version 0x0
Input device name: "Smart Control 2016 Keyboard"
Supported events:
  Event type 0 (EV_SYN)
  Event type 1 (EV_KEY)
    Event code 1 (KEY_ESC)
    Event code 2 (KEY_1)
    Event code 3 (KEY_2)
    Event code 4 (KEY_3)
    Event code 5 (KEY_4)
    Event code 6 (KEY_5)
    Event code 7 (KEY_6)
    Event code 8 (KEY_7)
    Event code 9 (KEY_8)
    Event code 10 (KEY_9)
    Event code 11 (KEY_0)
    Event code 12 (KEY_MINUS)
    Event code 13 (KEY_EQUAL)
    Event code 14 (KEY_BACKSPACE)
    Event code 15 (KEY_TAB)
    Event code 16 (KEY_Q)
    Event code 17 (KEY_W)
    Event code 18 (KEY_E)
    Event code 19 (KEY_R)
    Event code 20 (KEY_T)
    Event code 21 (KEY_Y)
    Event code 22 (KEY_U)
    Event code 23 (KEY_I)
    Event code 24 (KEY_O)
    Event code 25 (KEY_P)
    Event code 26 (KEY_LEFTBRACE)
    Event code 27 (KEY_RIGHTBRACE)
    Event code 28 (KEY_ENTER)
    Event code 29 (KEY_LEFTCTRL)
    Event code 30 (KEY_A)
    Event code 31 (KEY_S)
    Event code 32 (KEY_D)
    Event code 33 (KEY_F)
    Event code 34 (KEY_G)
    Event code 35 (KEY_H)
    Event code 36 (KEY_J)
    Event code 37 (KEY_K)
    Event code 38 (KEY_L)
    Event code 39 (KEY_SEMICOLON)
    Event code 40 (KEY_APOSTROPHE)
    Event code 41 (KEY_GRAVE)
    Event code 42 (KEY_LEFTSHIFT)
    Event code 43 (KEY_BACKSLASH)
    Event code 44 (KEY_Z)
    Event code 45 (KEY_X)
    Event code 46 (KEY_C)
    Event code 47 (KEY_V)
    Event code 48 (KEY_B)
    Event code 49 (KEY_N)
    Event code 50 (KEY_M)
    Event code 51 (KEY_COMMA)
    Event code 52 (KEY_DOT)
    Event code 53 (KEY_SLASH)
    Event code 54 (KEY_RIGHTSHIFT)
    Event code 55 (KEY_KPASTERISK)
    Event code 56 (KEY_LEFTALT)
    Event code 57 (KEY_SPACE)
    Event code 58 (KEY_CAPSLOCK)
    Event code 59 (KEY_F1)
    Event code 60 (KEY_F2)
    Event code 61 (KEY_F3)
    Event code 62 (KEY_F4)
    Event code 63 (KEY_F5)
    Event code 64 (KEY_F6)
    Event code 65 (KEY_F7)
    Event code 66 (KEY_F8)
    Event code 67 (KEY_F9)
    Event code 68 (KEY_F10)
    Event code 69 (KEY_NUMLOCK)
    Event code 70 (KEY_SCROLLLOCK)
    Event code 71 (KEY_KP7)
    Event code 72 (KEY_KP8)
    Event code 73 (KEY_KP9)
    Event code 74 (KEY_KPMINUS)
    Event code 75 (KEY_KP4)
    Event code 76 (KEY_KP5)
    Event code 77 (KEY_KP6)
    Event code 78 (KEY_KPPLUS)
    Event code 79 (KEY_KP1)
    Event code 80 (KEY_KP2)
    Event code 81 (KEY_KP3)
    Event code 82 (KEY_KP0)
    Event code 83 (KEY_KPDOT)
    Event code 86 (KEY_102ND)
    Event code 87 (KEY_F11)
    Event code 88 (KEY_F12)
    Event code 96 (KEY_KPENTER)
    Event code 97 (KEY_RIGHTCTRL)
    Event code 98 (KEY_KPSLASH)
    Event code 99 (KEY_SYSRQ)
    Event code 100 (KEY_RIGHTALT)
    Event code 102 (KEY_HOME)
    Event code 103 (KEY_UP)
    Event code 104 (KEY_PAGEUP)
    Event code 105 (KEY_LEFT)
    Event code 106 (KEY_RIGHT)
    Event code 107 (KEY_END)
    Event code 108 (KEY_DOWN)
    Event code 109 (KEY_PAGEDOWN)
    Event code 110 (KEY_INSERT)
    Event code 111 (KEY_DELETE)
    Event code 119 (KEY_PAUSE)
    Event code 125 (KEY_LEFTMETA)
    Event code 126 (KEY_RIGHTMETA)
    Event code 127 (KEY_COMPOSE)
  Event type 4 (EV_MSC)
    Event code 4 (MSC_SCAN)
  Event type 17 (EV_LED)
    Event code 0 (LED_NUML) state 0
    Event code 1 (LED_CAPSL) state 0
    Event code 2 (LED_SCROLLL) state 0
    Event code 3 (LED_COMPOSE) state 0
    Event code 4 (LED_KANA) state 0
Key repeat handling:
  Repeat type 20 (EV_REP)
    Repeat code 0 (REP_DELAY)
      Value    250
    Repeat code 1 (REP_PERIOD)
      Value     33
```
</details>


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
