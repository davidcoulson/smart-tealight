# Thread sleepy-end-device investigation — 2026-09-26

Bench board: XIAO ESP32-C6 (MAC …13:79:FC), ESPHome 2026.9.0, ESP-IDF 5.5.5,
flashed over USB. Border router: HA OpenThread Border Router on an SLZB
dongle, ~10 ft away, network `HomeThread` channel 15.

## Summary

| | |
|---|---|
| Thread + HA (FTD) | works |
| Thread + HA as an **MTD** | works, **with a workaround** (below) |
| `esp32_pm` light sleep | works, innocent |
| Sleepy **attach** | fixed 2026-09-27 via `CONFIG_LWIP_ND6=n` |
| Sleepy **data delivery** | **still broken** — API dies ~70 s in; battery target unmet |

## Finding 1: the external U.FL antenna path is dead

The pigtail is attached, but identical firmware attaches on the onboard
ceramic antenna and never attaches with `external_antenna: true`. Suspect an
unseated U.FL connector or a bad pigtail/antenna. Re-seat it before trusting
any `true` result — an earlier round of this bisect ran on that dead path and
produced wrong conclusions (it is why `esp32_pm` was briefly blamed).
The finished candle uses the onboard antenna anyway.

## Finding 2: ESPHome applies the Thread link mode too early

`OpenThreadComponent::apply_linkmode_()` is called from `openthread_esp.cpp`
*before* the dataset is activated and the stack is started. The stored
`NetworkInfo` is then restored over it (`Read NetworkInfo {... role:router,
mode:` in the boot log), so an MTD ends up advertising
`(rx_on=0, device_type=0, network_data=0)` — i.e. **sleepy** — even when no
`poll_period` is configured and ESPHome's own code intends
`mRxOnWhenIdle = (poll_period == 0) = true`.

Consequence: the device is sleepy from its very first Child ID Request and
the attach never completes:

```
Mle: Send Parent Request to routers      -> Receive Parent Response (OTBR, 0xdc00)
Mle: Send Child ID Request  x3           -> no response
Mac: Frame tx ... error:NoAck, type:Cmd(DataReq), dst:a684372864d85749
Mle: Attach attempt N unsuccessful, will try again in ...
```

It hears the border router fine (Parent Response arrives), so this is not RF
range. Re-asserting the link mode *after* the stack is running attaches as a
child in about one second:

```
[W][ot] forced rx_on_when_idle=1 -> OK
Mle: Receive Child ID Response (OTBR) -> Role detached -> child
[I][openthread] SRP client has started
```

**Workaround, now in `tealight-c6-thread-sed.yaml`:** a 10 s interval that,
whenever the role is `DETACHED`, re-asserts `mRxOnWhenIdle = true`. The
device runs as a Minimal End Device (MTD, radio on) and the same watchdog
recovers it if the link ever drops. Worth reporting upstream.

## Finding 3: sleepy polling does not hold the link — confirmed on two routers

**Update 2026-09-27.** Retested against a brand-new Thread network
(`SLZB-d6b5`, channel 15, PAN 0xd6b5) on a different border router
(extended address a21ff13d0ba4994b at 10.2.4.5), with the old OTBR gone. The
device attaches and runs fine as a MED, and HA drives it normally. Flipping
the sleepy switch, with the serial monitor attached throughout:

```
02:42:49.520  [W][api.connection] Home Assistant ...: Network down; disconnect
02:42:50.906  [W][ot] detached: re-asserted rx_on_when_idle=1 to re-attach
02:42:58.762  [W][component] api cleared Warning flag        (back as MED)
```

It detaches ~1.4 s after the radio stops listening. Identical behaviour to
the original OTBR, on a fresh network with an empty child table, a different
router and different credentials — so **the fault is on the ESP32-C6 /
ESPHome side, not the SLZB RCP and not accumulated network state.**
Interference is also ruled out: 20 MHz Wi-Fi, Thread on channel 15 (the gap
between Wi-Fi 1 and 6), Zigbee 50 MHz away on 25.

### Original single-router finding

