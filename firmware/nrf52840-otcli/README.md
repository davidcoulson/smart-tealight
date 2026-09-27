# nRF52840 (XIAO BLE) — OpenThread CLI, link-diagnostic build

Plain NCS `openthread/cli` on the XIAO nRF52840 — no Matter — so the same
radio can be driven by hand: join a network from a dataset, switch between
MTD/FTD/SED with `ot mode`, ping the border router, register an SRP service,
read MAC counters. This is what found the MR4U border-router problem (see
`docs/thread-sed-bisect-2026-09-26.md`).

Build / flash (same as the Matter builds: sysbuild, no bootloader image,
serial DFU into the Adafruit bootloader after a double-tap reset):
```sh
cd /opt/nordic/ncs/v3.2.4
nrfutil sdk-manager toolchain launch --ncs-version v3.2.4 -- \
  west build -p always -b xiao_ble/nrf52840 -d <this dir>/build <this dir> -- -DSB_CONFIG_BOOTLOADER_NONE=y
cd <this dir>/build/nrf52840-otcli/zephyr
adafruit-nrfutil dfu genpkg --dev-type 0x0052 --sd-req 0x0123 --application zephyr.hex otcli.zip
adafruit-nrfutil dfu serial --package otcli.zip -p /dev/cu.usbmodem101 -b 115200 --singlebank
```
Shell is on the board's own CDC ACM (115200). The shell RX buffer is 64 bytes,
so paste long lines (the dataset) slowly — `tools/otcmd.py` does that.

Typical session:
```
ot dataset set active <hex tlv from the border router>
ot mode rn            # rx-on MTD child (rdn = FTD, - = sleepy, + ot pollperiod 500)
ot ifconfig up
ot thread start
ot state / ot parent / ot ipaddr
ot ping <BR RLOC> 32 10 0.5        # and the BR's ML-EID (SRP server address)
ot srp client host name x ; ot srp client host address auto
ot srp client service add x _matter._tcp 5540 ; ot srp client autostart enable
ot srp client host                 # want state:Registered
ot counters mac
```
