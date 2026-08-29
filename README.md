# Late to KOSEN

A 2D side-scrolling **troll platformer** in two stages. You have overslept, roll call is in
eighteen minutes, and every single thing between your bed and the exam room is against you.

**Course:** Programming 7 — KOSEN-KMITL
**Team:** sixseven
**Engine:** Unity 6000.4.11f1, 2D (Built-In Render Pipeline)
**Submission deadline:** 31 August 2026

---

## Team

| Name | ID | Role | Responsibility |
|---|---|---|---|
| TJ (Jiranath W.) | 09 | Programmer / Lead | Gameplay code, scene generation, level scripting, build |
| Bun | 17 | Art / UI | 8-bit sprite art, UI art pass |
| Krin | 21 | Level Design / PM | Playtest, balance, trap placement review, schedule |

---

## The two stages

| # | Scene | Title | Where | Timer | What it is |
|---|---|---|---|---|---|
| 1 | `Level1.unity` | **LATE** | your room → the gate of Building 12 | 80 s | **The walk.** Dorm room, corridor, four flights, lobby, Soi 12, Chalong Krung Road, forecourt. 209 units, and it lies to you for about 190 of them. |
| 2 | `Level2.unity` | **INSIDE** | Krin's level | 65 s | **The building.** A short climb, then a one-way drop into a 30-unit arena, then the far wall. A third of stage 1's length and considerably more than a third of its difficulty. |

**Stage 2 is Krin's level, and it is his geometry to two decimal places.** The team read what he
built on `Lv1-Create`, agreed it was harder and better than what the generator had produced, and
voted to ship it rather than replace it. His sign copy is reproduced word for word. Six things
were repaired rather than redesigned — the biggest being that **his goal had no floor under it** —
and all six are listed at the top of `Tools/stage2.py` so he can put back anything he disagrees
with.

**Stage 1 exists to get you to stage 2, and it was built to match it rather than to warm up for
it.** Each of Krin's three signature moves is answered: a platform that is not a platform, a
reward that is a punishment, and a hazard placed *before* the sign that warns about it. The first
twenty units are honest, so that the other 190 have something to be a lie about.

**Why two and not three.** There was a third stage — a flooding campus — and it was cut on the
evening of 28 Aug. Once Krin's level became stage 2, stage 1 had to become the walk that reaches
it, and stage 3 had nothing left to be. Three days is not enough to invent a third act as good as
the two we have. `RisingWater` and the `Floodwater` prefab remain in the repo, working and
unused.

---

## Lives, and why they reset

**Three lives per stage.** Running out restarts *that stage only*, from the beginning, with
three lives again. You never get sent back to your room because a boulder caught you on the
third floor.

This is the thing that was wrong with the old single-level build: 3 lives across a 156-unit
level meant a checkpoint gave you position back but not survivability, so a run that went badly
early was already dead and you had to know it. Splitting the game into stages fixes it without
making the game easier — each stage is still a real fail state, it just costs you 65–80 seconds
instead of the whole morning.

The code mirrors this exactly:

- **`GameManager`** is **per stage.** It owns the timer, the lives, the checkpoint, the death
  count and the stage score. It is destroyed and rebuilt on every scene load, which is *why*
  all three of those reset when you enter a new stage — that is not a side effect, it is the
  design.
- **`GameSession`** is **per run.** It is `DontDestroyOnLoad`, it survives every scene load, and
  it holds the per-stage results, the totals and the "which stage are we on" pointer.

If you want something to reset between stages, put it on `GameManager`. If you want it to
survive, put it on `GameSession`. There is no third option and that is on purpose.

---

## How to run it

**From the Unity Editor**

1. Open the project folder in Unity **6000.4.11f1**.
2. Open `Assets/Scenes/Level1.unity`.
3. Press Play. Clearing stage 1 loads stage 2 by itself.

There is nothing to wire up in the Inspector. The HUD, stage banner, pause menu and result
screen all build themselves at runtime, so no scene reference exists for anyone to unassign.

**From a build**

`File → Build Settings → Windows/Mac/Linux → Build`. All three scenes are already enabled in
Build Settings in the right order, with `Level1` at index 0, so a build boots into stage 1.
The build is windowed **1280x720** and resizable — not exclusive fullscreen, so it behaves on
a projector.

---

## Controls

| Input | Action |
|---|---|
| `A` / `D` or `Left` / `Right` | Move |
| `Space` or `Up Arrow` | Jump |
| — | There is no sprint. It was removed on 28 Aug; see *Tuned values*. |
| `Esc` | Pause / Resume |
| `Space` or `Enter` | **Next stage** — on the STAGE CLEAR screen only |
| `R` | Retry (the current stage; on the final screen, the whole run) |
| `Q` | Quit (from the pause menu or a result screen) |

