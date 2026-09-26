# Shopping list (prototype, Amazon US)

Amazon listings found 2026-09-26; check the variant dropdown on each. Quantities
are per *pack* — one pack of each covers many candles.

## Already ordered / owned

| Part | Listing | Notes |
|---|---|---|
| XIAO ESP32-C6 | owned | prototype + Track B (ESP-Matter) |
| XIAO nRF52840 (Meshtastic kit) | ordered | fallback Track B; ignore the LoRa carrier |
| XIAO nRF54L15 | backordered at Seeed | stretch option |
| 8× WS2812B 32 mm ring, 2-pack | [DIYmall B08PCPJSRF](https://www.amazon.com/dp/B08PCPJSRF) | prototype ring |
| SK6812 RGB+**warm white** 5050 chips, 100 pcs | [BTF-LIGHTING B07C1XGD1X](https://www.amazon.com/dp/B07C1XGD1X) | for the v2 PCB (needs hot air / reflow) |
| SK6812 RGBWW 144/m strip, 1 m, IP30, 5 V | BTF-LIGHTING (Amazon, warm-white variant) | tea-light strip option and the flame bulb's columns |
| Hi-Link HLK-10M05 (5 V 2 A AC/DC) | Amazon | flame bulb power |
| Perfboard, 32-pc assortment | [Rindion B0DBZ1BXFZ](https://www.amazon.com/dp/B0DBZ1BXFZ) | cut the 4×6 cm board to a 34 mm disc |

## To order

| Part | Listing | Notes |
|---|---|---|
| LiPo 3.7 V 400 mAh **802030**, with PCM | [AKZYTUE B07TVDPRZK](https://www.amazon.com/dp/B07TVDPRZK) or [Qimoo B0CNLQDLJ2](https://www.amazon.com/dp/B0CNLQDLJ2) | Connector type doesn't matter — it gets cut off and soldered to I7/I8. If the 20×30 footprint won't fit the bore, [802525 (25×25×8.6)](https://www.amazon.com/dp/B0FRFY1F76) is the alternative |
| 2N7000 N-FET, TO-92 | [BOJACK 100 pcs B0831RFJ1B](https://www.amazon.com/dp/B0831RFJ1B) (or [20 pcs B0BJQ92VNT](https://www.amazon.com/dp/B0BJQ92VNT)) | Q2, Q3 |
| AO3401A P-FET, SOT-23 | [Todiys 100 pcs B08RHFLH1K](https://www.amazon.com/dp/B08RHFLH1K) | Q1 |
| SOT-23 → SIP-3 adapter | [Chironal 50 pcs B07MQBF2DD](https://www.amazon.com/dp/B07MQBF2DD) | 3-in-a-row pinout, exactly what the perfboard layout assumes (pads B9/C9/D9) |
| 0805 resistor kit | [Chanzon 1200 pcs / 60 values B08RYMY6XK](https://www.amazon.com/dp/B08RYMY6XK) | covers 82, 100, 330, 1k, 100k, 220k (200k also fine for the divider — just use two of the same) |
| 100 µF 6.3 V tantalum, B (3528) | [Fielect 50 pcs B08BYM7GR8](https://www.amazon.com/dp/B08BYM7GR8) | C1; 3.5 mm body bridges two adjacent pads. Mind polarity (stripe = +) |
| 3 mm warm-white LED, flat-top | [EDGELEC 100 pcs B077XBVZ5Y](https://www.amazon.com/dp/B077XBVZ5Y) | ~3000 K, wide beam, 29 mm leads. Ignore the bundled 6–12 V resistors; use 82 Ω from the kit. Long lead = anode → D4 |
| 6×6×5 mm tact switch | [Taiss 100 pcs B0796QHL5Z](https://www.amazon.com/dp/B0796QHL5Z) | SW1, off-board at the base |
| 30 AWG silicone wire, 6 colours | [TUOFENG B07G2SWB19](https://www.amazon.com/dp/B07G2SWB19) | all the underside jumpers |
| Kapton tape 10 mm | [GoGoRc B0CJQ544H8](https://www.amazon.com/dp/B0CJQ544H8) | under the XIAO |
| PETG, translucent/clear | [Bambu Lab PETG Translucent Clear refill B0FRQ9VX2K](https://www.amazon.com/dp/B0FRQ9VX2K) (Bambu printers) or [MatterHackers Clear PETG B010P3FEY8](https://www.amazon.com/dp/B010P3FEY8) | diffuser dome |
| PETG, black or white | any brand you already use | cup |

## Optional

| Part | Listing | Notes |
|---|---|---|
| Magnetic USB-C tips | [Magtame 24-pin, 4-pack B0DNZCGBBX](https://www.amazon.com/dp/B0DNZCGBBX) + one matching magnetic cable | one tip lives in each candle's recessed USB-C port; charging without fishing for the socket |
| SMD tweezers, flux pen, fine solder (0.5 mm) | — | if not already on the bench |
