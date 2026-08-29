# TJ — Programmer Tasks (Late to KOSEN)
**ID:** 09 | **Role:** Programmer / Lead
**Last updated: 28 Aug 2026 (evening) | Deadline: 31 Aug 2026 (hard, no extension) | 3 days left**

## Status: the game is two stages, and stage 2 is Krin's. Code is done and verified on paper. Tonight's build has never been opened in Unity. That is the only thing standing between here and a submission.

---

## READ THIS FIRST — the Unity gate

Everything below is bookkeeping. **This is the actual next action:**

1. Open the project in Unity **6000.4.11f1**.
2. Open `Assets/Scenes/Level1.unity`.
3. Press Play.

Both scenes, the `EditorBuildSettings.asset`, three prefabs (`MonitorLizard`, `BikeRack`, and a
regenerated `Bicycle`) and two scripts (`BikeRental.cs`, `BikeRack.cs`) were written outside the
editor and have **never been imported by Unity**. Until that import happens clean, nothing else is
worth doing. If the console is empty and the player moves, the risky part of this rewrite is over.

**The click-by-click version is in `UNITY_GATE.md` (Thai).** Follow that, not this summary — it
covers the Safe Mode dialog, reading the Console, checking each new prefab for
`Missing (Mono Script)`, Build Settings order, and what each stage has to show in the first two
seconds of Play.

**An earlier Unity open already found two compile errors, and they are fixed** — `Signpost.cs` set
`sortingOrder` through a `TMP_Text` field (that property is on the concrete `TextMeshPro` class
only), and `StageBannerUI.cs` asked for `UnityEngine.UI.CanvasGroup` twice when `CanvasGroup` is in
`UnityEngine`. If Unity still opens into Safe Mode, the errors are something new: copy the full
`Assets/Scripts/X.cs(line,col): error CSxxxx:` lines out of the Console rather than guessing.

**Two things that must not happen before then.**

- **Do not edit anything in `Assets/Scripts` or `Tools/` through the Linux sandbox.** The mount
  serves a **stale, truncated prefix** of any file last written from the Windows side, with no
  error of any kind. Verified today: `CampusBackground.cs` reads 59 lines through the mount and
  147 on Windows; `PlayerController.cs` reads 189 lines through the mount and 216 on Windows;
  `HudUI.cs` comes back NUL-padded. Anything that reads through the sandbox and writes back
  **silently truncates the real file**. It has already destroyed `Tools/level_kit.py` once and
  `PROGRESS.md` once. Read and edit these files in the editor or with a normal Windows tool.
- **Do not commit yet.** If Unity's reimport changes anything — and it usually touches meta files —
  you want that in the same commit as the generated scenes, not chasing them afterwards.

---

## What changed on 28 Aug (evening)

Three stages became two, and the second one is Krin's.

The team voted to keep the level on Krin's `Lv1-Create` branch because it is hard and it is fun.
It is now stage 2, the inside-the-building stage, and it ships at his coordinates with his sign
copy. Stage 1 is new: dorm room to the gate of Building 12. Stage 3 is cut — three days is not
enough to build a third act as good as his, and a weak third stage drags the whole grade down.

| # | Scene | Title | Timer | What it is |
|---|---|---|---|---|
| 1 | `Level1.unity` | **LATE** — your room to the gate of Building 12 | 80 s | new. Dorm, stairs, the soi, Chalong Krung Road, the forecourt |
| 2 | `Level2.unity` | **INSIDE** — the building, and it is not done with you | 65 s | **Krin's**, ported and repaired |

**Lives are per stage.** Three lives, and running out restarts *that stage only*, with three again.

- `GameManager` — **stage scope.** Timer, lives, checkpoint, death count, stage score. Destroyed
  and rebuilt on every scene load, which is why all of those reset. Not a side effect, the design.
- `GameSession` — **run scope.** `DontDestroyOnLoad`. Per-stage results, totals, and scene loading.

There is no third scope. If you find yourself wanting one, you probably want `GameSession`.