`Space` is bound to "continue" **only** on a mid-run stage clear. Binding it everywhere would
let a player mashing jump at the instant of death skip past their own game-over screen without
reading it.

Jumping is forgiving on purpose: **coyote time** (0.12 s) lets you jump just after walking off
an edge, **jump buffering** (0.12 s) lets you press Jump just before you land, and jump height
is variable — a tap is short, a hold is full.

---

## Win and lose

- **Stage clear** — reach the stage goal before the bell with at least one life left. Screen
  reads `STAGE CLEAR` and Space continues.
- **Run clear** — do that three times. Screen reads `YOU MADE IT!` with the run totals.
- **Lose (lives)** — the traps kill you three times in one stage. `OUT OF LIVES`. `R` retries
  that stage.
- **Lose (time)** — that stage's countdown reaches zero. `THE BELL RANG`. `R` retries that stage.

The two lose states are separate screens so the player always knows *which* thing beat them.

## Scoring

```
Stage score = (seconds remaining x 10) + (hazards survived x 100) - (deaths x 50)
Run score   = the three stage scores added up
```

"Hazards survived" counts every hazard the player has moved safely *past*, measured by the
furthest-right position the player has ever reached. Dying on a trap therefore never scores it,
and walking back and forth can never score it twice.

---

## The troll design

A troll platformer is only a troll platformer if it violates an assumption the player is
actively making. Every hazard in the game exists to break one specific assumption:

**"The floor is floor."** `TrapHidden` is invisible until it kills you, and it is placed exactly
where the ground looks safest — the landing after a visible trap, the bare gap between two
obvious ones, the rest platform. Once one kills you it stays permanently visible, so the retry
is fair. You get trolled once per trap, never forever. `PlatformFake` is the same sprite, same
layer and same solid collider as real ground, then it wobbles and drops half a second after you
land — and it is always placed over a gap the player can already clear unaided, so it is a
*temptation*, never a *requirement*.

**"I can see the danger."** `TrapSpike` is buried under the surface behind the ground sprite and
shoots up when you get close. Unlike a hidden trap it gives you a few frames, which makes it a
reflex test rather than a memory test.

**"Signs tell the truth."** `Signpost` mostly does. `FakeGoal` is the payoff: it looks exactly
like the school gate, the sign points at it, and touching it costs you seconds off the clock and
tells you `OUT OF ORDER`. There are two of them: the lift in the dorm lobby on stage 1, and
Building 9 in the forecourt, thirty units from the real door. Both are out of order. That is
the joke, told twice.

**"The level is the level."** `TrafficLane`, `ChaserHazard` and `FallingObject` move without
you — the motorbikes on Chalong Krung do not wait at the kerb, and the monitor lizard starts
walking the moment you enter its nine units. `Teleporter` takes the "SHORTCUT" sign at its word
and puts you thirty-four units *behind* where you were, at a checkpoint it helpfully moves for
you so you cannot undo it.

The rule the whole game is built on: **the player should laugh, not rage-quit.** Every death is
recoverable at a checkpoint a few seconds away, no troll is ever the only path forward, and the
flowerpot gag on the shophouse row is warned about the first time and not the second — which is
the entire joke, in one object.

---

## Level contents

102 placed objects across two scenes, every one a real Unity **PrefabInstance** rather than a
plain GameObject. That is what makes the art hand-off cheap: dropping a sprite onto the `Ground`
prefab updates all 27 platforms at once, with no scene editing and no merge conflict.

| | Level1 — LATE | Level2 — INSIDE |
|---|---|---|
| x range | −10 → 199 | −31 → 72 |
| Timer | 80 s | 65 s |
| Pure-walk time | 28 s (35%) | 14 s (21%) |
| Ground platforms | 16 | 11 |
| Visible traps | 4 | 5 |
| Hidden traps | 5 | 5 |
| Spike traps | 1 | 2 |
| Fake platforms | 1 | 1 |
| Fake goals | 2 | — |
| Signposts | 10 | 9 |
| Checkpoints | 9 | 4 |
| Teleporters | 1 | 2 |
| Stage-specific | 1 bicycle, 3 bike racks, 1 lizard, 2 flowerpots, 2 traffic lanes | 1 lizard, 2 boulders |
| **Total** | **59** | **43** |

