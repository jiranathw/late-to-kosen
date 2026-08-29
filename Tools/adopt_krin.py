#!/usr/bin/env python3
"""
Adopt Krin's level (origin/bun:Assets/Scenes/Level1_Krin.unity) as our stage 2.

TJ's instruction was "use Krin's file directly". So this script does NOT rebuild
the level. It copies his scene byte-for-byte and then applies a short, explicit
list of surgical patches - every one of which exists because the scene would
otherwise be broken or unplayable against OUR scripts:

  1. GameManager      levelIndex 2 (absent -> 0 -> clamps to 1 -> stage 2 would
                      announce itself as stage 1); drop infiniteLives, which is
                      Bun's test flag and does not exist on our GameManager.
  2. PlayerController Krin's block names sprint fields we deleted and omits the
                      three bike fields. Unity fills absent fields with
                      default(T), NOT the C# initialiser, so bikeSpeedMultiplier
                      would deserialise to 0 and riding would be perfectly
                      immobile. Every field is therefore written explicitly.
                      killY stays at Krin's -20: the secret area is at y -10.9
                      and our usual -12 would kill you inside it.
  3. Rigidbody2D      gravityScale 2.6 - our jump arc is meaningless at 1.
                      Interpolate on, same as Level1.
  4. Player           starts at 41.19 in Krin's file, which is two thirds of the
                      way through his own level. Moved onto SpawnPoint.
  5. Checkpoints      all three sit stacked at x ~ 0 at scales of 0.03-0.12, so
                      the player trips all of them in the first second and the
                      level has effectively no checkpoints after that. Spread
                      onto the two platforms Krin already named for them
                      (GroundCheckpoint1 at x 14, GroundCheckpoint2 at x 37).
                      Checkpoint1 stays at x ~ 0 on purpose: KrinTeleporter uses
                      it as startPoint, and "the secret sends you back to the
                      first checkpoint" is the joke.
  6. Goal             sits at (67.55, 4.50) in mid-air with nothing under it and
                      an invisible KillBlock below, i.e. unreachable. Three
                      platforms added to build a real route to it, threaded
                      under Krin's floating Trap (2) bar so his hazard still
                      does its job.
  7. Secret text      the two secret-ending captions are parked at y -12.5 and
                      -15.2, below every surface in the level, where no player
                      can ever read them. Moved into the SecretTeleporter zone
                      and the punchline finished.

Run:  python Tools/adopt_krin.py
Reads: git show origin/bun:Assets/Scenes/Level1_Krin.unity
Writes: Assets/Scenes/Level2.unity   (the .meta, and therefore the build-settings
        entry, is left alone on purpose)
"""

import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "Assets" / "Scenes" / "Level2.unity"
SRC_REF = "origin/bun:Assets/Scenes/Level1_Krin.unity"

GROUND_GUID = "6f851581bcfd4db3a0dfd1037b679b9a"
GROUND_GO = "7900112233440000000"
GROUND_TR = "7900112233440000001"

# --- physics for THIS scene, which is Krin's, so these are Krin's ------------
# Deliberately NOT the numbers in PlayerController.cs or build_levels.py. Stage 1
# is ours and uses those; stage 2 is his and uses these. See PLAYER_FIELDS below
# for the measurements behind the split.
MOVE_SPEED = 6.0
JUMP_FORCE = 7.0
GRAVITY_SCALE = 1.0
FALL_MULT = 1.5

G_UP = 9.81 * GRAVITY_SCALE
APEX = JUMP_FORCE ** 2 / (2 * G_UP)
T_RISE = JUMP_FORCE / G_UP
T_FALL = (2 * APEX / (G_UP * FALL_MULT)) ** 0.5
REACH = MOVE_SPEED * (T_RISE + T_FALL)
MAX_GAP = 0.75 * REACH
MAX_STEP = 0.70 * APEX


def read_source() -> str:
    out = subprocess.run(
        ["git", "show", SRC_REF],
        cwd=ROOT, capture_output=True, check=True,
    )
    return out.stdout.decode("utf-8")


# ---------------------------------------------------------------------------
# helpers that edit one YAML document inside the scene, addressed by its anchor
# ---------------------------------------------------------------------------

def split_docs(src: str):
    """[(header, body), ...] with docs[0] being the file header."""
    parts = re.split(r"^(--- !u!\d+ &\d+.*)$", src, flags=re.M)
    docs = [("", parts[0])]
    for i in range(1, len(parts), 2):
        docs.append((parts[i], parts[i + 1]))
    return docs


def join_docs(docs) -> str:
    return docs[0][1] + "".join(h + b for h, b in docs[1:])


def find(docs, anchor: int):
    for i, (h, _) in enumerate(docs):
        if h.startswith(f"--- !u!") and h.split("&")[1].split()[0] == str(anchor):
            return i
    raise KeyError(f"anchor {anchor} not found")


