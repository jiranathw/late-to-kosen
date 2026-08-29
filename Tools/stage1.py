#!/usr/bin/env python3
"""STAGE 1 - DORM TO BUILDING.  07:42, and the alarm already lost.

WHAT CHANGED, AND WHY
    The first version of this stage was two hundred units of straight line. It
    descended once, from left to right, and it never came back. Sixteen
    platforms, one branch, and the player crossed every x-coordinate exactly
    once. Krin's stage is half as long and has three times the ideas, and the
    reason is not that he had better traps - it is that he STACKS. His arena
    puts six floors inside thirteen vertical units between x=43 and x=61, so
    the player crosses the same stretch of ground three times at three
    different heights and it reads as three different places.

    So this stage stopped being long and started being tall. The dorm stairwell
    is four floors inside forty units of width, traversed in alternating
    directions - right, left, right, left - which is a hundred and twelve units
    of walking in the footprint of a house. You can see the street the whole way
    down. You walk along it at the end.

    Each drop is five units. The jump apex is 3.57. That means every floor is a
    door that closes behind you, and it costs nothing to build.

THE BIKE, AND WHY THERE IS ONLY ONE RACK
    Three racks was the bug. The player parked at the first one, the ride lasted
    twenty-one of two hundred units, and the whole rental gimmick evaporated.

    There is now exactly one bicycle and exactly one real rack, and the fifty
    units between them are not optional, because of this:

                             walk        ride
        speed                7.50       11.25
        jump apex            3.57        2.17
        max step-up          2.50        1.52

    Riding is faster and jumps lower. So a 2.35u step is comfortable on foot and
    flatly impossible on a bike - and the kerb at x=92 is 2.35u. Note that 2.35
    is above the riding APEX of 2.17, not merely above the 70% safety margin:
    a rider does not fail this jump by a hair on a bad attempt, he cannot reach
    the height at all, however well he times it. That is the difference between
    a wall and a hard jump, and TJ asked for a wall - "there's no way I'm gonna
    jump over it and go on without parking". Meanwhile 2.35 is 66% of a walking
    apex, so on foot it is not even a jump you think about. That is the
    exit gate, and it needs no key, no prompt and no rule: you park, or you do
    not continue. Tools/build_levels.py rule 9 knows about it and calls it a
    dismount gate instead of a softlock, because the rack is eight units behind
    it on the same slab.

    The entry gate is the ajarn. A gap cannot gate the bike - riding reach is
    only 17% longer than walking reach and the safety margin is 25%, so no gap
    exists that a walker fails and a rider clears safely. Speed can. A chaser at
    9.0 closes on a walker at 1.5u/s and loses to a rider at 2.25u/s, so the
    corridor is survivable on a bike and lethal on foot, every time, by
    arithmetic rather than by luck.

KRIN'S FOUR MOVES, ANSWERED
    a hazard placed after its warning  -> Hidden_01 at x=20, the WET FLOOR sign
                                          at x=22. You read it getting up.
    a fake that is a perfect copy      -> Rack_1_Fake. Same prefab, same sign,
                                          one boolean, and it is the first rack
                                          you meet while something is chasing
                                          you.
    a reward that is a punishment      -> the klong pit. Signposted SHORTCUT,
                                          seven units down, no way out but a
                                          teleporter back to your bed at the top
                                          of the tower - with your checkpoint.
    a door that shuts behind you       -> all four stairwell drops.

THE SECRET ENDING
    You go back to bed. The sign at ground level calls the hole a shortcut; the
    signs at the bottom point out that roll call is not for another seventeen
    minutes and that your bed is still warm; and the way out is a teleporter
    that puts you back on the mattress you started on, checkpoint and all, under
    an alarm set for 07:42. It is the only ending in the game that loops.
"""

from level_kit import (bicycle, bike_rack, chaser, checkpoint, fake, fake_goal,
                       goal, hidden, kill_floor, lane, lizard, pot, sign, spike,
                       teleporter, trap)

