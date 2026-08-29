# Late to KOSEN — Project Progress

**Team:** sixseven (TJ 09 / Bun 17 / Krin 21) · **Course:** Programming 7
**Repo:** https://github.com/jiranathw/late-to-kosen · **Branch:** `main`
**Last updated:** 28 Aug 2026, evening · **Deadline:** 31 Aug 2026 (hard) · **3 days left**

---

## What changed tonight: two stages, and one of them is Krin's

Stage 3 is cut. The game is two stages now, and the second one is the level Krin built on
`Lv1-Create` — the team read it, agreed it was harder and more fun than what the generator had
produced, and voted to ship it rather than replace it.

| # | Scene | Title | Timer | What it is |
|---|---|---|---|---|
| 1 | `Level1.unity` | **LATE** — your room to the gate of Building 12 | 80 s | the walk: dorm room, corridor, four flights, lobby, Soi 12, Chalong Krung Road, forecourt |
| 2 | `Level2.unity` | **INSIDE** — Krin's level, ported | 65 s | a short climb, then a drop into a 30-unit arena you cannot climb back out of |

**Why two and not three.** Once Krin's level became stage 2, stage 1 had to become the thing that
gets you to it — the dorm-to-building run — and stage 3 had nothing left to be. Three days is not
enough to invent a third act and make it as good as the two we have. Cutting it is the only
decision here that buys time rather than spending it.

**What that cost.** `RisingWater` and the flood set-piece are written, tested and no longer used
by any level. The script and the `Floodwater` prefab stay in the repo: they cost nothing, they
demonstrate a fourth hazard type, and if the flood ever comes back it is a two-line table edit.

**Stage 2 is Krin's geometry, to two decimal places.** Every platform is at the coordinate he put
it at and his sign copy is reproduced word for word, typos included. Six things were repaired
rather than redesigned, and all six are listed in the module docstring of `Tools/stage2.py` so he
can put back anything he disagrees with. The big one: **his goal had no floor under it**.

**Stage 1 was built to match his cruelty, not to warm up for it.** The brief was "as harsh as
Krin's, with similar gimmicks, equally hard", so each of his three moves is answered: a platform
that is not a platform (`Fake_01_Doormat`), a reward that is a punishment (`Secret_Shortcut`, free
to reach and it takes 27 units of checkpoint to leave), and a hazard placed *before* the sign that
warns about it (`Hidden_01_WetFloor` at x = 20, sign at x = 22).

---

## The three mechanical changes tonight

**Sprint is gone.** Krin's player was `moveSpeed 6 / jumpForce 7 / gravityScale 1` — 1.43 s of
airtime and an 8.56 u flat reach. Ours was 3.45 u after the first 28 Aug retune, and at 3.45 u his
stage is not hard, it is impossible: the opening gap alone is 5.00 u. So the player was rebuilt
around his level instead of the other way round, sprint came out, and its speed became the only
speed. **`moveSpeed 7.5`, `jumpForce 13.5`, `gravityScale 2.6`, `fallMultiplier 1.8`** — a 3.57 u
apex and a 6.93 u flat reach. A sprint that exists only to cross one gap is a hidden requirement,
not a choice, and removing it deleted the stamina bar, the lockout and three fields per scene.

**The bicycle is an Anywheel rental, not a boost.** It used to be +45% for 4.5 seconds. Now you
mount it and **the ride only ends at a rack** — there is no dismount button. Rack 1 (x = 90) is
real and generous, so the player learns racks work. Rack 2 (x = 136) is the same prefab, the same
size and the same sign, one boolean apart, and it is a lie. Rack 3 (x = 169) is real, on the far
side of Chalong Krung Road, which means the fake one strands you with a bike you cannot put down.

That is survivable on purpose, and the verifier proves it on every run: **rule 9** re-checks every
jump from the first bicycle to the goal against riding physics (2.17 u apex, 8.11 u reach, so a
1.52 u step ceiling and a 6.08 u gap ceiling). Riding is faster and jumps *lower*, and the second
half of that is what strands people. `BikeRental.cs` and `BikeRack.cs` are new.

