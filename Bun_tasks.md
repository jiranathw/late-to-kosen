# Bun — Art, UI & Audio Tasks (Late to KOSEN)
**ID:** 17 | **Role:** Artist, UI Designer & Sound
**Last updated: 28 Aug 2026 (evening) | Deadline: 31 Aug 2026 (hard) | 3 days left**

> Project-wide status is in **`PROGRESS.md`**. Read that first, then this.

---

## What changed on 28 Aug, and what it means for you

**The game is two stages, not three.** The team voted to keep Krin's level because it is hard and
fun, and that made it stage 2 — the inside-the-building stage. Stage 1 was rebuilt from scratch as
the walk from the dorm to the building. Stage 3, the flood level, is cut: three days is not enough
to make a third stage as good as Krin's, and a weak one would drag the grade down.

**That is good news for you.** Two backgrounds instead of three, and the layouts are frozen now, so
nothing you draw is going to be thrown away by a redesign.

| # | Stage | Setting to draw |
|---|---|---|
| 1 | **LATE** | a dorm room, a corridor, four flights of stairs, a lobby — then outside: a Thai soi with shophouses and balconies, Chalong Krung Road, and the forecourt of Building 12 |
| 2 | **INSIDE** | inside the building. Corridors, ledges, a stairwell arena, a service pit, the exam-room door |

If you only have time for one background, do **stage 1**. It is the one that reads as Thailand —
the soi and the road — and it is the one that ends up in the presentation screenshots.

**The art pipeline did not change.** Everything is still a prefab instance, so a sprite dropped on a
prefab updates every copy in both scenes at once.

### And you got the gimmick you asked for

The bicycle is now an **Anywheel rental**, not a speed boost. You pick it up, you ride whether you
like it or not, and you can only get off at a bike rack. There are three racks on stage 1 and
**the middle one is fake.**

That means one specific art requirement, and it is the same rule as `PlatformFake`:
**the fake rack must be drawn identically to the real ones.** If the player can tell which rack is
painted on, the joke does not exist. One sprite, three placements, `isReal` is a checkbox in code.

The soi dog is now a **monitor lizard** (ตัวเงินตัวทอง), which is funnier and more Thai. There is
one on each stage.

---

## Import settings — these matter more than the drawings

For every PNG, in the Inspector:

- **Texture Type = Sprite (2D and UI)**
- **Filter Mode = Point (no filter)** — without this your pixel art comes out blurry and stops
  being 8-bit, which is what the design form promised
- **Compression = None** — same reason
- **Pixels Per Unit identical across every file** — mixing values makes objects scale wrong
  relative to each other and it is painful to fix afterwards

**Drop art on the prefabs in `Assets/Prefabs`, never on objects in a scene.** All 102 objects across
the two scenes are prefab instances. Changing the prefab's Sprite field updates all of them.
Editing a scene instead means touching a hundred objects by hand *and* it gets overwritten the next
time TJ regenerates the levels from the data table.

---

## The art list — 16 prefabs

**Priority 1 — these are in both stages and carry the game**

| Prefab | Notes |
|---|---|
| `Ground` | platform tile. **27 instances across the two stages**, so this one sprite does most of the visual work |
| Player | idle + run frames. Sorting order 10, always in front. **Also needs a riding pose** — see below |
| `Trap` | obviously dangerous. The honest one |
| `Checkpoint1` | already has an armed/unarmed colour state in code — draw both, or draw one and let the tint do it |
| `Goal` | the destination. 2 units wide by 3 tall |

**Priority 2 — the trolls. Read the notes, they are not optional**

| Prefab | Notes |
|---|---|
| `PlatformFake` | **must use the exact same sprite as `Ground`.** If the player can tell it apart, the trap does not work and the joke dies |
| `FakeGoal` | **must use the exact same sprite as `Goal`,** for the same reason. It is the lift in the dorm lobby, and Building 9 in the forecourt |
| `BikeRack` | **one sprite for all three racks, real and fake.** Same rule again. A bike rack against a wall |
| `TrapHidden` | invisible during play; the sprite only shows *after* it kills you. So make it read as "gotcha" — this is the one place where being smug is correct |
| `TrapSpike` | spikes that rise out of the ground |

**Priority 3 — the gimmicks**

| Prefab | Notes |
|---|---|
| `Signpost` | a sign on a post. The **text draws itself in code** — do not draw text into the sprite, just the board and the post, and leave the board plain so words stay readable on top. 19 of them across the two stages, so this one earns its keep |
| `MonitorLizard` | ตัวเงินตัวทอง. Should read as *asleep* at rest and *awake* when chasing — it is a fright, not a monster. One per stage |
| `Flowerpot` | a pot falling off a balcony on stage 1, a chunk of ceiling on stage 2. Small, and it has to read at a glance while falling |
| `TrafficLane` | you do not draw the lane, you draw the **vehicle** — assign it to the lane prefab's `vehicleSprite` field. Two lanes: motorbikes (1.8 x 0.9 u) and pickups (2.6 x 1.1 u). **Draw them facing right;** the code flips them to face travel direction |
| `Bicycle` | the rental bike, sitting waiting to be picked up. Should read as collectable rather than scenery, and ideally look like an Anywheel — a bike with a rack lock on the back wheel |
| `Teleporter` | a doorway. Should look like a completely normal door, because the whole point is that the player walks into it on purpose. Three of them: the "SHORTCUT" on stage 1, and Krin's two identical doors at the bottom of the pit |
| `Floodwater` | **unused.** Stage 3 is cut. Skip it unless everything else is done |

