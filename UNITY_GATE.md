# UNITY GATE — ทำตามนี้ทีละข้อ (TJ)

**28 ส.ค. 2026 (ค่ำ) · เหลือ 3 วัน · ทำอันนี้ให้จบก่อนทำอย่างอื่นทุกอย่าง**

เป้าหมายของเอกสารนี้: พา Unity ไปถึง **"เปิด Level1 กับ Level2 ได้ กด Play ได้ Console เขียว"**
แล้วค่อย commit

> **รอบนี้ต่างจากรอบก่อนตรงไหน**
> เกมเหลือ **2 ด่าน** — ด่าน 2 คือด่านของคริน ส่วน `Level3.unity` **ถูกลบไปแล้วพร้อม `.meta`**
> ทั้ง 2 scene ถูก generate ใหม่ทับของเดิม มี prefab ใหม่ 2 ตัว (`MonitorLizard`, `BikeRack`)
> `Bicycle` ถูกสร้างใหม่ และมีสคริปต์ใหม่ 2 ตัว (`BikeRental.cs`, `BikeRack.cs`)
> ส่วน `BicyclePickup.cs` **ถูกลบ** — ของพวกนี้ยังไม่เคยผ่านสายตา Unity เลย

---

## 0. สรุปสั้นสุด ถ้าไม่อยากอ่านยาว

1. เปิด Unity → ถ้าเจอ dialog `Recovering Scene Backups` **กด No** (ข้อ 7)
2. ถ้าเจอ dialog Safe Mode **กด Enter Safe Mode** (ห้ามกด Ignore) แล้วดูข้อ 1-2
3. รอ import ให้จบ (แถบ progress มุมขวาล่าง) — ตรงนี้แหละที่ของใหม่ถูก Unity อ่านครั้งแรก
4. เช็ค prefab ใหม่ 3 ตัว → เช็ค Build Settings ว่าเหลือ **2 scene** → เปิด Level1 → กด Play
5. เล่นให้จบทั้ง 2 ด่าน โดยเฉพาะ**จักรยาน** (ข้อ 3.9)
6. ผ่านแล้วค่อย commit

---

## 1. ถ้าเจอ dialog Safe Mode — ปุ่มไหน และทำไม

**กด `Enter Safe Mode`**

| ปุ่ม | เกิดอะไรขึ้น |
|---|---|
| **Enter Safe Mode** ✅ | Unity คอมไพล์เฉพาะสคริปต์ ยังไม่ import asset อื่น เปิด Console ให้แก้ error ได้เลย ปลอดภัยที่สุด |
| Ignore ❌ | Unity import ทั้งโปรเจกต์ทั้งที่สคริปต์ยังพัง → ทุก object ที่ใช้สคริปต์นั้นจะกลายเป็น **Missing (Mono Script)** และ Unity จะ **เขียนทับ** scene/prefab ด้วยของที่พังไปแล้ว อันนี้คือทางที่ทำให้ต้อง `git checkout` กู้ไฟล์คืน |
| Quit | ปิดไปเฉยๆ ไม่ผิดอะไร แต่เปิดใหม่ก็เจอ dialog เดิม ถ้าไม่ได้แก้อะไร |

**ห้ามกด Ignore เด็ดขาด** — นี่คือกฎข้อเดียวของหน้านี้

---

## 2. error 2 ตัวที่เคยเจอ (แก้แล้ว แต่ต้องรู้ไว้ ตอน present อาจโดนถาม)

**ตัวที่ 1 — `Assets/Scripts/Signpost.cs`**

```
error CS1061: 'TMP_Text' does not contain a definition for 'sortingOrder'
```

`sortingOrder` ประกาศไว้บนคลาส `TextMeshPro` (ตัว 3D) เท่านั้น ไม่ได้อยู่บนคลาสแม่ `TMP_Text`
เช็คจาก source ของ package เองแล้ว: `TextMeshPro.cs:61` มี, `TMP_Text.cs` ไม่มี
แก้: เปลี่ยน field จาก `TMP_Text label` เป็น `TextMeshPro label`

**ตัวที่ 2 — `Assets/Scripts/StageBannerUI.cs` (2 บรรทัด)**

```
error CS0234: The type or namespace name 'CanvasGroup' does not exist
              in the namespace 'UnityEngine.UI'
```