**Design constraints (derived, not guessed).** With `jumpForce 13.5` against `gravityScale 2.6`
the jump apex is **3.573 u**. Because `fallMultiplier 1.8` makes the fall faster than the rise,
horizontal reach is shorter than a naive symmetric estimate — **6.93 u** flat, **6.48 u** onto a
1.0 u step-up, **5.93 u** onto a 2.0 u step-up, at walk speed.

Every gap is inside 75% of the applicable reach and every step-up is inside 70% of the apex. That
second ceiling is higher than it looks comfortable, and it is not a preference: Krin's climb out
of the arena is a 2.32 u rise, which is 65% of our apex. Anything over 55% still warns.

**Riding is checked separately.** A bike is faster (8.11 u flat reach) and jumps *lower* (2.174 u
apex), and a ride can only be ended at a rack. So the generator re-walks the whole route from the
first bicycle to the goal against riding physics and fails the build if a rider could get stuck.
All of it is recomputed from the physics constants on every run.

---

## Architecture

31 scripts in `Assets/Scripts`, 16 prefabs in `Assets/Prefabs`.

**Run and stage.** `GameSession` (run-scope, `DontDestroyOnLoad`) and `GameManager` (stage-scope,
singleton, rebuilt per scene) as described above. `PlayerController` owns movement, jumping, the
bike state and the ground check (`Physics2D.OverlapCircle` against the `Ground` layer).
`CameraFollow` tracks the player.

