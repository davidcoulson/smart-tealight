# SLZB-MR4U: Thread sleepy end devices cannot attach (indirect / CSL tx fails)

Report for SMLIGHT support — 2026-09-27.

## Summary

With the SLZB-MR4U's EFR32MG26 as the Thread radio, **rx-on Thread children work
but sleepy end devices (SED/SSED) never attach**: the border router queues the
Child ID Response for the sleeping child and every indirect (data-poll)
transmission fails, 4/4 attempts, on every attach. CSL (synchronized sleepy)
fails the same way. This happens both with the MR4U's built-in OTBR and with the
MR4U used as a network RCP by the Home Assistant OpenThread Border Router add-on
(stable and beta otbr-agent). Net effect: no battery-powered Matter-over-Thread
device can be commissioned through this radio.

## Hardware / firmware

| | |
|---|---|
| Device | SLZB-MR4U (hw 174), Ethernet mode, IPv6 "Off" in device settings, USB = debug port |
| Device firmware | v3.4.1.dev1 (dev channel) |
| Radio 1 | EFR32MG26, mode "Matter-over-Thread", firmware **20260416 (Dev)** — "Thread test firmware designed to fix problems with OTBR starting after device reboot" |
| RCP reported by otbr-agent | `SL-OPENTHREAD/3.0.1.0_GitHub-61e43cffb; EFR32; Apr 16 2026 06:14:46` |
| Radio 2 | CC2674P10, Zigbee coordinator (Zigbee2MQTT over tcp://10.2.4.5:7638) |
| Border router (config A) | MR4U built-in OTBR, network `SLZB-d6b5`, channel 15 |
| Border router (config B) | HA OpenThread Border Router add-on 3.2.0 on HA OS 18.3 (x86-64 VM), `network_device: 10.2.4.5:6638`, backbone `enp6s19` (same VLAN as the MR4U), tested with `beta: true` and `beta: false`; network `ha-thread-c912`, channel 15 |
| Test client | Seeed XIAO nRF52840, nRF Connect SDK v3.2.4 OpenThread CLI (`OPENTHREAD/ncs-thread-reference-20250402`), TX 0 dBm, same room; also an ESP32-C6 (ESPHome openthread) and the nRF52840 running Nordic's Matter `light_bulb` sample — all show the same behaviour |

Link quality between the MR4U and the test client is excellent in every test
(`ot parent`: Link Quality In 3 / Out 3; MR4U hears the client at about −68 dBm).

## Config A — MR4U built-in OTBR

Client joined as an rx-on MTD child (`ot mode rn`):

| test | result |
|---|---|
| attach | OK, parent = MR4U (RLOC 0xe000) |
| `ot ping <BR RLOC fd50:…:0:ff:fe00:e000>` ×10 | 9/10 answered, 23–51 ms, hlim 64 |
| `ot ping <BR mesh-local EID fd50:…:810:effc:8ad7:1b82>` (the SRP server address) ×10 | **2/10 answered**, hlim 255 |
| `ot srp client` registration of `_matter._tcp` | never reaches *Registered* (Adding → Refreshing forever) |

Consequence: a Matter device (Nordic light_bulb on nRF52840, sleepy or not)
gets through BLE commissioning, attaches to Thread, then logs
`SRP update error: timed out waiting on server response` ~14 times in a row (one
random success), so operational discovery fails and the commissioner's
fail-safe expires ("Commissioning failed: 32"). ESP32-C6/ESPHome behaves the
same as an MTD; as an FTD it happens to work.

## Config B — HA OTBR add-on, MR4U as network RCP

Same client, rx-on MTD child (`ot mode rn`):

| test | result |
|---|---|
| attach | OK, parent = add-on BR (RLOC 0x7000), LQI 3/3 |
| ping BR RLOC ×20 | 18/20, 24–40 ms |
| ping BR mesh-local EID ×20 | 13/20 |
| SRP registration | **Registered** in < 8 s (add-on log: `SrpServer: Send success response with granted lease: 7200`) |

Same client switched to a **sleepy end device** (`ot pollperiod 500`, `ot mode -`):

- `ot state` stays `detached` indefinitely (retested after 15 s, 20 s, and with
  `ot thread stop/start`). The client sends data polls (`TxDataPoll` counter
  increments) and the add-on receives its Child ID Requests.
- otbr-agent log, repeated on every attach attempt:
  ```
  Mle: Receive Child ID Request (fe80::4025:602e:becd:e0ac)
  Settings: Added ChildInfo {rloc:0x7001, extaddr:4225602ebecde0ac, timeout:240, mode:0x04, version:5}
  Mle: Send Child ID Response (fe80::4025:602e:becd:e0ac,0x7001)
  DataPollHandlr: Indirect tx to child 7001 failed, attempt 1/4
  DataPollHandlr: Indirect tx to child 7001 failed, attempt 2/4
  DataPollHandlr: Indirect tx to child 7001 failed, attempt 3/4
  DataPollHandlr: Indirect tx to child 7001 failed, attempt 4/4
  ```
- Identical with `beta: false` (stable otbr-agent) and `beta: true`.

Same client as a **synchronized sleepy end device** (`ot csl period 500000`):

- never attaches; otbr-agent log:
  ```
  CslTxScheduler: CSL tx to 7001 failed, attempt 1/4 … 4/4
  ```

Switching the client back to `ot mode rn` → attaches within seconds every time.

## Interpretation

Direct transmissions to an rx-on child work; the two transmission paths that
depend on the RCP (frame-pending / source-address-match after a data poll, and
CSL-timed transmission) fail 100 %. Both are timing-critical at the radio, so
either the EFR32 Thread firmware build or the ESP32 socket bridge between
otbr-agent and the RCP is breaking them. The same radio drives the MR4U's own
OTBR, which explains config A's SRP/ML-EID failures as well.

## How to reproduce

1. MR4U radio 1 in "Matter-over-Thread" mode; HA OTBR add-on with
   `network_device: <mr4u-ip>:6638`, form a network.
2. Any OpenThread CLI device (nRF52840 DK/dongle, or `ot-cli-ftd` on an
   EFR32 dev kit): `ot dataset set active <tlvs>`, `ot ifconfig up`,
   `ot thread start`, `ot mode rn` → attaches.
3. `ot pollperiod 500`, `ot mode -` → stays `detached`; watch the add-on log for
   `Indirect tx to child … failed`.
4. Alternatively commission any battery Matter-over-Thread device — it will
   fail after the Thread join.

## Questions for SMLIGHT

- Is indirect (data-poll) and CSL delivery to sleepy children known to be
  broken in the 20260416 EFR32MG26 Thread firmware, or in the network-RCP
  socket path on the MR4U?
- Is there a stable "Matter-over-Thread" firmware for the EFR32MG26 that we
  should test instead of the dev build?