`CanvasGroup` อยู่ใน namespace `UnityEngine` เฉยๆ ไม่ใช่ `UnityEngine.UI`
แก้: `UnityEngine.UI.CanvasGroup` → `CanvasGroup` ทั้ง 2 ที่

> **รอบนี้มีสคริปต์ใหม่ 2 ตัวที่ยังไม่เคยคอมไพล์เลย: `BikeRental.cs` กับ `BikeRack.cs`**
> และ `PlayerController.cs` ถูกแก้ (เอา sprint ออก ใส่ `MountBike()` / `ParkBike()`)
> กับ `HudUI.cs` (เอาหลอด sprint ออก) ถ้าจะมี error รอบนี้ มันน่าจะอยู่ใน 4 ไฟล์นี้
> **ก๊อป error มาทั้งบรรทัดส่งกู อย่านั่งเดาแก้เอง**

---

## 3. ขั้นตอนใน Unity — ทำตามลำดับ ห้ามข้าม

### ☐ 3.1 เปิด Console ก่อนเลย

`Window > General > Console` (หรือ `Ctrl+Shift+C`)

ที่แถบบนของ Console:
- กด **Clear** ทีนึง
- ปิดไอคอน ⚠️ (warning) กับ 💬 (info) ให้เหลือแค่ ❌ (error) — จะได้ไม่ต้องอ่าน warning เป็นร้อยอัน

### ☐ 3.2 บังคับให้ recompile

`Assets > Refresh` หรือ `Ctrl+R`

**ผลที่ควรได้:** Console โล่ง 0 error

**ถ้ามี error:** แต่ละบรรทัดหน้าตาแบบนี้
```
Assets/Scripts/XXX.cs(44,15): error CS1061: ...
```
`(44,15)` = บรรทัด 44 ตัวอักษรที่ 15 — ดับเบิลคลิกมันจะเปิดไฟล์ไปที่จุดนั้นเลย
**ก๊อปมาทั้งบรรทัดส่งกูเลย**

### ☐ 3.3 ปล่อยให้ import จนจบ — ห้ามกดอะไร

ดูแถบ progress มุมขวาล่าง มันจะขึ้นชื่อไฟล์ไล่ไปเรื่อยๆ

**ตรงนี้คือจุดที่ของใหม่ถูก Unity อ่านครั้งแรก** — prefab กับ scene ทั้งหมดถูกสร้างจากสคริปต์
Python นอก Unity รอบนี้คือรอบแรกที่ Unity อ่าน YAML ของ `Level1`/`Level2` เวอร์ชันใหม่
จับคู่ GUID ใน `.meta` กับสคริปต์จริง แล้วสร้าง cache ใน `Library/`

**อย่ากด Play ระหว่างนี้ อย่าเปิด scene ระหว่างนี้ อย่าปิด Unity ระหว่างนี้** รอให้แถบหายไปก่อน

### ☐ 3.4 เช็คว่า Level3 หายไปจริง

ไปที่ Project window → `Assets/Scenes` — ต้องมี **แค่ `Level1.unity` กับ `Level2.unity`**

ถ้ายังเห็น `Level3.unity` โผล่อยู่ แปลว่ามีคน pull ของเก่ามาทับ หรือ Unity กู้จาก cache
ลบทิ้งทั้งไฟล์และ `.meta` แล้วรัน `python3 Tools/build_levels.py` อีกรอบ

### ☐ 3.5 เช็ค prefab

ไปที่ Project window → `Assets/Prefabs` — ต้องมี **16 ไฟล์** และ **ต้องไม่มี `Dog.prefab`**
(มันถูกแทนที่ด้วย `MonitorLizard.prefab`)

**3 ตัวที่ต้องเช็ครอบนี้ (ใหม่หรือถูกสร้างใหม่):**

| Prefab | คลิกแล้วใน Inspector ต้องเห็น |
|---|---|
| `MonitorLizard` | Sprite Renderer + Box Collider 2D + **Chaser Hazard (Script)** |
| `BikeRack` | Sprite Renderer + Box Collider 2D + **Bike Rack (Script)** — และมีช่อง **Is Real** ติ๊กอยู่ |
| `Bicycle` | Sprite Renderer + Box Collider 2D + **Bike Rental (Script)** — **ไม่ใช่** `Bicycle Pickup` อีกแล้ว |

**ตัวอื่นที่เคยเช็คไปแล้วรอบก่อน ไม่ต้องเช็คซ้ำถ้า Console เขียว:**
`FakeGoal`, `Floodwater`, `Flowerpot`, `Signpost`, `Teleporter`, `TrafficLane`

