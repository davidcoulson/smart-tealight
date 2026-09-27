# nRF52840 (XIAO BLE) — Matter over Thread, sleepy end device

Same app as `../nrf54-matter` (Nordic `light_bulb`, NCS v3.2.4) ported to the
**Seeed XIAO nRF52840** as the stand-in while the nRF54L15 is backordered.
Builds: 727 KB of the 784 KB app partition, 64 % RAM. **Not yet tested on hardware.**

Board specifics:
- `boards/xiao_ble_nrf52840.overlay` — PWM light on **P0.04 = D4**, console on the
  chip's own USB CDC ACM (the XIAO BLE has no debug probe), a `buttons` node on D5
  (Nordic's Matter glue requires one; nothing needs to be wired), die-temp sensor.
- `pm_static_xiao_ble_nrf52840.yml` — the board's Adafruit-bootloader layout
  (app at 0x27000 after MBR + SoftDevice reservation) with a 4 KB `factory_data`
  partition carved from the top of the app.
- `prj.conf` additions — legacy USB stack only (`USB_DEVICE_STACK_NEXT=n`, both were
  linking), **MTD OpenThread library** (`OPENTHREAD_MTD=y`,
  `OPENTHREAD_NORDIC_LIBRARY_MTD=y` — the FTD set has no MTD lib), shells off, QSPI
  NOR off (unused, and it drags in an external-flash factory-data provider).

Build:
```sh
cd /opt/nordic/ncs/v3.2.4
nrfutil sdk-manager toolchain launch --ncs-version v3.2.4 -- \
  west build -p always -b xiao_ble/nrf52840 -d <this dir>/build <this dir> -- \
  -DSB_CONFIG_BOOTLOADER_NONE=y -DSB_CONFIG_MATTER_OTA=n -DSB_CONFIG_MATTER_FACTORY_DATA_GENERATE=y
```

Flash: double-tap reset → `XIAO-SENSE` drive → copy `build/nrf52840-matter/zephyr/zephyr.uf2`.
The board reboots as a "Tealight nRF52840" USB serial device carrying the log.
Commission: HA → Matter → Add device, test code `34970112332`.