**The soi dog is a monitor lizard.** Same `ChaserHazard`, new theme, and it is funnier because it
is true — a two-metre ตัวเงินตัวทอง out of a Lat Krabang klong at half past seven is not invented.
It chases at 7.0 against a walk of 7.5, so it never catches a player who keeps moving. On a bike
it is not even a fright, which is the first moment the bike pays for itself. It shows up again in
stage 2's arena at 7.2, having followed you inside.

---

## The generator is three files now, not one

`Tools/build_levels.py` had reached 900 lines and every level edit produced a diff against the
emitter and the verifier as well. Split:

- **`Tools/level_kit.py`** — physics constants, the prefab table, and one constructor per kind of
  thing a level can contain. Nothing here writes a file.
- **`Tools/stage1.py`** / **`Tools/stage2.py`** — the layouts, and the reasoning for each beat.
- **`Tools/build_levels.py`** — emitter, verifier, driver. It also deletes `Level3.unity`, because
  a cut stage that is still on disk is still in the build.

Three verifier capabilities are new. **Explicit route edges**: stage 2 is a vertical arena, and
sorting platforms by left edge pairs up ones no player ever travels between, so that level
declares its route by name. **An `offroute` ground flag**: pit floors and secret ledges are real
ground you can stand on, but threading them into the route would demand that a pit be climbable.
And **rule 9**, the bike-safety pass described above.

---


## Where we are

Both stages are generated, both verifiers pass with 0 problems, and Build Settings has exactly
Level1 and Level2 in that order. Everything the design form promises is implemented, plus three
optional features.

**The Unity gate was passed once, on the old build.** Level2 ran in Play mode on 28 Aug: HUD,
timer, lives, stage banner and score all correct on screen. **Tonight's build has not been opened
in the editor.** Both scenes, the three new prefabs and the two new scripts were written outside
Unity — whoever opens it first, watch the console and say so in the group before doing anything
else. That is the one outstanding risk on this project.

---

## Form compliance

| Form requirement | Status |
|---|---|
| 2D side-scrolling platformer with hidden troll traps | done — 9 hazard types, 30 instances across two stages |
| Jump and dodge mechanics | done — coyote time, jump buffer, variable height |
| Lives system (lose a life per trap) | done — 3 lives **per stage**, checkpoint respawn |
| Score from speed + traps survived | done — per stage, summed across the run |
| Arrow keys / A-D move, Space / Up jump | done — one speed, no sprint (see below) |
| Esc = Pause / Resume | done |
| Win: reach school in time with a life left | done |
| Lose: lives run out **or** timer hits zero | done — two distinct screens, per stage |
| Optional: bell timer countdown | done — 80 s / 65 s |
| Optional: death counter | done — per stage and per run |
| Optional: bicycle power-up | done — an Anywheel rental with real and fake racks, not a boost |
| Optional: **multiple levels** | done — 2 stages, run-scope score |
| 8-bit pixel art + chiptune | **Bun** — placeholders in place |
| Optional: SFX / BGM, school van shortcut | cut (the van became the Sai 1013 fake bus stop) |

Form asks for "more than one" optional feature. Three shipped, and the sprint requirement in the
control list was dropped deliberately rather than by accident — see the note on Krin's physics
above. If the marker objects to that, `PlayerController` is the only file that changes.

---

## Shipped this round

**Run vs stage architecture.** `GameSession` is new: `DontDestroyOnLoad`, run-scope, holds the
per-stage results and totals and does the scene loading. `GameManager` stays stage-scope and is
rebuilt on every scene load — which is *why* the timer, the lives and the checkpoint all reset
when you enter a stage. That split is the whole lives fix, expressed in code.

**14 new scripts** (31 total): `GameSession`, `HazardTrigger`, `ChaserHazard`, `FallingObject`,
`TrafficLane`, `Vehicle`, `RisingWater`, `Teleporter`, `FakeGoal`, `Signpost`, `SolidSprite`,
`StageBannerUI`, `BikeRental`, `BikeRack`. `BicyclePickup` is deleted — the last two replace it.

