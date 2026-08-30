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
        jump apex            3.11        1.89
        max step-up          2.18        1.33

    Riding is faster and jumps lower. So a 2.05u step is comfortable on foot and
    flatly impossible on a bike - and the kerb at x=92 is 2.05u. Note that 2.05
    is above the riding APEX of 1.89, not merely above the 70% safety margin:
    a rider does not fail this jump by a hair on a bad attempt, he cannot reach
    the height at all, however well he times it. That is the difference between
    a wall and a hard jump, and TJ asked for a wall - "there's no way I'm gonna
    jump over it and go on without parking". Meanwhile 2.05 is 66% of a walking
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
    #
    # THE THREE SHAFT WALLS ARE DELIBERATELY OVER-TALL. Each one used to stop
    # exactly level with the floor it stands beside - Wall_Shaft_Right topped
    # out at 20.0, which is Corridor_4's surface - and with a 5u flat run-up
    # inside a 6.47u reach the wall was not a wall, it was a step. You jumped
    # onto the top of it and walked over the shaft, skipping three floors of
    # the stage. They now stand 4u proud of the surface beside them - 0.89u
    # clear of the 3.11u apex, and the apex is measured at the feet - so there
    # is no timing, no run-up and no bike setup that gets a player on top of
    # one. Tools/build_levels.py cannot catch this class of bug: it checks the
    # jumps you are MEANT to make, not the ones the scenery accidentally offers.
    ("Wall_Room_Left",    -0.75,  24.0,   1.5,  8.0),  # x -1.5 ..  0,  y 20..28
    ("Wall_Shaft_Right",  31.75,  20.5,   1.5, 11.0),  # x 31   .. 32.5, y 15..26
    ("Wall_F2_Left",      -3.75,  14.5,   1.5,  9.0),  # x -4.5 .. -3,  y 10..19
    ("Wall_F1_Right",     34.75,   9.5,   1.5,  9.0),  # x 34   .. 35.5, y  5..14
    ("Wall_Ground_Left",  -6.75,   2.5,   1.5,  6.0),  # x -7.5 .. -6,  y -0.5..5.5

    # -- THE STREET ----------------------------------------------------------
    ("Ground_Soi_A",       0.0,   -0.5,  12.0,  1.0),  #  0.0   -6 .. 6
    ("Ground_Soi_A2",     22.0,   -0.5,  24.0,  1.0),  #  0.0   10 .. 34   gap 4 - the klong
    ("Ground_Soi_B",      45.0,   -0.5,  18.0,  1.0),  #  0.0   36 .. 54   gap 2
    ("Ground_Soi_C",      65.5,   -0.5,  17.0,  1.0),  #  0.0   57 .. 74   gap 3
    ("Ground_Soi_D",      84.5,   -0.5,  15.0,  1.0),  #  0.0   77 .. 92   gap 3
    # THE DISMOUNT GATE. 2.05u: 66% of a walking apex, 108% of a riding one -
    # over the riding apex itself, so it is not a hard jump on a bike, it is an
    # unreachable one. Everything from here to the goal sits 2.05u above the
    # street for exactly this reason.
    #
    # Was 2.35 when the apex was 3.57. Lowering the jump to a 3.11 apex moved
    # BOTH ends of the window it has to sit in: the walking step ceiling fell to
    # 2.18 (so 2.35 was no longer a legal step at all) and the riding apex fell
    # to 1.89. 2.05 is the height that is still comfortably walkable and still
    # flatly unreachable on a bike. The margin over the riding apex is only
    # 0.16u now, so if the jump is ever retuned again this number is the first
    # thing to re-derive - the gate is the whole reason the bike section works.
    ("Kerb_Near",         96.25,   1.55,  8.5,  1.0),  #  2.05  92 .. 100.5
    ("Road_ChalongKrung",111.0,    1.55, 22.0,  1.0),  #  2.05 100 .. 122
    ("Kerb_Far",         125.75,   1.55,  8.5,  1.0),  #  2.05 121.5..130
    ("Forecourt",        136.0,    2.55, 12.0,  1.0),  #  3.05 130 .. 142

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
    ("Ground_Soi_D",      "Kerb_Near"),           # step 2.05 - DISMOUNT GATE
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
    # POT TIMING. A pot rests at y 18.5 with a 0.35 half-height, so its underside
    # starts 3.15u above the floor 3 surface and falls at gravityScale 3.4. It is
    # level with a standing player's head 0.359s in and shatters on the pavement
    # 0.435s in, and at 7.5u/s the player covers 2.69u and 3.26u in those times.
    # A pot therefore only actually lands ON you if it is let go somewhere in
    #     triggerDistance = 2.69 .. 3.26
    # Anything larger shatters ahead of you and is a warning; anything smaller
    # drops behind you and is nothing at all.
    #
    # Pre-triggered, Krin-style: this one lets go 4.5u out - past the top of that
    # window on purpose - so it lands where you are ABOUT to be. It is the demo.
    pot("Pot_01_Warned", 24.0, 18.5, trigger=4.5),
    hidden("Hidden_02_Landing", 22.0, 15.0),
    trap("Trap_03_Extinguisher", 18.0, 15.0),

    # Same pot, sign removed. The stage teaches a rule and then takes it away,
    # which is the second time it does that and not the last - so this one is
    # inside the window at 3.0 and is the one that actually kills you.
    pot("Pot_02_Unwarned", 8.0, 18.5, trigger=3.0),
    trap("Trap_04_Recycling", 6.0, 15.0),
    hidden("Hidden_03_Landing", 10.0, 15.0),

    # ========================================================================
    # FLOOR 2
    # ========================================================================
    checkpoint("Checkpoint_2_Floor2", 3.0, 10.0),
    spike("Spike_02_Riser", 10.0, 10.0),
    trap("Trap_05_Bin", 19.0, 10.0),
    hidden("Hidden_04_Landing", 24.0, 10.0),

    # ========================================================================
    # FLOOR 1
    # ========================================================================
    trap("Trap_06_Post", 27.0, 5.0),
    hidden("Hidden_05_Landing", 21.0, 5.0),
    # Read on the way out, one floor and about ninety seconds too late.
    sign("Sign_07_Lift", 11.0, 5.0,
         "The lift was working.  It is on the other side of the building.",
         show=6.0),

    # ========================================================================
    # THE FOUR SHAFT KILLBLOCKS
    #
    # One in each mid-floor gap. A 2-3u gap is a jump you can make standing
    # still, so falling in is a mistake rather than a difficulty spike - but it
    # has to cost something, because the floor underneath every one of these
    # gaps runs the other way, and dropping through would carry the player PAST
    # content as a reward for missing a jump.
    #
    # SECOND ARGUMENT IS THE TOP OF THE FLOOR THE GAP IS IN, not a centre.
    # These used to hang two units down in the middle of the shaft, and that is
    # a metre and a half inside the arc of anyone jumping on the floor BELOW -
    # so a normal hop under one of them was a head-first death. Void_F1 hung
    # over the open street: every jump between x=14 and x=17 on the way out of
    # the tower killed you. They now plug the gap flush with the surface and
    # only bite from above; see kill_floor in Tools/level_kit.py.
    # ========================================================================
    kill_floor("Void_F4", 13.0, 20.0, 2.6),
    kill_floor("Void_F3", 15.0, 15.0, 2.6),
    kill_floor("Void_F2", 15.0, 10.0, 2.6),
    kill_floor("Void_F1", 15.5,  5.0, 3.0),

    # ========================================================================
    # STREET LEVEL - and the same forty units for the fifth time, from below.
    # ========================================================================
    sign("Sign_08_Klong", 3.0, 0.0,
         "v   SHORTCUT  -  the klong path.  Saves 40 seconds."),

    # -- THE SECRET ENDING ---------------------------------------------------
    # Seven units down, and the apex is 3.57, so this is one-way. Reaching it is
    # free; leaving it costs the entire tower and your checkpoint with it.
    # One sign, latched, doing the work three used to. Three signs down here
    # meant the punchline arrived in instalments and the player was reading
    # rather than moving; latching it means it is still on screen while he
    # walks into the teleporter, which is when the joke actually lands.
    sign("Sign_Bed_1", 6.0, -7.0,
         "SECRET ENDING  -  ROOM 402.  Your bed is still warm.",
         latch=True, show=7.0),
    # The loop. Destination is the spawn - the mattress you woke up on - and it
    # drags the checkpoint back with it, so the morning genuinely restarts.
    teleporter("Teleporter_01_Bed", 11.0, -7.0, 2.0, 21.0, move_checkpoint=True),

    # -- BACK ON THE STREET --------------------------------------------------
    # No sign on this one. A two-metre lizard sprinting at you is not a thing
    # that needs captioning, and the word RUN two units behind it was the game
    # explaining its own joke.
    lizard("Lizard_01_Klong", 16.0, 0.0, chase=7.0, give_up=20.0, trigger=8.0),
    trap("Trap_07_Cable", 26.0, 0.0),

    # ========================================================================
    # THE CHASE.  x=43 to x=92, and the only section of the stage that is not
    # optional in any sense: on foot the ajarn catches you at about x=65 every
    # single time, and the arithmetic is in the module docstring.
    # ========================================================================
    sign("Sign_10_Ajarn", 37.0, 0.0,
         "AJARN is doing his rounds.  He is faster than you are.", show=7.0),
    checkpoint("Checkpoint_3_Soi", 38.5, 0.0),
    bicycle("Bicycle_01_Anywheel", 41.0, 0.0,
            offer="ANYWHEEL  -  scan to unlock.  Ends at a rack.  Only at a rack."),

    # Rest position, not spawn position: he sits here asleep until the player is
    # past him, then takes 0.6s to stand up. 9.0 against a 7.5 walk and an 11.25
    # ride. Gives up after 42u, which puts him five units short of the kerb -
    # close enough to still be on screen when you park.
    chaser("Ajarn_01_Rounds", 43.0, 0.0, chase=9.0, give_up=42.0,
           trigger=10.0, wind_up=0.6),

    # The pixel-perfect fake, and the first rack you meet - four units into a
    # chase, which is exactly when you want it to be real.
    bike_rack("Rack_1_Fake", 47.0, 0.0, real=False,
              refused="CANNOT END RIDE HERE  -  outside docking zone",
              cost=0.0),

    trap("Trap_08_Roadworks", 62.0, 0.0),

    # The only sign in the chase, and it latches: at 11.25 u/s a 5.5u fade is
    # about one second of reading, which is not enough to react to the one
    # instruction in the section you cannot skip.
    sign("Sign_12_Dock", 80.0, 0.0, "ANYWHEEL DOCK  -  50m",
         latch=True, show=8.0),
    bike_rack("Rack_2_Dock", 88.0, 0.0, real=True),

    # ========================================================================
    # CHALONG KRUNG ROAD.  On foot from here - see the kerb.
    #
    # Two crossings with a 3.5u median between them, never one 22u gamble. Each
    # lane is 9u long and spaces its vehicles further apart than that (6.5 x 2.0
    # = 13.0u, 4.5 x 2.8 = 12.6u), so a lane holds at most one vehicle and the
    # crossing is always solvable rather than usually solvable.
    # ========================================================================
    checkpoint("Checkpoint_4_Kerb", 96.0, 2.05),
    sign("Sign_13_LookRight", 99.0, 2.05,
         "CHALONG KRUNG ROAD.  Look right.", show=7.0),
    lane("Lane_A_Motorbikes", 105.0, 2.50, 9.0, -6.5, 2.0, 0.4,
         (1.8, 0.9), (0.95, 0.75, 0.2)),
    lane("Lane_B_Pickups", 117.5, 2.60, 9.0, -4.5, 2.8, 1.7,
         (2.6, 1.1), (0.85, 0.35, 0.3)),

    checkpoint("Checkpoint_5_FarKerb", 125.0, 2.05),
    trap("Trap_09_Bollard", 128.0, 2.05),

    # ========================================================================
    # THE FORECOURT.  The last lie, and the cheapest: three seconds for walking
    # into the wrong lobby, which is what the previous hundred and forty units
    # have trained you to do.
    # ========================================================================
    sign("Sign_14_Building", 132.0, 3.05, "BUILDING 12  -  main entrance  -->"),
    fake_goal("FakeGoal_02_WrongBuilding", 134.5, 3.05,
              "BUILDING 9  -  WRONG BUILDING", 3.0, "ENTRANCE"),
    hidden("Hidden_06_Doorstep", 137.0, 3.05),
    goal("Goal_Building12", 140.0, 3.05),
]

# =============================================================================
# SCENE SETTINGS
#
# The verifier measures the run as goal_x minus the leftmost edge, which on a
# stage that doubles back four times is a large underestimate: 146u of width is
# about 248u of walking, or 33s, and rule 7 only sees 19s. 95s is set against
# the real number and leaves room for roughly two deaths.
#
# kill_y is -12, one unit under the pit floor, so the secret is survivable and
# missing the klong jump into open air is not.
#
# The spawn is the mattress. It is also where Teleporter_01_Bed sends you.
# =============================================================================
LEVEL = dict(
    index=1,
    scene="Level1",
    guid="015d47d998009ba4ab9f815ba8ce3520",   # committed - must not change
    time=95.0,
    kill_y=-12.0,
    spawn=(2.0, 21.0),
    grounds=GROUND,
    objects=OBJECTS,
    route=ROUTE,
)
