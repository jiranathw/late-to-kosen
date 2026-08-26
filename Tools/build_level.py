#!/usr/bin/env python3
"""
Generates prefab instances for Level1.unity (Late to KOSEN).

Writes real Unity PrefabInstance blocks (not plain GameObjects) so that when Bun
drops artwork onto the Trap/Ground/Checkpoint/Goal prefabs, every placed copy in
the level updates automatically.

Player physics (from PlayerController on Level1): moveSpeed 8, jumpForce 13,
gravityScale 3, fallMultiplier 1.5 -> apex 2.87u, max flat gap 6.42u. Layout
below keeps every gap <= 4u and every step-up <= 1.5u, i.e. inside 62% of
maximum reach even on the tightest rising jump.
"""

import os
import subprocess
import sys

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCENE = os.path.join(PROJECT, "Assets", "Scenes", "Level1.unity")

# guid -> (GameObject fileID, Transform fileID) taken from each .prefab / .prefab.meta
PREFABS = {
    "Ground":       ("6f851581bcfd4db3a0dfd1037b679b9a", 7900112233440000000, 7900112233440000001),
    "Trap":         ("55752b5a5fb9b304e9683d3333ccb256", 7474925521374357586, 1486569431692548854),
    "Checkpoint":   ("ac963368351871d439aade9dab6607ad",   50924625783960144, 5790916828929868942),
    "Goal":         ("5503e4868b9e32640925196fa63b0062", 7496332456263003369, 8596259638677655486),
    "TrapHidden":   ("1614458680214683aa039ba0c7e3881b", 6100000000000000101, 6100000000000000102),
    "PlatformFake": ("00451637c4b84e86886316ae1a3e24a0", 6100000000000000201, 6100000000000000202),
    "TrapSpike":    ("35c9464f042948d59b07c0d428239327", 6100000000000000301, 6100000000000000302),
    "Bicycle":      ("09c5f8c63ef746a6aad3543a707b5a76", 6100000000000000401, 6100000000000000402),
}

# ---------------------------------------------------------------- level design
# Physics after the tuning pass: moveSpeed 8, jumpForce 13, gravityScale 3,
# fallMultiplier 1.5.  Rise g = 3*9.81 = 29.43 -> apex 2.871u, t_rise 0.4418s.
# Fall g = 3*1.5*9.81 = 44.145 -> falling is faster than rising, so horizontal
# reach is SHORTER than the naive symmetric estimate.  Worked out below:
#   flat gap  6.42u | +1.0u step 5.86u | +1.5u step 5.53u
# Every gap here is <= 4u, i.e. under 62% of the tightest reach.  That headroom
# is deliberate: it has to be clearable by a first-time player on a keyboard.

# Ground: (name, x_center, y_center, width, height). Top surface = y + height/2.
GROUNDS = [
    ("Ground_Wall_Left",   -7.5,  2.0,   1.0, 6.0),  # spans -8 .. -7, FLUSH with the start platform.
                                                     # At -8.0 it left a 0.5u slot between wall and
                                                     # ground - exactly the player's collider width -
                                                     # and the player wedged in it instead of falling.
    ("Ground_01_Start",     5.0, -0.5,  24.0, 1.0),  # top 0.0   spans  -7 .. 17
    ("Ground_02",          24.0, -0.5,   8.0, 1.0),  # top 0.0   spans  20 .. 28   gap 3
    ("Ground_03",          35.0,  0.5,   8.0, 1.0),  # top 1.0   spans  31 .. 39   gap 3, up 1.0
    ("Ground_04",          46.0,  1.5,   8.0, 1.0),  # top 2.0   spans  42 .. 50   gap 3, up 1.0
    ("Ground_05_Gauntlet", 60.0,  1.5,  16.0, 1.0),  # top 2.0   spans  52 .. 68   gap 2
    ("Ground_06",          76.0,  1.5,  10.0, 1.0),  # top 2.0   spans  71 .. 81   gap 3
    ("Ground_07",          89.0,  1.5,  10.0, 1.0),  # top 2.0   spans  84 .. 94   gap 3
    ("Ground_08_Rest",    103.0,  1.5,  12.0, 1.0),  # top 2.0   spans  97 .. 109  gap 3
    ("Ground_09_Climb",   115.0,  3.0,   6.0, 1.0),  # top 3.5   spans 112 .. 118  gap 3, up 1.5
    ("Ground_10_Climb",   124.0,  4.5,   6.0, 1.0),  # top 5.0   spans 121 .. 127  gap 3, up 1.5
    ("Ground_11_Climb",   133.5,  6.0,   7.0, 1.0),  # top 6.5   spans 130 .. 137  gap 3, up 1.5
                                                     # widened by 1u so the last jump is 3u not 4u,
                                                     # because moveSpeed came down 8 -> 6
    ("Ground_12_School",  148.0,  6.0,  16.0, 1.0),  # top 6.5   spans 140 .. 156  gap 4
]

