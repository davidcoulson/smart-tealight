# nRF54L15 — Matter over Thread, sleepy end device

Nordic's `samples/matter/light_bulb` (NCS v3.2.4) adapted for the Seeed XIAO
nRF54L15 as a sleepy ICD. Builds clean; **not yet flashed or tested on hardware.**

What changed vs. the stock sample:
- `boards/xiao_nrf54l15_nrf54l15_cpuapp.overlay` — PWM light on P1.10 (= XIAO **D4**,
  same pin as the tea light), watchdog, full RRAM/SRAM, die-temp sensor for the
  802.15.4 radio.
- `pm_static_xiao_nrf54l15_nrf54l15_cpuapp.yml` — no MCUboot: app + factory_data +
  settings_storage only (the XIAO has no external flash for a secondary slot).
- `prj.conf` additions — ICD (`CONFIG_CHIP_ENABLE_ICD_SUPPORT`, 1 s slow poll,
  500 ms fast poll), `CONFIG_SENSOR`, no OTA/DFU/NFC (all need MCUboot or pins the
  XIAO lacks), `CONFIG_CHIP_BOOTLOADER_NONE`.
- AWS IoT integration removed.

Build (toolchain already installed under `/opt/nordic/ncs`):

```sh
cd /opt/nordic/ncs/v3.2.4
nrfutil sdk-manager toolchain launch --ncs-version v3.2.4 -- \
  west build -p always -b xiao_nrf54l15/nrf54l15/cpuapp -d <this dir>/build <this dir> -- \
  -DSB_CONFIG_BOOTLOADER_NONE=y -DSB_CONFIG_MATTER_OTA=n -DSB_CONFIG_MATTER_FACTORY_DATA_GENERATE=y
```

Note `SB_CONFIG_MATTER_OTA` must be off at the *sysbuild* level: sysbuild injects
`CONFIG_CHIP_OTA_REQUESTOR=y` after `prj.conf`, so setting it in `prj.conf` is
silently overridden.

Flash: the XIAO's onboard SAMD11 CMSIS-DAP probe via pyOCD (`pyocd flash --target
nrf54l build/merged.hex`) or `west flash`. Commission in HA → Matter → Add device
with the sample's test code `34970112332` (test DAC; HA warns and proceeds).