# =============================================================================
# GEOMETRY
#
# Four floors, five units apart, each one traversed in the opposite direction to
# the one above it. Column 'top' is what the object constructors are given -
# nothing below ever names a centre.
#
#            x=-6      0        14       26      34
#   y=20      |        [Room_Floor]  [Corridor_4]        ->  exit right
#   y=15      |     [Hall_3]        [Landing_3]          <-  exit left
#   y=10   [Landing_2]              [Hall_2]             ->  exit right
#   y= 5      |     [Lobby]         [Landing_1]          <-  exit left
#   y= 0   [Soi_A] () [-------- Soi_A2 --------]         ->  and out
#   y=-7        [Basement_Bed]                               (the secret)
#
# The 2-3u gap in the middle of every floor is a jump. Missing it does NOT drop
# you to the floor below - each gap has a KillBlock under it - because the floor
# below is traversed backwards, so falling through would skip content as a
# reward for failing a jump.
# =============================================================================
GROUND = [
    # -- THE STAIRWELL -------------------------------------------------------
    #  name                cx      cy      w      h        top    spans
    ("Room_Floor",         6.0,   19.5,  12.0,  1.0),  # 20.0    0 .. 12
    ("Corridor_4",        20.0,   19.5,  12.0,  1.0),  # 20.0   14 .. 26   gap 2
    ("Landing_3",         23.5,   14.5,  15.0,  1.0),  # 15.0   16 .. 31   catches the drop from x=26
    ("Hall_3",             8.0,   14.5,  12.0,  1.0),  # 15.0    2 .. 14   gap 2, leftward
    ("Landing_2",          5.5,    9.5,  17.0,  1.0),  # 10.0   -3 .. 14   catches the drop from x=2
    ("Hall_2",            22.5,    9.5,  13.0,  1.0),  # 10.0   16 .. 29   gap 2
    ("Landing_1",         25.5,    4.5,  17.0,  1.0),  #  5.0   17 .. 34   catches the drop from x=29
    ("Lobby",              8.0,    4.5,  12.0,  1.0),  #  5.0    2 .. 14   gap 3, leftward

    # -- SHAFT WALLS ---------------------------------------------------------
    # Under 3u wide, so Tools/build_levels.py drops them from the route and they
    # are pure collision. Every one of them blocks a fall that would otherwise
    # skip a floor or two: without the first, walking left out of your own
    # bedroom lands you on the street with the entire tower unplayed.
    ("Wall_Room_Left",    -0.75,  24.0,   1.5,  8.0),  # x -1.5 ..  0,  y 20..28
    ("Wall_Shaft_Right",  31.75,  17.5,   1.5,  5.0),  # x 31   .. 32.5, y 15..20
    ("Wall_F2_Left",      -3.75,  12.5,   1.5,  5.0),  # x -4.5 .. -3,  y 10..15
    ("Wall_F1_Right",     34.75,   7.5,   1.5,  5.0),  # x 34   .. 35.5, y  5..10
    ("Wall_Ground_Left",  -6.75,   2.5,   1.5,  6.0),  # x -7.5 .. -6,  y -0.5..5.5

    # -- THE STREET ----------------------------------------------------------
    ("Ground_Soi_A",       0.0,   -0.5,  12.0,  1.0),  #  0.0   -6 .. 6
    ("Ground_Soi_A2",     22.0,   -0.5,  24.0,  1.0),  #  0.0   10 .. 34   gap 4 - the klong
    ("Ground_Soi_B",      45.0,   -0.5,  18.0,  1.0),  #  0.0   36 .. 54   gap 2
    ("Ground_Soi_C",      65.5,   -0.5,  17.0,  1.0),  #  0.0   57 .. 74   gap 3
    ("Ground_Soi_D",      84.5,   -0.5,  15.0,  1.0),  #  0.0   77 .. 92   gap 3
    # THE DISMOUNT GATE. 2.35u: 66% of a walking apex, 108% of a riding one -
    # over the riding apex itself, so it is not a hard jump on a bike, it is an
    # unreachable one. Everything from here to the goal sits 0.45u higher than
    # the street for exactly this reason.
    ("Kerb_Near",         96.25,   1.85,  8.5,  1.0),  #  2.35  92 .. 100.5
    ("Road_ChalongKrung",111.0,    1.85, 22.0,  1.0),  #  2.35 100 .. 122
    ("Kerb_Far",         125.75,   1.85,  8.5,  1.0),  #  2.35 121.5..130
    ("Forecourt",        136.0,    2.85, 12.0,  1.0),  #  3.35 130 .. 142

    # -- OFF THE ROUTE -------------------------------------------------------
    # The floor of the klong pit, seven units down. Flagged so the verifier does
    # not ask for a way to climb out of it; there is not one, on purpose.
    ("Basement_Bed",       7.0,   -7.5,  10.0,  1.0, "offroute"),  # -7.0   2 .. 12
]