# Trap: (name, x, ground_top). Trap prefab is scale 0.5 -> 0.5u box, so it sits
# at top + 0.25 and the player must clear only 0.5u of the 2.87u jump arc.
TRAPS = [
    ("Trap_01",  10.0, 0.0),
    ("Trap_02",  24.0, 0.0),
    ("Trap_03",  57.0, 2.0),
    ("Trap_04",  61.0, 2.0),
    ("Trap_05",  66.0, 2.0),
    ("Trap_06",  76.0, 2.0),
    ("Trap_07",  88.0, 2.0),
    ("Trap_08",  92.0, 2.0),
    ("Trap_09", 101.0, 2.0),
    ("Trap_10", 106.0, 2.0),
    ("Trap_11", 124.0, 5.0),
    ("Trap_12", 146.0, 6.5),
]

# Checkpoint: (name, x, ground_top). Respawn point = this transform's position,
# so it sits at top + 0.6 -> player's feet land just above the surface.
CHECKPOINTS = [
    ("Checkpoint_1_AfterTutorial",  15.0, 0.0),
    ("Checkpoint_2_BeforeGauntlet", 54.0, 2.0),
    ("Checkpoint_3_Rest",           99.0, 2.0),
    ("Checkpoint_4_MidClimb",      115.0, 3.5),
    ("Checkpoint_5_TopOfClimb",    133.0, 6.5),
]

# ------------------------------------------------------------ TROLL TRAPS
# This is the part that makes it a *troll* platformer rather than a platformer.
# Three flavours, each trolling a different assumption the player is making.

# TYPE 1 - invisible. (name, x, ground_top)
# Placed where the ground looks safest: the landing spot after a visible trap,
# and the gap between two visible traps, i.e. exactly where you'd choose to
# stand. Reveals itself permanently the moment it kills you, so the retry is
# fair - you get trolled once per trap, not forever.
HIDDEN_TRAPS = [
    ("TrapHidden_01_LandingSpot",  26.0, 0.0),   # right where you land after Trap_02
    ("TrapHidden_02_OpenGround",   47.0, 2.0),   # a bare platform with nothing on it
    ("TrapHidden_03_SafeGap",      63.5, 2.0),   # the gap between Trap_04 and Trap_05
    ("TrapHidden_04_RestArea",    104.0, 2.0),   # the "rest" platform is not a rest
    ("TrapHidden_05_HomeStraight",144.0, 6.5),   # you can see the school gate from here
]

# TYPE 2 - looks exactly like Ground, same layer, same solid collider, then
# drops out of the world half a second after you land on it.
# (name, x_center, top, width)
# ALWAYS placed mid-gap over a pit the player can already clear unaided, so it
# is a temptation and never a requirement. It destroys itself after falling,
# which means the retry forces the honest jump.
FAKE_PLATFORMS = [
    ("PlatformFake_01",  29.5, 0.5, 2.0),   # sits in the 3u gap 28 -> 31
    ("PlatformFake_02",  82.5, 2.0, 2.0),   # sits in the 3u gap 81 -> 84
    ("PlatformFake_03", 138.5, 6.5, 2.0),   # centred in the last gap, 137 -> 140
]

# TYPE 3 - buried under the surface, shoots up when you get close.
# (name, x, ground_top). Sorting order is behind the ground sprite so it is
# genuinely invisible at rest. Gives a few frames of warning, unlike type 1.
SPIKE_TRAPS = [
    ("TrapSpike_01",  36.0, 1.0),   # first one, on an empty-looking platform
    ("TrapSpike_02",  79.0, 2.0),   # right on the landing spot after Trap_06
    ("TrapSpike_03", 150.0, 6.5),   # two metres from the school gate
]

# Bicycle power-up (Optional feature on the design form): +45% speed for 4.5s.
# Deliberately placed on OPEN ground, never right before a hazard - the boost is
# meant to buy back time on the safe stretches, not to be a trap in disguise.
# (name, x, ground_top)
BICYCLES = [
    ("Bicycle_01_Dorm",     13.0, 0.0),   # long safe start: teaches the pickup
    ("Bicycle_02_BeforeClimb", 108.0, 2.0),   # after the rest platform's traps, before the climb
]

# Goal: school gate, made 2x3 so it reads as a doorway and is impossible to miss.
GOAL = ("Goal_SchoolGate", 152.0, 8.0, 2.0, 3.0)

