# Bun — Art & UI Tasks (Late to KOSEN)
**ID:** 17 | **Role:** Artist & UI Designer
**Last updated: 25 Aug 2026 | Deadline: 31 Aug 2026 (hard) | 6 days left — you're starting today, not day 1, so move fast**

---

## UPDATE 26 Aug 2026 — read this before the older notes below

**Import settings matter more than the drawings.** For every PNG, in the Inspector:

- **Texture Type = Sprite (2D and UI)**
- **Filter Mode = Point (no filter)** — without this your pixel art comes out blurry
  and it stops being 8-bit, which is what the form promised
- **Compression = None** — same reason
- **Pixels Per Unit identical across every file** — mixing values makes objects
  scale wrong relative to each other and it is painful to fix later

**Drop art on the prefabs in `Assets/Prefabs`, never on objects in the scene.**
Every object in the level is a prefab instance, so changing the parent prefab's
Sprite field updates all of them at once. Touching the scene instead means editing
44 objects by hand and risking a merge conflict with Krin.

**The art list has grown.** Prefabs that need a sprite:

| Prefab | Notes |
|---|---|
| `Ground` | platform / campus tile |
| `PlatformFake` | **must use the exact same sprite as `Ground`** — if the player can tell it apart, the trap doesn't work |
| `Trap` | obviously dangerous |
| `TrapHidden` | invisible in play; the sprite only shows after it kills you, so make it read as "gotcha" |
| `TrapSpike` | spikes that rise out of the ground |
| `Bicycle` | pickup, should read as collectable rather than scenery |
| `Checkpoint1` | has an armed/unarmed colour state already |
| `Goal` | school gate, 2 units wide by 3 tall |
| Player | idle + run frames |
| Background | one static image is fine |

**HUD is already built and styled in code** (`HudUI.cs`) — lives icons, sprint bar,
score, bicycle timer. You are not rebuilding it. If you want a different look,
talk to TJ rather than adding Canvas objects to the scene, because the HUD creates
itself at runtime and anything you add in the scene will sit underneath it.

**All in-game text must stay English.** The bundled TMP font has no Thai glyphs —
Thai text renders as empty boxes. Same for symbols like hearts, which is why lives
are drawn as coloured blocks rather than heart characters. If you want Thai text or
a custom font, it has to be imported as a TMP Font Asset first; tell TJ.

---

## First: get access (do this before anything else)
1. Check email / GitHub notifications for a collaborator invite to `late-to-kosen` — accept it. The repo is Private, you can't see it at all without accepting.
2. Install Unity Hub if you don't have it, then install Unity **6000.4.11f1** via Hub → Installs tab (must match this exact version).
3. `git clone https://github.com/jiranathw/late-to-kosen.git` — **don't create a new Unity project yourself.** The whole project (TJ's scripts, settings, prefabs — already working) is inside this repo.
4. Unity Hub → Add project from disk → select the cloned folder → open it (first open takes a few minutes to import, that's normal).

You can do the art sourcing/drawing below in parallel while that installs/clones — it doesn't need to wait.

## Style guide (lock this in, don't deviate)
- 8-bit pixel art, limited color palette
- Setting: Thai engineering college campus (dorm → school route)
- Character: student rushing to class — 2-3 frame walk cycle is enough if time is short
- Pick one pixel size and stick to it everywhere (e.g. 32x32 or 16x16 base tile) — mixing sizes causes scaling headaches in Unity

## What to produce, in priority order
1. **Player sprite** — idle + run cycle, 2-3 frames minimum
2. **Tileset** — ground/platform tiles for the campus setting
3. **Trap/hazard sprite** — visually obvious as dangerous
4. **Background** — a single static image is fine, no parallax needed
5. **HUD styling** — visual style for the timer/death-counter text. The live-updating logic already works (built by TJ) — you're styling around it, not rebuilding it
6. **Main menu** — one static screen, title + "press any key to start"

## Where to find assets fast
Search itch.io: "pixel platformer asset pack", "school pixel tileset", "2D character sprite sheet free" — filter by Free, confirm the page says it's usable in a student project.

## Handoff naming convention
- Animation clips: `Player_Idle`, `Player_Run`
- Import into: `Assets/Art/Sprites`, `Assets/Art/Tiles`, `Assets/Art/UI`
- Don't touch `Assets/Scripts`, don't rename the `Player` tag or `Ground` layer

## Day-by-day
**25 Aug (today)** — Get repo access set up (above). Source or start drawing player sprite + tileset.

**26 Aug** — Import sprites into Unity (`Assets/Art/Sprites`, Sprite (2D and UI) import type). Get background/tileset into `Level1.unity` alongside Krin.

**27 Aug (checkpoint)** — Join the team playtest. After this, polish only, no new asset categories.

**28 Aug** — Build the HUD visuals (Canvas) around TJ's existing timer/death-counter text objects, and the static main menu screen.

**29 Aug** — Minor polish only.

**30 Aug** — Record the demo video/gameplay clip for submission (confirm with Krin this is still yours).

**31 Aug** — Standby for last-minute needs, submit.

## If things fall behind
Cut animation first — static sprite, flipped left/right (already automatic in the code, no extra work needed). Cut the main menu to a single text screen. Never let art work block TJ or Krin — hand off placeholder/rough versions rather than polishing before integrating.