### Three mechanical changes you have to know about

**Sprint is gone.** The old sprint speed is now the only speed: `moveSpeed 7.5`. Krin's opening gap
is 5.00 u, and a game where exactly one jump requires a modifier key is not a design, it is a
stamina bar built to paper over a single gap. The whole system came out.

**The bicycle is an Anywheel rental, not a power-up.** You pick it up and you ride until you find a
rack. You cannot dismount on demand. Riding is faster (8.11 u reach) and jumps *lower* (2.17 u
apex), so a step-up that is nothing on foot can strand a rider. Stage 1 has three racks and **the
middle one is painted on.** `PlayerController.MountBike()` / `ParkBike()`, driven by
`BikeRental.cs` and `BikeRack.cs`.

**The soi dog is a monitor lizard.** Same `ChaserHazard`, same numbers, better joke. One on each
stage — stage 2's replaces Krin's death beam.

---

## The form is still the spec

| Form says | Where it lives | Status |
|---|---|---|
| 2D side-scrolling platformer with hidden troll traps | 10 hazard types, 102 placed objects across two scenes | done |
| Jump and dodge mechanics | `PlayerController` — coyote time, jump buffer, variable height | done |
| Lives system, lose a life per trap | `GameManager.Lives`, 3 **per stage**, respawn at checkpoint | done |
| Score from speed + traps survived | `GameManager.Score`, summed by `GameSession.TotalScore` | done |
| Left/Right or A/D — move | `Horizontal` axis | done |
| Space or Up Arrow — jump | `Jump` axis, altPositive `up` | done |
| Shift — sprint | **removed** — one speed now, and it is the old sprint speed | cut, deliberately |
| Esc — Pause / Resume | `PauseMenu.cs` | done |
| Win: reach school in time **with a life left** | `GameManager.WinGame()` asserts `Lives > 0` | done |
| Lose: lives run out **or** timer hits zero | `LoseGame("lives")` / `LoseGame("time")`, distinct screens | done |
| 8-bit pixel art, chiptune | Bun — placeholders in place, import settings documented | Bun |
| Optional: bell timer countdown | 80 / 65 s + "THE BELL RANG" | done |
| Optional: death counter | `DeathCounterUI`, per stage and per run | done |
| Optional: bicycle | **reworked** into the Anywheel rental with real and fake racks | done |
| Optional: **multiple levels** | 2 stages, run-scope score | done |
| Optional: SFX / chiptune BGM | Bun, once layouts are frozen | Bun |
| Optional: school van shortcut | became the SHORTCUT teleporter on stage 1 | cut |

The form asks for "more than one" optional feature. Three are shipped and a fourth is Bun's.
Sprint was dropped for a design reason, and the reason is written down in `README.md` under
*Tuned values* so it reads as a decision rather than a gap.

---

## Done — 28 Aug evening round

- [x] Physics retuned around Krin's level: `moveSpeed 7.5`, `jumpForce 13.5`, `gravityScale 2.6`,
      `fallMultiplier 1.8`. Apex 3.573 u, flat reach 6.93 u. His 5.00 u opening gap is 72% of it
- [x] Sprint and stamina deleted from `PlayerController`, `HudUI` and the input docs
- [x] `BikeRental.cs` + `BikeRack.cs` — mount on pickup, dismount only at a rack, `isReal` flag on
      the rack so a fake one costs a detour and never a softlock
- [x] `ChaserHazard` retheme to `MonitorLizard`, plus a second instance ported into Krin's arena
      where his death beam was
- [x] `build_levels.py` split into `level_kit.py` (physics, rules, constructors), `stage1.py` and
      `stage2.py`. Each file is now small enough to read in one sitting
- [x] **Verifier rule 9 — bike safety.** From the first bicycle to the goal, every route edge is
      re-walked against riding physics (gap ≤ 6.08 u, step-up ≤ **1.52 u**) and the build fails if
      a rider could be stranded. This is what makes the fake rack safe to ship