# ---------------------------------------------------------------- scene values
# Values that live in the scene rather than in a prefab or a script, keyed by
# the YAML anchor of the component that owns them. Applied idempotently: if the
# new value is already there the edit is skipped, so re-running is safe.
#
# WHY each one:
#   gravityScale 1 -> 3      jumpForce 7 -> 13    the tutorial defaults are floaty
#   moveSpeed 6 -> 8         you cannot finish the level in time at 6
#   m_Interpolate 0 -> 1     kills the camera judder at 3x gravity
#   killY -20 -> -12         respawn sooner after falling off; -20 is a long wait
#   sorting order 0 -> 10    player must never render behind Bun's ground art
#   startingTime 90 -> 70    at 90 the countdown never mattered
#   UiScaleMode 0 -> 1       constant-pixel UI explodes at other resolutions
SCENE_VALUES = [
    (1645035013, "m_UiScaleMode: 0",                  "m_UiScaleMode: 1"),
    (1645035013, "m_ReferenceResolution: {x: 800, y: 600}",
                 "m_ReferenceResolution: {x: 1920, y: 1080}"),
    (1645035013, "m_MatchWidthOrHeight: 0",           "m_MatchWidthOrHeight: 0.5"),
    ( 771653308, "m_GravityScale: 1",                 "m_GravityScale: 3"),
    ( 771653308, "m_Interpolate: 0",                  "m_Interpolate: 1"),
    ( 771653306, "moveSpeed: 8",                      "moveSpeed: 6"),
    ( 771653306, "jumpForce: 7",                      "jumpForce: 13"),
    ( 771653306, "killY: -20",                        "killY: -12"),
    ( 771653309, "m_SortingOrder: 0",                 "m_SortingOrder: 10"),
    ( 598578337, "startingTime: 90",                  "startingTime: 85"),
    (1640853499, "m_AnchoredPosition: {x: 0, y: -30}",
                 "m_AnchoredPosition: {x: -30, y: -30}"),
    (1730641361, "m_text: New Text",                  "m_text: 01:25"),
    (1640853501, "m_text: New Text",                  "m_text: 'Deaths: 0'"),
]


def apply_scene_values(scene):
    """Edit inside one anchor block at a time so we never hit the same string
    somewhere else in a 1000-line scene file."""
    applied = skipped = 0
    for anchor, old, new in SCENE_VALUES:
        marker = "&%d\n" % anchor
        i = scene.find(marker)
        if i < 0:
            sys.exit("anchor %d not found - is this the right Level1.unity?" % anchor)
        j = scene.find("\n--- ", i)
        if j < 0:
            j = len(scene)
        block = scene[i:j]
        if new in block:
            skipped += 1
            continue
        if old not in block:
            sys.exit("anchor %d: expected %r, found neither it nor %r" % (anchor, old, new))
        scene = scene[:i] + block.replace(old, new, 1) + scene[j:]
        applied += 1
    return scene, applied, skipped


FIRST_ID = 1900000000


def modification(target_id, guid, path, value):
    return (
        f"    - target: {{fileID: {target_id}, guid: {guid}, type: 3}}\n"
        f"      propertyPath: {path}\n"
        f"      value: {value}\n"
        f"      objectReference: {{fileID: 0}}\n"
    )


def fmt(v):
    """Unity writes 5 not 5.0, and -0.5 stays -0.5."""
    return str(int(v)) if float(v).is_integer() else repr(float(v))


def make_instance(kind, name, pos, scale, instance_id, transform_id):
    guid, go_id, tf_id = PREFABS[kind]

    mods = [modification(go_id, guid, "m_Name", name)]
    for axis, val in zip("xyz", pos):
        mods.append(modification(tf_id, guid, f"m_LocalPosition.{axis}", fmt(val)))
    for axis, val in zip("xyz", scale):
        mods.append(modification(tf_id, guid, f"m_LocalScale.{axis}", fmt(val)))
    for axis, val in (("w", 1), ("x", 0), ("y", 0), ("z", 0)):
        mods.append(modification(tf_id, guid, f"m_LocalRotation.{axis}", val))
    for axis in "xyz":
        mods.append(modification(tf_id, guid, f"m_LocalEulerAnglesHint.{axis}", 0))

    block = (
        f"--- !u!1001 &{instance_id}\n"
        "PrefabInstance:\n"
        "  m_ObjectHideFlags: 0\n"
        "  serializedVersion: 2\n"
        "  m_Modification:\n"
        "    serializedVersion: 3\n"
        "    m_TransformParent: {fileID: 0}\n"
        "    m_Modifications:\n"
        + "".join(mods) +
        "    m_RemovedComponents: []\n"
        "    m_RemovedGameObjects: []\n"
        "    m_AddedGameObjects: []\n"
        "    m_AddedComponents: []\n"
        f"  m_SourcePrefab: {{fileID: 100100000, guid: {guid}, type: 3}}\n"
        f"--- !u!4 &{transform_id} stripped\n"
        "Transform:\n"
        f"  m_CorrespondingSourceObject: {{fileID: {tf_id}, guid: {guid}, type: 3}}\n"
        f"  m_PrefabInstance: {{fileID: {instance_id}}}\n"
        "  m_PrefabAsset: {fileID: 0}\n"
    )
    return block, transform_id