With the attach fixed, switching to a 1 s poll (`openthread.set_poll_period`,
which re-applies link mode with `rx_on=false`) drops the device: it detaches
and the polls go unanswered with the same `Cmd(DataReq) ... error:NoAck`.
Since a sleepy child retrieves everything from its parent by polling, and the
parent never ACKs the poll, the link cannot survive.

The MAC-layer ACK window is ~192 µs after transmit, so a plausible cause is
the C6 missing ACKs on radio wake rather than anything in ESPHome — ordinary
frames are received fine, only the tight post-TX ACK is missed. Not proven.

Sleepy mode is exposed as an **experimental switch** (`Sleepy mode
(experimental)`, default off) so it can be retried without reflashing; the
watchdog pulls the device back to MED when it drops.

## Finding 4 (2026-09-27): ND6 was breaking the sleepy attach

Espressif's own `ot_sleepy_device` reference sets **`CONFIG_LWIP_ND6=n`**.
Our builds had it **on**: `esp32_pm` only disables ND6 when `poll_period` is
set at *compile* time, and we set it at runtime, so that guard never fired.
With ND6 on, IPv6 Neighbour Discovery keeps probing; once the radio stops
listening the probes fail, the neighbour goes unreachable and the interface
drops — the `Network down; disconnect` we had been chasing.

Adding it explicitly fixes the detach:

```yaml
esp32:
  framework:
    sdkconfig_options:
      CONFIG_LWIP_ND6: "n"
```

Verified: went sleepy and stayed attached for minutes with no detach and no
watchdog activity, and lights were still controllable from HA immediately
after the transition. Ruled out along the way, all measured not assumed:

* `esp32_pm` / radio sleep — sleepy fails identically with `CONFIG_PM_ENABLE`
  unset entirely.
* RF/range — parent link is **avg RSSI -53..-56 dBm, LQI 3/3 both
  directions** (3 is the maximum).