- [x] Six repairs to Krin's committed scene, all documented at the top of `stage2.py` and in
      `Krin_tasks.md`. The big one: **his goal had no floor under it**
- [x] `Level3.unity` and its `.meta` deleted; `EditorBuildSettings.asset` rewritten to two scenes
- [x] `GameSession.LevelCount = 2`, scene names, titles and subtitles updated
- [x] Both verifiers clean: `build_levels.py --check` → 0 fails, 5 intended warnings;
      `verify_scenes.py` → 0 problems
- [x] Docs rewritten: `PROGRESS.md`, `README.md`, `HANDOFF.md`, `Krin_tasks.md`, this file

## Carried over (still true, do not regress)
- [x] HUD moved clear of the scene-authored `TimerText` at (30,−30)
- [x] No slot narrower than 1 u between same-height platforms — the player collider is 0.5 u wide
      and wedges. The generator refuses to write one
- [x] Zero-friction `PhysicsMaterial2D` assigned in `PlayerController.Awake`
- [x] `CampusBackground` hooks `SceneManager.sceneLoaded`, not just `RuntimeInitializeOnLoadMethod`
- [x] `SolidSprite` uses `SpriteMeshType.FullRect` so sliced vehicles draw at their collider size
- [x] Teleporters are one-shot per stage load — their exits are behind their entrances

---

## Next — in order

- [ ] **Open `Assets/Scenes/Level1.unity` and press Play.** THIS IS THE GATE.
- [ ] Open `Level2.unity` too and confirm it loads with an empty console. A scene can be
      structurally valid and still surprise you on import.
- [ ] `File → Build Settings` — confirm **two** scenes, both enabled, `Level1` at index 0, and that
      `Level3` is not lurking in the list.
- [ ] Check the three new prefabs in the Inspector for `Missing (Mono Script)`: `MonitorLizard`,
      `BikeRack`, `Bicycle`.
- [ ] Play both end to end and confirm by hand:

**Movement and input (either stage)**
- [ ] One speed, and it feels like the old sprint. Shift does nothing and no stamina bar appears
- [ ] Space **and** Up Arrow both jump
- [ ] Esc pauses, Esc unpauses, the timer actually stops while paused
- [ ] Q quits from the pause menu

**The bike — new, test this hardest**
- [ ] Riding starts automatically on pickup at stage 1 x 69 and cannot be cancelled
- [ ] Riding is visibly faster and the jump is visibly shorter
- [ ] Rack 1 (x 90) parks you. Rack 3 (x 169) parks you
- [ ] **Rack 2 (x 136) does not park you** and the game says so rather than just ignoring the input
- [ ] You can still finish stage 1 while riding the whole way from x 136 to the goal — this is what
      verifier rule 9 asserts, and a mismatch between the rule and the game is the worst bug class
      in the project
- [ ] Dying while riding does the right thing on respawn (still riding, or parked — either, but the
      same every time)

**Stage flow**
- [ ] Stage banner shows the right title on each scene load, not just the first
- [ ] Reaching the stage 1 goal shows `STAGE CLEAR`, not `YOU MADE IT!`
- [ ] Space on `STAGE CLEAR` loads stage 2, timer at 65, lives back to 3
- [ ] Clearing stage 2 shows `YOU MADE IT!` with **run totals**, not just stage 2's numbers
- [ ] `R` on a mid-run failure retries **that stage**; `R` on the final screen restarts the run
- [ ] Dying three times shows `OUT OF LIVES`; running the clock out shows `THE BELL RANG`
- [ ] Background and HUD are present in stage 2, not only stage 1
      *(this is the `CampusBackground` fix — if it regresses, it regresses here)*

