#!/usr/bin/env python3
"""STAGE 2 - INSIDE THE BUILDING.  Krin's level, ported.

WHOSE LEVEL THIS IS
    Krin built this and the team voted to keep it, so the job here was NOT to
    redesign it. Every platform below is at the coordinate he put it at, to two
    decimal places, and the goal sits at (67.55, 4.50) because that is where his
    goal sits. His sign copy is reproduced verbatim, typos and all.

    What changed is listed under FIXES, and it is all repair work: things that
    were broken in his committed scene rather than things that were merely
    cruel. He should read that list and put back anything he disagrees with.

WHY THIS STAGE SET THE PHYSICS
    Krin's player was moveSpeed 6, jumpForce 7, gravityScale 1 - a 1.43s
    airtime and an 8.56u flat reach, extremely floaty. Ours was 3.45u flat
    after the 28 Aug retune, and at 3.45u this stage is not hard, it is
    impossible: the opening gap alone is 5.00u.

    So the player was rebuilt around this level rather than the other way
    round. Sprint came out, its speed became the only speed, and the numbers
    landed at moveSpeed 7.5 / jumpForce 13.5 / gravityScale 2.6. Two edges here
    are what pinned them:

        Ground_Start -> GroundCheckpoint1   gap 5.00u   = 72% of a 6.93u reach
        GroundCheckpoint2 -> Ledge_3        rise 2.32u  = 65% of a 3.57u apex

    The first is why the reach cannot go below ~6.7u. The second is why the
    verifier's step-up ceiling is 0.70 of apex and not the 0.55 that reads
    comfortably. Both sit inside the margins on purpose and neither has any
    room left, which is the correct amount of room for the hardest jump in a
    game about being late.

THE SHAPE
    Not a corridor. A short approach, two ledges up, then a DROP into a 30-unit
    arena you cannot climb back out of, and the only way on is across it and up
    the far wall. That is why this file carries an explicit ROUTE: sorting
    platforms by left edge produces a nonsense chain in an arena, and the
    verifier needs to be told which jumps are actually jumps.

THE PIT
    Undershoot the Ledge_3 -> Ledge_4 gap and you land on Ledge_5, three ledges
    down, and this is NOT death - kill_y is -14 and Ledge_7 is at -9.46. It is
    worse. The pit cannot be climbed out of (Ledge_7 -> Ledge_6 is a 2.80u step
    against a 3.57u apex - 78%, over the ceiling, and that is deliberate), and
    the bottom holds two teleporters that look exactly alike.

    One is Krin's "secret ending" and it sends you to spawn AND drags your
    checkpoint back with you. The other is a staff lift back to the arena.
    There is no way to tell them apart. That is the level's best joke and it is
    entirely his.

FIXES APPLIED TO THE COMMITTED SCENE
    1. Three checkpoints were stacked on top of each other at x~0, so two of
       them did nothing. Spread to x = 2, 12, 26, 55.
    2. Trap1/2/3 floated at y = 16.24, 20.16 and 33.41 with no platform under
       or near them. Dropped, and the same count of traps re-placed on surfaces.
    3. THE GOAL HAD NO FLOOR. It hung in the air past the last ledge with
       nothing to land on. Ground_Exit is new, and it is the only platform in
       this file that is not Krin's.
    4. FakeGround had its renderer switched off, so it was an invisible
       collider rather than a fake platform - it helped the player. It is a
       visible PlatformFake now, over the opening gap, which is what it was
       clearly meant to be.
    5. FakeFallingRock had no script on it at all, so it never fell. Kept
       exactly that way (triggerDistance 0) and given a real twin at x=33, so
       the inert one is a joke instead of an oversight.
    6. KillBlock became a kill_floor under the opening gap.
"""

from level_kit import (boulder, checkpoint, fake, goal, hidden, kill_floor,
                       lizard, sign, spike, teleporter, trap)