**9 generated prefabs** (16 total): `MonitorLizard` (was `Dog`), `BikeRack`, `Bicycle`,
`Flowerpot`, `TrafficLane`, `Floodwater`, `Teleporter`, `FakeGoal`, `Signpost`. All nine are
rebuilt by `Tools/make_prefabs.py`, so Bun replaces the placeholder sprite once per prefab and
every placement in both scenes follows.

**Two generated scenes**, 102 placed objects, all PrefabInstances so Bun's art still propagates
from the prefab without anyone touching a scene:

```
Level1  stage 1   x -10 -> 199   timer 80s   walk 28s (35%)   59 instances, 16 scoring hazards
Level2  stage 2   x -31 ->  72   timer 65s   walk 14s (21%)   43 instances, 15 scoring hazards
```

Stage 2 is a third of stage 1's length and considerably more than a third of its difficulty. The
timer is loose in both because the clock is not where either stage gets its difficulty — a timer
tight enough to punish a first run would punish reading the signs, and the signs are the game.

**Two verifiers, and they do not overlap.**

```
python3 Tools/build_levels.py --check    # design rules, writes nothing
python3 Tools/build_levels.py            # regenerate both scenes + Build Settings
python3 Tools/verify_scenes.py           # structural check on the written YAML
```

`build_levels.py` enforces nine design rules derived from the physics, not guessed: gap ≤ 75% of
the real horizontal reach for that step-up, step-ups ≤ 70% of the apex, no wedge slot narrower
than 1 u, everything ground-standing actually over ground, no hazard within 1.2 u of a checkpoint,
fake platforms only over gaps that are already clearable, checkpoint spacing, walk time ≤ 75% of
the timer, the flood ceiling leaving the goal dry, and **rule 9** — every jump from the first
bicycle onward re-checked against riding physics, so a rental can never become a softlock.

The step-up ceiling is 70% of apex rather than the 55% that reads comfortably, and that number is
not a preference: Krin's climb out of the arena is a 2.32 u rise against a 3.57 u apex, which is
65%. Anything above 55% still emits a warning.

`verify_scenes.py` catches the other failure mode — the one where Unity opens the scene and it is
silently wrong: duplicate YAML anchors, dangling fileIDs, unresolvable prefab GUIDs, missing
script `.meta`, scene roots that do not exist, parentless transforms, Build Settings order.

Current output: **0 problems**. Five design warnings, all intentional — one checkpoint gap on
stage 1 and four tall-step warnings on stage 2, which are Krin's ledges and are the level.

**Bugs found and fixed while verifying.**

1. *`CampusBackground` only applied to the first scene loaded.* `RuntimeInitializeOnLoadMethod`
   fires once at game start, **not** once per scene load, and the component had no
   `DontDestroyOnLoad` and no per-scene hook. Stages 2 and 3 would have come up on Unity's
   default grey-blue with no background sprite — which reads as "the art is broken", not "the art
   is missing". Now hooks `SceneManager.sceneLoaded`. This is the one real cross-level bug the
   sweep found.
2. *Teleporter respawn loop, caught before it shipped.* Re-arming the stage-3 teleporter on
   respawn looked correct until you notice its exit is fourteen units *behind* its entrance — a
   re-armed teleporter catches the player again on every walk forward, forever, without ever
   costing a life. Unloseable and unwinnable at the same time. It is now one-shot per stage load,
   with the reasoning written into the file so nobody helpfully "fixes" it back.
3. *Six checkpoints added.* The generator warned about 36–63 unit stretches with no checkpoint in
   all three stages. Fixed by placing `Checkpoint_2_Corridor` and `Checkpoint_3_MidStairs` in
   stage 1, `Checkpoint_3_Balcony` in stage 2, and `Checkpoint_2_Canteen` and `Checkpoint_5_Tower`
   in stage 3.
4. *`RisingWater` needed a respawn hook.* `PlayerController.Respawn()` now calls
   `GameManager.NotifyRespawned()`, which resets the flood. Without it you respawn under nine
   metres of water and stage 3 is unwinnable.