**อาการที่แปลว่าพัง:**

- ไอคอนเป็นสี**ชมพู/ขาวเปล่า** แทนที่จะเป็นกล่องน้ำเงิน = prefab เสีย
- Inspector ขึ้น **`Missing (Mono Script)`** สีเหลือง = GUID ใน prefab ไม่ตรงกับ `.meta` ของสคริปต์
  **ถ้าเจอบน `Bicycle` โดยเฉพาะ** = มันยังชี้ไปที่ `BicyclePickup.cs` ที่ถูกลบไปแล้ว
- ชื่อ component ขึ้นเป็น **`Script (Script)`** = ชื่อคลาสไม่ตรงชื่อไฟล์

ถ้าเจออันไหน **แคปหน้าจอมาให้กู** อย่าเพิ่งลอง fix เอง เพราะทั้ง 16 ตัวถูกอ้างอิงด้วย GUID
จาก 102 object ใน 2 scene — ลบทิ้งสร้างใหม่คือพังทั้งเกม

> ถ้าอยากดูละเอียดกว่านั้น: ดับเบิลคลิก prefab → เข้า **Prefab Mode** (ฉากจะเปลี่ยนเป็นพื้นหลังเทา
> มีชื่อ prefab บนหัว) → ถ้าเปิดได้ไม่มี error แปลว่าโอเคจริง → กดลูกศรย้อนกลับซ้ายบนเพื่อออก

### ☐ 3.6 เช็ค Build Settings

`File > Build Settings` (Unity 6 อาจอยู่ใต้ `File > Build Profiles > Scene List`)

ต้องเห็น **แค่ 2 บรรทัดนี้ เรียงแบบนี้เป๊ะๆ**:
```
Assets/Scenes/Level1.unity    0
Assets/Scenes/Level2.unity    1
```

ทั้ง 2 ต้องติ๊กถูก **และต้องไม่มี Level3 ค้างอยู่ในลิสต์**
ถ้ามีบรรทัด `Level3` ที่ชี้ไปไฟล์ที่ไม่มีแล้ว ให้ลบทิ้ง
ถ้าลำดับสลับ = ผ่านด่าน 1 แล้วไม่ไปไหน (ลากสลับใน list ได้เลย ไม่ต้องแก้โค้ด)

### ☐ 3.7 เปิด Level1.unity

ดับเบิลคลิก `Assets/Scenes/Level1.unity`

**เช็คใน Hierarchy:** ต้องมีประมาณ **65 root object** — `GameManager`, `Player`, `Main Camera`,
`SpawnPoint`, `EventSystem`, `Canvas`, แล้วก็ 59 ตัวที่ generate มา (`Ground_*`, `Trap_*`,
`Checkpoint_*`, `Sign_*`, `Rack_*`, `Lane_*`, `Goal`)

**เช็ค Console:** ต้อง 0 error ตอนเปิด scene
ถ้ามี `The referenced script on this Behaviour is missing!` = ย้อนกลับไปข้อ 3.5

**เช็คสายตา:** ใน Scene view กด `F` ทับ `Player` แล้วซูมออก ควรเห็นแท่งสี่เหลี่ยมสีๆ เรียงเป็นด่าน
ยาวๆ ไปทางขวา ~208 หน่วย (ตอนนี้ยังเป็น programmer art อยู่ ยังไม่มีรูปของบุ้น — ถูกแล้ว)

### ☐ 3.8 กด Play

> ⛔ **ก่อนกด Play ทุกครั้ง ดูมุมขวาล่างก่อน**
> ถ้ามีวงกลมหมุนๆ (compile/import spinner) อยู่ = **ห้ามกด** รอให้มันหายก่อน
> การกด Play ตอน Unity ยัง compile ไม่เสร็จ คือสาเหตุของ crash `TempOverflow` รอบ 28 ส.ค.
> รายละเอียดอยู่ข้อ 7

**สิ่งที่ต้องเห็นภายใน 2 วินาทีแรก:**

- การ์ดกลางจอ `STAGE 1  LATE` แล้วจางหายไปเอง (ไม่ค้าง ไม่หยุดเกม)
- มุมบนซ้าย: ตัวเลขเวลานับถอยหลังจาก **80**
- ใต้เวลา: บล็อกแดง **3 อัน** = ชีวิต
- **ไม่มีแถบ SHIFT / stamina แล้ว** — ถ้ายังเห็นอยู่ แปลว่า `HudUI.cs` ยังเป็นตัวเก่า
- มุมบนขวา: Score / Traps / Deaths
- บนกลาง: `STAGE 1/2   LATE`

