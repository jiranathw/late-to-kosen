# Late to KOSEN

A 2D side-scrolling **troll platformer**. You have overslept. The bell rings in 85 seconds,
the road to school is rigged against you, and the ground itself is not on your side.

**Course:** Programming 7 — KOSEN-KMITL
**Team:** sixseven
**Engine:** Unity 6000.4.11f1, 2D (Built-In Render Pipeline)
**Submission deadline:** 31 August 2026

---

## Team

| Name | ID | Role | Responsibility |
|---|---|---|---|
| TJ (Jiranath W.) | 09 | Programmer / Lead | All gameplay code, scene assembly, level scripting, build |
| Bun | 17 | Art / UI | 8-bit sprite art, UI art pass |
| Krin | 21 | Level Design / PM | Level layout review, trap placement, schedule |

---

## How to run it

**From the Unity Editor**

1. Open the project folder in Unity **6000.4.11f1**.
2. Open `Assets/Scenes/Level1.unity`.
3. Press Play.

There is nothing to wire up in the Inspector. The HUD, pause menu and result screen build
themselves at runtime (see *Architecture* below), so the scene cannot be broken by an
accidentally unassigned reference.

**From a build**

`File → Build Settings → Windows/Mac/Linux → Build`. `Level1` is already the only enabled
scene, at index 0. The build is windowed **1280x720** and resizable — not exclusive
fullscreen, so it behaves on a projector.

---

## Controls

| Input | Action |
|---|---|
| `A` / `D` or `Left` / `Right` | Move |
| `Space` or `Up Arrow` | Jump |
| `Shift` (hold) | Sprint — 2.5 s of stamina, then it locks until you release |
| `Esc` | Pause / Resume |
| `R` | Restart (from the pause menu or the result screen) |
| `Q` | Quit (from the pause menu or the result screen) |

Jumping is forgiving on purpose: **coyote time** (0.12 s) lets you jump just after walking off
an edge, and **jump buffering** (0.12 s) lets you press Jump just before you land. Jump height
is variable — a tap is short, a hold is full height.

---

## Win and lose conditions

- **Win** — reach the school gate before the bell, with at least one life remaining.
- **Lose (lives)** — the traps kill you three times. Screen reads `OUT OF LIVES`.
- **Lose (time)** — the 85-second countdown reaches zero. Screen reads `THE BELL RANG`.

The two lose states are deliberately distinct screens so the player knows *why* they failed.

## Scoring

```
Score = (seconds remaining x 10) + (traps survived x 100) - (deaths x 50)
```

"Traps survived" counts every hazard the player has moved safely past, tracked by the
furthest-right position the player has reached, so you cannot farm it by walking back and forth.

---

## The troll design

A troll platformer is only a troll platformer if it violates an assumption the player is
actively making. Three hazard types, each attacking a different assumption:

**Visible traps (12)** — ordinary spikes. These are honest, and they exist to teach the player
what "danger" looks like so the dishonest ones have something to lie about.

**Hidden traps (5)** — completely invisible until they kill you, and placed exactly where the
ground looks safest: the landing spot right after a visible trap, the bare gap between two
visible traps, the "rest" platform. Once one kills you it stays permanently visible, so the
retry is fair. You get trolled once per trap, never forever.

**Fake platforms (3)** — identical sprite, identical layer, identical solid collider as real
ground, then they wobble and drop out of the world half a second after you land. Each one is
placed mid-air over a gap the player can already clear unaided, so a fake platform is always a
*temptation* and never a *requirement*. They destroy themselves after falling, which means the
retry forces the honest jump.

**Spike traps (3)** — buried under the surface with a sorting order behind the ground sprite,
so they are genuinely invisible at rest, and shoot upward when the player gets close. Unlike
hidden traps these give a few frames of warning, which makes them a reflex test rather than a
memory test.

The rule the whole level is built on: **the player should laugh, not rage-quit.** Every death
is recoverable at a checkpoint 1-3 seconds away, and no troll is ever the only path forward.

---

## Level

`Level1` runs from x = -7 to x = 156, with the finish line at x = 152.

| Element | Count |
|---|---|
| Ground platforms | 13 |
| Visible traps | 12 |
| Hidden traps | 5 |
| Fake platforms | 3 |
| Spike traps | 3 |
| Bicycle power-ups | 2 |
| Checkpoints | 5 |
| Goal | 1 |

Every one of the 44 placed objects is a real Unity **PrefabInstance**, not a plain GameObject.
That matters for the art hand-off: dropping a sprite onto the `Ground` prefab updates all 13
placed platforms at once, with no scene editing.

**Design constraints (derived, not guessed):** with `jumpForce 13` and `gravityScale 3` the
jump apex is **2.871 u**. Because `fallMultiplier 1.5` makes the fall faster than the rise,
horizontal reach is shorter than a naive symmetric estimate — **4.81 u** on the flat and
**4.15 u** onto a 1.5 u step-up, at walk speed. Every gap in the level is **≤ 3 u** and every
step-up **≤ 1.5 u**, i.e. inside 73% of the tightest reach. That headroom is deliberate: a
first-time player on a keyboard has to be able to clear it.

---

## Architecture

16 scripts in `Assets/Scripts`.

