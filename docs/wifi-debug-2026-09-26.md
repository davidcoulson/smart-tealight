# Wi-Fi bring-up problem — RESOLVED 2026-09-26

**Cause: a case typo in `secrets.yaml`** (`Iot` vs `IoT`). ESPHome's
`No networks found` means *no network matching the configured SSID*, not an
empty scan, which sent the debugging down the antenna-switch path.

**Lesson for the notes:** on "No networks found", check the SSID spelling
first; add `fast_connect: false` + DEBUG and look for the actual scan
results before suspecting hardware.

The XIAO C6 antenna-switch handling (`enable_on_boot: false`, GPIO3/GPIO14
set from `on_boot`, then `wifi.enable`) stays in the config: it's how the
board's ceramic/U.FL antenna gets selected and it's what Seeed's own
Arduino variant does.

---

Original investigation, kept for reference:


**Symptom:** XIAO ESP32-C6 running ESPHome scans and finds **zero** networks
(`[W][wifi:1506]: No networks found`), then loops through
RETRY_HIDDEN → "Probe Request Unsuccessful" → restart adapter.

**Ruled out so far (all give the identical result):**
- Two different XIAO C6 boards (MACs …1A:EB:00 and …13:79:FC)
- ESPHome 2026.9.0 (brew) and 2026.5.0 (venv) — same YAML
- Full `tealight-c6.yaml` with GPIO3/GPIO14 driven at on_boot priority 600
  (both antenna settings) — note ESPHome starts Wi-Fi ~7 ms into setup(),
  before on_boot 600, so those writes were probably too late
- `minimal-c6.yaml` without any antenna handling
- `minimal-c6.yaml` with `wifi.enable_on_boot: false` and the pins set from
  on_boot before `wifi.enable` (ceramic antenna selected)
- Arduino framework: not supported by ESPHome on the C6, could not test

**Not yet checked:**
- The `enable_on_boot: false` minimal with `antenna_select` turned **on**
  (U.FL) — bench board has an external antenna attached
- Whether the config dump actually shows `[C][gpio.output]` for GPIO3/14
  (i.e. the antenna block really compiled in)
- Multimeter on the GPIO3 / GPIO14 pads after boot (expect 0 V / 0 V or 3.3 V)
- Environment sanity: a phone next to the board sees 2.4 GHz networks?
- A non-ESPHome firmware (plain ESP-IDF wifi scan example) as a reference
- Seeed forum / ESPHome issues for "No networks found" on this board revision

**Board facts:** GPIO3 = WIFI_ENABLE (low powers the RF switch),
GPIO14 = WIFI_ANT_CONFIG (low = ceramic, high = U.FL). Neither is on the
header. Seeed's Arduino variant drives both low in initVariant().