def main():
    if "--reset" in sys.argv:
        # Regenerating requires a scene with no prefab instances in it. Pull the
        # committed one back rather than making the user do it by hand.
        out = subprocess.run(["git", "show", "HEAD:Assets/Scenes/Level1.unity"],
                             cwd=PROJECT,
                             capture_output=True)
        if out.returncode != 0:
            sys.exit("git show failed: " + out.stderr.decode(errors="replace"))
        with open(SCENE, "wb") as fh:
            fh.write(out.stdout)
        print("scene reset to HEAD")

    with open(SCENE, "r", encoding="utf-8") as fh:
        scene = fh.read()

    scene, applied, skipped = apply_scene_values(scene)
    print("scene values: %d applied, %d already correct" % (applied, skipped))

    # Note: must match the block header, not the "m_PrefabInstance:" field that
    # every single GameObject in the scene already carries.
    if "\nPrefabInstance:\n" in scene:
        sys.exit("Level1.unity already contains prefab instances - aborting so "
                 "nothing gets placed twice. Revert the scene first.")

    placements = []
    for name, x, y, w, h in GROUNDS:
        placements.append(("Ground", name, (x, y, 0), (w, h, 1)))
    for name, x, top in TRAPS:
        placements.append(("Trap", name, (x, top + 0.25, 0), (0.5, 0.5, 0.5)))
    for name, x, top in CHECKPOINTS:
        placements.append(("Checkpoint", name, (x, top + 0.6, 0), (1, 1, 1)))
    for name, x, top in HIDDEN_TRAPS:
        # thin floor patch: y sits just above the surface so the box overlaps
        # the player's feet no matter how they arrive
        placements.append(("TrapHidden", name, (x, top + 0.2, 0), (1.2, 0.4, 1)))
    for name, x, top, w in FAKE_PLATFORMS:
        placements.append(("PlatformFake", name, (x, top - 0.5, 0), (w, 1, 1)))
    for name, x, top in SPIKE_TRAPS:
        # rest position is fully inside the platform; SpikeTrap.riseHeight lifts
        # it 1.1u, which clears the surface by 0.1u
        placements.append(("TrapSpike", name, (x, top - 0.5, 0), (0.8, 1, 1)))
    for name, x, top in BICYCLES:
        # floats at chest height so it reads as a pickup, not as scenery
        placements.append(("Bicycle", name, (x, top + 0.95, 0), (0.9, 0.9, 1)))
    gname, gx, gy, gw, gh = GOAL
    placements.append(("Goal", gname, (gx, gy, 0), (gw, gh, 1)))

    blocks, new_roots = [], []
    next_id = FIRST_ID
    for kind, name, pos, scale in placements:
        block, tf = make_instance(kind, name, pos, scale, next_id, next_id + 1)
        blocks.append(block)
        new_roots.append(tf)
        next_id += 2

    # Splice the new objects in ahead of SceneRoots, then extend the roots list.
    marker = "--- !u!1660057539 &9223372036854775807\n"
    head, tail = scene.split(marker, 1)
    roots_addition = "".join(f"  - {{fileID: {tf}}}\n" for tf in new_roots)
    tail = tail.rstrip("\n") + "\n" + roots_addition

    with open(SCENE, "w", encoding="utf-8") as fh:
        fh.write(head + "".join(blocks) + marker + tail)

    print("placed %d objects" % len(placements))
    print("  %2d ground        %2d checkpoints   1 goal" % (len(GROUNDS), len(CHECKPOINTS)))
    print("  %2d visible traps %2d hidden traps  %d spike traps  %d fake platforms"
          % (len(TRAPS), len(HIDDEN_TRAPS), len(SPIKE_TRAPS), len(FAKE_PLATFORMS)))
    print("  %2d hazards score toward 'traps survived'"
          % (len(TRAPS) + len(HIDDEN_TRAPS) + len(SPIKE_TRAPS)))
    print("  %2d bicycle power-ups" % len(BICYCLES))
    print("level runs x=-7 -> x=156, finish line at x=%s" % gx)


if __name__ == "__main__":
    main()
