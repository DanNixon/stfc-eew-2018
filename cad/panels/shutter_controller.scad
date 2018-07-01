use <../library.scad>;

difference()
{
  Panel([50, 25]);

  translate([0, 6])
    PanelTitle("Shutter");

  translate([-18, -2])
    NeoPixel();

  translate([-2, -2])
  {
    Pushbutton();

    translate([0, -5])
      PanelLabel("Open");

    translate([15, 0])
    {
      Pushbutton();

      translate([0, -5])
        PanelLabel("Close");
    }
  }
}