* `CONFIG_FREERTOS_HZ` — already 1000, matching the reference.
* Child timeout / supervision ([PR #16387](https://github.com/esphome/esphome/pull/16387))
  — that concerns poll periods over 180 s; ours is 1 s.

## Finding 5: data delivery to a sleepy child still fails

With the attach fixed, the device **stays attached** but HA's API connection
dies ~70 s after it goes sleepy, and the device logs *nothing* — it never
sees a disconnect. HA's pings simply stop arriving. So the parent is not
delivering queued (indirect) traffic to the sleepy child, even though the
MLE link is healthy.

This is the same delivery failure as before, one layer up: previously it
killed the attach, now it kills the data path.

Auto-sleepy is therefore **disabled** in `tealight-c6-thread-sed.yaml`; the
`Sleepy mode` switch remains for manual testing, and the detach watchdog
still recovers the device.

Also worth knowing: an OTA/version probe that lands while the device is
sleepy hangs the OTA component for ~170 s and blocks the main loop. Turn
Sleepy mode off before any OTA.

## Where this leaves battery life

An MED keeps its radio in RX permanently — tens of mA — so `esp32_pm` light
sleep saves little on its own. **The week-long target is unmet and blocked on
Finding 3.**

Next things to try:
1. A different Thread router (an Apple/Google border router, or a second C6 as
   an FTD parent) to establish whether the failure is the SLZB RCP or the C6.
2. A longer poll period (5–10 s) — fewer polls, but the same ACK problem.
3. `CONFIG_IEEE802154_*` timing/sleep options on the C6.
4. Failing all that: the nRF54L15 (backordered), whose Thread stack is mature,
   or accept mains/USB power for the tea light and keep battery for later.

## Current state of the bench board

`tealight-c6-thread-sed.yaml` — MTD + attach watchdog + `esp32_pm` light
sleep, online in HA over Thread, lights verified from HA. Sleepy switch off.

## On writing our own power-management component

Not needed. `esp32:` accepts raw `sdkconfig_options` (user values take
precedence) and the runtime half is one `esp_pm_configure()` call from an
`on_boot` lambda — ~15 lines, no external component. `esp32_pm` from
[PR #12325](https://github.com/esphome/esphome/pull/12325) already works, so
this is only worth doing to drop the PR dependency.

## 2026-09-27 — Finding 6: it was the border router, not the C6

Retested with the nRF52840 (Nordic Matter light_bulb as sleepy ICD, then the
same with ICD off, then a bare OpenThread CLI — `firmware/nrf52840-otcli`).

- Matter build, sleepy **and** non-sleepy: attaches as CHILD, every SRP update
  "timed out waiting on server response" (1 success in ~14), commissioner
  never finds the node, fail-safe expires. Identical to the C6 MTD symptoms.
- OT CLI as an rx-on MTD child of the **SLZB-MR4U** (fw v3.4.1.dev1, the only
  router/leader, link quality 3/3):
  - ping BR RLOC `…:0:ff:fe00:e000` → 9/10, ~30 ms, hlim 64
  - ping BR ML-EID `…:810:effc:8ad7:1b82` (SRP server) → **2/10**, hlim 255
  - `srp client` registration never reaches Registered.

The two hop limits mean the RLOC is answered inside the OT core and the
ML-EID by the MR4U's host IP stack; the OT→host forwarding path on the MR4U
drops ~80 %. SRP (and therefore Matter commissioning) depends on that path.
Findings 3–5 blaming the C6 sleepy implementation are withdrawn: the C6 FTD
only "worked" because it happened to survive the loss.

Next: run the MR4U as an RCP with the HA OTBR add-on as the border router and
repeat the CLI test.

## 2026-09-27 — Finding 7: the MR4U's Thread radio can't deliver to sleepy children

Moved the border router to the HA **OTBR add-on** (3.2.0) with the SLZB-MR4U's
EFR32MG26 as a network RCP (`10.2.4.5:6638`, SMLIGHT "Matter-over-Thread" dev
firmware 20260416). New network `ha-thread-c912`. Same nRF52840 OT CLI child,
link quality 3/3 both ways:

| child mode | attach | ping BR RLOC | ping BR ML-EID | SRP |
|---|---|---|---|---|
| MED (`rn`, rx-on)      | yes | 18/20 | 13/20 | **Registered** in <8 s |
| SED (`-`, poll 500 ms) | never — stays detached | — | — | — |
| SSED (CSL 500 ms)      | never | — | — | — |

The add-on log shows why: for the sleepy child the BR queues the Child ID
Response and then logs `DataPollHandlr: Indirect tx to child 7001 failed,
attempt 1/4 … 4/4` on every poll; with CSL it is `CslTxScheduler: CSL tx to
7001 failed, attempt 1/4 … 4/4`. Direct transmissions (rx-on child) work.
Indirect and CSL delivery both rely on RCP radio-firmware features (source
address match / frame-pending, CSL tx scheduling); direct tx does not. So the
sleepy failure is in the MR4U's EFR32 RCP firmware, and it also explains
Findings 3–6 (the MR4U's own OTBR used the same radio).

Consequence: **no sleepy Thread device — ESPHome C6, Nordic Matter ICD, or a
bare OT CLI — can work behind this radio.** Fix is a different Thread RCP
(SMLIGHT stable firmware if it behaves, a Connect ZBT-1/SkyConnect, or an
nRF52840 running the NCS `coprocessor` RCP sample on the HA host's USB).

## 2026-09-27 — Finding 8: EFR32 fw 2.7.2 lets sleepy children attach, ~40 % delivery

Radio 1 re-flashed to SMLIGHT 20251218 (SL-OPENTHREAD 2.7.2.0): the OT CLI SED
attaches and registers SRP, but indirect delivery is 17–21 of 50 pings. Raising
the child's `OPENTHREAD_CONFIG_MAC_DATA_POLL_TIMEOUT` to 500 ms
(`firmware/nrf52840-otcli/overlay-polltimeout.conf`, OT built from source)
changed nothing → not host↔RCP latency. Full write-up for SMLIGHT:
`docs/smlight-mr4u-sleepy-thread-report.md`.

Decision: the MR4U is not a usable Thread border-router radio for sleepy
devices until SMLIGHT fixes it. Use a directly attached RCP for the tea light.
