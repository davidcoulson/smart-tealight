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
| **Sleepy (radio-off) polling** | **does not hold the link** — battery target still unmet |

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
