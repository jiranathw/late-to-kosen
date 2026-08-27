# TJ — Programmer Tasks (Late to KOSEN)
**ID:** 09 | **Role:** Programmer
**Last updated: 27 Aug 2026 | Deadline: 31 Aug 2026 (hard, no extension) | 4 days left**

## Status: every mechanic promised on the design form is now implemented. What's left is verification, art, and packaging.

## The form is the spec

The submitted form calls this a **2D troll platformer**. That word is the whole grade.
Anything that removes the troll traps, the lives system, or the score system makes the
build disagree with the document the instructor is marking against.

| Form says | Where it lives | Status |
|---|---|---|
| 2D side-scrolling platformer with hidden troll traps | `HiddenTrap` / `FakePlatform` / `SpikeTrap` + 11 placed instances | done |
| Jump and dodge mechanics | `PlayerController` — coyote time, jump buffer, variable height | done |
| Lives system, lose a life per trap | `GameManager.Lives`, 3 lives, respawn at checkpoint | done |
| Score from speed + traps survived | `GameManager.Score` = time x10 + traps x100 − deaths x50 | done |
| Left/Right or A/D — move | `Horizontal` axis: left/right + a/d | done |
| Space or Up Arrow — jump | `Jump` axis: space, altPositive `up` | done |
| Shift — sprint (short speed boost) | `PlayerController.UpdateSprint`, 2.5s stamina | done |
| Esc — Pause / Resume | `PauseMenu.cs` (Esc used to quit — that was wrong, fixed) | done |
| Win: reach school in time **with a life left** | `GameManager.WinGame()` asserts `Lives > 0` | done |
| Lose: lives run out **or** timer hits zero | `LoseGame("lives")` / `LoseGame("time")`, different screens | done |
| 8-bit pixel art, chiptune | Bun — placeholder colours in place, import settings documented | Bun |
| Optional: bell timer countdown | 85s countdown + "THE BELL RANG" lose screen | done |
| Optional: death counter | `DeathCounterUI`, also on the result screen | done |
| Optional: bicycle power-up | `BicyclePickup.cs`, +45% speed for 4.5s, 2 placed | done |
| Optional: sound effects & chiptune BGM | not started | cuttable |
| Optional: school van shortcut | not started | cuttable |

Form says Optional Features "more than one" — three are shipped, so this is already satisfied.

## Done
- [x] Unity project, Force Text + Visible Meta Files, private GitHub repo, collaborators invited
- [x] Folder structure, `Player` tag, `Ground` layer (index 3), Active Input Handling = Both
- [x] 16 scripts in `Assets/Scripts` — full loop plus lives, score, pause, three troll trap types, bicycle
- [x] 8 reusable prefabs: `Ground`, `Trap`, `TrapHidden`, `TrapSpike`, `PlatformFake`, `Bicycle`, `Checkpoint1`, `Goal`
- [x] `Level1.unity` rebuilt: 13 platforms, 12 visible traps, 5 hidden traps, 3 spikes, 3 fake platforms, 2 bicycles, 5 checkpoints, 1 goal — **all PrefabInstances**, so Bun's art propagates automatically
- [x] Game-feel pass — coyote time 0.12, jump buffer 0.12, variable jump height, fall multiplier 1.5, Rigidbody2D interpolation on
- [x] Physics retuned — jumpForce 13, gravityScale 3 (were 7 / 1 and floaty). moveSpeed went 6 -> 8 -> **back to 6** after playtest: 8 felt like a permanent sprint. sprintSpeed 8.5.
- [x] Timer 90 → 85 (clean run ~27s at moveSpeed 6, ~50-70s realistic)
- [x] Canvas scaler → Scale With Screen Size @ 1920x1080, so UI doesn't explode at other resolutions
- [x] Checkpoints have a visible sprite and turn green when armed (they were invisible before)
- [x] **Esc changed from quit to Pause/Resume** — the old behaviour contradicted the form. Quit moved to Q inside the pause menu.
- [x] HUD: lives as icon row, sprint stamina bar, bicycle timer, live score + traps-survived counter
- [x] Three distinct result screens: `YOU MADE IT!` / `OUT OF LIVES` / `THE BELL RANG`
- [x] `HudUI`, `PauseMenu`, `ResultUI` all self-bootstrap via `RuntimeInitializeOnLoadMethod` — zero scene wiring, nothing anyone can unassign in the Inspector
- [x] All in-game strings ASCII-only — the bundled TMP font has no Thai glyphs and no heart glyph, both would render as empty boxes
- [x] Player sprite sorting order 10, so art never renders behind the ground
- [x] Build is windowed 1280x720, resizable, not exclusive fullscreen
- [x] `companyName` → `sixseven`, `productName` → `Late to KOSEN`
- [x] `.gitattributes` — `.unity`/`.prefab`/`.asset` marked `-text merge=binary` so git can never silently corrupt a scene
- [x] `Tools/build_level.py --reset` rebuilds the entire level from a data table in one command
- [x] Level verified: 130 YAML docs, no duplicate anchors, 50 scene roots all resolve, no dangling prefab refs, all 8 prefab GUIDs resolve. Gameplay verifier: 0 fails, 0 warnings.

## Playtest round 1 — fixed 26 Aug
- [x] **Lives icons were drawn on top of the timer.** The scene Canvas puts `TimerText` at (30,-30) 200x50; `HudUI` was starting at y=-32. Whole HUD block moved down clear of it, and score moved clear of the death counter.
- [x] **`Ground_Wall_Left` left a 0.5u slot.** Wall spanned -8.5..-7.5, the start platform begins at -7 — a hole exactly the width of the player collider, so you fell in and wedged instead of dropping. Wall moved to span -8..-7, flush.
- [x] **Player caught on platform edges instead of falling.** Collider had no PhysicsMaterial2D, so default friction 0.4 held it against vertical faces. `PlayerController.Awake` now assigns a zero-friction material. No ice-skating, because horizontal velocity is assigned outright every FixedUpdate.
- [x] **moveSpeed 8 felt like a permanent sprint.** Down to 6 (the original), sprint 11.5 → 8.5. Shorter jump reach as a result, so `Ground_11_Climb` was widened 6u → 7u to bring the last 4u gap down to 3u, and the timer went 70 → 85.

