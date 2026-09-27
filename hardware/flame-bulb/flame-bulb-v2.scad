// Flame bulb v2 — PSU INSIDE the LED mast, strips run the full height.
// Three printed parts:
//   part = "cap"    E26 plug cup + Ø57 lip + spigot into the mast    PC-FR (mains)
//   part = "mast"   10-facet tube: PSU stands in the bore, XIAO above it,
//                   SK6812 strips on the facets from bottom to top      PC-FR (mains inside)
//   part = "shade"  Ø57 tube with a closed top, slides down over the
//                   mast onto the cap lip                               TRANSLUCENT PETG
//   part = "all"    preview (exploded = true)
//
// UNTESTED. HLK-10M05 = 47 x 28 x 22; 36 mm diagonal upright -> Ø37 bore.

part = "all"; exploded = false;

od = 57; diff_wall = 1.2; clr = 0.3;
psu_l = 47; psu_w = 28; psu_t = 22;
bore   = 37;                          // clears the PSU's 28x22 end with margin
n_facets = 10; strip_w = 12; facet_w = strip_w + 0.2;
core_r_min = facet_w / (2 * sin(180 / n_facets));      // radius needed for the strips
core_r     = max(core_r_min, bore/2 + 1.8);            // or bore + 1.8 mm wall
core_f2f   = 2 * core_r * cos(180 / n_facets);
n_px   = 15;                          // pixels per column at 6.94 mm -> 150 px total (T19 height)
mast_h = n_px * 6.94 + 2;             // 85.3
cap_lip = 3; spigot_h = 6;            // short lip: retention only, the mast's top fins centre the shade
// Shade runs right down over the cap lip, ending flush at the E26 plug (the
// lip is sized to the shade bore; glue or friction retains it).
shade_over_lip = true;
lip_d = shade_over_lip ? od - 2*diff_wall - 2*clr : od;
e26_body_d = 26.5; e26_cup_h = 12; e26_wall = 2.5;
shade_h = mast_h + 6 + (shade_over_lip ? cap_lip : 0); shade_cap = 1.6;
$fn = 160;

module cap() {
  difference() {
    union() {
      cylinder(d = lip_d, h = cap_lip);                                  // lip (inside the shade)
      translate([0, 0, cap_lip]) cylinder(d = bore - 2*clr, h = spigot_h); // into the mast bore
      translate([0, 0, -e26_cup_h]) cylinder(d = e26_body_d + 2*e26_wall, h = e26_cup_h + 0.01);
    }
    translate([0, 0, -e26_cup_h - 1]) cylinder(d = e26_body_d, h = e26_cup_h + 1 - 2); // plug cup, 2 mm floor
    translate([0, 0, -e26_cup_h - 1]) cylinder(d = 9, h = e26_cup_h + cap_lip + spigot_h + 2); // mains leads
  }
}

fin_h = 8; fin_t = 1.2;               // centring fins at the mast top, out to the shade bore
module mast() {
  difference() {
    union() {
      cylinder(r = core_r, h = mast_h, $fn = n_facets);
      // three thin fins on facet corners reach the shade bore and centre it
      for (a = [0, 120, 240]) rotate([0, 0, a + 18])
        translate([0, -fin_t/2, mast_h - fin_h]) cube([od/2 - diff_wall - clr, fin_t, fin_h]);
    }
    translate([0, 0, -1]) cylinder(d = bore, h = mast_h + 2);            // PSU + XIAO live here
    // strip power/data exit at the bottom of one facet
    translate([0, -3, spigot_h + 1]) cube([core_r + 1, 6, 8]);
    // notch at the top for the GND ring's lead back down the bore
    translate([-core_r - 1, -2, mast_h - 8]) cube([core_r + 1 - bore/2 + 1, 4, 9]);
    // vent slots near the top of two opposite facets (PSU makes ~3 W of heat)
    for (a = [90, 270]) rotate([0, 0, a]) translate([core_r - 4, -1.5, mast_h - 14]) cube([6, 3, 10]);
  }
}

module shade() {
  difference() {
    union() { cylinder(d = od, h = shade_h - 2); translate([0, 0, shade_h - 2]) cylinder(d1 = od, d2 = od - 4, h = 2); }
    translate([0, 0, -1]) cylinder(d = od - 2*diff_wall, h = shade_h - shade_cap + 1);
  }
}

g = exploded ? 22 : 0;
if (part == "cap") cap();
else if (part == "mast") mast();
else if (part == "shade") shade();
else {
  color("dimgray") cap();
  color("dimgray") translate([0, 0, cap_lip + g]) mast();
  color("steelblue", 0.7) translate([-psu_w/2, -psu_t/2, cap_lip + spigot_h + 1 + g]) cube([psu_w, psu_t, psu_l]);   // PSU
  color("royalblue", 0.8) translate([-10.5, -2, cap_lip + spigot_h + psu_l + 4 + g]) cube([21, 4, 17.8]);          // XIAO on edge
  color("lightyellow", 0.30) translate([0, 0, (shade_over_lip ? 0 : cap_lip) + 2*g]) shade();
}
