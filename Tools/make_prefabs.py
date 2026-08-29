#!/usr/bin/env python3
"""
Generates the .meta files for new scripts and the hazard prefabs for stages 2-3.

Why generate prefabs instead of making them in the editor: everything the player
touches has to be a PrefabInstance, so when Bun drops a sprite on Dog.prefab all
eleven dogs in the game change at once and nobody has to open a scene. Building
them by hand in Unity and committing the result works too, but it is not
reviewable as a diff and it is not reproducible if a scene file gets mangled.

Idempotent: re-running overwrites the prefabs with identical bytes and leaves
every GUID alone, because the GUIDs are derived from the asset name rather than
generated randomly. That is the whole trick - a random GUID on a re-run would
detach every placed instance in every scene.

Usage:  python3 Tools/make_prefabs.py
"""

import hashlib
import os

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS = os.path.join(PROJECT, "Assets", "Scripts")
PREFABS = os.path.join(PROJECT, "Assets", "Prefabs")

# Unity's built-in white square, the same one every existing prefab in this
# project already points at. Placeholder art until Bun's sprites land.
SQUARE = "{fileID: 7482667652216324306, guid: 311925a002f4447b3a28927169b83ea6, type: 3}"


def stable_guid(seed: str) -> str:
    """A GUID that never changes for a given asset name.

    Unity only cares that a GUID is 32 hex characters and unique in the project.
    Deriving it from the name means re-running this script cannot orphan the
    instances already placed in the three scenes.
    """
    return hashlib.md5(("late-to-kosen::" + seed).encode()).hexdigest()


# --------------------------------------------------------------------- metas

SCRIPT_META = """fileFormatVersion: 2
guid: {guid}
MonoImporter:
  externalObjects: {{}}
  serializedVersion: 2
  defaultReferences: []
  executionOrder: 0
  icon: {{instanceID: 0}}
  userData:
  assetBundleName:
  assetBundleVariant:
"""

PREFAB_META = """fileFormatVersion: 2
guid: {guid}
PrefabImporter:
  externalObjects: {{}}
  userData:
  assetBundleName:
  assetBundleVariant:
"""