5. *Two compile errors, found the moment Unity was first opened.* The project came up on the
   "Enter Safe Mode?" dialog. `Signpost.cs` assigned `sortingOrder` through a `TMP_Text`-typed
   field, but that property is declared on the concrete `TextMeshPro` class only (CS1061); the
   field is now typed `TextMeshPro`. `StageBannerUI.cs` asked for `UnityEngine.UI.CanvasGroup`
   twice, but `CanvasGroup` lives in `UnityEngine` — only `CanvasScaler` and `Image` are in
   `UnityEngine.UI` (CS0234). Both fixed; the other 28 scripts were read line by line and are
   clean. This is the cost of generating a project outside the editor, and it is why the Unity
   gate exists.
6. *Editor hard-crash on Play — an editor-state bug, not a game bug.* With the compile errors
   cleared, Level1 opened and rendered fine, then pressing Play killed the editor outright with
   `Could not allocate memory: System out of memory! Trying to allocate: 18446744059507624804B …
   MemoryLabel: TempOverflow`. That figure is 2⁶⁴ − 14.2e9, i.e. a **negative 13.2 GB** request
   that underflowed — and the same log records only 203 MB in `ALLOC_DEFAULT`, about 250 MB across
   all allocators, so the machine was nowhere near out of memory. The stack trace resolves it:
   `PlayerLoopController::EnterPlayMode` → `EditorSceneManager::RestoreSceneBackups` →
   `ImportOutOfDateAssets` → `MonoManager::FinalizeReload` →
   `SerializableManagedRefsUtilities::RestoreBackups` →
   `Transfer_Blittable_ArrayField<StreamedBinaryRead, Vector3f>` → the bad malloc. Unity was
   restoring managed state across a domain reload it had been forced to run *in the middle of*
   entering Play mode, against a serialized-reference blob written under a different assembly
   layout by the earlier Safe-Mode session; the array length came back as garbage. Nothing in the
   project can cause this: no script declares a `Vector3[]` or `List<Vector3>` field, none uses
   `[SerializeReference]`, memory/time/physics settings are all stock, and the crash lands before a
   single `Awake()` runs. Three conditions had to coincide — a session that did not close cleanly,
   answering **Yes** to "Recovering Scene Backups", and pressing Play while a recompile was still
   in flight. The standing rules are now in `UNITY_GATE.md` §7: always answer **No** to that
   dialog, and never press Play while the spinner is turning bottom-right.

**The checkpoint warning we are keeping.** Stage 1 reports 39 units between checkpoints around
x = 133. Deliberate: the next platform is Chalong Krung Road, and a checkpoint on the road
respawns the player into moving traffic. The comment is in `Tools/stage1.py`. Do not "fix" it.

**The four step-up warnings on stage 2 are Krin's ledges**, at 56–65% of the apex. They are the
level. The verifier fails above 70% and warns above 55% precisely so that these show up in the
output and get read rather than silently passing.

**Hand-timed the set-pieces so they are frights, not walls.**

- *Flowerpot:* falls 6 u at gravity 3.4 = 0.60 s. The player covers the 3.4 u trigger distance in
  0.45 s at walk speed. It lands on your head. That is the point, and the second one has no
  warning sign, which is the joke.
- *Monitor lizard:* wakes within 9 u, chases at 7.0 against a walk of 7.5, gives up after 24 u. It
  cannot catch a player who keeps moving, and on a bike it is irrelevant — which is the first
  moment the rental justifies itself. The stage 2 copy chases at 7.2 across a 30 u arena, so it
  stays behind you for the whole crossing without ever quite arriving.
- *Krin's inert rock:* his `FakeFallingRock` had no script on it at all and never fell. Kept
  exactly that way (`triggerDistance 0`) and given a real twin at x = 33, so the one that does
  nothing is a joke rather than an oversight.

---

## History — first playtest: four fixes (28 Aug afternoon, from Level2 in Play mode)

*Kept as a record. The physics numbers in the third item were superseded that same evening when
stage 2 became Krin's level — see the top of this file. The other three still hold.*