## Next (27 Aug) — in order
- [ ] **Open `Level1.unity` in Unity and press Play.** All scene YAML and the new prefabs were generated outside the editor and have never been opened in Unity. Confirm it loads clean with no console errors before anything else stacks on top. **THIS IS THE GATE.**
- [ ] Play it end-to-end and confirm each of these by hand:
      - [ ] Shift sprints and the stamina bar drains, then locks until released
      - [ ] Space **and** Up Arrow both jump
      - [ ] Esc pauses, Esc unpauses, the game actually freezes (timer stops)
      - [ ] R restarts from the pause menu and from the result screen
      - [ ] Hitting a trap costs one life icon and respawns at the last checkpoint
      - [ ] Third death shows `OUT OF LIVES`, not `THE BELL RANG`
      - [ ] Letting the timer expire shows `THE BELL RANG`
      - [ ] Reaching the goal shows `YOU MADE IT!` with a non-zero score
      - [ ] Hidden traps are invisible until they kill you, then stay visible
      - [ ] Fake platforms wobble, drop, and are gone on the retry
      - [ ] Spikes rise with enough warning to react at walking speed
      - [ ] Bicycle noticeably speeds you up and the HUD timer counts down
- [ ] If 3 lives makes the level unwinnable for a first-timer, raise `startingLives` on the `GameManager` object to 5. One field, no code change.
- [x] Committed and pushed — `ec3025b` is on `origin/main`, 38 files, +5697 lines.
- [ ] Tell Krin to read the "กฎการวางกับดัก troll" section in `HANDOFF.md` before placing anything. Tell Bun the import settings: Sprite (2D and UI), **Filter Mode = Point**, **Compression = None**, identical Pixels Per Unit, dropped on the **prefabs** not the scene — and that `PlatformFake` must use the exact same sprite as `Ground`.

## Day-by-day from here
**27 Aug (checkpoint)** — Team playtest with fresh eyes: someone who hasn't played it. Watch where they die and how they react. Troll games live or die on whether the player laughs or rage-quits. If art won't land in time, ship with placeholder colours; your call, don't wait for consensus.

**28-29 Aug** — Bug fixing only, no new features. First full build, confirm it runs outside the editor. Nice-to-haves only if there's real slack: instructions screen, jump/death/win SFX.

**30-31 Aug** — Test the build, fix only game-breaking bugs, final build, presentation (use real screenshots once the game is locked), hand off for submission packaging.

## Shared architecture contract
- Tag: `Player` / Layer: `Ground` (index 3) — `PlatformFake` also lives on layer 3
- Folders: `Assets/Scripts`, `Assets/Prefabs`, `Assets/Scenes`, `Assets/Art`, `Assets/Audio`
- Never rename: `GameManager`, `PlayerController`, `TrapTrigger`, `HiddenTrap`, `FakePlatform`, `SpikeTrap`, `BicyclePickup`, `Checkpoint`, `GoalTrigger`, `CameraFollow`, `TimerUI`, `DeathCounterUI`, `HudUI`, `PauseMenu`, `ResultUI`
- `AppControls.cs` is dead — superseded by `PauseMenu.cs`. Delete it from the Unity Project window when convenient.
- Public API:
  `GameManager.Instance` → `.PlayerDied()` (returns true if a life remains), `.WinGame()`, `.LoseGame(reason)`,
  `.SetCheckpoint(pos)`, `.GetCheckpoint()`, `.RegisterTrap(worldX)`, `.TogglePause()`, `.SetPaused(bool)`, `.RestartLevel()`, `.QuitGame()`,
  `.TimeRemaining`, `.Lives`, `.StartingLives`, `.Score`, `.TrapsSurvived`, `.TrapTotal`, `.DeathCount`, `.IsGameOver`, `.IsPaused`, `.DidWin`, `.LoseReason`
  `PlayerController` → `.Die()`, `.Respawn()`, `.GrantBike(seconds)`, `.Stamina01`, `.IsSprinting`, `.HasBike`, `.BikeSecondsLeft`

## Level design constraints (tell Krin, enforce in review)
Jump apex 2.87u, max horizontal reach **4.81u flat / 4.15u on a 1.5u step-up** (at moveSpeed 6).
**Gaps <= 3u. Step-ups <= 1.5u.** Anything past that and a first-time player cannot clear it.
**Never leave a slot narrower than 1u between two same-height platforms** — the player collider is 0.5u wide and wedges in it.
Troll placement rules are written out in `HANDOFF.md`; the short version is that a fake platform
must never be the only way across, a hidden trap must reveal itself permanently after one kill,
and nothing may sit closer than 1.2u to a checkpoint.
`Tools/build_level.py --reset` regenerates the whole level from a data table and re-runs the geometry checks.

## Cut list (your call, in this order)
1. Main menu → static instructions screen
2. Character animation → static sprite, flipped by direction (flip already coded)
3. Bicycle power-up → delete the two instances from the scene; nothing else depends on it
4. Number of traps → reduce **visible** traps first, keep the troll ones
5. Music/SFX → cut entirely; bell timer + death counter + bicycle already satisfy "more than one" optional feature

**Never cut:** movement/jump/sprint, timer, lives, score, troll traps, win/lose conditions.
All six are written into the form the instructor is grading against.