**Hazards**
- [ ] Hidden traps are invisible until they kill you, then stay visible on the retry
- [ ] Fake platforms wobble, drop, and are gone on the retry
- [ ] Spikes rise with enough warning to react at 7.5
- [ ] Both `FakeGoal`s say `OUT OF ORDER`, cost seconds, and do not end the stage
- [ ] The monitor lizard wakes, chases, and gives up — survivable at full speed on both stages
- [ ] Stage 1's first flowerpot is warned by a sign and the second one is not
- [ ] Stage 1's traffic kills you and the median at x 151.5–154.5 is genuinely standable
- [ ] Stage 1's SHORTCUT teleporter fires once, sends you back to x 84, moves your checkpoint, and
      does **not** fire again
- [ ] Stage 2's pit cannot be climbed out of, and both teleporters at the bottom work
- [ ] Krin's inert rock at x 47 does nothing, and the real one at x 33 falls

- [ ] If a stage is unwinnable for a first-timer, raise `startingLives` or `startingTime` on that
      stage's `GameManager`. One field each, no code change.
- [ ] Commit and push once the gate passes. Nothing from this round is committed yet.
- [ ] Tell Krin: play both, **check the six repairs to his level**, and send balance notes as
      data-table positions rather than Inspector edits.
- [ ] Tell Bun: layouts are frozen, so art and audio can start. Two backgrounds, SFX, BGM.

---

## Day-by-day from here

**28 Aug (tonight)** — Unity gate, then the checklist above. Then get someone who has never played
it to run both stages while you watch. Watch where they die and whether they laugh. A troll
platformer lives or dies on that one reaction.

**29 Aug** — Bug fixing only, no new features. First standalone build. Confirm the stage transition
works in a build, not just in the editor — `SceneManager.LoadScene` behaves differently when a
scene is missing from Build Settings, and the failure is silent in the editor.

**30 Aug** — Test the build, fix only game-breakers, screenshots from the locked game, presentation.

**31 Aug** — Final build, submission packaging.

---

## Tooling

```
python3 Tools/build_levels.py --check    # design rules only, writes nothing
python3 Tools/build_levels.py            # regenerate both scenes + Build Settings
python3 Tools/verify_scenes.py           # structural check on the written YAML
```

Run both after any data-table change. They do **not** overlap: `build_levels.py` checks whether the
level is *playable*, `verify_scenes.py` checks whether the file is a *valid Unity scene*. A level
can pass one and fail the other.

Geometry lives in `Tools/stage1.py` and `Tools/stage2.py`; the physics constants, design rules and
placement constructors live in `Tools/level_kit.py`. Changing those and regenerating is the
supported path; editing a scene in Unity works until the next regeneration silently reverts it.

`Tools/build_level.py` (singular) is the old single-level generator and is superseded. It still
references geometry that no longer exists — do not run it.

**Never open a `Tools/*.py` file with a Windows editor and then edit it from the sandbox, or the
reverse.** Pick one side per file and stay there. See the truncation warning at the top.

---

## Shared architecture contract

- Tag `Player` / Layer `Ground` (index 3). `PlatformFake` is also on layer 3, deliberately.
- Folders: `Assets/Scripts`, `Assets/Prefabs`, `Assets/Scenes`, `Assets/Art`, `Assets/Audio`
- Never rename: `GameSession`, `GameManager`, `PlayerController`, `HazardTrigger`, `TrapTrigger`,
  `HiddenTrap`, `FakePlatform`, `SpikeTrap`, `ChaserHazard`, `FallingObject`, `TrafficLane`,
  `Vehicle`, `RisingWater`, `Teleporter`, `FakeGoal`, `Signpost`, `SolidSprite`, `BikeRental`,
  `BikeRack`, `Checkpoint`, `GoalTrigger`, `CameraFollow`, `CampusBackground`, `TimerUI`,
  `DeathCounterUI`, `HudUI`, `PauseMenu`, `ResultUI`, `StageBannerUI`, `PlayerAnimator`
- `BicyclePickup.cs` is **deleted**. `BikeRental` + `BikeRack` replace it.
- `RisingWater.cs` and the `Floodwater` prefab are unused now that stage 3 is cut. They compile,
  they cost nothing, and the generator still has a rule for them. Leave them.
