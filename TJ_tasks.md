# TJ — Programmer Tasks (Late to KOSEN)
**ID:** 09 | **Role:** Programmer
**Last updated: 25 Aug 2026 | Deadline: 31 Aug 2026 (hard, no extension) | 6 days left**

## Status so far (done)
- [x] Unity project created (`LateToKOSEN`, Unity 6000.4.11f1, 2D Built-In Render Pipeline)
- [x] Force Text + Visible Meta Files set
- [x] Private GitHub repo created & pushed: `https://github.com/jiranathw/late-to-kosen`
- [x] Bun + Krin invited as collaborators (confirm they've accepted before Day 3)
- [x] Folder structure + `Player` tag + `Ground` layer set up
- [x] 8 core scripts in `Assets/Scripts`
- [x] Full core gameplay loop built and tested: movement, jump, ground collision, trap → death → respawn, checkpoint, goal (win), bell timer countdown, death counter UI, camera follow
- [x] `Trap`, `Checkpoint1`, `Goal` converted to reusable Prefabs in `Assets/Prefabs`
- [x] Active Input Handling fixed (set to "Both") — saved in the repo, Bun/Krin don't need to redo it

## What's left for you today (25 Aug)
- [ ] Duplicate `Assets/Scenes/SampleScene` → rename copy to `Level1` — this becomes Krin's real level, already wired with Player/GameManager/Camera/UI
- [ ] In `Level1`, delete the placeholder `Ground`, `Trap`, `Checkpoint1`, `Goal` test objects (Krin places the real ones from `Assets/Prefabs`)
- [ ] Commit + push: `git add .` then `git commit -m "Level1 template scene ready"` then `git push` (run each line separately in PowerShell, not chained with `&&`)
- [ ] Send Bun and Krin their task files + the repo link, confirm they've accepted the GitHub invite

## Day-by-day from here
**26 Aug** — Sit with Krin, help wire the real level in `Level1.unity` using the Trap/Checkpoint/Goal prefabs. Fix integration issues as Bun's tileset comes in.

**27 Aug (checkpoint)** — Team playtest: is there one level, start to finish, winnable and losable? If not on track, cut immediately (see cut list below) — this is your call, don't wait for consensus.

**28-29 Aug** — Bug fixing only, no new features. First full build (File → Build Settings → Build), confirm it runs outside the editor.

**30-31 Aug** — Test the build, fix only game-breaking bugs, final build, hand off for submission packaging.

## Shared architecture contract (unchanged — still applies)
- Tag: `Player` / Layer: `Ground`
- Folders: `Assets/Scripts`, `Assets/Prefabs`, `Assets/Scenes`, `Assets/Art`, `Assets/Audio`
- Classes already built, never rename: `GameManager`, `PlayerController`, `TrapTrigger`, `Checkpoint`, `GoalTrigger`, `CameraFollow`, `TimerUI`, `DeathCounterUI`
- Public API: `GameManager.Instance.PlayerDied()`, `.WinGame()`, `.SetCheckpoint(pos)`, `.TimeRemaining`, `.DeathCount`

## Cut list (your call, in this order)
1. Main menu → static instructions screen
2. Character animation → static sprite, flipped by direction
3. Death counter UI polish → plain text
4. Number of traps → reduce
5. Music/SFX → cut entirely

**Never cut:** movement/jump, timer, win/lose condition. Without these there's no game to submit.
