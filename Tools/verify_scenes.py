#!/usr/bin/env python3
"""
Structural check on the three generated scenes. Run it before opening Unity.

    python3 Tools/verify_scenes.py

This does NOT check level design - Tools/build_levels.py already does that.
This checks the things that make Unity refuse to open a scene, or open it
silently wrong, which is worse:

  1. duplicate YAML anchors         -> Unity keeps one object and drops the rest
  2. dangling fileID references     -> "The referenced script is missing"
  3. unresolvable prefab GUIDs      -> pink boxes, or nothing at all
  4. scene roots that do not exist  -> objects present in the file but not in
                                       the hierarchy, which is the confusing one
  5. missing script .meta files     -> every MonoBehaviour on the object breaks
  6. build settings order           -> scene 0 is what a build boots into
"""

import os
import re
import sys

PROJECT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Stage 3 was cut on the evening of 28 Aug: the team took Krin's level as stage 2 and
# built the dorm-to-building run as stage 1, which left stage 3 with no
# story to tell and three days to tell it in. Tools/build_levels.py
# deletes Level3.unity, and this list is the other half of that.
SCENES = ["Level1", "Level2"]

DOC = re.compile(r"^--- !u!(\d+) &(\d+)(?: (stripped))?\s*$", re.M)
FILEID = re.compile(r"fileID: (\d+)(?:, guid: ([0-9a-f]{32}))?")
GUID_META = re.compile(r"^guid: ([0-9a-f]{32})", re.M)


def asset_guids():
    """Every guid the project can actually resolve, from the .meta files."""
    found = {}
    for root, _, files in os.walk(os.path.join(PROJECT, "Assets")):
        for f in files:
            if not f.endswith(".meta"):
                continue
            path = os.path.join(root, f)
            try:
                m = GUID_META.search(open(path, encoding="utf-8").read())
            except UnicodeDecodeError:
                continue
            if m:
                found[m.group(1)] = os.path.relpath(path[:-5], PROJECT)
    return found


def check_scene(name, guids, problems):
    path = os.path.join(PROJECT, "Assets", "Scenes", name + ".unity")
    if not os.path.exists(path):
        problems.append(f"{name}: scene file missing")
        return
    if not os.path.exists(path + ".meta"):
        problems.append(f"{name}: .meta missing - Unity will invent a new guid "
                        "and every reference to this scene breaks")
    text = open(path, encoding="utf-8").read()

    docs = DOC.findall(text)
    anchors, stripped, dupes = set(), set(), []
    for _, anchor, strip in docs:
        a = int(anchor)
        if a in anchors:
            dupes.append(a)
        anchors.add(a)
        if strip:
            stripped.add(a)
    for d in sorted(set(dupes)):
        problems.append(f"{name}: duplicate anchor {d}")

    # every internal fileID reference must point at a document in this file
    dangling = set()
    for m in FILEID.finditer(text):
        target, guid = int(m.group(1)), m.group(2)
        if guid or target == 0:
            continue                       # external asset, or a null reference
        if target in anchors:
            continue
        if target > 10 ** 15:
            continue                       # a fileID inside a prefab asset
        if target in (100100000, 11500000, 2180264):
            continue                       # well-known built-in ids
        dangling.add(target)
    for d in sorted(dangling):
        problems.append(f"{name}: reference to fileID {d}, which is not in the scene")

    # every prefab guid the scene names must exist on disk
    used = {}
    for m in re.finditer(r"m_SourcePrefab: \{fileID: 100100000, guid: ([0-9a-f]{32})",
                         text):
        used[m.group(1)] = used.get(m.group(1), 0) + 1
    for g, n in sorted(used.items(), key=lambda kv: -kv[1]):
        if g not in guids:
            problems.append(f"{name}: prefab guid {g} ({n} instances) resolves "
                            "to no file in Assets/")

    # Every guid for a script WE own must exist. Package scripts (TextMeshPro,
    # the EventSystem) live in Library/PackageCache, not Assets/, so they are
    # correctly absent here - m_EditorClassIdentifier tells them apart.
    for m in re.finditer(
            r"m_Script: \{fileID: 11500000, guid: ([0-9a-f]{32}).*?\n"
            r"(?:.*?\n)*?  m_EditorClassIdentifier: (\S*)", text):
        guid, owner = m.group(1), m.group(2)
        if owner.startswith("Assembly-CSharp::") and guid not in guids:
            problems.append(f"{name}: script guid {guid} ({owner}) has no .meta")

    # scene roots must all exist, and every root must be a Transform
    roots_block = text.split("SceneRoots:", 1)
    if len(roots_block) != 2:
        problems.append(f"{name}: no SceneRoots document")
        roots = []
    else:
        roots = [int(x) for x in re.findall(r"- \{fileID: (\d+)\}", roots_block[1])]
    for r in roots:
        if r not in anchors:
            problems.append(f"{name}: SceneRoots lists {r}, which does not exist")
    if len(roots) != len(set(roots)):
        problems.append(f"{name}: SceneRoots has a duplicate entry")

    # anything with no parent should be in SceneRoots, or it is invisible
    orphans = 0
    for m in re.finditer(r"--- !u!4 &(\d+)\n(.*?)(?=\n--- |\Z)", text, re.S):
        anchor = int(m.group(1))
        body = m.group(2)
        if "stripped" in body[:40]:
            continue
        father = re.search(r"m_Father: \{fileID: (\d+)\}", body)
        if father and father.group(1) == "0" and anchor not in roots:
            orphans += 1
    if orphans:
        problems.append(f"{name}: {orphans} parentless Transform(s) not in SceneRoots")

    instances = len(re.findall(r"^PrefabInstance:$", text, re.M))
    print(f"  {name}: {len(docs)} docs, {len(anchors)} anchors, "
          f"{instances} prefab instances, {len(roots)} roots, "
          f"{len(used)} distinct prefabs")


