# Late to KOSEN — Project Progress

**Team:** sixseven (TJ 09 / Bun / Krin) · **Course:** Programming 7
**Repo:** https://github.com/jiranathw/late-to-kosen · **Branch:** `main`
**Last updated:** 27 Aug 2026 · **Deadline:** 31 Aug 2026 (hard) · **4 days left**

---

## Where we are

The build now matches the submitted design form. That was the single biggest risk
in the project: the form promises a **2D troll platformer** with hidden traps, a
lives system, a score system and `Esc = Pause`, and until 26 Aug none of those
existed in the game — `Esc` was actually wired to *quit*, which directly
contradicted the document the instructor grades against. All of it is now
implemented, generated into the scene, and verified.

Latest commit on `origin/main`:

```
ec3025b  Troll traps, lives, score, sprint, pause + playtest fixes
         38 files changed, 5697 insertions(+), 117 deletions(-)
```

Working tree is byte-identical to that commit across all 453 tracked files —
nothing is sitting unsaved.

---

## Form compliance

Every required item is done. Optional features required "more than one"; three
shipped.

| Form requirement | Status |
|---|---|
| 2D side-scrolling platformer with hidden troll traps | done — 3 trap types, 11 troll instances |
| Jump and dodge mechanics | done — coyote time, jump buffer, variable height |
| Lives system (lose a life per trap) | done — 3 lives, checkpoint respawn |
| Score from speed + traps survived | done — time x10 + traps x100 − deaths x50 |
| Arrow keys / A-D move, Space / Up jump, Shift sprint | done |
| **Esc = Pause / Resume** | done — was quit, now a real pause menu |
| Win: reach school in time with a life left | done |
| Lose: lives run out **or** timer hits zero | done — two distinct screens |
| Optional: bell timer countdown | done — 85s |
| Optional: death counter | done |
| Optional: bicycle power-up | done — +45% for 4.5s, 2 placed |
| 8-bit pixel art + chiptune | **Bun** — placeholders in place |
| Optional: SFX / BGM, school van shortcut | not started, cuttable |

---

## Shipped this round

**Systems (16 scripts).** Lives, score, pause, three troll trap types
(`HiddenTrap`, `FakePlatform`, `SpikeTrap`), `BicyclePickup`, plus a HUD.
`HudUI`, `PauseMenu` and `ResultUI` self-bootstrap through
`RuntimeInitializeOnLoadMethod`, so there is no scene wiring anyone can break in
the Inspector.

**Level.** `Level1.unity` rebuilt from a data table: 13 platforms, 12 visible
traps, 5 hidden traps, 3 spikes, 3 fake platforms, 2 bicycles, 5 checkpoints,
1 goal — 44 objects, all PrefabInstances, so Bun's art propagates automatically
without touching the scene. `Tools/build_level.py --reset` regenerates the whole
thing and re-runs the geometry checks in one command.

**Physics.** jumpForce 13, gravityScale 3, fallMultiplier 1.5, moveSpeed 6,
sprintSpeed 8.5. Jump apex 2.87u, horizontal reach 4.81u flat / 4.15u on a 1.5u
step-up. Every gap in the level is 2–3u, so the tightest jump still has 1.15u of
margin.

**Playtest round 1 — four bugs TJ found by playing, all root-caused:**

1. *Lives icons drawn on top of the timer.* The scene Canvas puts `TimerText` at
   (30, −30) at 200×50; `HudUI` started drawing at y = −32. The HUD block moved
   below it, and score moved clear of the death counter.
2. *Hole in the wall at the start, player wedged in it.* `Ground_Wall_Left`
   spanned x −8.5..−7.5 while the start platform begins at −7 — a 0.5u slot
   **exactly the width of the player's capsule collider**. You fell in, didn't
   die, couldn't get out. Wall moved flush to −8..−7, and the level verifier now
   permanently checks for any slot narrower than 2× player width.
3. *Player caught on platform edges instead of falling.* The collider had no
   `PhysicsMaterial2D`, so Unity's default friction 0.4 held it against vertical
   faces. `PlayerController.Awake` now assigns a zero-friction material — safe,
   because horizontal velocity is assigned outright every FixedUpdate, so there
   is no ice-skating.
4. *Character ran too fast.* moveSpeed 8 → 6 (the original), sprint 11.5 → 8.5.
   That shortened jump reach, so `Ground_11_Climb` was widened 6u → 7u to bring
   the last gap from 4u down to 3u, and the timer went 70 → 85s.

**Verification.** Scene YAML: 130 documents, no duplicate anchors, 50 scene roots
all resolve, no dangling prefab references, all 8 prefab GUIDs resolve to real
files with the right instance counts. Gameplay verifier: **0 fails, 0 warnings**,
level completable with ~58s of timer slack.

---

## What's left

### TJ — this is the gate
Open `Level1.unity` in Unity and press Play. The scene YAML and the newer prefabs
(`TrapHidden`, `TrapSpike`, `PlatformFake`, `Bicycle`) were generated outside the
editor and have **never been opened in Unity**. Confirm the scene loads with no
console errors before anything else stacks on top. Then walk the 12-item manual QA
checklist in `TJ_tasks.md`.

If 3 lives makes it unwinnable for a first-timer, raise `startingLives` to 5 on the
`GameManager` object. One field, no code change.

### Krin — level
Re-theme the map as the dorm → KOSEN walk. The generated layout is a working
fallback, not a mandate; replace it freely, but respect the constraints:
**gaps ≤ 3u, step-ups ≤ 1.5u, never a slot narrower than 1u** between two
same-height platforms. Troll placement rules are written out in `HANDOFF.md`.

### Bun — art
8-bit sprites dropped on the **prefabs**, not the scene. Sprite (2D and UI),
**Filter Mode = Point**, **Compression = None**, identical Pixels Per Unit across
every sprite. `PlatformFake` must reuse the exact `Ground` sprite or the troll
doesn't work. All in-game text is ASCII-only — the bundled TMP font has no Thai
and no heart glyph, both render as empty boxes.

---

## Schedule

| Day | Focus |
|---|---|
| **27 Aug** | Unity Play-test gate. Then a fresh-eyes playtest — watch whether they laugh or rage-quit. Troll games live or die on that. |
| **28–29 Aug** | Bug fixing only, no new features. First standalone build; confirm it runs outside the editor. |
| **30–31 Aug** | Test the build, fix only game-breakers, final build, presentation with real screenshots, submission packaging. |

---

## Cut list, in order

Instructions screen → character animation → bicycle power-up → number of
**visible** traps → music and SFX.

**Never cut:** movement/jump/sprint, timer, lives, score, troll traps, win/lose
conditions. All six are written into the form being graded.

---

## Known housekeeping

The git **index** is missing entries for 13 files (most of `ProjectSettings/`,
`TJ_tasks.md`, `Tools/build_level.py`) — leftover from tooling, not real changes.
The file contents are identical to `HEAD`, so nothing is at risk, but GitHub
Desktop will show them as phantom deletions. Fix from PowerShell with GitHub
Desktop closed:

```powershell
cd C:\Users\tjhae\Y4\Programming7\Final\LateToKOSEN
git reset
git status
```

`git reset` only rebuilds the index from the last commit. It touches no files.