**ถ้าเห็นครบ = ประตูนี้ผ่านแล้ว** ที่เหลือคือเทสเกม ไม่ใช่เทสว่าโปรเจกต์พังไหม

### ☐ 3.9 เทสจักรยาน — อันนี้ใหม่ทั้งหมด เทสหนักสุด

จักรยานเป็นระบบใหม่ที่ยังไม่เคยรันเลยแม้แต่ครั้งเดียว เดินไปทางขวาเรื่อยๆ แล้วเช็คตามนี้:

- [ ] ที่ **x ≈ 69** (ในล็อบบี้) เจอจักรยาน แตะแล้ว**ขึ้นขี่เอง** ไม่ต้องกดปุ่ม
- [ ] ขี่แล้ว**เร็วขึ้นชัดเจน** และ**กระโดดเตี้ยลงชัดเจน**
- [ ] **ลงเองไม่ได้** ไม่ว่าจะกดปุ่มอะไร
- [ ] ที่ **x ≈ 90** เจอที่จอดอันแรก → **จอดได้** (อันนี้ของจริง วางไว้ใจดีเพื่อสอนว่าที่จอดใช้งานได้)
- [ ] ที่ **x ≈ 136** เจอที่จอดอันที่สอง → **จอดไม่ได้** และเกมต้องบอกอะไรสักอย่าง
      ไม่ใช่เงียบเฉยๆ (อันนี้ของปลอม เป็นมุก)
- [ ] ที่ **x ≈ 169** เจอที่จอดอันที่สาม → **จอดได้**
- [ ] **ขี่รวดเดียวจาก x 136 ถึงเส้นชัยได้จริง** — ข้อนี้สำคัญที่สุด generator รับประกันไว้ว่า
      คนขี่ต้องไปต่อได้เสมอ (กฎข้อ 9) ถ้าจริงๆ แล้วติด แปลว่ากฎกับเกมไม่ตรงกัน
      **นั่นคือบั๊กที่ร้ายแรงที่สุดที่จะเกิดได้ในโปรเจกต์นี้**
- [ ] ตายตอนขี่อยู่ แล้วเกิดใหม่ → พฤติกรรมต้อง**เหมือนเดิมทุกครั้ง** (จะยังขี่อยู่หรือลงไปแล้วก็ได้
      แต่ต้องอย่างเดียวกันทุกรอบ)

### ☐ 3.10 เทสด่าน 2 (ด่านของคริน)

เปิด `Level2.unity` กด Play:
- การ์ด `STAGE 2  INSIDE` เวลาเริ่มที่ **65**
- Hierarchy ประมาณ **49 root object**
- Console 0 error

แล้วเช็คของที่แก้ไปในด่านเขา:
- [ ] หลุมแรก **5.00 หน่วย** ข้ามได้จริงด้วยความเร็วเดียวที่มี (ไม่ต้องกดอะไรเพิ่ม)
- [ ] แท่นปลอมเหนือหลุมแรก **มองเห็น** และเหยียบแล้วร่วง (เดิมมันโปร่งใส = ช่วยคนเล่น ผิดจุดประสงค์)
- [ ] **เส้นชัยมีพื้นให้ยืน** (`Ground_Exit` — ของเดิมเส้นชัยลอยอยู่กลางอากาศ)
- [ ] ก้อนหินที่ x 33 **ตกจริง** ส่วนที่ x 47 **ไม่ตก** (อันหลังคือของครินที่ไม่มีสคริปต์ เก็บไว้เป็นมุก)
- [ ] checkpoint อยู่ที่ x 2 / 12 / 26 / 55 กระจายกัน (เดิมซ้อนกันหมดที่ x≈0)
- [ ] ตกลงหลุมแล้ว**ปีนออกไม่ได้** และประตูวาร์ป 2 บานข้างล่างทำงานทั้งคู่

> ที่ต้องเช็คทีละ scene เพราะบั๊ก `CampusBackground` รอบก่อนคือ "ด่าน 1 มีพื้นหลัง ด่าน 2 ไม่มี"
> — บั๊กแบบนี้เห็นได้ก็ต่อเมื่อเปิดทุก scene เท่านั้น

