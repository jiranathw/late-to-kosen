# Krin — Level Design & PM Tasks (Late to KOSEN)
**ID:** 21 | **Role:** Level Designer & Project Manager
**Last updated: 28 Aug 2026 (evening) | Deadline: 31 Aug 2026 (hard) | 3 days left**

> Project-wide status is in **`PROGRESS.md`**. Read that first, then this.
> The single most important section of this file is **"Six things we changed in your level"**.

---

## Your level is in the game. It is stage 2, and it is the reason for everything else

The team voted on 28 Aug to keep the level on your `Lv1-Create` branch, because it is hard and it
is fun, and neither of those is easy to make. It is now **stage 2**, the inside-the-building
stage, and it ships essentially as you built it: every platform is at the coordinate you put it
at to two decimal places, the goal sits at (67.55, 4.50) because that is where your goal sits,
and your sign copy is reproduced verbatim, typos included.

What that decision cost is stage 3. We had three stages planned; three days is not enough to
build a third act as good as yours, and a weak third stage would drag the whole grade down. So
the flood level is cut and the game is **two stages**.

| # | Scene | Title | Timer | What it is |
|---|---|---|---|---|
| 1 | `Level1.unity` | **LATE** — your room to the gate of Building 12 | 80 s | new. Dorm, stairs, the soi, Chalong Krung Road, the forecourt |
| 2 | `Level2.unity` | **INSIDE** — the building, and it is not done with you | 65 s | **yours**, ported and repaired |

Three lives per stage, lives reset every stage, running out restarts *that stage only*.

---

## Your level set the physics for the whole game

This is worth knowing because it explains why the player feels different from the build you last
played. Your player was `moveSpeed 6 / jumpForce 7 / gravityScale 1` — 1.43 s of airtime and an
8.56 u flat reach, very floaty. Ours after the 28 Aug retune was 3.45 u flat, and at 3.45 u your
level is not hard, it is **impossible**: the opening gap alone is 5.00 u.

So we rebuilt the player around your level instead of the other way round. Sprint was removed and
its speed became the only speed. The numbers landed at `moveSpeed 7.5 / jumpForce 13.5 /
gravityScale 2.6 / fallMultiplier 1.8`. Two of your edges pinned them:

```
Ground_Start      -> GroundCheckpoint1    gap 5.00 u   = 72% of a 6.93 u reach
GroundCheckpoint2 -> Ledge_3              rise 2.32 u  = 65% of a 3.57 u apex
```

The first is why the reach cannot drop below about 6.7 u. The second is why the generator's
step-up ceiling is 0.70 of apex rather than the 0.55 that reads comfortably. Neither has any
margin left, which is the correct amount of margin for the hardest jump in a game about being
late. If you ever want to move those two platforms, tell TJ *before* you do — they are load
bearing for both stages.

---

## Six things we changed in your level, and why

All of it is repair work — things that were broken in the committed scene, not things that were
merely cruel. Read this list and say if you disagree with any of it; there is still time to put
something back.

1. **Three checkpoints were stacked on top of each other at x≈0,** so two of them did nothing.
   They are spread to x = 2, 12, 26 and 55 now.
2. **Trap1, Trap2 and Trap3 floated at y = 16.24, 20.16 and 33.41** with no platform under or
   near them — unreachable, so they were decoration. Dropped, and the same number of traps
   re-placed on actual surfaces.
3. **The goal had no floor.** It hung in the air past the last ledge with nothing to land on.
   `Ground_Exit` (cx 66, w 12, top 3.0) is new, and it is the only platform in stage 2 that is
   not yours. The goal itself did not move.
4. **`FakeGround` had its renderer switched off,** so it was an invisible collider rather than a
   fake platform — which *helped* the player instead of tricking them. It is a visible
   `PlatformFake` now, sitting over the opening gap, which is clearly what it was meant to be.
5. **`FakeFallingRock` had no script on it at all,** so it never fell. We kept it exactly that way
   (`triggerDistance 0`) and gave it a real twin at x = 33 — so now the inert one is a joke
   rather than an oversight. You see one fall; you flinch at the next one; it does nothing.
6. **`KillBlock` became a `kill_floor`** stretched under the opening gap, so missing the 5.00 u
   jump kills you cleanly instead of dropping you somewhere undefined.

One retheme, not a fix: **the soi dog is a monitor lizard** (ตัวเงินตัวทอง). Same script, same
numbers, funnier and more Thai. Your arena ambush at x = 27 is a lizard now.

---

## The pit is the best joke in the game and we did not touch it