def check_build_settings(problems):
    path = os.path.join(PROJECT, "ProjectSettings", "EditorBuildSettings.asset")
    text = open(path, encoding="utf-8").read()
    entries = re.findall(r"- enabled: (\d)\n\s+path: (\S+)\n\s+guid: ([0-9a-f]{32})",
                         text)
    ordered = [p for e, p, _ in entries if e == "1"]
    want = ["Assets/Scenes/%s.unity" % s for s in SCENES]
    if ordered != want:
        problems.append("EditorBuildSettings: enabled scenes are %s, expected %s"
                        % (ordered, want))
    for _, p, g in entries:
        meta = os.path.join(PROJECT, p + ".meta")
        if not os.path.exists(meta):
            problems.append(f"EditorBuildSettings: {p} has no .meta")
            continue
        actual = GUID_META.search(open(meta, encoding="utf-8").read()).group(1)
        if actual != g:
            problems.append(f"EditorBuildSettings: {p} guid {g} != .meta {actual}")
    print("  build settings: %s" % ", ".join(os.path.basename(p) for p in ordered))


def check_scripts(problems):
    d = os.path.join(PROJECT, "Assets", "Scripts")
    n = 0
    for f in sorted(os.listdir(d)):
        if not f.endswith(".cs"):
            continue
        n += 1
        if not os.path.exists(os.path.join(d, f + ".meta")):
            problems.append(f"Assets/Scripts/{f} has no .meta - Unity will "
                            "generate a new guid and unassign every reference")
    print(f"  scripts: {n} .cs files, all with .meta")


def main():
    problems = []
    guids = asset_guids()
    print("assets: %d guids on disk" % len(guids))
    check_scripts(problems)
    for s in SCENES:
        check_scene(s, guids, problems)
    check_build_settings(problems)

    print()
    if problems:
        for p in problems:
            print("FAIL " + p)
        sys.exit("%d problem(s)" % len(problems))
    print("0 problems.")


if __name__ == "__main__":
    main()
