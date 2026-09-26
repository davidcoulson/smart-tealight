# Sleepy-end-device bisect — 2026-09-26

Phase 1 (FTD over Thread) works; the sleepy build does not. Bisected on the
bench board (XIAO ESP32-C6, MAC …13:79:FC), ESPHome 2026.9.0, ESP-IDF 5.5.5,
flashed over USB. "Attach" = `[openthread] SRP client has started`.

## Finding 1: the external U.FL antenna path is dead

The pigtail is physically attached, but the *same* known-good FTD firmware
attaches on the onboard ceramic antenna and **never** attaches with
`external_antenna: true`. Suspect an unseated U.FL connector or a bad
pigtail/antenna. The finished candle uses the onboard antenna anyway.

An earlier round of this bisect was run on that dead path and its results were
wrong; everything below is on the **onboard antenna**.

## Finding 2: `device_type: MTD` is the only blocker

| device_type | poll_period | esp32_pm | Attach? |
|---|---|---|---|
| FTD | — | no | **yes** (~40 s; 15:02, 16:10, 16:18) |
| FTD | — | **yes** | **yes** (17:05) |
| MTD | at runtime | no | no (170 s) |
| MTD | 1000 ms | no | no (150 s) |
| MTD | at runtime | **yes** | no (170 s) |

So the [esp32_pm PR](https://github.com/esphome/esphome/pull/12325) is fine —
light sleep is available to us. **`device_type: MTD` never attaches**, with or
without polling or power management, with the OTBR (SLZB dongle) ~10 ft away.

This matters because MTD is not optional: an FTD keeps its radio in RX
permanently (tens of mA), so light sleep alone saves little. The radio has to
sleep, and only an MTD/SED can do that.

## Next step

`SRP client has started` is our only attach indicator, so we cannot yet tell
"never attached" from "attached as a child, but SRP failed". Log the
OpenThread role directly to separate them:

```yaml
interval:
  - interval: 10s
    then:
      - lambda: ESP_LOGI("ot", "role=%d", otThreadGetDeviceRole(esp_openthread_get_instance()));
```

Roles: 0 disabled, 1 detached, 2 child, 3 router, 4 leader. A steady `2` means
the MTD *is* attaching and the problem is SRP/mDNS; a steady `1` means it
genuinely cannot find a parent, which is an ESPHome/OpenThread issue worth
reporting upstream with these logs.

Meanwhile the bench board stays on `tealight-c6-thread.yaml` (FTD) so it is
usable in HA at ~20–40 mA. **The week-long battery target remains unproven.**

## On writing our own power-management component

Not needed. ESPHome's `esp32:` block accepts raw `sdkconfig_options` (user
values take precedence), and the runtime half is one `esp_pm_configure()` call
from an `on_boot` lambda — about fifteen lines, no external component, and
each knob can be toggled independently. Worth doing only if we later want to
drop the PR dependency.