### ☐ 3.11 เทสรอยต่อระหว่างด่าน

จาก Level1 เล่นให้จบ → ต้องขึ้น `STAGE CLEAR` (ไม่ใช่ `YOU MADE IT!`)
→ กด Space → เข้า Level2 เวลา 65 ชีวิตกลับเป็น 3
→ จบ Level2 → ต้องขึ้น `YOU MADE IT!` พร้อม**คะแนนรวมทั้งรัน** ไม่ใช่แค่ของด่าน 2

---

## 4. เสร็จแล้วค่อย commit

**อย่า commit ก่อนข้อ 3.11 ผ่าน** — เพราะตอน Unity import มันจะเขียน `.meta` เพิ่ม
และอาจปรับ `EditorBuildSettings.asset` เอง อยากให้ของพวกนั้นอยู่ใน commit เดียวกัน

ปิด GitHub Desktop ก่อน แล้วเปิด PowerShell:

```powershell
cd C:\Users\tjhae\Y4\Programming7\Final\LateToKOSEN
git reset          # ซ่อม index ที่ค้าง ไม่แตะไฟล์เลย
git status
git add -A
git commit -m "Two stages: Krin's level as stage 2, new stage 1, Anywheel bike, no sprint"
git push
```

`git status` รอบนี้จะเห็น `deleted: Assets/Scenes/Level3.unity` และ
`deleted: Assets/Scripts/BicyclePickup.cs` — **ถูกแล้ว อย่า checkout กลับมา**

---

## 5. กฎ 3 ข้อที่ห้ามลืม

1. **ห้ามแก้ไฟล์ใน `Assets/Scripts` หรือ `Tools/` ผ่าน shell/script ฝั่ง Linux**
   mount ฝั่ง Linux เสิร์ฟ **ต้นไฟล์ที่ถูกตัดทิ้งท้าย** ของไฟล์ที่เพิ่งถูกเขียนจากฝั่ง Windows
   โดยไม่มี error อะไรทั้งนั้น เช็คจริงเมื่อคืนนี้:

   | ไฟล์ | mount อ่านได้ | ของจริงบน Windows |
   |---|---|---|
   | `CampusBackground.cs` | 59 บรรทัด | 147 บรรทัด |
   | `PlayerController.cs` | 189 บรรทัด | 216 บรรทัด |
   | `HudUI.cs` | เจอ NUL ต่อท้าย | ปกติ |
   | `GameManager.cs` | เคยอ่านได้ 196 | 309 บรรทัด |

   ใครอ่านผ่านทางนั้นแล้วเขียนกลับ = **ตัดไฟล์จริงทิ้งเงียบๆ** โดนมาแล้ว 2 รอบ
   (`Tools/level_kit.py` กับ `PROGRESS.md`) จะแก้ ให้แก้ใน Unity / VS Code บน Windows เท่านั้น

2. **สคริปต์ที่รันแล้วไม่ print อะไรเลย ให้สงสัยว่าไฟล์ถูกตัดก่อน** อย่าเพิ่งไปสงสัย logic
   เช็คจำนวนบรรทัดสองฝั่งให้ตรงกันก่อนเสมอ และ**ไฟล์ที่ลงท้ายกลางประโยค = ถูกตัด**

3. **ห้ามขยับ object ใน Scene แล้วเซฟ** ถ้าอยากปรับ level — ทุกอย่างถูก generate จาก
   `Tools/stage1.py` กับ `Tools/stage2.py` รันทีเดียวทับหมด
   ปรับ balance ให้บอกเป็นตัวเลข x แล้วแก้ที่ไฟล์นั้น
   ยกเว้น `startingTime` กับ `startingLives` ของ `GameManager` — 2 ตัวนี้แก้ใน Inspector ได้

---

## 6. ถ้ามันพังหนักจนงง — ปุ่ม reset

ถ้า Unity มั่วไปหมด (prefab ชมพู, missing script เต็มไปหมด) แต่ไฟล์ `.cs` ถูกต้อง:

1. ปิด Unity
2. ลบโฟลเดอร์ `Library/` ทั้งอัน (ห้ามลบอย่างอื่น — `Library/` คือ cache ล้วนๆ สร้างใหม่ได้)
3. เปิด Unity ใหม่ → มัน import ใหม่หมดตั้งแต่ต้น (ช้า 3–10 นาที)