`Signpost`, `TrafficLane` and the rest all fall back to a plain generated square if you give them
nothing, so the game runs either way — they just look like programmer art until you get to them.

**The riding pose.** `PlayerAnimator` already switches to a faster frame rate while `IsRiding` is
true, so if you give it a second sprite set it will use it. If you do not, the player just runs
faster on the bike and nobody dies of it. Nice to have, not a blocker.

---

## Audio — new on your plate

The layouts are frozen, so this can start now. Priority order:

1. **Death SFX** — it plays constantly in a troll platformer, so it must be short and it must not
   get annoying by the twentieth time. This is the single most-heard sound in the game
2. **Stage clear** — the reward. Worth more than music
3. **Jump** — very short, very quiet, or it fights everything else
4. **Trap reveal / spike rise / vehicle pass** — one each, subtle
5. **BGM** — one chiptune loop is enough. Two if there is time, one per stage

Keep everything 8-bit / chiptune to match the art. Drop files in `Assets/Audio`. Tell TJ when the
first one lands — wiring a clip to an event is a two-line change and he would rather do it once
with all of them than five times.

If the schedule collapses, **cut BGM before SFX.** A game with sound effects and no music sounds
unfinished; a game with music and no feedback sounds broken.

---

## HUD and UI — already built, do not rebuild

`HudUI.cs` creates the lives icons, the score and the bike indicator **at runtime**. `ResultUI` and
`StageBannerUI` do the same for the result screens and the stage title cards. None of them exist in
the scene files, so anything you add to a scene Canvas will sit underneath them and be invisible.

**The sprint bar is gone** — sprint was removed on 28 Aug and there is one speed now. If you have
already drawn a stamina bar, it has nowhere to go. What replaced it is a bike indicator, which just
shows whether you are riding; there is no timer on it, because the ride ends at a rack or not at all.

If you want a different look, talk to TJ — it is a change in code, and a small one. What you *can*
usefully do is give him a colour palette and font-size direction to apply.

**All in-game text must stay English.** The bundled TMP font has no Thai glyphs — Thai renders as
empty boxes. Same for symbols like hearts, which is why lives are drawn as coloured blocks rather
than heart characters. If you want Thai text or a custom font, it has to be imported as a TMP Font
Asset first; tell TJ, it is about twenty minutes of work.

---

## Style guide

- 8-bit pixel art, limited palette, one base tile size everywhere (32x32 or 16x16 — pick one)
- Setting: Thai engineering college — dorm, soi, road, campus building. Look at actual KOSEN-KMITL
  photos before drawing; the more it looks like the real place, the better this lands with the
  people grading it
- Character: a student rushing to class. A 2–3 frame walk cycle is plenty
- Two backgrounds if there is time, one if there is not (do stage 1)

## Where to find assets fast

itch.io: "pixel platformer asset pack", "school pixel tileset", "2D character sprite sheet free".
For audio: "8-bit SFX pack", "chiptune loop free". Filter by Free and confirm the page says it is
usable in a student project. Mixing a pack with your own work is fine as long as the palette and
pixel size match.

## Handoff naming

- Animation clips: `Player_Idle`, `Player_Run`, `Player_Ride`
- Import into `Assets/Art/Sprites`, `Assets/Art/Tiles`, `Assets/Art/UI`, `Assets/Audio`
- Do not touch `Assets/Scripts`, do not rename the `Player` tag or the `Ground` layer

---

## Day-by-day — 3 days left

**28 Aug (tonight)** — Priority 1 and 2. `Ground`, player, `Trap`, `Goal`, then `PlatformFake`,
`FakeGoal` and `BikeRack` reusing their originals' sprites exactly. That alone makes the game look
finished.

**29 Aug** — Priority 3, then the death SFX and stage-clear SFX. Then backgrounds, stage 1 first.
Join the playtest.

**30 Aug** — Polish only, no new asset categories. BGM if there is room. Record the demo clip for
submission (confirm with Krin that this is still yours).

**31 Aug** — Standby for last-minute needs, submit.

## If things fall behind

Cut animation first — a static sprite flipped left/right is already automatic in the code and costs
you nothing. Then cut BGM. Then cut to one background. Then let priority 3 ship as programmer-art
squares; they all fall back gracefully.

**But never cut the three identical-sprite rules.** `PlatformFake` = `Ground`, `FakeGoal` = `Goal`,
fake `BikeRack` = real `BikeRack`. Those three are not art decisions, they are the game's trolls,
and a visible difference kills them.

**Never let art block TJ or Krin.** Hand over rough versions and iterate in the project rather than
polishing offline — a placeholder in the build is worth more than a finished PNG on your laptop on
31 August.