Undershoot `Ledge_3 -> Ledge_4` and you land on `Ledge_5`, three ledges down. That is not death —
kill_y is −14 and the bottom ledge is at −9.46. It is worse. You cannot climb out (`Ledge_7 ->
Ledge_6` is a 2.80 u step against a 3.57 u apex, 78%, over the ceiling, deliberately), and the
bottom holds two teleporters that look identical. One is your secret ending: it sends you to spawn
**and drags your checkpoint back with you**. The other is a staff lift back into the arena. There
is no way to tell them apart.

That is entirely yours and it stays exactly as it is.

---

## Stage 1 was built to match yours

The brief was that stage 1 must be as cruel as stage 2, with similar gimmicks and similar
difficulty. It answers your three signature moves directly:

- your stacked-checkpoint mistake → nine checkpoints, deliberately spaced 12–39 u
- your invisible fake ground → a fake platform over a gap that is *already* clearable, plus five
  hidden traps, one of them placed **before** the WET FLOOR sign that warns about it
- your two-teleporters-that-look-alike → one teleporter behind a sign reading `SHORTCUT`, which
  sends you 34 u backwards *and* moves your checkpoint so you cannot undo it

Plus three things stage 2 does not have: live traffic on Chalong Krung, a flowerpot gag that is
warned about the first time and not the second, and the bike.

**The bike is new and you have not seen it.** It is an Anywheel rental, not a boost: you pick it
up, you ride whether you want to or not, and you can only get off at a rack. Riding is faster
(8.11 u reach) but jumps *lower* (2.17 u apex), so a step-up that is trivial on foot can strand
you. There are three racks and **the middle one is fake**. The generator re-walks the entire route
from the bicycle to the goal against riding physics and fails the build if a rider could get
stuck, so the trap is a detour, never a softlock.

---

## Your job now: play them and be honest

Both stages exist, are completable, and pass every automated check. What no script can tell us is
whether they are *fun*. That is you.

- [ ] Play both, start to finish, at least three times each.
- [ ] Confirm stage 2 still feels like your level. If a fix above ruined something, say which.
- [ ] Mark every place you were **bored** — flat ground with nothing on it.
- [ ] Mark every place you felt **cheated rather than tricked**. The difference is whether you
      knew what to do differently on the retry. If you did not, it is unfair, not a troll.
- [ ] Mark every place you died **more than twice in the same spot**.
- [ ] Time a clean run of each against the timers: 80 s and 65 s.
- [ ] **Ride the bike badly on purpose.** Try to strand yourself. If you succeed, that is the
      highest-priority bug in the project.
- [ ] **Then watch someone who has never seen the game play both.** Do not help. Do not explain.
      Write down where they die and whether they laugh. For a troll platformer, laugh-vs-rage-quit
      is the only test that matters, and you cannot run it on yourself.

Report to TJ as a list of **x positions and what is wrong**, e.g. "Level1 x≈160, second traffic
lane, died 6 times, felt random". Positions are what he needs to change the data table.

---

## How to change a level — this part is important

**Do not fix level geometry in the Unity Inspector.** Every platform, trap and checkpoint is
generated from a data table, and the next time anyone regenerates, your Inspector edits are
silently gone.

```
python3 Tools/build_levels.py --check    # design rules, writes nothing
python3 Tools/build_levels.py            # regenerate both scenes + Build Settings
python3 Tools/verify_scenes.py           # structural check on the written YAML
```

The generator is **three files** now, which makes it much easier to read than the old single one:

| File | What is in it |
|---|---|
| `Tools/level_kit.py` | the physics constants, the design rules, and the one-line constructors (`ground`, `trap`, `hidden`, `lizard`, `bicycle`, `bike_rack`, …) |
| `Tools/stage1.py` | stage 1's geometry and object list, and a long comment explaining every beat |
| `Tools/stage2.py` | **your stage.** Your coordinates, your sign copy, and the six fixes documented at the top |

`stage1.py` and `stage2.py` read like level design rather than like code — a list of "put this
thing at this x". If you are comfortable editing them, do, and run both verifiers afterwards. If
not, send TJ the positions and he will.

**Safe to change in the Inspector,** because they are not geometry:

- `startingTime` on that stage's `GameManager` (80 / 65)
- `startingLives` on that stage's `GameManager` (3)

Those two are the fastest difficulty dials in the project. Use them before proposing layout
changes.

---

## Placement rules — the generator enforces these, so proposals that break them get rejected

1. **Gaps ≤ 75% of real jump reach.** Reach is 6.93 u flat on foot, less onto a step-up, because
   the fall is faster than the rise. Budget: gap ≤ 5.20 u, step-up ≤ 2.50 u.
