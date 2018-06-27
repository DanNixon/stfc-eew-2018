# Project Outline

## Overview

Design and implement a prototype safety system for instrument blockhouses at
ISIS.

### Engineering Disciplines

- Software
- Electronics

### Prior reading

This is a list of general concepts that would be useful to have done a small
amount of background reading in before the week.

- Python
- Finite State Machines
- Arduino framework
- CAN bus

### Mentor

Dan Nixon

## Problem Description

To ensure the safety of scientists and facility users in the experimental halls
at ISIS, instruments are typically built within a structure known as a
blockhouse. These blockhouses ensure that area (and people) around the
instrument is safe from stray beam and environmental hazards as a result of the
experiment (for example, crush hazards from a sample stage, very low or high
temperatures from a cryostat or furnace).

In order for the blockhouse to serve its purpose (form a safety perspective) a
"search and lock" procedure is used, where once the instrument is setup and the
experiment is ready to start a scientist or user will walk a predetermined path
through the blockhouse checking for anything out of the ordinary (from basic
things such as people/items/tools left in the blockhouse to issues with the
instrument or supporting equipment to problems with the experimental setup).
Once the instrument has been searched the blockhouse door is closed and locked,
at this point it is considered safe to open the beam shutter and begin the
experiment. If the blockhouse door were to be opened then the search procedure
would have to be carried out again.

Outside the blockhouse there is also a key rack containing several (usually
5-10) keys that must all be present for the search procedure to be completed.
The keys are to be taken when entering the blockhouse, requiring them all to be
placed back in the rack once the door is closed ensures that no one is still in
the blockhouse prior to the experiment starting.

This search and lock procedure is orchestrated by an electronic system that
monitors the state of certain sensors and user inputs and determines the state
of the instrument using a finite state machine.

The project will be to model this safety system using low cost hardware.

## Requirements

- Finite state machine implemented in Python on a Linux single board computer
- CAN bus for communication between sensors and SBC
- Several sensor/input nodes based on microcontroller development boards
  - Door controller
    - Door motor
    - Open limit switch
    - Closed limit switch
    - Safety edge
    - Open button
    - Close button
  - 3x search points
    - "Next point" lamp
    - Searched button
  - Shutter interface
    - Enable output
    - State (open, closed, opening, closing, fault) input
  - Motion controller interface
    - Enable output
  - Key rack
    - "All keys present" input

## Task breakdown

Group 1:

1. CAN bus prototype
2. Controller software

Group 2:

1. Shutter interface
2. Key rack
3. Door controller
4. Motion controller interface

Both groups:

1. Search points
