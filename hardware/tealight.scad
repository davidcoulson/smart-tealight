// Smart tea light body — parametric, three printed parts.
//
//   part = "cup"      lower body: battery, perfboard, XIAO, button, USB-C slot   (opaque PETG)
//   part = "carrier"  spacer that sits on the perfboard and carries the LED ring (opaque PETG)
//   part = "cap"      diffuser dome, plugs into the cup                          (translucent PETG)
//   part = "all"      assembled preview (exploded = true to spread the parts)
//
// Render each part:  openscad -D 'part="cup"' -o cup.stl tealight.scad
//
// Stack (z, mm): floor 0–1 | cell 1–9.5 | perfboard 9.5–11.1 | XIAO 11.1–15.5
//                | carrier 11.1–15.6 | LED ring 15.6–19.1 | cap cavity to 22 | top 23

part = "all";
exploded = false;

// ---- dimensions -------------------------------------------------------
od        = 38;    // tea-light standard
wall      = 1.0;
id        = od - 2*wall;          // 36
floor_t   = 1.0;
cell_h    = 8.5;                  // 802030 cell + swell room
perf_t    = 1.6;
perf_d    = 34;
ledge_z   = floor_t + cell_h;     // 9.5: perfboard rests here
cup_h     = 15.5;                 // cup rim
cap_h     = 7.5;                  // cap above the rim → total 23
skirt_h   = 2.0;                  // cap plug depth into the cup
clr       = 0.2;                  // fit clearance

ring_od   = 32;   ring_id = 18;   ring_t = 1.6;  led_h = 1.9;
carrier_od = 34;  carrier_id = 29;  carrier_h = 4.5;
xiao_cut_x = 11;                  // carrier is cut away for x > this (XIAO + USB-C)

usb_w = 10;  usb_z0 = 12.0;       // USB-C slot in the wall, open to the rim
btn_d = 4;   btn_x = -14;         // floor hole for the tact switch plunger

$fn = 120;

// ---- cup -------------------------------------------------------------
module cup() {
  difference() {
    cylinder(d = od, h = cup_h);
    // cavity
    translate([0, 0, floor_t]) cylinder(d = id, h = cup_h);
    // USB-C notch, +x side, open at the rim
    translate([id/2 - 1, -usb_w/2, usb_z0]) cube([wall + 2, usb_w, cup_h]);
    // button plunger hole
    translate([btn_x, 0, -1]) cylinder(d = btn_d, h = floor_t + 2);
  }
  // three perfboard ledge tabs (none on the USB side)
  for (a = [90, 210, 330])
    rotate([0, 0, a])
      translate([id/2 - 1.5, -1.5, ledge_z - 1]) cube([1.5 + 0.01, 3, 1]);
}

// ---- carrier (spacer between perfboard and LED ring) --------------------
module carrier() {
  difference() {
    cylinder(d = carrier_od, h = carrier_h);
    translate([0, 0, -1]) cylinder(d = carrier_id, h = carrier_h + 2);
    translate([xiao_cut_x, -od/2, -1]) cube([od, od, carrier_h + 2]);
  }
}

// ---- cap (diffuser) ------------------------------------------------------
module cap() {
  // outer shell, rounded top edge
  difference() {
    hull() {
      cylinder(d = od, h = cap_h - 2);
      translate([0, 0, cap_h - 2]) rotate_extrude() translate([od/2 - 2, 0]) circle(r = 2);
    }
    translate([0, 0, -1]) cylinder(d = id, h = cap_h - wall + 1);
  }
  // plug skirt, notched for the USB-C
  translate([0, 0, -skirt_h]) difference() {
    cylinder(d = id - 2*clr, h = skirt_h + 0.01);
    translate([0, 0, -1]) cylinder(d = id - 2*clr - 2*wall, h = skirt_h + 2);
    translate([id/2 - 3, -(usb_w + 2)/2, -1]) cube([5, usb_w + 2, skirt_h + 2]);
  }
}

// ---- reference geometry for the preview (not printed) -------------------
module electronics() {
  color("orange", 0.5) translate([-10, -15, floor_t]) cube([20, 30, 8]);                 // cell
  color("green", 0.6)  translate([0, 0, ledge_z]) cylinder(d = perf_d, h = perf_t);      // perfboard
  color("steelblue", 0.7) translate([-5.8, -8.75, ledge_z + perf_t]) cube([21, 17.5, 4]); // XIAO
  color("white", 0.8) translate([0, 0, ledge_z + perf_t + carrier_h]) difference() {     // LED ring
    cylinder(d = ring_od, h = ring_t); translate([0,0,-1]) cylinder(d = ring_id, h = ring_t + 2); }
}

// ---- assembly ------------------------------------------------------------
gap = exploded ? 12 : 0;
if (part == "cup") cup();
else if (part == "carrier") carrier();
else if (part == "cap") cap();
else {
  color("dimgray") cup();
  electronics();
  color("dimgray") translate([0, 0, ledge_z + perf_t + gap]) carrier();
  color("lightyellow", 0.5) translate([0, 0, cup_h + 2*gap]) cap();
}