2. **Never a slot narrower than 1 u between two same-height platforms.** The player collider is
   0.5 u wide: it drops in, does not die, and cannot get out.
3. **Nothing within 1.2 u of a checkpoint.** Respawn-into-death is the fastest way to make a
   playtester quit — and it is what the stacked checkpoints in your scene would have caused.
4. **A fake platform must span a gap that is already clearable without it.** A temptation, never
   the only route.
5. **A hidden trap must reveal permanently after one kill,** and never chain into a second one.
   You get trolled once per trap, never forever.
6. **At least 1 u of run-up before any hazard, 0.5 u of platform after it.**
7. **Bicycles on open ground only,** no hazard within 8 u ahead.
8. **Pure-walk time ≤ 75% of the stage timer.** Currently 34% and 20%, so there is real slack for
   dying — intentional, not sloppy.
9. **Riding is checked separately.** From the first bicycle to the goal, every route edge is
   re-walked against riding physics (gap ≤ 6.08 u, step-up ≤ **1.52 u**) and the build fails if a
   rider could be stranded. This rule is why the bike is safe to be cruel with.

Rules 1 and 9 are the two that will reject your proposals most often. Both are arithmetic, not
opinion — ask TJ for the numbers on a specific gap and he can tell you in one command.

---

## Two warnings we are deliberately keeping

**`Level1: 39u between checkpoints around x=133`.** Leave it. The next platform is Chalong Krung
Road, and a checkpoint on the road respawns the player into moving traffic. Walking 5 seconds back
is a worse outcome than that, but only slightly, and dying on respawn with no input is much worse.
If you find a better spot on the *kerb* rather than the road, that is a real improvement — say so.

**Four `step-up is N% of apex` warnings on Level2.** All four are your ledges: 59%, 56%, 65%, 56%.
They warn above 55% and fail above 70%. They are meant to be near the top of the arc. Leave them.

---

## The set-pieces, and the numbers behind them

Hand-timed. If one feels wrong, quote the number back rather than guessing.

**Monitor lizard (Level1 x 101, Level2 x 27).** Wakes within 9 u, chases at 7.0–7.2 against your
7.5, gives up after 24–30 u. Survivable at full speed with a few units to spare. It is meant to be
a fright, not a wall. If people are dying to it, it is too fast.

**Flowerpot (Level1 x 121 and x 126).** Falls at gravity 3.4 and lands on your head at walking
pace. The first has a warning sign above it. The second does not. That is the whole joke — if
playtesters do not react to the second one, the joke failed and we should move it, not remove it.

**Traffic (Level1, x 140–166).** Two lanes with different periods, both moving left: motorbikes
every 2.0 s at speed 6.5, pickups every 2.8 s at speed 4.5, offset by 1.3 s so the road is never
simultaneously blocked. There is a standable median at x 151.5–154.5. It is a rhythm puzzle, not a
reflex test.

**The SHORTCUT teleporter (Level1 x 118).** Fires once per stage load, sends you back to x 84 and
moves your checkpoint with you. Not re-armed on respawn, because its exit is behind its entrance
and a repeating one would trap the player in an inescapable loop that costs no lives. Do not ask
for it to repeat — this is the same reason your secret-ending teleporter is one-shot.

---

## PM responsibility — 3 days left

| Day | Who | What |
|---|---|---|
| **28 Aug** | TJ | **Unity gate.** Both scenes must open and run clean. Tonight's build has *never been opened in the editor* — two scenes, three new prefabs and two new scripts were all authored outside Unity. This is the one real risk left. |
| | You | Play both, report positions. Confirm the six fixes to your level. Then find a fresh playtester. |
| | Bun | Sprites and audio. Two backgrounds, SFX, BGM. He starts once the layouts are frozen. |
| **29 Aug** | all | Bug fixing only, no new features. First standalone build — confirm the stage transition survives it. |
| **30 Aug** | you | Documentation: GDD summary, how each mechanic works, team contributions. Screenshots from the locked game. |
| **31 Aug** | all | Final build, presentation, submit. |

Chase both of them daily. **If TJ's Unity gate fails, everything else stops** — that is the one
dependency in the schedule, so check it first thing.

---

## Git rule for you specifically

Pull before every session, push when you finish a chunk. Do not leave uncommitted work overnight.

If you edit a scene in Unity and TJ regenerates it, git will show a conflict on a binary-marked
file and you will lose the edit — which is another reason to send positions rather than scene
changes. Scene files are marked `-text merge=binary` in `.gitattributes` precisely so git cannot
line-merge them into something that looks fine and crashes.
