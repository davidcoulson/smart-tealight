# OTBR on a Linux box (USB RCP)

1. Flash `firmware/nrf52840-rcp` onto a XIAO nRF52840 (double-tap reset →
   `adafruit-nrfutil dfu serial --package rcp.zip -p /dev/cu.usbmodem101 -b 115200 --singlebank`)
   and plug it into the Linux box. It enumerates as "Thread RCP nRF52840",
   `/dev/ttyACM0` (check `ls -l /dev/serial/by-id/`).
2. `BACKBONE=<lan-if> docker compose up -d` in this directory.
3. Form a network once (the container keeps it in the `otbr-data` volume):
   `docker exec otbr ot-ctl dataset init new && docker exec otbr ot-ctl dataset commit active && docker exec otbr ot-ctl ifconfig up && docker exec otbr ot-ctl thread start`
   then `docker exec otbr ot-ctl state` → `leader`.
4. Home Assistant → Settings → Devices & services → Thread: the new border
   router appears (mDNS `_meshcop._udp`) → "Make preferred network".
5. Sanity check with the OT CLI board (`firmware/nrf52840-otcli`): join with
   `docker exec otbr ot-ctl dataset active -x`, `ot mode -`, 50 pings to the
   BR's ML-EID (`docker exec otbr ot-ctl ipaddr mleid`) — expect ~100 %.

Web UI: http://<box>:80, REST: http://<box>:8081/node.