อันนี้แก้ได้เกือบทุกอาการที่เกิดจาก "ไฟล์ถูก แต่ cache เก่า" ซึ่งเป็นอาการปกติของโปรเจกต์
ที่ถูกสร้าง asset จากข้างนอกแบบนี้ **และรอบนี้มีโอกาสเจอสูงกว่าปกติ** เพราะ `Level3.unity`
ถูกลบไปทั้งที่ Unity เคย cache มันไว้แล้ว

---

## 7. Crash `TempOverflow` ตอนกด Play (28 ส.ค. 2026) — สาเหตุจริงและวิธีกัน

**อาการ:** กด Play แล้ว Unity เด้ง `Fatal Error!`

```
Could not allocate memory: System out of memory!
Trying to allocate: 18446744059507624804B with 16 alignment.
MemoryLabel: TempOverflow
```

**ตัวเลขนั้นไม่ใช่ RAM เต็ม** — `18446744059507624804` = 2⁶⁴ − 14,201,926,812 คือ
**ค่าติดลบ ~13.2 GB** ที่ underflow วนไปเป็นเลขบวกมหาศาล ตอน crash log บอกว่าใช้ RAM จริงแค่
`ALLOC_DEFAULT used: 203214920B` = 203 MB รวมทุก allocator ~250 MB

**stack trace จาก `editor_log.txt` ชี้ตรงเป๊ะ:**

```
PlayerLoopController::EnterPlayMode
  EditorSceneManager::RestoreSceneBackups     ← restore backup ของ session ที่ crash ไปก่อนหน้า
    StopAssetImportingV2Internal
      ImportOutOfDateAssets
        ScriptingInitializer::FinalizeReload  ← forced synchronous recompile กลาง Play
          MonoManager::FinalizeReload
            CodeReloadSerialization::RestoreAndAwakeManagedObjects
              SerializableManagedRefsUtilities::RestoreBackups
                Transfer_Blittable_ArrayField<StreamedBinaryRead, Vector3f>
                  core::vector::resize_buffer_nocheck
                    MemoryManager::OutOfMemoryError   ← ตาย
```

อ่านจากล่างขึ้นบน: Unity กำลัง **restore managed state ข้าม domain reload** อยู่ แล้วเจอ
array length ที่เป็นขยะ เพราะ blob ที่ backup ไว้ถูกเขียนตอน assembly layout เป็นอีกแบบ
(session ก่อนหน้าที่ Safe Mode / crash ไป) พอ deserialize ก็ขอ memory เป็นเลขติดลบ → ตาย

**ยืนยันว่าไม่ใช่บั๊กในโค้ดเกม:**

- crash เกิดใน `MonoManager::FinalizeReload` — **ก่อน `Awake()` ตัวไหนจะรันสักตัว**
- ไล่อ่านสคริปต์ครบทุกไฟล์ ไม่มีตัวไหนมี field เป็น `Vector3[]` หรือ `List<Vector3>`
  (`grep -rnE "Vector[23]\[\]|List<Vector[23]>" Assets/Scripts` → 0 match)
- ไม่มีตัวไหนใช้ `[SerializeReference]` เลย
- `MemorySettings.asset` / `TimeManager.asset` / `Physics2DSettings.asset` เป็นค่า default หมด
- asset ที่ใหญ่ที่สุดในโปรเจกต์คือ `background_kosen.png` **14 KB**

**เงื่อนไขที่ทำให้เกิด (ต้องครบทั้ง 3 พร้อมกัน):**

1. session ก่อนหน้าปิดไม่สนิท → เหลือ scene backup ค้าง
2. ตอบ **Yes** ที่ dialog `Recovering Scene Backups`
3. กด Play ตอนที่ script ยังคอมไพล์ไม่เสร็จ → Unity ยัด domain reload เข้าไปกลางทาง `EnterPlayMode`

**วิธีกัน — จำ 2 ข้อพอ:**

| สถานการณ์ | ทำ |
|---|---|
| dialog `Recovering Scene Backups` โผล่ | กด **No** เสมอ (scene จริงอยู่ใน git อยู่แล้ว backup พวกนี้ไม่มีค่า) |
| จะกด Play | ดูมุมขวาล่าง ไม่มี spinner ค่อยกด |

**ถ้าเกิดซ้ำ:** ปิด Unity → ลบ `Library/` (ข้อ 6) → เปิดใหม่ → รอ import จบ → ค่อย Play