- `AppControls.cs` is dead, superseded by `PauseMenu.cs`. Leave it — deleting it churns meta files
  three days before submission for no gain.

**Public API**

```
GameSession.Instance
  .LoadLevel(n)  .StartNewRun()  .RecordClear(level, score, deaths, timeUsed)
  .RecordFailedAttempt(level, deaths)  .ResetRun()
  .TotalScore  .TotalDeaths  .TotalTimeUsed  .LevelsCleared  .FurthestLevel
  .ScoreFor(n)  .DeathsFor(n)  .TimeUsedFor(n)  .ClearedLevel(n)
GameSession (static)
  .LevelCount (= 2)  .SceneNames  .Titles  .Subtitles
  .IsFinalLevel(n)  .TitleFor(n)  .SubtitleFor(n)  .SceneNameFor(n)

GameManager.Instance
  .PlayerDied()   -> true if a life remains
  .WinGame()  .LoseGame(reason)  .NextLevel()  .RestartLevel()  .RestartRun()  .QuitGame()
  .SetCheckpoint(pos)  .GetCheckpoint()  .NotifyRespawned()  .PlayerRespawned (event)
  .RegisterTrap(worldX)  .SpendTime(seconds)  .TogglePause()  .SetPaused(bool)
  .TimeRemaining  .StartingTime  .TimeUsed  .Lives  .StartingLives  .Score
  .TrapsSurvived  .TrapTotal  .DeathCount  .IsGameOver  .IsPaused  .DidWin  .LoseReason
  .LevelIndex  .LevelTitle  .LevelSubtitle  .IsFinalLevel

PlayerController
  .Die()  .Respawn()  .MountBike()  .ParkBike()
  .IsRiding
```

`Stamina01`, `IsSprinting`, `HasBike` and `BikeSecondsLeft` are gone. `IsRiding` replaces the last
two and there is no timer on it — the ride ends at a rack or not at all.

---

## Level design constraints (enforced by the generator, tell Krin anyway)

Jump apex **3.573 u** walking, **2.174 u** riding. Real horizontal reach: **6.93 u** flat walking,
**8.11 u** flat riding — shorter than a symmetric estimate because `fallMultiplier 1.8` makes the
fall faster than the rise.

- Gaps ≤ **75%** of the reach for that step-up: **5.20 u** walking, **6.08 u** riding.
- Step-ups ≤ **70%** of apex: **2.50 u** walking, **1.52 u** riding. Warns above 55%.
- **Never a slot narrower than 1 u** between two same-height platforms. The player collider is
  0.5 u wide, drops in, does not die, and cannot get out. This shipped once already.
- Nothing within **1.2 u** of a checkpoint.
- A fake platform must span a gap that is already clearable without it.
- Pure-walk time ≤ **75%** of the stage timer. Currently 34% and 20%.
- **Every route edge after the first bicycle must also pass the riding budget.**

The riding rule is the one that will surprise you: the bike is horizontally better and vertically
worse, so a 2 u step that is trivial on foot is a hard stop on a bike, and a bike can only be
parked at a rack. That asymmetry is the whole gimmick, and rule 9 is what keeps it from becoming a
softlock.

Full troll placement rules are in `HANDOFF.md`.

---

## Cut list (your call, in this order)

1. Instructions screen (never started)
2. Character animation → static sprite, flipped by direction (flip is already coded)
3. BGM → keep SFX; the death and stage-clear sounds carry more than music does
4. One of the two backgrounds → flat colour. Not both
5. The bike system → delete the bicycle and the three racks from `stage1.py`; nothing else depends
   on it. This costs the gimmick Bun asked for, so it is low on the list on purpose
6. Number of **visible** traps → reduce those first, keep the troll ones

**Never cut:** movement/jump, timer, lives, score, troll traps, win/lose conditions. Those six are
in the form that went to the lecturer.

And do **not** cut back to a single level — "multiple levels" is a claimed optional feature. Two
stages is the floor, not the target.
