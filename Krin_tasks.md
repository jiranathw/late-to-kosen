# Krin — Level Design & PM Tasks (Late to KOSEN)
**ID:** 21 | **Role:** Level Designer & Project Manager
**Last updated: 25 Aug 2026 | Deadline: 31 Aug 2026 (hard) | 6 days left — you're starting today, not day 1, so move fast**

> **27 Aug 2026 — 4 days to deadline.** All programming promised on the
> design form is done and pushed (`ec3025b`). Project-wide status lives in
> **`PROGRESS.md`**; read that first, then the section below.


---

## UPDATE 26 Aug 2026 — read this before the older notes below

**The level already exists and is finished enough to submit.** TJ built out all of
`Level1.unity`: 13 platforms, 12 visible traps, 5 hidden traps, 3 pop-up spikes,
3 fake platforms, 2 bicycle power-ups, 5 checkpoints and the school gate, running
from x = -7 to x = 156. You are no longer building a level from an empty scene —
**you are tuning one that works.** The old brief below (5-6 traps, 2-3 checkpoints)
is superseded.

**The game is a troll platformer, and that word is the spec.** Three trap types
now exist as prefabs and they behave differently:

- `TrapHidden` — invisible in play, kills once, then stays visible forever
- `PlatformFake` — looks exactly like `Ground`, wobbles for 0.35s when you land, then drops
- `TrapSpike` — buried in the platform, rises when the player gets within 2.2 units

**Placement rules — these are not suggestions, the level verifier enforces them:**

1. A fake platform must sit over a gap the player can already clear **without it**.
   It is a temptation, never the only route.
2. A hidden trap must reveal permanently after one kill. Never chain two of them
   so that surviving the first drops you straight onto the second.
3. Leave at least **1 unit of run-up** before any hazard and **0.5 units** of platform
   after the last one, or the player has no room to react.
4. Nothing may sit within **1.2 units of a checkpoint** — respawn-into-death loops
   are the fastest way to make a playtester quit.
5. Bicycles go on open ground only, with no hazard within 8 units ahead.
6. Gaps <= **3 units**. Step-ups <= 1.5 units. Hard limits, straight out of the jump
   physics: at moveSpeed 6 the player reaches 4.81u on the flat and only 4.15u
   when also climbing 1.5u.
7. **Never leave a slot narrower than 1 unit between two platforms at the same
   height.** The player collider is 0.5u wide, so it drops in and wedges — it
   doesn't fall, doesn't die, and can't get out. This already happened once at
   the left wall and it is very confusing when you hit it.

**Your actual job now:** play it repeatedly, find the boring stretches and the
unfair ones, and move things. Then watch someone else play it — the only real test
of a troll level is whether the player laughs or rage-quits.

If you break the scene, `python Tools/build_level.py --reset` rebuilds the whole
thing from scratch and re-runs the geometry checks.

Full details, including every tuned physics number, are in `HANDOFF.md`.

---

## First: get access (do this before anything else)
1. Accept the GitHub collaborator invite to `late-to-kosen` (check email/GitHub notifications) — the repo is Private, you can't see it without accepting.
2. Install Unity Hub if you don't have it, install Unity **6000.4.11f1** via Hub → Installs tab.
3. `git clone https://github.com/jiranathw/late-to-kosen.git` — **don't create a new Unity project**, clone the existing one.
4. Unity Hub → Add project from disk → select the cloned folder → open it.

## Good news: you're unblocked already
TJ already built and tested the full core loop (movement, jump, traps, checkpoints, goal, timer, death counter) and turned `Trap`, `Checkpoint`, `Goal` into reusable Prefabs in `Assets/Prefabs`. There's also a `Level1.unity` scene already wired with Player/GameManager/Camera/UI — you don't build any of that. You just **place prefabs along a path**.

## Shared architecture contract (give this to your AI if you vibe-code anything)
Reuse these, don't recreate:
- `TrapTrigger`, `Checkpoint`, `GoalTrigger` — already scripted, just drag prefabs from `Assets/Prefabs` into the scene
- `GameManager.Instance` — has `.TimeRemaining`, `.DeathCount`, `.SetCheckpoint()`, `.WinGame()`, `.LoseGame()`
- Tag: `Player` / Layer: `Ground` — already set up

**Prompt template if you need something level-specific** (e.g. a moving platform):
> "Write a Unity C# script called `MovingPlatform` that moves a platform between two points. Do not touch or duplicate `GameManager`, `PlayerController`, `TrapTrigger`, `Checkpoint`, or `GoalTrigger` — those already exist. Use tag `Player` and layer `Ground`, already set up in the project."

## Level design brief
- **One level only** — dorm → campus obstacles → school gate
- Length: roughly **70-80% of the timer's duration** on a clean run — real pressure, but beatable
- 5-6 trap placements is a reasonable target
- 2-3 checkpoints spread through the level so death doesn't send the player back to the very start
- "Troll" moments should be readable after one death — surprising but not unfair on the second try

## Day-by-day
**25 Aug (today)** — Get repo access set up (above). Once cloned, open `Level1.unity`. Do a quick 15-30 min sketch of the layout on paper/Canva first (start, end, rough path, trap spots), then start placing `Ground` (placeholder for now — Bun's tileset comes later), `Trap`, `Checkpoint`, `Goal` prefabs along it.

**26 Aug** — Continue building the level. TJ will sit with you to help wire things. Swap in Bun's tileset/background as it arrives.

**27 Aug (checkpoint)** — Play your own level start to finish. Report honestly whether it's completable — this is the moment to flag if scope needs cutting further.

**28 Aug** — Balance the timer: adjust `startingTime` on the `GameManager` object's Inspector so a clean run takes 70-80% of it.

**29 Aug** — Start documentation (GDD summary, how each core mechanic works, team contributions).

**30 Aug** — Finish documentation, final playtest pass focused on breaking the game (walk into every trap, try to leave the level bounds), package everything for submission.

**31 Aug** — Submit.

## PM responsibility
Track whether TJ and Bun are on schedule. If either is stuck, flag it in the group chat the same day — don't wait for the 27 Aug checkpoint to find out something's blocked.

## Git rule for you specifically
Work in `Level1.unity` only — don't touch `SampleScene` (that's TJ's test scene, leave it alone). Pull before you start each session, push when you finish a chunk of level work, don't leave uncommitted changes overnight.
