#!/usr/bin/env python3
"""Builds Level1.unity and Level2.unity for Late to KOSEN.

    python3 Tools/build_levels.py            # write both scenes
    python3 Tools/build_levels.py --check    # verify only, write nothing

WHAT THIS FILE IS
    The machinery, and only the machinery: it turns a level table into scene
    YAML, then checks that the table describes a level a person can finish.

    The physics and the vocabulary live in Tools/level_kit.py. The two levels
    live in Tools/stage1.py and Tools/stage2.py. This used to be one 900-line
    file and every level edit produced a diff against the emitter as well,
    which made review harder than it needed to be for a four-day project.

WHY IT REBUILDS FROM A SKELETON
    Tools/scene_skeleton.unity is every non-PrefabInstance document from the
    original Level1.unity: camera, player, spawn point, GameManager, the HUD
    canvas, the EventSystem. Six scene roots, no geometry. A level is that
    skeleton plus its own prefab instances plus a handful of field overrides.

    So running this twice produces byte-identical output, and the level stays
    reviewable as a Python diff instead of as 150KB of YAML. Its predecessor,
    Tools/build_level.py, patched the committed scene in place and stopped
    being re-runnable the moment that scene had instances in it.

TWO STAGES, NOT THREE
    Stage 3 was cut on the evening of 28 Aug. The team took Krin's level as stage 2 and the
    dorm-to-building run became stage 1, which left stage 3 with no story left
    to tell and three days to tell it in. Level3.unity is deleted by main().

WHAT THE VERIFIER GUARANTEES
    Nine rules, all re-derived from the tables on every run, all fatal except
    checkpoint spacing. Between them they say: every jump on the route is
    inside the arc with a quarter of it spare, no gap can swallow the player
    collider, nothing stands over a hole, no respawn lands on a hazard, no fake
    platform is load-bearing, no flood drowns ground you still need, the level
    fits its timer, and - rule 9 - a player who took the bike can still finish.

    Rule 9 exists because a ride can only be ended at a rack. A rider is faster
    and jumps lower, so the whole stretch from the first bicycle to the goal
    has to satisfy BOTH sets of physics or a bike is a softlock rather than a
    decision.
"""

import hashlib
import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from level_kit import (AIRBORNE_KINDS, GAP_SAFETY, P, STEP_APEX,
                       STEP_APEX_WARN, WALK_SPEED, ground, horizontal_reach,
                       jump_apex)
import stage1
import stage2

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SKELETON = os.path.join(PROJECT, "Tools", "scene_skeleton.unity")
SCENES_DIR = os.path.join(PROJECT, "Assets", "Scenes")
BUILD_SETTINGS = os.path.join(PROJECT, "ProjectSettings", "EditorBuildSettings.asset")

# Stages this file OWNS: it generates them, verifies them, and overwrites them.
BUILT = [stage1.LEVEL]

# Stages this file must never touch. Level2.unity is Krin's own scene, taken
# whole from origin/bun and patched by Tools/adopt_krin.py - Tools/stage2.py is
# now only a record of the layout we would have built, kept because the verifier
# numbers in it are what proved his level needed the current jump arc.
#
# This split is not tidiness. Running build_levels.py while stage2 was still in
# the build list would silently replace 7000 lines of Krin's work with our
# reconstruction of it, and the diff would look like a normal rebuild.
ADOPTED = [stage2.LEVEL]

# Both, in play order - the only thing EditorBuildSettings cares about.
LEVELS = BUILT + ADOPTED

# Scenes that used to exist and must not be left behind. A stale Level3.unity
# in Assets/ still gets imported, still shows up in the Build Settings list the
# next person opens, and still references prefabs - deleting it here is the
# only way the cut actually lands.
RETIRED_SCENES = ["Level3"]


def stable_guid(seed):
    """Same helper Tools/make_prefabs.py uses. Deterministic, so regenerating
    an asset never orphans a reference to it."""
    return hashlib.md5(("late-to-kosen::" + seed).encode()).hexdigest()


# ============================================================================
# YAML EMIT
# ============================================================================
FIRST_ID = 1900000000


def quote(s):
    """Single-quoted YAML scalar, applied to every string unconditionally.

    The sign copy contains commas, colons, arrows, exclamation marks and full
    stops. Deciding per-string whether a plain scalar happens to be safe is
    exactly the kind of cleverness that produces a scene Unity silently
    mis-parses, and a mis-parsed scene does not fail loudly - it opens with one
    sign missing."""
    return "'" + s.replace("'", "''") + "'"