**The background was a 1.75x zoom into one building.** `background_kosen.png` is 800x450 imported
at 32 pixels per unit, so it is already 25 x 14.06 world units — bigger than the 17.8 x 10 the
camera sees at `orthographicSize 5`. `CampusBackground` then scaled it a further 1.25x and pushed
it 3.5 u up, so the player was looking at the middle of the white central building and the
"KOSEN-KMITL" banner filled a third of the screen, squashed. The magic number is gone: the scale
is now derived from the camera with a cover fit, `k = max(viewW/spriteW, viewH/spriteH)`, and
recomputed whenever the window or the ortho size changes. Cover, not contain — contain would
letterbox and expose the clear colour at the edges. The component also self-installs per scene via
`sceneLoaded` instead of once at startup, or stages 2 and 3 would have had no background at all,
and it now loads through `Resources.Load` (a copy lives in `Assets/Resources/Sprites/`) because
`FindObjectsOfTypeAll` only sees already-loaded sprites and would have gone blank in a build.

**The vehicles drew at the wrong shape.** `SolidSprite.Get()` built its 1x1 placeholder with
`Sprite.Create`'s default Tight mesh, but `TrafficLane` and `RisingWater` both use
`SpriteDrawMode.Sliced`, which needs Full Rect. That is the "Sprite Tiling might not appear
correctly" warning on screen, and the consequence was worse than cosmetic: the renderer drew one
shape while the `BoxCollider2D` kept the correct size, so a motorbike killed you from somewhere
other than where it looked. One argument: `SpriteMeshType.FullRect`.

**The jump went too far, so no gap was ever a decision.** Measured: `jumpForce 13` against
`gravityScale 3` gave a 2.87 u apex, 0.80 s of airtime and a 4.81 u flat reach at walk speed —
over gaps that are 1–2 u wide. You cleared everything without aiming. Now `jumpForce 12` against
`gravityScale 3.4`: apex 2.16 u, airtime 0.63 s, reach 3.45 u walking and 4.71 u sprinting. Walk
dropped 6 -> 5.5 and sprint 8.5 -> 7.5. That is 28% less reach and 22% less airtime. These numbers
live in three places and must stay in sync: `PlayerController.cs` defaults,
`Tools/scene_skeleton.unity` (gravity is a Rigidbody2D property, not the script's), and the
constants at the top of `Tools/build_levels.py` that the design-rule checker measures against.
The retune tightened stage 3's towers past the safety margin, so Plaza -> Tower_L1 and the L2/L3/L4
steps went from 2 u gaps to 1 u. Stages 1 and 2 needed no geometry changes. *(All three of those
stages have since been replaced or cut.)*

**Chalong Krung Road could deal an unpassable hand.** Not bad luck — structural. Both lanes sat at
x = 104 with `laneLength 32`, so they shared one strip of road and one band of air above a single
continuous surface. A motorbike and a pickup arriving together formed a wall with no gap to time
and no island to wait on. Split into a near lane at x = 95 and a far lane at x = 113, each 14 u
long, with a **standable 4 u median between them at x = 102–106**. Each lane's vehicle spacing now
exceeds its own length (18.2 u for bikes, 16.6 u for pickups), so there is never more than one
vehicle in a lane at a time. Pickups also shrank from 3.0 x 1.5 to 2.6 x 1.1 so they are jumpable rather than only dodgeable.

*(Both lanes now live on stage 1, at x 146 and x 160, re-timed to 2.0 s / 6.5 and 2.8 s / 4.5 with
a 1.3 s offset and a standable median at x 151.5–154.5. The split-lane-plus-median principle is
unchanged; only the coordinates moved when the road became part of the walk to the building.)*

---

## Note on editing these files

Two of the source files in this repo have been silently truncated during this project by a
read-modify-write that went through a stale filesystem view: once `Tools/level_kit.py`, once this
file. The symptom is a file that ends mid-word with no error anywhere.

The rule that came out of it: **write whole files, never read-modify-write, and check the last
line afterwards.** If a file ends mid-sentence, it was truncated, and `git diff` is the fastest way
to see how much went missing.