# =============================================================================
# GEOMETRY - Krin's coordinates, unedited except where FIXES says otherwise.
# =============================================================================
GROUND = [
    #  name                  cx      cy      w      h        top     spans
    ("Ground_Start",       -13.0,   0.38,  36.0,  1.0),   #  0.88  -31.00 ..   5.00
    ("GroundCheckpoint1",   14.0,   0.38,   8.0,  1.0),   #  0.88   10.00 ..  18.00
    ("Ledge_1",             19.0,   2.79,   6.0,  0.4),   #  2.99   16.00 ..  22.00
    ("Ledge_2",             25.0,   4.79,   4.1,  0.4),   #  4.99   22.95 ..  27.05
    ("GroundCheckpoint2",   37.0,  -2.81,  30.0,  0.5),   # -2.56   22.00 ..  52.00
    ("Ledge_3",             47.75, -0.44,   8.44, 0.4),   # -0.24   43.53 ..  51.97
    ("Ledge_4",             55.94,  0.79,   6.0,  0.4),   #  0.99   52.94 ..  58.94
    # FIX 3 - new. Krin's goal had nothing underneath it.
    ("Ground_Exit",         66.0,   2.5,   12.0,  1.0),   #  3.00   60.00 ..  72.00
    # The pit. Off the route by definition: you only arrive here by missing,
    # and you cannot leave on foot.
    ("Ledge_5",             54.27, -4.95,   8.44, 0.4, "offroute"),  # -4.75  50.05 .. 58.49
    ("Ledge_6",             48.54, -6.86,  10.0,  0.4, "offroute"),  # -6.66  43.54 .. 53.54
    ("Ledge_7",             57.08, -9.66,   8.0,  0.4, "offroute"),  # -9.46  53.08 .. 61.08
]

# =============================================================================
# ROUTE - the jumps that are actually jumps.
#
# Sorting by left edge would pair Ledge_2 with GroundCheckpoint2 and Ledge_3
# with Ledge_5, because the arena starts to the LEFT of the ledge you enter it
# from and the pit sits underneath everything. In a level with a vertical axis
# the chain has to be written down.
#
# Listed with the cost of each edge, which is the whole reason the file exists:
# =============================================================================
ROUTE = [
    ("Ground_Start",      "GroundCheckpoint1"),   # gap 5.00u = 72% of reach  <- hardest jump in the game
    ("GroundCheckpoint1", "Ledge_1"),             # overlap, rise 2.11u = 59% of apex
    ("Ledge_1",           "Ledge_2"),             # gap 0.95u, rise 2.00u = 56%
    ("Ledge_2",           "GroundCheckpoint2"),   # a 7.55u drop into the arena, one way
    ("GroundCheckpoint2", "Ledge_3"),             # overlap, rise 2.32u = 65% of apex  <- sets STEP_APEX
    ("Ledge_3",           "Ledge_4"),             # gap 0.97u, rise 1.23u = 34%.  MISS THIS AND YOU ARE IN THE PIT
    ("Ledge_4",           "Ground_Exit"),         # gap 1.06u, rise 2.01u = 56%
]