**Core loop.** `GameManager` is a singleton that owns the timer, lives, score, checkpoint
position and game-over state. Everything else talks to it through `GameManager.Instance`.
`PlayerController` owns movement, jumping, sprint stamina and the ground check
(`Physics2D.OverlapCircle` against the `Ground` layer). `CameraFollow` tracks the player.

**Hazards.** `TrapTrigger`, `HiddenTrap`, `FakePlatform`, `SpikeTrap`. Each calls
`GameManager.PlayerDied()`, which returns whether a life remains, and the player respawns at
the last `Checkpoint`. `GoalTrigger` calls `WinGame()`.

**UI without scene wiring.** `HudUI`, `PauseMenu` and `ResultUI` each bootstrap themselves via
`[RuntimeInitializeOnLoadMethod(RuntimeInitializeLoadType.AfterSceneLoad)]`. They construct
their own Canvas at runtime and locate the `GameManager` by themselves. Nothing about them
exists in the scene file, so there is no reference for anyone to unassign and no merge conflict
for anyone to cause. `TimerUI` and `DeathCounterUI` drive the scene-authored HUD text.

**Repeatable level generation.** `Tools/build_level.py` regenerates the entire level from a
data table of coordinates in one command (`--reset`), writing real Unity PrefabInstance YAML
and re-running the geometry checks. The level layout is therefore reviewable as a diff rather
than as a scene file.

**Git safety.** `.gitattributes` marks `.unity`, `.prefab` and `.asset` as `-text merge=binary`,
so git can never line-merge a scene into a silently corrupt state.

---

## Features against the design form

| Form requirement | Implementation | Status |
|---|---|---|
| 2D side-scrolling platformer with hidden troll traps | `HiddenTrap` / `FakePlatform` / `SpikeTrap`, 11 placed | Done |
| Jump and dodge mechanics | `PlayerController` — coyote time, jump buffer, variable height | Done |
| Lives system, one life per trap | `GameManager.Lives`, 3 lives, checkpoint respawn | Done |
| Score from speed + traps survived | `GameManager.Score` | Done |
| Left/Right or A/D — move | `Horizontal` axis | Done |
| Space or Up Arrow — jump | `Jump` axis, `altPositive: up` | Done |
| Shift — sprint | `PlayerController.UpdateSprint`, 2.5 s stamina | Done |
| Esc — Pause / Resume | `PauseMenu` | Done |
| Win: reach school in time with a life left | `GameManager.WinGame()` asserts `Lives > 0` | Done |
| Lose: lives run out **or** timer expires | `LoseGame("lives")` / `LoseGame("time")` | Done |
| 8-bit pixel art, chiptune | Placeholder colours in place; art pending | Pending |
| *Optional:* bell timer countdown | 85 s countdown + `THE BELL RANG` screen | Done |
| *Optional:* death counter | `DeathCounterUI`, also on the result screen | Done |
| *Optional:* bicycle power-up | `BicyclePickup`, +45% speed for 4.5 s, 2 placed | Done |
| *Optional:* sound effects & chiptune BGM | Not started | Cut |
| *Optional:* school van shortcut | Not started | Cut |

The form asks for "more than one" optional feature. Three are shipped.

---

## Tuned values

These were arrived at by playtest, not by default, and are worth knowing before changing anything.

| Value | Setting | Why |
|---|---|---|
| `moveSpeed` | 6 | 8 read as a permanent sprint even when walking |
| `sprintSpeed` | 8.5 | Roughly the old walk speed, now earned |
| `maxStamina` | 2.5 s | Long enough to cross a stretch, short enough to matter |
| `jumpForce` | 13 | 7 with gravity 1 was floaty and unresponsive |
| `gravityScale` | 3 | Same reason — weight |
| `fallMultiplier` | 1.5 | Falls faster than it rises; standard platformer feel |
| `coyoteTime` | 0.12 s | Forgives leaving the edge |
| `jumpBufferTime` | 0.12 s | Forgives pressing early |
| `startingTime` | 85 s | Clean run is ~27 s; realistic run is 50-70 s |
| `startingLives` | 3 | Raise to 5 on the `GameManager` object if playtesters stall |

All of these are serialized explicitly on the `GameManager` and `Player` objects in
`Level1.unity`, so what you see in the Inspector is what actually runs.

---

## Known limitations

- **No final art or audio.** The game runs on placeholder solid colours. Prefabs are structured
  so that art drops in without touching the scene, but as of this writing the 8-bit sprite pass
  and the chiptune track have not been delivered. Sound effects and BGM are formally cut.
- **One level.** `Level1` is the whole game. There is no main menu and no level select; the
  build boots straight into play.
- **English text only.** The bundled TextMeshPro font (LiberationSans SDF) has no Thai glyphs,
  so Thai strings would render as empty boxes. Adding Thai requires importing a Thai TTF as a
  TMP Font Asset first.
- **No character animation.** The player is a static sprite, flipped by facing direction.
- **`Assets/Scripts/AppControls.cs` is dead**, superseded by `PauseMenu.cs`. Left in place to
  avoid a last-minute meta-file churn before submission.

---

## Repository

`https://github.com/jiranathw/late-to-kosen` (private)

Additional documentation in the repository root: `HANDOFF.md` (team handoff, Thai, includes
the troll-trap placement rules), `TJ_tasks.md`, `Bun_tasks.md`, `Krin_tasks.md`, `PROGRESS.md`.
