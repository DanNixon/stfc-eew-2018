module Panel(dimensions, radius=3)
{
  minkowski()
  {
    square(dimensions - [radius, radius], center=true);
    circle(r=radius, $fn=32);
  }
}

module PanelTitle(t)
{
  text(t, halign="center", valign="baseline", size=5);
}

module PanelLabel(t)
{
  text(t, halign="center", valign="top", size=3);
}

module NeoPixel()
{
  square([5.1, 5.1], center=true);
}

module Pushbutton()
{
  circle(d=7.1, $fn=16);
}

module ToggleSwitch()
{
  circle(d=6.1, $fn=16);
}