OBJECTS = [
    # -- THE APPROACH --------------------------------------------------------
    # Krin's opening line, verbatim.
    sign("Sign_01_Hurry", -26.0, 0.88,
         "Hurry!  We're gonna be late for our Final Exam!!", show=7.0),
    spike("Spike_01_Bench", -22.0, 0.88),
    trap("Trap_01_Crate", -18.0, 0.88),
    hidden("Hidden_01_Tile", -11.0, 0.88),
    sign("Sign_02_Dangerous", -6.0, 0.88, "This is dangerous!"),
    sign("Sign_03_Checkpoint", 0.0, 0.88, "This is checkpoint!"),
    checkpoint("Checkpoint_1_Start", 2.0, 0.88),

    # -- THE OPENING GAP -----------------------------------------------------
    # 5.00u, and every bit of it. FIX 4: his FakeGround with the renderer back
    # on, so it reads as a stepping stone and is not one. It is bait over a gap
    # a standing jump already clears - the verifier refuses to let a fake
    # platform be load-bearing.
    fake("Fake_01_KrinGround", 7.5, 0.88, 2.0),
    # FIX 6: his KillBlock, as the floor of the gap. Trusting the fake platform
    # does not drop you into a long silent fall, it just ends the attempt.
    kill_floor("KillBlock_01_Gap", 7.5, -5.0, 5.0),

    # -- THE CLIMB -----------------------------------------------------------
    checkpoint("Checkpoint_2_Ledges", 12.0, 0.88),
    sign("Sign_04_ThisWay", 14.0, 0.88, "This way ><   -->"),
    trap("Trap_02_Ledge1", 16.5, 0.88),
    hidden("Hidden_02_Ledge1", 20.0, 2.99),
    checkpoint("Checkpoint_3_ArenaLip", 26.0, 4.99),

    # -- THE ARENA -----------------------------------------------------------
    # You drop in at x~25 and cannot get back up. The lizard from stage 1
    # followed you inside, which is both a callback and, for anyone who has
    # been to Lat Krabang, not especially unlikely. It wakes at x=27, chases at
    # 7.2 against a walk of 7.5, and gives up 30 units later - so it stays
    # behind you for the whole crossing without ever quite arriving.
    lizard("Lizard_01_Indoors", 27.0, -2.56, chase=7.2, give_up=30.0, trigger=9.0),
    sign("Sign_05_Run", 29.0, -2.56, "RUN.", latch=True),
    # FIX 5, part two: this one is real and it does fall.
    boulder("Rock_01_Real", 33.0, 4.0, 1.6, 1.6, trigger=4.0),
    trap("Trap_03_Arena", 31.0, -2.56),
    hidden("Hidden_03_Arena", 35.0, -2.56),
    trap("Trap_04_Arena", 39.0, -2.56),
    spike("Spike_02_Arena", 42.0, -2.56),
    # FIX 5, part one: Krin's FakeFallingRock, still scriptless in spirit -
    # triggerDistance 0 means it never falls. You do not find that out until
    # you have already sprinted underneath it.
    boulder("Rock_02_Inert", 47.0, 6.3, 1.8, 1.8, trigger=0.0),

    # -- THE FAR WALL --------------------------------------------------------
    sign("Sign_06_Up", 45.0, -0.24, "Almost!"),
    trap("Trap_05_Ledge3", 48.5, -0.24),
    checkpoint("Checkpoint_4_Ledge4", 55.0, 0.99),
    # Last trap in the game, two units before the last jump in the game.
    hidden("Hidden_04_LastStep", 57.5, 0.99),

    # -- THE PIT -------------------------------------------------------------
    # Two doors, no way to tell them apart, and the sign is Krin's word for
    # word. Picking wrong does not kill you - it takes your checkpoint.
    sign("Sign_07_Secret", 54.0, -9.46,
         "OMG!  You Found the Secret Ending!!!   1,000 baht", show=6.5),
    teleporter("Teleporter_01_SecretEnding", 55.5, -9.46, -28.66, 1.5,
               move_checkpoint=True),
    sign("Sign_08_StaffLift", 57.5, -9.46, "STAFF LIFT", show=6.5),
    teleporter("Teleporter_02_StaffLift", 58.5, -9.46, 25.0, -2.0,
               move_checkpoint=False),

    # -- THE DOOR ------------------------------------------------------------
    sign("Sign_09_Goal", 63.0, 3.0, "This is our goal!"),
    goal("Goal_ExamRoom", 67.55, 3.0),
]

# =============================================================================
# SCENE SETTINGS
#
# 103 units end to end, 13.7s of pure walking - a third of stage 1's length and
# far more than a third of its difficulty. 65s, because the deaths here are
# expensive: a bad landing at Ledge_3 costs the whole arena crossing again.
#
# kill_y is -14, four units under the pit floor, so the pit is somewhere you
# survive being stuck in rather than somewhere you die.
# =============================================================================
LEVEL = dict(
    index=2,
    scene="Level2",
    guid="c690b194a583229e4753adb268fe102b",   # committed
    time=65.0,
    kill_y=-14.0,
    spawn=(-28.66, 1.5),
    grounds=GROUND,
    objects=OBJECTS,
    route=ROUTE,
)