# The order the player actually travels, which on this stage is not left to
# right - four of the sixteen jumps go backwards. build_levels.py derives the
# chain from x-order unless a stage says otherwise, and on a stairwell that
# pairs up platforms nobody ever travels between.
ROUTE = [
    ("Room_Floor",        "Corridor_4"),          # gap 2
    ("Corridor_4",        "Landing_3"),           # drop 5
    ("Landing_3",         "Hall_3"),              # gap 2, leftward
    ("Hall_3",            "Landing_2"),           # drop 5
    ("Landing_2",         "Hall_2"),              # gap 2
    ("Hall_2",            "Landing_1"),           # drop 5
    ("Landing_1",         "Lobby"),               # gap 3, leftward
    ("Lobby",             "Ground_Soi_A"),        # drop 5, out of the tower
    ("Ground_Soi_A",      "Ground_Soi_A2"),       # gap 4 - the klong
    ("Ground_Soi_A2",     "Ground_Soi_B"),        # gap 2
    ("Ground_Soi_B",      "Ground_Soi_C"),        # gap 3   |
    ("Ground_Soi_C",      "Ground_Soi_D"),        # gap 3   | the chase
    ("Ground_Soi_D",      "Kerb_Near"),           # step 2.35 - DISMOUNT GATE
    ("Kerb_Near",         "Road_ChalongKrung"),
    ("Road_ChalongKrung", "Kerb_Far"),
    ("Kerb_Far",          "Forecourt"),           # step 1.00
]

OBJECTS = [
    # ========================================================================
    # FLOOR 4 - YOUR ROOM.  The only honest twenty units in the game.
    # ========================================================================
    sign("Sign_01_Alarm", 1.0, 20.0,
         "07:42.  Roll call is 08:00.  You have slept through four alarms.",
         show=7.0),
    trap("Trap_01_Laundry", 4.0, 20.0),
    sign("Sign_02_Trap", 6.0, 20.0, "That is what a trap looks like."),
    spike("Spike_01_FloorFan", 7.5, 20.0),
    checkpoint("Checkpoint_1_Doorway", 10.5, 20.0),

    # The first fake platform, over a 2u gap a standing jump already clears -
    # bait, never load-bearing, and rule 5 enforces that. What is new is what is
    # underneath it: stepping on it now drops you onto Void_F4.
    fake("Fake_01_Doormat", 13.0, 20.0, 2.0),

    trap("Trap_02_MopBucket", 17.0, 20.0),
    # Krin's move: the hazard at x=20, the warning at x=22. You read it while
    # you are getting up.
    hidden("Hidden_01_WetFloor", 20.0, 20.0),
    sign("Sign_03_WetFloor", 22.0, 20.0, "CAUTION  -  WET FLOOR"),
    fake_goal("FakeGoal_01_Lift", 24.5, 20.0, "OUT OF ORDER", 3.0, "LIFT"),

    # ========================================================================
    # FLOOR 3 - you land at about x=29 and walk back the way you came, one
    # floor down, past the underside of everything you just crossed.
    # ========================================================================
    sign("Sign_04_Falling", 28.0, 15.0,
         "^  FALLING OBJECTS.  Hard hats are not provided."),
    # Pre-triggered, Krin-style: it lets go 4.5u before you arrive, so it lands
    # where you are ABOUT to be rather than where you are.
    pot("Pot_01_Warned", 24.0, 18.5, trigger=4.5),
    hidden("Hidden_02_Landing", 22.0, 15.0),
    trap("Trap_03_Extinguisher", 18.0, 15.0),

    # Same pot, sign removed. The stage teaches a rule and then takes it away,
    # which is the second time it does that and not the last.
    pot("Pot_02_Unwarned", 8.0, 18.5, trigger=4.5),
    trap("Trap_04_Recycling", 6.0, 15.0),
    hidden("Hidden_03_Landing", 10.0, 15.0),

    # ========================================================================
    # FLOOR 2
    # ========================================================================
    checkpoint("Checkpoint_2_Floor2", 3.0, 10.0),
    spike("Spike_02_Rise