def set_scalar(body: str, key: str, value) -> str:
    """Replace `  key: old` at two-space indent (component-level field)."""
    new, n = re.subn(rf"^  {re.escape(key)}: .*$", f"  {key}: {value}",
                     body, count=1, flags=re.M)
    if n != 1:
        raise KeyError(f"field {key} not found")
    return new


def set_override(body: str, prop: str, value) -> str:
    """Replace the `value:` of a PrefabInstance m_Modifications entry."""
    pat = rf"(propertyPath: {re.escape(prop)}\n      value: )[^\n]*"
    new, n = re.subn(pat, lambda m: m.group(1) + str(value), body, count=1)
    if n != 1:
        raise KeyError(f"override {prop} not found")
    return new


def has_override(body: str, prop: str) -> bool:
    return f"propertyPath: {prop}\n" in body


def add_override(body: str, target: str, prop: str, value) -> str:
    """Append a modification entry just before m_RemovedComponents."""
    entry = (f"    - target: {{fileID: {target}, guid: {GROUND_GUID}, type: 3}}\n"
             f"      propertyPath: {prop}\n"
             f"      value: {value}\n"
             f"      objectReference: {{fileID: 0}}\n")
    new, n = re.subn(r"(?m)^    m_RemovedComponents: \[\]$",
                     entry + "    m_RemovedComponents: []", body, count=1)
    if n != 1:
        raise KeyError("m_RemovedComponents anchor not found")
    return new


def set_or_add(body: str, target: str, prop: str, value) -> str:
    return (set_override(body, prop, value) if has_override(body, prop)
            else add_override(body, target, prop, value))


# ---------------------------------------------------------------------------

def ground_instance(anchor: int, name: str, x: float, y: float,
                    sx: float, sy: float) -> str:
    """A clean Ground prefab instance, no added children, parented to the scene."""
    def mod(target, prop, value):
        return (f"    - target: {{fileID: {target}, guid: {GROUND_GUID}, type: 3}}\n"
                f"      propertyPath: {prop}\n"
                f"      value: {value}\n"
                f"      objectReference: {{fileID: 0}}\n")

    mods = mod(GROUND_GO, "m_Name", name)
    for prop, val in (("m_LocalScale.x", sx), ("m_LocalScale.y", sy),
                      ("m_LocalScale.z", 1),
                      ("m_LocalPosition.x", x), ("m_LocalPosition.y", y),
                      ("m_LocalPosition.z", 0),
                      ("m_LocalRotation.w", 1), ("m_LocalRotation.x", -0),
                      ("m_LocalRotation.y", -0), ("m_LocalRotation.z", -0),
                      ("m_LocalEulerAnglesHint.x", 0),
                      ("m_LocalEulerAnglesHint.y", 0),
                      ("m_LocalEulerAnglesHint.z", 0)):
        mods += mod(GROUND_TR, prop, val)

    return (f"--- !u!1001 &{anchor}\n"
            f"PrefabInstance:\n"
            f"  m_ObjectHideFlags: 0\n"
            f"  serializedVersion: 2\n"
            f"  m_Modification:\n"
            f"    serializedVersion: 3\n"
            f"    m_TransformParent: {{fileID: 0}}\n"
            f"    m_Modifications:\n"
            f"{mods}"
            f"    m_RemovedComponents: []\n"
            f"    m_RemovedGameObjects: []\n"
            f"    m_AddedGameObjects: []\n"
            f"    m_AddedComponents: []\n"
            f"  m_SourcePrefab: {{fileID: 100100000, guid: {GROUND_GUID}, type: 3}}\n")


# ---------------------------------------------------------------------------
# the patch list
# ---------------------------------------------------------------------------

# KRIN'S OWN PHYSICS, kept for stage 2 only.
#
# origin/bun's Level1_Krin.unity ships moveSpeed 6, sprintSpeed 8.5, jumpForce 7,
# gravityScale 1, fallMultiplier 1.5. Stage 1 uses our numbers (7.5 / 13.5 / 2.6
# / 1.8); this scene uses his, because his level was measured against his arc and
# nothing else. The two scenes can disagree because the player is a plain
# GameObject in each scene rather than a shared prefab, so these are two
# independent sets of serialised fields and neither can leak into the other.
#
# Why the arc has to move together with the speed rather than the speed alone:
#
#              apex    flat reach    biggest gap in his level (5.03u)
#   his        2.50u      7.78u              65% - comfortable
#   ours       3.57u      6.93u              73% - comfortable
#   mixed      3.57u      5.54u              91% - a coin flip
#
# His jump is floatier (gravityScale 1 against our 2.6), so it hangs long enough
# to carry a slow walk across a wide gap. Our jump is snappier and needs the
# faster walk to cover the same ground. Take his speed with our gravity and the
# 5.03u gap after Ground_Start becomes a jump you miss one time in three.
#
# sprintSpeed is gone from PlayerController, so there is one speed here and it
# has to be his walk: his level's widest gap is 5.03u against a 5.83u walking
# budget, so nothing in it actually required the sprint.
#
# THE ONE TIGHT SPOT, measured: GroundCheckpoint2 (top -2.57) up to the ledge at
# top -0.24 is a 2.33u step against his 2.50u apex - 93%, a full-height jump with
# almost nothing spare. It is his level at his numbers so it shipped that way,
# but if it turns out to be miserable, raise jumpForce here to 7.6 (apex 2.94u,
# 79%) and change nothing else.
PLAYER_FIELDS = """  moveSpeed: 6
  jumpForce: 7
  coyoteTime: 0.12
  jumpBufferTime: 0.12
  fallMultiplier: 1.5
  lowJumpMultiplier: 3
  bikeSpeedMultiplier: 1.5
  bikeJumpMultiplier: 0.78
  bikeAccelTime: 0.35
  groundCheck: {fileID: 586544842}
  groundCheckRadius: 0.13
  groundLayer:
    serializedVersion: 2
    m_Bits: 8
  killY: -20
"""