def fmt(v):
    """Unity writes 5, not 5.0. Keeps the diff readable and matches what the
    editor would write back on the next save."""
    if isinstance(v, bool):
        return "1" if v else "0"
    if isinstance(v, str):
        return quote(v)
    return str(int(v)) if float(v).is_integer() else repr(float(v))


def modification(target_id, guid, path, value):
    return (
        f"    - target: {{fileID: {target_id}, guid: {guid}, type: 3}}\n"
        f"      propertyPath: {path}\n"
        f"      value: {value}\n"
        f"      objectReference: {{fileID: 0}}\n"
    )


def make_instance(place, instance_id, transform_id):
    """One PrefabInstance plus its stripped Transform.

    Rotation and the euler hint are written even though they are always
    identity: Unity fills in missing modifications from the prefab, and a
    placement that inherits a rotation it never asked for is a bug that only
    shows up as one crooked platform."""
    spec = P[place.kind]
    guid = spec["guid"]
    tf_id = spec["tf"]

    mods = [modification(spec["go"], guid, "m_Name", place.name)]
    for axis, val in zip("xyz", place.pos):
        mods.append(modification(tf_id, guid, f"m_LocalPosition.{axis}", fmt(val)))
    for axis, val in zip("xyz", place.scale):
        mods.append(modification(tf_id, guid, f"m_LocalScale.{axis}", fmt(val)))
    for axis, val in (("w", 1), ("x", 0), ("y", 0), ("z", 0)):
        mods.append(modification(tf_id, guid, f"m_LocalRotation.{axis}", val))
    for axis in "xyz":
        mods.append(modification(tf_id, guid, f"m_LocalEulerAnglesHint.{axis}", 0))

    for key in sorted(place.props):
        comp, _, field = key.partition(".")
        if comp not in spec:
            sys.exit(f"{place.name}: prefab {place.kind} has no component "
                     f"'{comp}' (known: {sorted(spec)})")
        mods.append(modification(spec[comp], guid, field, fmt(place.props[key])))

    return (
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


# ============================================================================
# SKELETON EDITS
# ============================================================================
def edit_block(scene, anchor, old, new):
    """Replace `old` with `new` inside one anchor's document only.

    A 1300-line scene contains 'm_LocalPosition' forty times; a global replace
    would be a coin flip."""
    marker = "&%d\n" % anchor
    i = scene.find(marker)
    if i < 0:
        sys.exit(f"anchor {anchor} not in the skeleton - regenerate "
                 "Tools/scene_skeleton.unity from a clean Level1.unity")
    j = scene.find("\n--- ", i)
    if j < 0:
        j = len(scene)
    block = scene[i:j]
    if old not in block:
        sys.exit(f"anchor {anchor}: expected {old!r}, not found")
    return scene[:i] + block.replace(old, new, 1) + scene[j:]


def insert_field(scene, anchor, after, line):
    """Add a serialized field the skeleton predates.

    Unity's YAML reader is key-based, so position inside the block is purely
    cosmetic - it goes after `after` so the diff reads in declaration order."""
    marker = "&%d\n" % anchor
    i = scene.find(marker)
    j = scene.find("\n--- ", i)
    block = scene[i:j]
    key = line.split(":")[0] + ":"
    if key in block:
        existing = [l for l in block.splitlines() if l.strip().startswith(key)][0]
        return edit_block(scene, anchor, existing.strip(), line.strip())
    k = block.find(after)
    if k < 0:
        sys.exit(f"anchor {anchor}: no anchor line {after!r} to insert after")
    k += len(after)
    return scene[:i] + block[:k] + line + block[k:] + scene[j:]


def mmss(seconds):
    return "%02d:%02d" % (int(seconds) // 60, int(seconds) % 60)


def build_scene(skeleton, level):
    s = skeleton

    # --- GameManager: which stage this is, and how long the bell gives you
    s = insert_field(s, 598578337,
                     "m_EditorClassIdentifier: Assembly-CSharp::GameManager\n",
                     "  levelIndex: %d\n" % level["index"])
    s = edit_block(s, 598578337, "startingTime: 85",
                   "startingTime: %s" % fmt(level["time"]))

    # --- PlayerController: how far you fall before it counts as a death
    s = edit_block(s, 771653306, "killY: -12", "killY: %s" % fmt(level["kill_y"]))

    # --- spawn point and the player's authored position
    sx, sy = level["spawn"]
    s = edit_block(s, 1497045125, "m_LocalPosition: {x: 0, y: 2, z: 0}",
                   "m_LocalPosition: {x: %s, y: %s, z: 0}" % (fmt(sx), fmt(sy)))
    s = edit_block(s, 771653310, "m_LocalPosition: {x: 0, y: 1, z: 0}",
                   "m_LocalPosition: {x: %s, y: %s, z: 0}" % (fmt(sx), fmt(sy)))

    # --- camera starts on the player instead of sliding in from the origin
    s = edit_block(s, 519420032, "m_LocalPosition: {x: 0, y: 0, z: -10}",
                   "m_LocalPosition: {x: %s, y: %s, z: -10}" % (fmt(sx), fmt(sy + 1)))

    # --- the scene-authored HUD shows the right number before the first frame
    s = edit_block(s, 1730641361, "m_text: 01:25", "m_text: %s" % mmss(level["time"]))

    placements = [ground(*g) for g in level["grounds"]] + list(level["objects"])

    blocks, roots = [], []
    next_id = FIRST_ID
    for p in placements:
        blocks.append(make_instance(p, next_id, next_id + 1))
        roots.append(next_id + 1)
        next_id += 2

    marker = "--- !u!1660057539 &9223372036854775807\n"
    head, tail = s.split(marker, 1)
    tail = tail.rstrip("\n") + "\n" + "".join(f"  - {{fileID: {r}}}\n" for r in roots)
    return head + "".join(blocks) + marker + tail, placements


# ============================================================================
# VERIFIER
# ============================================================================
MIN_STANDABLE = 3.0     # narrower than this is scenery, not a platform


class Surface:
    """A platform, as the verifier sees it: edges and a top, not a centre."""

    __slots__ = ("name", "left", "right", "top", "bottom", "offroute")

    def __init__(self, row):
        name, cx, cy, w, h = row[:5]
        self.name = name
        self.left = cx - w / 2.0
        self.right = cx + w / 2.0
        self.top = cy + h / 2.0
        self.bottom = cy - h / 2.0
        self.offroute = len(row) > 5 and "offroute" in row[5]


def surfaces(grounds):
    """Everything wide enough to stand on, left to right."""
    out = [Surface(g) for g in grounds]
    return sorted([s for s in out if s.right - s.left >= MIN_STANDABLE],
                  key=lambda s: s.left)


def route_edges(level, walk):
    """The jumps that are actually jumps.

    A left-to-right chain is right for a stage that runs left to right, and
    wrong the moment a level has a vertical axis: stage 2's arena starts to the
    LEFT of the ledge you drop into it from, so sorting by left edge pairs up
    platforms that no player ever travels between. Those levels declare a
    `route` explicitly and this just resolves the names.

    Platforms flagged "offroute" are dropped from the derived chain. They are
    real ground - you can stand on them, and rule 3 still checks things placed
    there - but they are dead ends, secrets and pit floors, and threading them
    into the route would demand that a pit be climbable."""
    by_name = {s.name: s for s in walk}
    if level.get("route"):
        edges = []
        for a, b in level["route"]:
            for n in (a, b):
                if n not in by_name:
                    sys.exit(f"Level{level['index']}: route names {n}, which is "
                             f"not a standable platform (needs width >= "
                             f"{MIN_STANDABLE}u)")
            edges.append((by_name[a], by_name[b]))
        return edges
    chain = [s for s in walk if not s.offroute]
    return list(zip(chain, chain[1:]))


def separation(a, b):
    """Horizontal gap between two platforms, whichever way the player travels.

    `b.left - a.right` is only the gap if b is to the RIGHT of a. Stage 1's
    stairwell doubles back on every floor - four of its jumps are leftward - and
    for those the old expression returns a large negative number, which the
    rules below read as "overlapping, nothing to clear" and wave through. A
    2u leftward jump and a 9u leftward jump both looked like -24.

    Negative still means genuinely overlapping, and still means no jump."""
    return max(b.left - a.right, a.left - b.right)


def verify(level, placements):
    fails, warns = [], []
    label = "Level%d" % level["index"]
    walk = surfaces(level["grounds"])
    edges = route_edges(level, walk)
    apex = jump_apex()

    # --- 1. every jump on the route is inside the arc, with room to spare
    for a, b in edges:
        gap = separation(a, b)
        rise = b.top - a.top
        if rise > STEP_APEX * apex + 1e-6:
            fails.append(f"{label}: {a.name} -> {b.name} step-up {rise:.2f}u is "
                         f"{rise / apex * 100:.0f}% of the {apex:.2f}u apex "
                         f"(ceiling is {STEP_APEX * 100:.0f}%)")
        elif rise > STEP_APEX_WARN * apex:
            warns.append(f"{label}: {a.name} -> {b.name} step-up {rise:.2f}u is "
                         f"{rise / apex * 100:.0f}% of apex - has to be taken "
                         "near the top of the arc")
        if gap < -0.001:
            continue                       # overlapping platforms are fine
        reach = horizontal_reach(max(0.0, rise))
        if reach <= 0.0:
            fails.append(f"{label}: {a.name} -> {b.name} needs a {rise:.2f}u "
                         f"rise, higher than the {apex:.2f}u apex")
        elif gap > reach * GAP_SAFETY:
            fails.append(f"{label}: {a.name} -> {b.name} gap {gap:.2f}u vs reach "
                         f"{reach:.2f}u ({gap / reach * 100:.0f}%, over the "
                         f"{GAP_SAFETY * 100:.0f}% safety margin)")

    # --- 2. no slot the player can wedge in
    # The capsule is 0.5u wide, and a 0.5u slot between two same-height
    # platforms swallowed the player in the old build: you fell in, did not
    # die, and could not get out.
    for a, b in edges:
        gap = separation(a, b)
        if abs(b.top - a.top) < 0.01 and 0.001 < gap < 1.0:
            fails.append(f"{label}: {gap:.2f}u slot between {a.name} and "
                         f"{b.name} - the collider wedges in anything under 1u")

    # --- 3. everything that stands on the ground is actually standing on ground
    #
    # Height is part of this now. On a flat stage "some platform spans this x"
    # was the same question as "this thing has a floor", but stage 1 stacks four
    # floors inside forty units of width, so every x in the tower is spanned by
    # four platforms and the old test passed everything unconditionally.
    #
    # The window is -1.0 to +3.5 above a platform top because that is the range
    # the constructors in level_kit use: a spike sits 0.5u INTO the floor and a
    # goal sits 1.5u above it with 1.5u of its own height.
    for p in placements:
        if p.kind in AIRBORNE_KINDS or "airborne" in p.note:
            continue                       # rule 5 checks fake platforms properly
        x, y = p.pos[0], p.pos[1]
        if not any(s.left - 0.6 <= x <= s.right + 0.6
                   and -1.0 <= y - s.top <= 3.5 for s in walk):
            fails.append(f"{label}: {p.name} at ({x}, {y}) has no floor under it")

    # --- 4. a checkpoint you respawn onto must not have a hazard on top of it
    #
    # Also height-aware, and for the same reason: a bin on floor 2 and a
    # checkpoint on floor 4 can share an x-coordinate and be ten units apart.
    cps = [p for p in placements if p.kind == "Checkpoint"]
    haz = [p for p in placements
           if p.kind in ("Trap", "TrapHidden", "TrapSpike")
           and "airborne" not in p.note]
    for c in cps:
        for h in haz:
            d = abs(c.pos[0] - h.pos[0])
            if d < 1.2 and abs(c.pos[1] - h.pos[1]) < 1.5:
                fails.append(f"{label}: {h.name} is {d:.1f}u from {c.name} - "
                             "respawn lands on it")

    # --- 5. a fake platform must sit over a gap the player can ALREADY clear
    # Otherwise it is not a troll, it is a dead end, and the difference is the
    # whole reason the level is fun instead of unfair.
    for p in placements:
        if p.kind != "PlatformFake":
            continue
        x = p.pos[0]
        spanned = next(((a, b) for a, b in edges if a.right <= x <= b.left), None)
        if spanned is None:
            fails.append(f"{label}: {p.name} at x={x} is not over a gap on the route")
            continue
        a, b = spanned
        gap = separation(a, b)
        reach = horizontal_reach(max(0.0, b.top - a.top))
        if reach <= 0 or gap > reach * GAP_SAFETY:
            fails.append(f"{label}: {p.name} spans a {gap:.2f}u gap that is NOT "
                         "clearable unaided - it is load-bearing")

    # --- 6. checkpoint spacing: a death should cost seconds, not a minute
    goal_x = max(p.pos[0] for p in placements if p.kind == "Goal")
    xs = sorted([level["spawn"][0]] + [c.pos[0] for c in cps])
    for a, b in zip(xs, xs[1:] + [goal_x]):
        if b - a > 34.0:
            warns.append(f"{label}: {b - a:.0f}u between checkpoints around "
                         f"x={a:.0f} ({(b - a) / WALK_SPEED:.0f}s of walking back)")

    # --- 7. the level has to be completable inside the timer
    left = min(s.left for s in walk)
    run = (goal_x - left) / WALK_SPEED
    if run > level["time"] * 0.75:
        fails.append(f"{label}: {run:.0f}s of pure walking against a "
                     f"{level['time']:.0f}s timer - no room for mistakes")

    # --- 8. the flood must never rise above ground the player still has to cross
    for p in placements:
        if p.kind != "Floodwater":
            continue
        top = p.pos[1] + p.props["mb.surfaceSize.y"] / 2.0 + p.props["mb.maxHeight"]
        dry = [s for s in walk if s.top > top and s.right > goal_x - 40]
        if not dry:
            fails.append(f"{label}: {p.name} tops out at y={top:.2f}, above every "
                         "platform near the goal - the finish drowns")

    # --- 9. BIKE SAFETY
    # A ride ends at a rack or it does not end, so from the first bicycle to the
    # goal the route has to work for a rider as well as a walker. Riding is
    # faster (every gap gets easier) and jumps lower (every step-up gets harder),
    # and the second half of that is what strands people: a 2u step a walker
    # does not notice is a wall on a bike, and there is no dismount button.
    bikes = [p for p in placements if p.kind == "Bicycle"]
    gates = []
    if bikes:
        bike_x = min(p.pos[0] for p in bikes)
        ride_apex = jump_apex(riding=True)
        real_racks = [p for p in placements if p.kind == "BikeRack"
                      and p.props.get("mb.isReal", 1)]

        # A step-up over the riding limit is a softlock everywhere EXCEPT on a
        # platform that has a real rack on it. There, it is the point: park or
        # do not continue. Stage 1's Ground_Soi_D -> Kerb_Near is 1.90u against
        # a 1.52u riding ceiling and a 2.50u walking one, so the wall is a wall
        # only while you are on the bike, and the rack is eight units behind it.
        #
        # This is the rule TJ asked for in as many words: "there is no way I am
        # going to jump over it and go on without parking". Geometry says it, so
        # nothing has to say it out loud.
        def rack_on(surface):
            return any(surface.left <= p.pos[0] <= surface.right
                       for p in real_racks)

        ridable_until = None
        for a, b in edges:
            if b.right <= bike_x:
                continue                   # behind the bike, walker-only ground
            if ridable_until is not None:
                continue                   # past the gate: the player is on foot
            gap = separation(a, b)
            rise = b.top - a.top
            if rise > STEP_APEX * ride_apex + 1e-6:
                if rack_on(a):
                    gates.append(f"{label}: dismount gate at {a.name} -> "
                                 f"{b.name} - {rise:.2f}u step, walkable "
                                 f"({rise / apex * 100:.0f}% of apex) and not "
                                 f"ridable ({rise / ride_apex * 100:.0f}%). "
                                 "The rack is the only way past")
                    ridable_until = a.name
                    continue
                fails.append(f"{label}: BIKE SOFTLOCK - {a.name} -> {b.name} "
                             f"step-up {rise:.2f}u vs a {ride_apex:.2f}u riding "
                             f"apex. A rider past x={bike_x:.0f} cannot get up "
                             "it and cannot put the bike down")
            if gap > 0:
                reach = horizontal_reach(max(0.0, rise), riding=True)
                if reach <= 0 or gap > reach * GAP_SAFETY:
                    fails.append(f"{label}: BIKE SOFTLOCK - {a.name} -> {b.name} "
                                 f"gap {gap:.2f}u vs a {reach:.2f}u riding reach")

        if not real_racks:
            fails.append(f"{label}: has a bicycle and no real BikeRack - the "
                         "ride can never be ended")
        elif ridable_until is None and max(p.pos[0] for p in real_racks) < goal_x - 40:
            # Only worth saying when the ride could actually have continued. If
            # a dismount gate closed the section, a rider finishing on the bike
            # is not possible and the warning would be noise.
            last = max(p.pos[0] for p in real_racks)
            warns.append(f"{label}: last real rack is at x={last:.0f}, "
                         f"{goal_x - last:.0f}u short of the goal - a rider "
                         "finishes on the bike")

    return fail