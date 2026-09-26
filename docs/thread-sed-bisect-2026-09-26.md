# Sleepy-end-device bisect — 2026-09-26

Phase 1 (FTD over Thread) works. Phase 2 (sleepy + light sleep) does not.
Bisected on the bench board (XIAO ESP32-C6, MAC …13:79:FC), ESPHome 2026.9.0,
ESP-IDF 5.5.5, all flashed over USB with the **onboard ceramic antenna**
unless noted. "Attach" = `[openthread] SRP client has started` appears.

| Config | device_type | poll_period | esp32_pm | Result |
|---|---|---|---|---|
| `tealight-c6-thread.yaml` | FTD | — | no | **attaches** in ~40 s; HA connects (16:10, 16:18, and 15:02 via Device Builder) |
| `bisect-b-ftd-pm.yaml` | FTD | — | **yes** | no attach in 150 s |
| `bisect-c-mtd-runtime.yaml` | **MTD** | at runtime | no | no attach in 170 s |
| `bisect-a-sed-nopm.yaml` | **MTD** | 1000 ms | no | no attach in 150 s |
| `tealight-c6-thread-sed.yaml` | **MTD** | at runtime | **yes** | no attach in 170 s (tried both antenna settings) |

**Two independent blockers**, either one enough to prevent the attach:

1. **`device_type: MTD`** — never attaches, with or without `poll_period`,
   with or without power management. Only the FTD builds ever attach.
2. **`esp32_pm`** (PR [#12325](https://github.com/esphome/esphome/pull/12325))
   — an otherwise-identical FTD build stops attaching once the component is
   added. Note light sleep should not even engage while USB is connected
   (`CONFIG_USJ_NO_AUTO_LS_ON_CONNECTION`), so the cause is more likely
   something else it sets: `CONFIG_IEEE802154_SLEEP_ENABLE=y`, or CPU
   frequency scaling down to `min_frequency: 40MHz` breaking 802.15.4 timing.

**Alternative explanation not yet ruled out: marginal RF.** One FTD run logged
`SRP client reported an error: ResponseTimeout` right after attaching, which
suggests the link to the OTBR is not strong. An FTD attaches more
aggressively than an MTD, which must find and hold a parent — so a weak link
could produce exactly this FTD-works/MTD-fails split without either component
being at fault.

## Next experiments (cheapest first)

1. **Move the board next to the HA server / OTBR and retry MTD.** Settles the
   RF hypothesis before any more firmware work. Also try the U.FL antenna,
   confirming first that the pigtail is actually on *this* board.
2. **PM with frequency scaling disabled**: `min_frequency: 160MHz` (or drop
   `enable_light_sleep`) on an FTD, to find which sdkconfig option breaks it.
3. If MTD still fails next to the border router, it is an ESPHome/OpenThread
   issue worth reporting upstream with these logs.

Until one of these lands, the bench board stays on `tealight-c6-thread.yaml`
(FTD, radio always on) so it remains usable in HA — at ~20–40 mA, i.e. no
battery saving yet. **The week-long battery target is unproven.**
