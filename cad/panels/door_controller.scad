use <../library.scad>;

difference()
{
  Panel([60, 25]);

  translate([0, 5])
    PanelTitle("Door");

  translate([-25, 7.5])
    NeoPixel();

  translate([-23, -2])
  {
    ToggleSwitch();

    translate([0, -5])
      PanelLabel("Limit");

    translate([13, 0])
    {
      ToggleSwitch();

      translate([0, -5])
        PanelLabel("Safety");
    }
  }

  translate([8, -2])
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
