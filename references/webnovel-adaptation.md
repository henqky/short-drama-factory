# Webnovel-to-Short-Drama Adaptation Pipeline

> New in v3.0: delivers the "one web novel → script" capability. Core principle: **a short drama is not an abbreviation of a web novel; it is an amplification of the single most satisfying emotional thread in the novel.** Cut everything that doesn't serve one obsession or one payoff.

---

## I. The Five-Step Pipeline

### Step 1: Extract (read the source novel / outline; produce three tables)
1. **Emotional-thread table**: list every "face-slap / counterattack / identity reveal / reunion / crushing" showpiece in the whole book, in order of appearance. Record only each event's function, not its details.
2. **Character function table**: each character's function slot (protagonist / pressuring villain / helper / pawn / "white moonlight" love interest). Merge characters who share a name but have different functions. Trim cases where several characters serve the same function.
3. **Genre call**: can the book's emotional experience be condensed into a one-line emotional contract (e.g., "those who looked down on me can't afford to reach me")?
   - If **yes** → emotion-flow adaptation. The contract runs throughout, each source volume's conflicts map to a unit chain, and each unit gets one round-trip table (see `emotion-flow-roundtrip.md` §2.5).
   - If **no** (mystery / puzzle type) → plot-flow adaptation, walking an information ladder.
   - Note: one web-novel volume ≈ one short-drama unit (20-30 episodes). Forcing one volume's conflict across the whole book satisfies neither audience.

### Step 2: Cut and Merge (hard rules for subtraction)
- **Cut subplots**: delete every subplot that doesn't directly affect the main emotional thread. Fold subplot information into main-line props or lines.
- **Merge characters**: merge characters with duplicate functions into one (three disposable ex-partners become one). Demote characters who die on arrival to "named extras" that take up no character-ledger entry.
- **Compress the timeline**: skip all the filler stretches common in million-word web novels ("training / saving money / travel"), and keep only the scenes where relationships change.
- **Iron rule to keep**: for every cut, check whether it damages the "setup build-up for the next payoff." If it does, replace it with one line of dialogue that covers it.

### Step 3: Map (chapter → episode)
- **Unit of measure**: 1 episode = 1 relationship-changing node. (Not 1 chapter! A web-novel rhythm of one payoff per three chapters does not match a short drama's one payoff per episode, so re-sequence.) **Long tier**: 1 long-tier episode = 2 change nodes (two rounds). After conversion, the total episode count is halved in proportion to content volume (30 / 40 / 50 episodes).
- **One episode holds only**: one act of pressure plus one rebuttal or counterattack, or one build-up plus one payoff. If it doesn't fit, split the episode. If it's too thin, merge episodes.
- **Volume-end climaxes** are aligned to paywall episodes (first-, second-, or third-tier). Reshape the pacing before and after to hit cliffhanger positions. Never let cliffhangers bend to the source's chapter order.
- **The first quarter of the source usually lacks material for 15 episodes** (about 7-8 long-tier episodes). Use "added conflict" (move the source's chapter-20 humiliation forward to the chapter-3 position) or "manufactured rounds" (split a one-off misunderstanding into a six-tier evidence ladder).

### Step 4: Unitize and Round-ify (the core operation of emotion-flow adaptation)
First cut into units (20-30 episodes each; 10-15 long-tier episodes). Each unit closes its loop and leaves an ember, and the opponent changes tier. Then hang each unit's showpiece scenes onto the six-tier ladder. Map source scenes that fit a tier. Where a tier is empty, fabricate by the same logic. Fabricated material must respect the boundary in `mechanism-imitation.md` and may not carry expression lifted from other books. **Output**: a unit chain plus one round-trip table per unit.

### Step 5: Load into the System
Turn the adaptation into this package's standard artifacts: greenlight sheet (genre + track + one-line obsession) → character bible → round-trip table + paywall → episode plan → single-episode writing (all routed through the ledger and validators).

---

## II. Adaptation Red Lines

1. **Personas' values can be reworked; the core obsession cannot.** The source protagonist's "won't believe / won't acknowledge / won't submit" is emotional capital. The adaptation must keep it intact or swap in an equivalent.
2. **Never copy showpiece dialogue wholesale** (for both copyright and pacing reasons). Keep the event structure and the punchline's function, and rewrite the expression.
3. **Turn the "worldbuilding exposition" that original-novel fans rely on into visual conflict.** Settings may not be established by narration (the reverse-exposition death penalty applies to adaptation too).
4. For web novels over 200 chapters, the first version adapts only the first third plus the book's 20 strongest showpieces. Leave the rest as season-two material. Do not adapt everything at once.
