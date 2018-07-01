use <../library.scad>;

difference()
{
  Panel([60, 18]);

  translate([0, 4])
    PanelTitle("Key Rack");

  translate([-25, -4])
    NeoPixel();

  for(x=[-15:10:30])
    translate([x, -4])
      ToggleSwitch();
}