def ensure_script_metas():
    """Every .cs needs a .meta or Unity invents one on import - with a random
    GUID that differs on each teammate's machine, which is how a prefab ends up
    with a missing script for one person and not another."""
    created = []
    for fname in sorted(os.listdir(SCRIPTS)):
        if not fname.endswith(".cs"):
            continue
        meta = os.path.join(SCRIPTS, fname + ".meta")
        if os.path.exists(meta):
            continue
        with open(meta, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(SCRIPT_META.format(guid=stable_guid("script:" + fname)))
        created.append(fname)
    return created


def script_guids():
    """class name -> meta GUID, read back off disk so generated and
    pre-existing scripts are treated identically."""
    out = {}
    for fname in os.listdir(SCRIPTS):
        if not fname.endswith(".cs.meta"):
            continue
        with open(os.path.join(SCRIPTS, fname), encoding="utf-8") as fh:
            for line in fh:
                if line.startswith("guid: "):
                    out[fname[:-len(".cs.meta")]] = line.split(None, 1)[1].strip()
                    break
    return out


# ----------------------------------------------------------- component blocks

def game_object(fid, name, components, layer=0, tag="Untagged"):
    comps = "".join(f"  - component: {{fileID: {c}}}\n" for c in components)
    return (
        f"--- !u!1 &{fid}\n"
        "GameObject:\n"
        "  m_ObjectHideFlags: 0\n"
        "  m_CorrespondingSourceObject: {fileID: 0}\n"
        "  m_PrefabInstance: {fileID: 0}\n"
        "  m_PrefabAsset: {fileID: 0}\n"
        "  serializedVersion: 6\n"
        "  m_Component:\n" + comps +
        f"  m_Layer: {layer}\n"
        f"  m_Name: {name}\n"
        f"  m_TagString: {tag}\n"
        "  m_Icon: {fileID: 0}\n"
        "  m_NavMeshLayer: 0\n"
        "  m_StaticEditorFlags: 0\n"
        "  m_IsActive: 1\n"
    )


def transform(fid, go, scale=(1, 1, 1)):
    sx, sy, sz = scale
    return (
        f"--- !u!4 &{fid}\n"
        "Transform:\n"
        "  m_ObjectHideFlags: 0\n"
        "  m_CorrespondingSourceObject: {fileID: 0}\n"
        "  m_PrefabInstance: {fileID: 0}\n"
        "  m_PrefabAsset: {fileID: 0}\n"
        f"  m_GameObject: {{fileID: {go}}}\n"
        "  serializedVersion: 2\n"
        "  m_LocalRotation: {x: 0, y: 0, z: 0, w: 1}\n"
        "  m_LocalPosition: {x: 0, y: 0, z: 0}\n"
        f"  m_LocalScale: {{x: {sx}, y: {sy}, z: {sz}}}\n"
        "  m_ConstrainProportionsScale: 0\n"
        "  m_Children: []\n"
        "  m_Father: {fileID: 0}\n"
        "  m_LocalEulerAnglesHint: {x: 0, y: 0, z: 0}\n"
    )


def sprite_renderer(fid, go, color, order=1, draw_mode=0, size=(1, 1)):
    r, g, b, a = color
    sx, sy = size
    return (
        f"--- !u!212 &{fid}\n"
        "SpriteRenderer:\n"
        "  serializedVersion: 2\n"
        "  m_ObjectHideFlags: 0\n"
        "  m_CorrespondingSourceObject: {fileID: 0}\n"
        "  m_PrefabInstance: {fileID: 0}\n"
        "  m_PrefabAsset: {fileID: 0}\n"
        f"  m_GameObject: {{fileID: {go}}}\n"
        "  m_Enabled: 1\n"
        "  m_CastShadows: 0\n"
        "  m_ReceiveShadows: 0\n"
        "  m_DynamicOccludee: 1\n"
        "  m_StaticShadowCaster: 0\n"
        "  m_MotionVectors: 1\n"
        "  m_LightProbeUsage: 1\n"
        "  m_ReflectionProbeUsage: 1\n"
        "  m_RayTracingMode: 0\n"
        "  m_RayTraceProcedural: 0\n"
        "  m_RayTracingAccelStructBuildFlagsOverride: 0\n"
        "  m_RayTracingAccelStructBuildFlags: 1\n"
        "  m_SmallMeshCulling: 1\n"
        "  m_ForceMeshLod: -1\n"
        "  m_MeshLodSelectionBias: 0\n"
        "  m_RenderingLayerMask: 1\n"
        "  m_RendererPriority: 0\n"
        "  m_Materials:\n"
        "  - {fileID: 10754, guid: 0000000000000000f000000000000000, type: 0}\n"
        "  m_StaticBatchInfo:\n"
        "    firstSubMesh: 0\n"
        "    subMeshCount: 0\n"
        "  m_StaticBatchRoot: {fileID: 0}\n"
        "  m_ProbeAnchor: {fileID: 0}\n"
        "  m_LightProbeVolumeOverride: {fileID: 0}\n"
        "  m_ScaleInLightmap: 1\n"
        "  m_ReceiveGI: 1\n"
        "  m_PreserveUVs: 0\n"
        "  m_IgnoreNormalsForChartDetection: 0\n"
        "  m_ImportantGI: 0\n"
        "  m_StitchLightmapSeams: 1\n"
        "  m_SelectedEditorRenderState: 0\n"
        "  m_MinimumChartSize: 4\n"
        "  m_AutoUVMaxDistance: 0.5\n"
        "  m_AutoUVMaxAngle: 89\n"
        "  m_LightmapParameters: {fileID: 0}\n"
        "  m_GlobalIlluminationMeshLod: 0\n"
        "  m_SortingLayerID: 0\n"
        "  m_SortingLayer: 0\n"
        f"  m_SortingOrder: {order}\n"
        "  m_MaskInteraction: 0\n"
        f"  m_Sprite: {SQUARE}\n"
        f"  m_Color: {{r: {r}, g: {g}, b: {b}, a: {a}}}\n"
        "  m_FlipX: 0\n"
        "  m_FlipY: 0\n"
        f"  m_DrawMode: {draw_mode}\n"
        f"  m_Size: {{x: {sx}, y: {sy}}}\n"
        "  m_AdaptiveModeThreshold: 0.5\n"
        "  m_SpriteTileMode: 0\n"
        "  m_WasSpriteAssigned: 1\n"
        "  m_SpriteSortPoint: 0\n"
    )


def box_collider(fid, go, is_trigger=1, size=(1, 1)):
    sx, sy = size
    return (
        f"--- !u!61 &{fid}\n"
        "BoxCollider2D:\n"
        "  m_ObjectHideFlags: 0\n"
        "  m_CorrespondingSourceObject: {fileID: 0}\n"
        "  m_PrefabInstance: {fileID: 0}\n"
        "  m_PrefabAsset: {fileID: 0}\n"
        f"  m_GameObject: {{fileID: {go}}}\n"
        "  m_Enabled: 1\n"
        "  serializedVersion: 3\n"
        "  m_Density: 1\n"
        "  m_Material: {fileID: 0}\n"
        "  m_IncludeLayers:\n    serializedVersion: 2\n    m_Bits: 0\n"
        "  m_ExcludeLayers:\n    serializedVersion: 2\n    m_Bits: 0\n"
        "  m_LayerOverridePriority: 0\n"
        "  m_ForceSendLayers:\n    serializedVersion: 2\n    m_Bits: 4294967295\n"
        "  m_ForceReceiveLayers:\n    serializedVersion: 2\n    m_Bits: 4294967295\n"
        "  m_ContactCaptureLayers:\n    serializedVersion: 2\n    m_Bits: 4294967295\n"
        "  m_CallbackLayers:\n    serializedVersion: 2\n    m_Bits: 4294967295\n"
        f"  m_IsTrigger: {is_trigger}\n"
        "  m_UsedByEffector: 0\n"
        "  m_CompositeOperation: 0\n"
        "  m_CompositeOrder: 0\n"
        "  m_Offset: {x: 0, y: 0}\n"
        "  m_SpriteTilingProperty:\n"
        "    border: {x: 0, y: 0, z: 0, w: 0}\n"
        "    pivot: {x: 0.5, y: 0.5}\n"
        "    oldSize: {x: 1, y: 1}\n"
        "    newSize: {x: 1, y: 1}\n"
        "    adaptiveTilingThreshold: 0.5\n"
        "    drawMode: 0\n"
        "    adaptiveTiling: 0\n"
        "  m_AutoTiling: 0\n"
        f"  m_Size: {{x: {sx}, y: {sy}}}\n"
        "  m_EdgeRadius: 0\n"
    )


def rigidbody(fid, go, body_type=2, gravity=0):
    """body_type 0 dynamic, 1 kinematic, 2 static. Hazards rest kinematic and
    are switched to dynamic in code at the moment they are supposed to fall."""
    return (
        f"--- !u!50 &{fid}\n"
        "Rigidbody2D:\n"
        "  serializedVersion: 5\n"
        "  m_ObjectHideFlags: 0\n"
        "  m_CorrespondingSourceObject: {fileID: 0}\n"
        "  m_PrefabInstance: {fileID: 0}\n"
        "  m_PrefabAsset: {fileID: 0}\n"
        f"  m_GameObject: {{fileID: {go}}}\n"
        f"  m_BodyType: {body_type}\n"
        "  m_Simulated: 1\n"
        "  m_UseFullKinematicContacts: 1\n"
        "  m_UseAutoMass: 0\n"
        "  m_Mass: 1\n"
        "  m_LinearDamping: 0\n"
        "  m_AngularDamping: 0.05\n"
        f"  m_GravityScale: {gravity}\n"
        "  m_Material: {fileID: 0}\n"
        "  m_IncludeLayers:\n    serializedVersion: 2\n    m_Bits: 0\n"
        "  m_ExcludeLayers:\n    serializedVersion: 2\n    m_Bits: 0\n"
        "  m_Interpolate: 1\n"
        "  m_SleepingMode: 1\n"
        "  m_CollisionDetection: 1\n"
        "  m_Constraints: 4\n"
    )


def mono(fid, go, script_guid, class_name, fields):
    body = "".join(f"  {k}: {v}\n" for k, v in fields)
    return (
        f"--- !u!114 &{fid}\n"
        "MonoBehaviour:\n"
        "  m_ObjectHideFlags: 0\n"
        "  m_CorrespondingSourceObject: {fileID: 0}\n"
        "  m_PrefabInstance: {fileID: 0}\n"
        "  m_PrefabAsset: {fileID: 0}\n"
        f"  m_GameObject: {{fileID: {go}}}\n"
        "  m_Enabled: 1\n"
        "  m_EditorHideFlags: 0\n"
        f"  m_Script: {{fileID: 11500000, guid: {script_guid}, type: 3}}\n"
        "  m_Name: \n"
        f"  m_EditorClassIdentifier: Assembly-CSharp::{class_name}\n"
        + body
    )


# ------------------------------------------------------------------- prefabs
# Base fileIDs continue the scheme the existing prefabs already use
# (6100000000000000101 for TrapHidden, ...201 PlatformFake, ...301 TrapSpike,
# ...401 Bicycle). New ones start at 501 so nothing collides.
#
# Every one of these is a placeholder colour. The point of the prefab is the
# collider, the script and the GUID; the art is Bun's job and drops in without
# any of this changing.

SPECS = [
    # name, base id, colour, builder key
    ("Bicycle",    401, (0.35, 0.85, 1.00, 1)),
    # Was Dog.prefab. Renamed 28 Aug (evening): the soi dog became a monitor lizard,
    # which is both funnier and more accurate to a Lat Krabang morning. Same
    # script, same 501 fileID block, new asset name and therefore new GUID -
    # which is fine only because every scene is regenerated from this repo.
    ("MonitorLizard", 501, (0.30, 0.42, 0.26, 1)),
    ("Flowerpot",  601, (0.80, 0.36, 0.26, 1)),
    ("TrafficLane", 701, None),
    ("Floodwater", 801, (0.35, 0.55, 0.75, 0.72)),
    ("FakeGoal",   901, (0.62, 0.66, 0.72, 1)),
    ("Signpost",  1001, (0.95, 0.80, 0.35, 1)),
    ("Teleporter", 1101, (0.45, 0.35, 0.62, 1)),
    ("BikeRack",  1201, (0.55, 0.60, 0.66, 1)),
]

# Prefabs that existed before this script did, and whose GUID therefore is not
# stable_guid("prefab:<name>"). Overwriting these with a derived GUID would
# detach every instance already placed in a scene, so their original GUID is
# pinned here instead. Bicycle is the only one so far: it moved into this
# generator on 28 Aug (evening) when BicyclePickup became BikeRental, and it kept both its
# asset GUID and its 401 fileID block so build_levels.py did not have to change.
FIXED_GUIDS = {
    "Bicycle": "09c5f8c63ef746a6aad3543a707b5a76",
}

BASE = 6100000000000000000


def build(name, base, colour, guids):
    go = BASE + base
    tf, sr, col, rb, mb, mb2 = (go + i for i in range(1, 7))

    if name == "Bicycle":
        # An Anywheel bike. The Signpost on the same object is what makes it
        # legible from a distance - the player has to be able to decide whether
        # to touch it, because touching it is a commitment they cannot undo.
        comps = [tf, sr, col, mb, mb2]
        docs = [
            game_object(go, name, comps),
            transform(tf, go, (0.9, 0.9, 1)),
            sprite_renderer(sr, go, colour, order=2),
            box_collider(col, go, is_trigger=1),
            mono(mb, go, guids["BikeRental"], "BikeRental", [
                ("playerTag", "Player"),
                ("bobHeight", 0.14),
                ("bobSpeed", 2.6),
                ("offerMessage", "ANYWHEEL - scan to unlock"),
                ("mountMessage", "RIDE STARTED - park at a rack to end it"),
            ]),
            mono(mb2, go, guids["Signpost"], "Signpost", [
                ("message", ""),
                ("showRange", 7),
                # TMP world-space fontSize is NOT world units. A 3D TextMeshPro
                # renders at roughly fontSize/10 world units per line, so 6 gives
                # a 0.4u line against a camera that shows 10u of height. Do not
                # copy the 0.5 that Krin's checkpoint label uses: that one is a
                # TextMeshProUGUI inside a scaled canvas, where the number means
                # something completely different.
                ("fontSize", 4),
                ("offset", "{x: 0, y: 1.5, z: 0}"),
                ("color", "{r: 0.6, g: 0.92, b: 1, a: 1}"),
                ("playerTag", "Player"),
                ("latch", 0),
            ]),
        ]

    elif name == "BikeRack":
        # isReal defaults to 1. A fake rack is the SAME prefab with that one
        # field overridden in the scene - deliberately, so the two can never
        # drift apart visually. If you ever find yourself wanting a separate
        # FakeBikeRack.prefab, that is the moment the joke starts leaking.
        comps = [tf, sr, col, mb, mb2]
        docs = [
            game_object(go, name, comps),
            transform(tf, go, (2.6, 1.2, 1)),
            sprite_renderer(sr, go, colour, order=1),
            box_collider(col, go, is_trigger=1),
            mono(mb, go, guids["BikeRack"], "BikeRack", [
                ("playerTag", "Player"),
                ("isReal", 1),
                ("idleMessage", "ANYWHEEL PARKING"),
                ("parkedMessage", "RIDE ENDED - thanks for using Anywheel"),
                ("refusedMessage", "CANNOT END RIDE HERE - outside docking zone"),
                ("refusalTimeCost", 0),
                ("refusalCooldown", 1.5),
            ]),
            mono(mb2, go, guids["Signpost"], "Signpost", [
                ("message", ""),
                ("showRange", 7),
                # TMP world-space fontSize is NOT world units. A 3D TextMeshPro
                # renders at roughly fontSize/10 world units per line, so 6 gives
                # a 0.4u line against a camera that shows 10u of height. Do not
                # copy the 0.5 that Krin's checkpoint label uses: that one is a
                # TextMeshProUGUI inside a scaled canvas, where the number means
                # something completely different.
                ("fontSize", 4),
                ("offset", "{x: 0, y: 1.4, z: 0}"),
                ("color", "{r: 0.6, g: 0.92, b: 1, a: 1}"),
                ("playerTag", "Player"),
                ("latch", 0),
            ]),
        ]

    elif name == "MonitorLizard":
        comps = [tf, sr, col, mb]
        docs = [
            game_object(go, name, comps),
            transform(tf, go, (1.9, 0.7, 1)),
            sprite_renderer(sr, go, colour, order=5),
            box_collider(col, go, is_trigger=1),
            mono(mb, go, guids["ChaserHazard"], "ChaserHazard", [
                ("chaseSpeed", 7.6),
                ("giveUpDistance", 34),
                ("playerTag", "Player"),
                ("triggerDistance", 8),
                ("windUpSeconds", 0.45),
                ("rearmOnDeath", "{fileID: 0}"),
            ]),
        ]

    elif name == "Flowerpot":
        comps = [tf, sr, col, rb, mb]
        docs = [
            game_object(go, name, comps),
            transform(tf, go, (0.7, 0.7, 1)),
            sprite_renderer(sr, go, colour, order=5),
            box_collider(col, go, is_trigger=1),
            rigidbody(rb, go, body_type=1, gravity=0),
            mono(mb, go, guids["FallingObject"], "FallingObject", [
                ("triggerDistance", 3.4),
                ("fallGravity", 3.4),
                ("resetAfterSeconds", 3.5),
                ("playerTag", "Player"),
                ("rearmOnReset", "{fileID: 0}"),
            ]),
        ]

    elif name == "TrafficLane":
        # No renderer and no collider: the lane is a spawner, the vehicles it
        # makes are the thing you can hit.
        comps = [tf, mb]
        docs = [
            game_object(go, name, comps),
            transform(tf, go),
            mono(mb, go, guids["TrafficLane"], "TrafficLane", [
                ("laneLength", 26),
                ("speed", -6.5),
                ("spawnEverySeconds", 2.2),
                ("firstSpawnDelay", 0.4),
                ("vehicleSize", "{x: 1.8, y: 0.9}"),
                ("vehicleColor", "{r: 0.95, g: 0.75, b: 0.2, a: 1}"),
                ("vehicleSprite", "{fileID: 0}"),
                ("playerTag", "Player"),
                ("activationRange", 30),
            ]),
        ]

    elif name == "Floodwater":
        comps = [tf, sr, col, mb]
        docs = [
            game_object(go, name, comps),
            transform(tf, go),
            # Sliced so RisingWater can set .size in world units without the
            # transform scale fighting the collider size.
            sprite_renderer(sr, go, colour, order=20, draw_mode=1, size=(120, 24)),
            box_collider(col, go, is_trigger=1, size=(120, 24)),
            mono(mb, go, guids["RisingWater"], "RisingWater", [
                ("riseSpeed", 0.62),
                ("maxHeight", 9),
                ("risingFromStart", 0),
                ("triggerAtPlayerX", 0),
                ("surfaceSize", "{x: 120, y: 24}"),
                ("waterColor", "{r: 0.35, g: 0.55, b: 0.75, a: 0.72}"),
                ("playerTag", "Player"),
                ("graceDepth", 0.35),
            ]),
        ]

    elif name == "FakeGoal":
        # Signpost sits on the same object, which is legal and which
        # FakeGoal.Awake finds via GetComponentInChildren (that includes self).
        comps = [tf, sr, col, mb, mb2]
        docs = [
            game_object(go, name, comps),
            transform(tf, go, (2, 3, 1)),
            sprite_renderer(sr, go, colour, order=2),
            box_collider(col, go, is_trigger=1),
            mono(mb, go, guids["FakeGoal"], "FakeGoal", [
                ("playerTag", "Player"),
                ("revealText", "OUT OF ORDER"),
                ("timePenalty", 0),
                ("revealedColor", "{r: 0.55, g: 0.55, b: 0.6, a: 1}"),
            ]),
            mono(mb2, go, guids["Signpost"], "Signpost", [
                ("message", ""),
                ("showRange", 6),
                # TMP world-space fontSize is NOT world units. A 3D TextMeshPro
                # renders at roughly fontSize/10 world units per line, so 6 gives
                # a 0.4u line against a camera that shows 10u of height. Do not
                # copy the 0.5 that Krin's checkpoint label uses: that one is a
                # TextMeshProUGUI inside a scaled canvas, where the number means
                # something completely different.
                ("fontSize", 4),
                ("offset", "{x: 0, y: 1, z: 0}"),
                ("color", "{r: 1, g: 0.95, b: 0.6, a: 1}"),
                ("playerTag", "Player"),
                ("latch", 0),
            ]),
        ]

    elif name == "Signpost":
        comps = [tf, sr, mb]
        docs = [
            game_object(go, name, comps),
            transform(tf, go, (0.25, 1.4, 1)),
            sprite_renderer(sr, go, colour, order=2),
            mono(mb, go, guids["Signpost"], "Signpost", [
                ("message", ""),
                ("showRange", 5.5),
                # TMP world-space fontSize is NOT world units. A 3D TextMeshPro
                # renders at roughly fontSize/10 world units per line, so 6 gives
                # a 0.4u line against a camera that shows 10u of height. Do not
                # copy the 0.5 that Krin's checkpoint label uses: that one is a
                # TextMeshProUGUI inside a scaled canvas, where the number means
                # something completely different.
                ("fontSize", 4),
                ("offset", "{x: 0, y: 1.6, z: 0}"),
                ("color", "{r: 1, g: 0.95, b: 0.6, a: 1}"),
                ("playerTag", "Player"),
                ("latch", 0),
            ]),
        ]

    elif name == "Teleporter":
        comps = [tf, sr, col, mb]
        docs = [
            game_object(go, name, comps),
            transform(tf, go, (1.6, 3, 1)),
            sprite_renderer(sr, go, colour, order=2),
            box_collider(col, go, is_trigger=1),
            mono(mb, go, guids["Teleporter"], "Teleporter", [
                ("destination", "{x: 0, y: 0}"),
                ("destinationTransform", "{fileID: 0}"),
                ("playerTag", "Player"),
                ("moveCheckpointToExit", 1),
                ("cooldownSeconds", 1.2),
                # Unity does not fall back to a C# field initialiser when a key
                # is absent