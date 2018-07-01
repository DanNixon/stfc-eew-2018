use <../library.scad>;

difference()
{
  Panel([40, 30]);

  translate([0, 8])
    PanelTitle("Search Point");

  translate([0, 2])
    NeoPixel();

  translate([0, -8])
    Pushbutton();
}
