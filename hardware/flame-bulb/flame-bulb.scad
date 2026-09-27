// Flame bulb — E26, SK6812 RGBWW columns around a hex mast.
// Companion to the smart tealight; see docs/ideas/flame-bulb.md.
//
//   part = "base"     body + PSU chamber        PC-FR (mains inside)
//   part = "cap"      bottom cap + E26 boss     PC-FR
//   part = "core"     faceted mast for the strips   opaque PETG
//   part = "shade"    tube + closed top, ONE PIECE   TRANSLUCENT PETG
//   part = "diffuser" outer tube alone          } the two-piece alternative
//   part = "top"      end cap alone             } (not used by the 3mf)
//   part = "all"      preview (exploded = true)
//
//   openscad --export-format binstl -D 'part="base"' -o base.stl flame-bulb.scad
//
// UNTESTED — dimensions from the Linkind T19 envelope, the HLK-10M05
// datasheet and the SK6812 144/m strip. Nothing has been fitted in hand.
//
// Note the HLK-10M05 (47 x 28 x 22) stands UPRIGHT: laid flat its 54.7 mm
// diagonal will not fit inside a 57 mm body. That makes the base taller than
// a stock T19, so the bulb ends up ~150 mm rather than 131 mm. An HLK-5M05
// (38 x 23 x 18, 1 A) would lie flat and save ~25 mm if that matters.

part = "all";
exploded = false;

od        = 57;   // body diameter
wall      = 1.6;
diff_wall = 1.2;
clr       = 0.3;  // print fit clearance

psu_l = 47; psu_w = 28; psu_t = 22;   // HLK-10M05, standing on its 28x22 end
base_h    = 56;                        // chamber: psu_l upright + clearance
cap_h     = 5;
e26_d     = 24; e26_h = 12;            // boss the bought E26 shell slips over

n_facets  = 10;   // columns of strip around the mast. 10 leaves ~4.5 mm
                  // between LED and diffuser; 8 leaves ~7 mm if hotspots
                  // show; 12 does not fit. One number to change.
strip_w   = 12;   // BTF SK6812 144/m strip is 12 mm wide
facet_w   = strip_w + 0.2;                        // strips are cut segments,
                                                  // they only need to seat
core_r    = facet_w / (2 * sin(180 / n_facets));  // polygon circumradius
core_f2f  = 2 * core_r * cos(180 / n_facets);     // 37.5 mm for 10 x 12.2
core_h    = 70;   // 10 px per column at 6.94 mm pitch -> 100 px total
core_bore = core_f2f - 8;                         // 4 mm walls; XIAO inside
foot_h    = 6;

diff_h    = 74;
top_h     = 5;
shade_h   = 78;   // one-piece shade: tube + closed top
shade_cap = 1.6;  // thickness of the closed end
plug_h    = 4;

chamber_d = od - 2*wall;               // 53.8
spigot_d  = od - 2*diff_wall - 2*clr;  // diffuser slides over this

$fn = 160;

// ---------------------------------------------------------------- base --
// Open at the BOTTOM so the PSU drops in; the cap closes it afterwards.
module base() {
  difference() {
    union() {
      cylinder(d = od, h = base_h - plug_h);
      translate([0, 0, base_h - plug_h]) cylinder(d = spigot_d, h = plug_h);
    }
    // PSU chamber, open to the bottom face
    translate([0, 0, -1]) cylinder(d = chamber_d, h = base_h - wall + 1);
    // hex socket for the core foot, in the top face
    translate([0, 0, base_h - foot_h])
      cylinder(r = core_r + clr, h = foot_h + 1, $fn = n_facets);
    // low-voltage wires up into the core
    translate([0, 0, base_h - wall - 2]) cylinder(d = 8, h = 10);
    // lip the bottom cap presses into
    translate([0, 0, -0.01]) cylinder(d = chamber_d + 2*clr, h = cap_h);
  }
}

// ----------------------------------------------------------------- cap --
module cap() {
  union() {
    cylinder(d = od, h = wall);                       // flange, sits flush
    translate([0, 0, wall])
      cylinder(d = chamber_d - clr, h = cap_h - wall); // press-in plug
    translate([0, 0, -e26_h]) difference() {           // E26 boss
      cylinder(d = e26_d, h = e26_h + 0.01);
      translate([0, 0, -1]) cylinder(d = 9, h = e26_h + wall + 2);
    }
  }
}

// ---------------------------------------------------------------- core --
module core() {
  difference() {
    cylinder(r = core_r, h = core_h, $fn = n_facets);
    translate([0, 0, -1]) cylinder(d = core_bore, h = core_h + 2);
    translate([-2*core_r, -3, foot_h]) cube([4*core_r, 6, 9]); // wire slot
  }
}

// ------------------------------------------------------------ diffuser --
module diffuser() {
  difference() {
    cylinder(d = od, h = diff_h);
    translate([0, 0, -1]) cylinder(d = od - 2*diff_wall, h = diff_h + 2);
  }
}

// --------------------------------------------------------------- shade --
// Diffuser and top as one closed-ended tube. Print CLOSED END DOWN: the flat
// top sits on the bed and the walls rise from it, so there is no bridge over
// the bore and no supports. Slides down over the core onto the base spigot.
module shade() {
  difference() {
    union() {
      cylinder(d = od, h = shade_h - 2);
      translate([0, 0, shade_h - 2]) cylinder(d1 = od, d2 = od - 4, h = 2);
    }
    // bore, stopping short of the top to leave the closed end
    translate([0, 0, -1])
      cylinder(d = od - 2*diff_wall, h = shade_h - shade_cap + 1);
  }
}

// ----------------------------------------------------------------- top --
module top() {
  union() {
    cylinder(d = od, h = top_h - 2);
    translate([0, 0, top_h - 2]) cylinder(d1 = od, d2 = od - 4, h = 2);
    translate([0, 0, -plug_h]) difference() {
      cylinder(d = spigot_d, h = plug_h + 0.01);
      translate([0, 0, -1]) cylinder(d = spigot_d - 2*wall, h = plug_h + 2);
    }
  }
}

// ------------------------------------------------------------ assembly --
g = exploded ? 20 : 0;
if (part == "shade") shade();
else if (part == "base") base();
else if (part == "cap") cap();
else if (part == "core") core();
else if (part == "diffuser") diffuser();
else if (part == "top") top();
else {
  color("dimgray")  base();
  color("dimgray")  translate([0, 0, -g]) cap();
  color("orange")   translate([0, 0, base_h - foot_h + g]) core();
  color("lightyellow", 0.30)
                    translate([0, 0, base_h - plug_h + 2*g]) shade();
}