**Hazards.** `TrapTrigger`, `HiddenTrap`, `FakePlatform`, `SpikeTrap`, `ChaserHazard` (the monitor
lizard), `FallingObject` (flowerpots and Krin's boulders), `TrafficLane` + `Vehicle` (the road),
`RisingWater` (written, currently unused), `Teleporter` and `FakeGoal`. The bike is
`BikeRental` + `BikeRack`, and it is the only hazard-adjacent system that is not a hazard: you can
finish either stage without ever touching it. They all share `HazardTrigger`, they all self-trigger on player
proximity, and none of them holds a scene reference to anything else — which is exactly why the
scene generator only ever has to emit self-contained prefab instances.

**Death and respawn.** A hazard calls `GameManager.PlayerDied()`, which returns whether a life
remains, and `PlayerController.Respawn()` puts the player at the last `Checkpoint` and then
fires `GameManager.NotifyRespawned()`. Stateful hazards subscribe to that and undo themselves.
`RisingWater` is the reason it exists: respawning at a checkpoint that is already nine metres
underwater is not a level, it is a cutscene about drowning.

**UI without scene wiring.** `HudUI`, `PauseMenu`, `ResultUI`, `StageBannerUI` and
`CampusBackground` each bootstrap via `[RuntimeInitializeOnLoadMethod]` and, where they need to
run per-scene rather than once, additionally hook `SceneManager.sceneLoaded` — that hook matters,
because `RuntimeInitializeOnLoadMethod` fires **once at game start, not once per scene load**, so
without it stages 2 and 3 come up with no background and no banner. Nothing about them exists in
the scene file, so there is no reference to unassign and no merge conflict to cause. `TimerUI`
and `DeathCounterUI` drive the scene-authored HUD text.

**Repeatable level generation.** `Tools/build_levels.py` regenerates all three scenes *and*
`EditorBuildSettings.asset` from a data table of coordinates in one command, writing real Unity
PrefabInstance YAML and re-running eight design checks. The level layout is therefore reviewable
as a diff rather than as a scene file.

```
python3 Tools/build_levels.py --check    # verify the data table, write nothing
python3 Tools/build_levels.py            # regenerate all three scenes
python3 Tools/verify_scenes.py           # structural check on the written YAML
```

`build_levels.py` checks *design* (reach, step-ups, wedge slots, hazards over ground, hazard
distance from checkpoints, fake platforms over already-clearable gaps, checkpoint spacing, walk
time against the timer, flood ceiling). `verify_scenes.py` checks *structure* — the things that
make Unity refuse to open a scene, or open it silently wrong: duplicate YAML anchors, dangling
fileIDs, unresolvable prefab GUIDs, missing script `.meta` files, scene roots that do not exist,
and Build Settings order. Run both. They do not overlap.

**Git safety.** `.gitattributes` marks `.unity`, `.prefab` and `.asset` as `-text merge=binary`,
so git can never line-merge a scene into a silently corrupt state.

---

## Features against the design form

| Form requirement | Implementation | Status |
|---|---|---|
| 2D side-scrolling platformer with hidden troll traps | 9 hazard types, 31 instances across two stages | Done |
| Jump and dodge mechanics | `PlayerController` — coyote time, jump buffer, variable height | Done |
| Lives system, one life per trap | `GameManager.Lives`, 3 per stage, checkpoint respawn | Done |
| Score from speed + traps survived | `GameManager.Score`, summed by `GameSession` | Done |
| Left/Right or A/D — move | `Horizontal` axis | Done |
| Space or Up Arrow — jump | `Jump` axis, `altPositive: up` | Done |
| Shift — sprint | **Removed.** One speed now, and it is the old sprint speed | Cut, deliberately |
| Esc — Pause / Resume | `PauseMenu` | Done |
| Win: reach school in time with a life left | `GameManager.WinGame()` asserts `Lives > 0` | Done |
| Lose: lives run out **or** timer expires | `LoseGame("lives")` / `LoseGame("time")` | Done |
| 8-bit pixel art, chiptune | Placeholder colours in place; art pending | **Bun** |
| *Optional:* bell timer countdown | Per-stage countdown + `THE BELL RANG` screen | Done |
| *Optional:* death counter | `DeathCounterUI`, per stage and per run | Done |
| *Optional:* bicycle power-up | `BikeRental` + `BikeRack` — an Anywheel rental with two real racks and one fake | Done |
| *Optional:* multiple levels | Two stages with a run-scope score | Done |
| *Optional:* sound effects & chiptune BGM | Not started | Cut |
| *Optional:* school van shortcut | Superseded by the Sai 1013 bus-stop fake goal | Cut |

The form asks for "more than one" optional feature. Three are shipped. Sprint was dropped on
purpose rather than missed: it existed only to make one gap crossable, which makes it a hidden
requirement rather than a choice. If the marker wants it back, `PlayerController` is the only
file that changes.

---

## Tuned values

Arrived at by playtest, not by default. Worth knowing before changing anything.

| Value | Setting | Why |
|---|---|---|
| `moveSpeed` | 7.5 | The old sprint speed, now the only speed. Krin's 5.00 u opening gap needs it |
| `jumpForce` | 13.5 | Krin's climb out of the arena is a 2.32 u step; 12 could not make it |
| `gravityScale` | 2.6 | Weight, without losing the reach the 13.5 buys |
| `fallMultiplier` | 1.8 | Falls faster than it rises; standard platformer feel |
| `bikeSpeedMultiplier` | 1.5 | 11.25 u/s riding — the reason anyone takes the bike |
| `bikeJumpMultiplier` | 0.78 | And the reason taking it is a decision. A 2.17 u apex, so tall steps become walls |
| `coyoteTime` | 0.12 s | Forgives leaving the edge |
| `jumpBufferTime` | 0.12 s | Forgives pressing early |
| `startingTime` | 80 / 65 s | Pure-walk time is 35% / 21% — the rest is for dying, and you will |
| `startingLives` | 3, per stage | Raise on that stage's `GameManager` if playtesters stall |

`sprintSpeed` and `maxStamina` are gone. A sprint that exists to make exactly one gap crossable is
a requirement the game never tells you about, and deleting it removed the stamina bar, the lockout
and three serialized fields per scene.

All of these are serialized explicitly on the `GameManager` and `Player` objects in each scene,
so what you see in the Inspector is what actually runs. Changing a timer in the Inspector is
fine; changing level *geometry* in the Inspector will be overwritten the next time anyone runs
`build_levels.py`, so geometry changes belong in the data table.

---

## Known limitations

- **No final art or audio.** The game runs on placeholder solid colours. Prefabs are structured
  so art drops in without touching a scene, but as of this writing the 8-bit sprite pass and the
  chiptune track have not been delivered. SFX and BGM are formally cut.
- **No main menu and no level select.** The build boots straight into stage 1. Progress is not
  saved between sessions — a run is a run.
- **English text only.** The bundled TextMeshPro font (LiberationSans SDF) has no Thai glyphs,
  so Thai strings render as empty boxes. Every in-game string is ASCII by design. Adding Thai
  means importing a Thai TTF as a TMP Font Asset first.
- **No character animation.** The player is a static sprite, flipped by facing direction.
- **`Assets/Scripts/AppControls.cs` is dead**, superseded by `PauseMenu.cs`. Left in place to
  avoid meta-file churn before submission.
- **One intentional generator warning.** Level2 reports 40 units between checkpoints around
  x = 84. That gap is deliberate: the next platform is Chalong Krung Road, and a checkpoint on
  the road respawns the player into moving traffic. Do not "fix" it.

---

## Repository

`https://github.com/jiranathw/late-to-kosen` (private)

Also in the repository root: `HANDOFF.md` (team handoff, Thai, includes the troll-trap placement
rules), `PROGRESS.md`, `TJ_tasks.md`, `Bun_tasks.md`, `Krin_tasks.md`.