GAME_MANAGER_FIELDS = """  levelIndex: 2
  startingTime: 90
  startingLives: 3
  pointsPerSecondLeft: 10
  pointsPerTrapSurvived: 100
  penaltyPerDeath: 50
  defaultSpawnPoint: {fileID: 1497045125}
"""

# Krin's world-space sign canvas sits at this anchored offset; a child's
# anchoredPosition is therefore (worldPos - CANVAS_ORIGIN).
CANVAS_ORIGIN = (368.66666, 149.5)

SECRET_TEXT = (
    "Congratulations! If you reach this secret goal, you will be rewarded with "
    "1,000 baht!\\n\\n*reward payable at the Registrar office.\\nthe Registrar "
    "office is back at the start of the level.\\nenjoy the walk."
)

# anchor, name, x, y, sx, sy  -- the route from Ground (4) up to the Goal.
#
# The underpass threads beneath Krin's floating Trap (2) bar, which spans
# x 59.56..63.52 at y 2.07..2.61. Standing on the underpass the player's head
# is at 1.60 and the bar starts at 2.07: you can walk under it, you cannot jump
# under it, and if you try to jump the gap from Ground (4) instead of dropping
# down you hit the bar and die. That is the gag, and it is Krin's bar - we only
# gave it a floor to be a ceiling over.
#
# The underpass deliberately runs 2.1u past the far end of the bar so there is
# somewhere to stand and jump from that is not directly under the hazard.
NEW_GROUND = [
    (900000001, "GroundGoal_Underpass", 62.2, 0.4, 6.8, 0.4),  # [58.80, 65.60] top 0.60
    (900000002, "GroundGoal_Step",      67.1, 2.1, 1.8, 0.4),  # [66.20, 68.00] top 2.30
    (900000003, "GroundGoal_Floor",     71.5, 3.7, 5.0, 0.4),  # [69.00, 74.00] top 3.90
]

# Krin left the Goal at (67.55, 4.50) hanging in the void with an invisible
# KillBlock underneath. Its x is not load-bearing - nothing references it and no
# sign points at it - so it moves the 3.5u needed to stand on the new floor
# rather than the floor contorting to reach it.
GOAL = (1702008326, 71.0, 4.45)

CHECKPOINTS = [
    # anchor,      name,          x,     y,    reason
    (1015208410, "Checkpoint1", 0.15,  1.48),   # KrinTeleporter startPoint
    (344311544,  "Checkpoint2", 14.0,  1.48),   # on GroundCheckpoint1
    (2017160689, "Checkpoint3", 37.0, -1.97),   # on GroundCheckpoint2
]


def main() -> int:
    src = read_source()
    docs = split_docs(src)

    # 1 - GameManager -------------------------------------------------------
    i = find(docs, 598578337)
    h, b = docs[i]
    b = re.sub(r"^  startingTime: .*?^  defaultSpawnPoint: .*?$\n",
               GAME_MANAGER_FIELDS, b, count=1, flags=re.M | re.S)
    assert "levelIndex: 2" in b and "infiniteLives" not in b
    docs[i] = (h, b)

    # 2 - PlayerController --------------------------------------------------
    i = find(docs, 771653306)
    h, b = docs[i]
    b = re.sub(r"^  moveSpeed: .*?^  killY: .*?$\n", PLAYER_FIELDS,
               b, count=1, flags=re.M | re.S)
    assert "sprintSpeed" not in b and "bikeAccelTime: 0.35" in b
    docs[i] = (h, b)

    # 3 - Player Rigidbody2D ------------------------------------------------
    i = find(docs, 771653308)
    h, b = docs[i]
    b = set_scalar(b, "m_GravityScale", GRAVITY_SCALE)
    b = set_scalar(b, "m_Interpolate", 1)
    docs[i] = (h, b)

 