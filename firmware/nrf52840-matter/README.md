# nRF52840 (XIAO BLE) — Matter over Thread, sleepy end device

Same app as `../nrf54-matter` (Nordic `light_bulb`, NCS v3.2.4) ported to the
**Seeed XIAO nRF52840** as the stand-in while the nRF54L15 is backordered.
Builds: 723 KB of the 784 KB app partition, 64 % RAM. **Boots and advertises Matter
over BLE on the XIAO nRF52840** (2026-09-27); commissioning is the next test.

Board specifics:
- `boards/xiao_ble_nrf52840.overlay` — PWM light on **P0.04 = D4**, console on the
  chip's own USB CDC ACM (the XIAO BLE has no debug probe), a `buttons` node on D5
  (Nordic's Matter glue requires one; nothing needs to be wired), die-temp sensor.
- `pm_static_xiao_ble_nrf52840.yml` — the board's Adafruit-bootloader layout
  (app at 0x27000 after MBR + SoftDevice reservation). It still reserves a 4 KB
  `factory_data` slot, but **factory data is off** (`CHIP_FACTORY_DATA=n`): the
  Adafruit bootloader only flashes the app image, so a generated factory-data
  partition never reaches the chip and the app sat silent at boot waiting for it.
  The build uses the CHIP test identity instead (VID 0xFFF1, PID 0x8005,
  discriminator 3840, passcode 20202021 — code `34970112332`).
- `prj.conf` additions — legacy USB stack only (`USB_DEVICE_STACK_NEXT=n`, both were
  linking), **MTD OpenThread library** (`OPENTHREAD_MTD=y`,
  `OPENTHREAD_NORDIC_LIBRARY_MTD=y` — the FTD set has no MTD lib), shells off, QSPI
  NOR off (unused, and it drags in an external-flash factory-data provider).

Build:
```sh
cd /opt/nordic/ncs/v3.2.4
nrfutil sdk-manager toolchain launch --ncs-version v3.2.4 -- \
  west build -p always -b xiao_ble/nrf52840 -d <this dir>/build <this dir> -- \
  -DSB_CONFIG_BOOTLOADER_NONE=y -DSB_CONFIG_MATTER_OTA=n -DSB_CONFIG_MATTER_FACTORY_DATA_GENERATE=n
```

Flash (double-tap reset first → green LED pulses, `XIAO-SENSE` mounts), either:
```sh
# serial DFU (what worked; the zip is made by the build)
adafruit-nrfutil dfu serial --package build/nrf52840-matter/zephyr/tealight.zip \
  -p /dev/cu.usbmodem101 -b 115200 --singlebank
```
or copy `build/nrf52840-matter/zephyr/zephyr.uf2` onto the `XIAO-SENSE` drive.
The board reboots as a "Tealight nRF52840" USB serial device carrying the log
(115200; on macOS it enumerates as a *new* `cu.usbmodem` port, not the bootloader's).
Commission: HA companion app → Settings → Devices → Add device → Matter, code
`34970112332` (BLE, so it has to be the phone app or a Matter server with a
Bluetooth adapter — the HA server's "Add device" only works if the host has BT).
