# Matter over Thread test on the XIAO ESP32-C6

Goal: prove the C6 can join your Home Assistant as a Matter-over-Thread
light through the existing OpenThread Border Router, using Espressif's stock
`light` example with two small XIAO-specific tweaks. No custom app yet.

Budget: the esp-matter checkout is ~10 GB and the first build takes
20–40 min on a Mac. Everything below runs on the Mac, not in the cloud.

## 1. Install ESP-IDF + esp-matter (once)

```bash
mkdir -p ~/esp && cd ~/esp
git clone --recursive https://github.com/espressif/esp-idf.git
cd esp-idf && git checkout v6.0.2 && git submodule update --init --recursive
./install.sh esp32c6
cd ..

source esp-idf/export.sh
git clone --depth 1 https://github.com/espressif/esp-matter.git
cd esp-matter
git submodule update --init --depth 1
cd connectedhomeip/connectedhomeip
./scripts/checkout_submodules.py --platform esp32 darwin --shallow
cd ../..
./install.sh
cd ..
```

Every new terminal:

```bash
source ~/esp/esp-idf/export.sh
source ~/esp/esp-matter/export.sh
export IDF_CCACHE_ENABLE=1
```

## 2. XIAO tweaks to the light example

```bash
cd ~/esp/esp-matter/examples/light
cp ~/dev/smart-tealight/firmware/matter-thread-test/sdkconfig.xiao_c6 .
```

Then in `main/app_main.cpp`, add the include and the RF-switch block from
[`xiao_rf_switch.inc`](xiao_rf_switch.inc): the include at the top, the block
as the **first lines of `app_main()`** (before `nvs_flash_init()`). Without it
the radio is connected to no antenna (same trap as ESPHome).

## 3. Build, flash, watch

```bash
idf.py -D SDKCONFIG_DEFAULTS="sdkconfig.defaults;sdkconfig.defaults.c6_thread;sdkconfig.xiao_c6" set-target esp32c6 build
idf.py -p /dev/cu.usbmodem101 flash monitor
```

In the monitor you should see OpenThread start and BLE advertising for
commissioning. The example ships with the Matter **test** credentials:

| | |
|---|---|
| Manual pairing code | `34970112332` |
| QR payload | `MT:Y.K9042C00KA0648G00` |
| Passcode / discriminator | `20202021` / `3840` |

(`matter onboardingcodes ble` in the monitor's console prints them too.)

## 4. Commission from Home Assistant

HA → Settings → Devices & services → **Matter** → Add device → *Add Matter
device* → enter the manual code (or scan the QR from the phone app). HA's
Matter server commissions over BLE, hands the device your Thread network
credentials from the OTBR, and it joins as a Thread end device. You get an
"Extended Color Light" with on/off, brightness and colour.

Test-credential caveat: HA accepts them (it warns about the test DAC). Real
products need their own attestation cert; for our own devices we keep using
test certs and click through.

## 5. What to measure

* **Does it commission and stay reachable?** Toggle it from HA a dozen
  times over ten minutes. Thread signal → HA Thread panel shows the device.
* **Sleep current.** The stock example is *not* a sleepy end device: expect
  ~20–40 mA idle. That's fine for this test; ICD/SED config is step 6.
* **RF switch:** if BLE advertising never shows up on the phone or
  commissioning times out, re-check the `xiao_rf_switch.inc` block.

## 6. Next (after this passes)

* Turn it into a sleepy end device: `CONFIG_ENABLE_ICD_SERVER=y`,
  `CONFIG_PM_ENABLE=y`, `CONFIG_FREERTOS_USE_TICKLESS_IDLE=y`, ICD slow-poll
  interval ~1 s; measure with a USB power meter — the target is ≤200 µA idle.
* Then the real app in `firmware/tealight/`: WS2812 ring on D4 (GPIO22)
  via the BSP RMT driver, warm LED PWM on D2, ring rail on D3, Mode Select
  endpoint for effects, battery via Power Source cluster.
