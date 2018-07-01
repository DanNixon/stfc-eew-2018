# PlatformIO Guide

[PlatformIO](https://platformio.org/) is the tool we will use to build, upload
and debug firmware for the microcontroller boards.

There are two ways we can use PlatformIO; via the CLI or via Visual Studio Code.
The CLI is the clean and efficient way, VSCode is the *jack of all trades,
master of none* way.

## Building

Builds the firmware.

- VSCode: *Tasks* > *Run task...* > *PlatformIO: Build*
- CLI: `pio run`

## Upload

Builds and uploads the firmware to the board.

For simplicity just connect the board you want to flash to the PC.

- VSCode: *Tasks* > *Run task...* > *PlatformIO: Upload*
- CLI: `pio run -t upload`

## Serial monitor

Send and receive text from the USB virtual COM port (`Serial`).

- VSCode: *Tasks* > *Run task...* > *PlatformIO: Monitor*
- CLI: `pio device monitor`
