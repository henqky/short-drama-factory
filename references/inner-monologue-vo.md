# Controlled Protocol for Inner Monologue and Narration (Inner Monologue / Voice-Over)

> **This library fills a gap the whole library had before**: through v3.3, none of the 24 files in the full package had a single positive rule governing non-spoken narrative channels. The only six mentions were prohibitions or validator whitelist entries ("no long narration establishing the era," "settings may not be established by narration," "golden-finger reveals do not rely on narration"). At the same time, red line 2 (no dialogue explaining setting) stacked on the micro-expression rule (only physically observable actions) made it read as if this channel were off by default.
>
> **Conclusion: monologue is not forbidden territory; it is a quota-controlled tool.** Used correctly, it is the final kick. Used too often, it becomes padding and AI-flavored writing. This library specifies where it may be used, how much, how to write it, and how the validator judges it.

---

## 0. Why this had to be added: source-data basis (live search, 2026-09)

In the Douyin hit-drama timelines we live-searched, inner monologue and narration are **real devices in active use**, and they are used with restraint:

| Source | Timecode | Form | Function |
|---|---|---|---|
| *So What If I'm Old* | 1:13 | Heroine **self-narrates**: "I've toiled my whole life." | Plants the protagonist's grievance; the audience picks a side |
| *So What If I'm Old* | 2:10 | **On-screen caption / narration**: "The meek Zhou Shaohua has fought back." | Thematic pivot: the honest person starts to resist |
| *So What If I'm Old* | 50 s – 2:01 (Act Four) | The whole family takes turns attacking + the protagonist **self-narrates her grievance** | Emotion maxed out; **also uses 30 seconds to explain the family background** |
| *Superhuman Wife of the Seventies* | Opening line | **Self-narration** that establishes the persona: "I can take down a wild boar on the mountain." | An against-type persona that makes the character memorable |

The same source data also draws a boundary: in Act Two, where the "rebirth is revealed," the timeline explicitly notes **"golden-finger reveals do not rely on narration."**

**Two conclusions**: (1) emotion and thematic pivots may borrow monologue; (2) setting reveals (golden finger / worldbuilding) **do not** borrow monologue. This boundary is the master principle of this library.

---

## I. Three Channels and Their Division of Labor (First principle: monologue is not dialogue)

| Channel | Body-text marker | Who can hear it | Function | Line length | Validator ownership |
|---|---|---|---|---|---|
| **Dialogue** | `Character (expression):` | Everyone in the scene | Turn-based conflict | Normal 8-12 words, cap 17 (over-length triggers WARN, not a block) | Counts toward E9 dialogue lines and E1 body volume |
| **Inner Monologue** (OS) | `Inner Monologue:` | **Only the audience** | Planting grievance / externalizing thoughts | Standard ≤17 · Long ≤20 · Comic ≤13 words | **Not counted in E9**; counts only toward E1 body volume; per-instance length checked by E12 |
| **Narration / Caption** (VO) | `Narration:` | **Only the audience** | Thematic pivot / time anchor | ≤8 words | **Not counted in E9**; counts only toward E1 body volume; per-instance length checked by E12 |

**Execution rules**:
- The body text **always uses the English markers** (`Inner Monologue:` / `Narration:`). The abbreviations OS/VO appear only in this table and in internal discussion, never in the body. The format lines are for production staff and reviewers.
- Monologue lines **count toward E1 body volume** (they take up runtime on screen), but **are not counted toward E9 dialogue lines** (they are not turns in an exchange).
- Monologue lines **are not subject to the E2 25-character line cap**; instead they are measured per instance against the E12 limits in the table above.

---

## II. Five Legitimate Uses (Whitelist)

Monologue is valid only if it falls into one of these five categories:

1. **Plant the grievance**: after emotion peaks, add the final kick that locks in whether the audience should sympathize. *Example: I gave him five children.*
2. **Thematic pivot**: at a unit-level or series-level turning point, give the audience one line that sets the tone. *Example: The meek Zhou Shaohua has fought back.*
3. **Establish the character**: one line that makes a person's ability or stance clear. *Example: Can take down a wild boar on the mountain.*
4. **Externalize the unspoken**: a substitute outlet for words that can't be said aloud. **Hard constraint: it must contrast with or add to the action in the same scene; it may not restate the action.** (If the △ already shows her gripping her apron, a monologue that says "I gripped my apron" is padding.)
5. **Age / time anchor**: a line that confirms the coordinates of a rebirth or time-travel. *Example: I actually came back to the year I turned 42.* **But the golden finger itself is never revealed through monologue** (stated explicitly in the source data).

---

## III. Four Prohibitions (red-line level, same weight as the SKILL red lines)

1. **No establishing setting or backstory**: monologue that explains background is the worst AI flavor. Red line 2 ("no dialogue explaining setting") **applies to monologue too, and more strictly**: dialogue can hide behind the opponent's reaction, while monologue is pure exposure.
2. **No restating an action already performed**: whatever the △ has shown, monologue must not say again (zero information, only added word count).
3. **No substituting for conflict**: monologue may not replace the confrontation that should happen. This is also a **validator anti-evasion rule**: before v3.3, monologue was counted as dialogue lines, so monologue could pad the count and bypass the E9 exchange-structure check. v3.4 fixed this.
4. **No back-to-back placement**: two consecutive monologue/narration lines, or monologue directly before the cliffhanger ending, are both rejected drafts. Monologue lines must be separated by action or dialogue.

---

## IV. Quotas (hard limits, validator E12)

| Tier | Inner Monologue | Narration / Caption |
|---|---|---|
| **Standard tier** 90-120 s | ≤1 instance · ≤17 words each | ≤1 instance · ≤8 words |
| **Long tier** 150-195 s | ≤2 instances · ≤20 words each | ≤1 instance · ≤8 words |
| **Comic tier** 60-90 s | ≤1 instance · ≤13 words each | ≤1 instance · ≤8 words |

**Series-level quota**: allowed in pivot episodes, not in aftermath episodes (aftermath episodes land through reaction shots and everyday detail). Narration at most **once per unit**.

---

## V. Placement Discipline (three hard constraints)

1. **Banned in the first 3 seconds**: the golden 3 seconds must be the opponent's pressure. A monologue opening is a soft open, straight into red line 1. Validator E15.
2. **Banned at the cliffhanger**: the cliffhanger must land on a frame or an event. A monologue ending is a soft ending (breaks red line 4). Validator E13.
3. **Placement = after the pressure peak**: place monologue 0.5 seconds **after** the cruelest line has landed, never before it. Before it, monologue is a preview that releases the pressure early.

---

## VI. Division of Labor with the Micro-Expression Rule (Resolving the Apparent Conflict)

`craft-quality-layer.md` requires that △ lines contain only physically observable action, never "his heart is a churn of mixed feelings." **That constraint governs △ action lines; it does not forbid monologue.** The two do not conflict. There is only one test:

| Writing | Verdict |
|---|---|
| A △ line that says "his heart churns with mixed feelings" | **Violation** (unfilmable; psychology mixed into an action line) |
| Monologue that says "my heart churns with mixed feelings" | **Also a violation** (abstract feeling; the audience gets no information) |
| Monologue that says "I gave him five children, and the day he left I was still mending his padded jacket" | **Passes** (a concrete ledger) |

**Rule of thumb: monologue writes the concrete ledger, not abstract emotion.** Validator E14 issues a WARN for abstract emotion words.

---

## VII. Three Writing Templates (ready to use)

| Type | Structure | Example |
|---|---|---|
| **Grievance ledger** | number/year + sacrifice + betrayal | I gave him five children, and the day he left I was still mending his padded jacket. |
| **Thematic line** | subject + pivot verb + short closing clause | The meek Zhou Shaohua has fought back. |
| **Character-setup line** | ability + concrete setting | Can take down a wild boar on the mountain. |

**Counterexamples (obviously fake)**: "My heart is a tangle of feelings, my mind a flood of thoughts" / "It all began thirty years ago" / "Turns out I was dead all along" / "In this life I will make you all pay" (an empty oath with no concrete ledger).

---

## VIII. Platform and Track Differences

- **Hongguo · Family Drama (middle-aged and older audiences)**: self-narrated grievance has the highest acceptance (verified in the source data) and is the main tool for planting grievance. But keep it under 17 words, and give it only once per episode.
- **Douyin · Rebirth / Comeback**: narration and on-screen captions are for thematic pivots; use them sparingly. A caption that repeats what the frame already shows is double waste.
- **Comic drama**: voiceover narration is naturally forgiving (narration is a standard tool in animation), but family and middle-aged comic dramas still keep to ≤1 instance, and narration may not be used to establish setting.
- **Male-led power fantasy**: monologue is rare; prefer action and the opponent's reaction. Male-led audiences tolerate self-pity poorly, and too much monologue kills the rush.

---

## IX. Validator Rules (E12-E15 + E2/E9 corrections)

| Item | Rule | Level |
|---|---|---|
| **E9 correction** | Monologue/narration is **not counted** as dialogue lines (closes the loophole of padding to evade the exchange-structure check) | WARN |
| **E2 exemption** | Monologue is not judged by the 17-word dialogue cap; it is judged by this tier's `os_len` / `vo_len` | — |
| **E12** | Monologue/narration count over quota, or per-instance length over cap | FAIL |
| **E13** | Two consecutive monologue/narration lines; or monologue directly before the cliffhanger ending | FAIL |
| **E14** | Monologue contains setting-exposition signal phrases ("it all started when..." / "that's why" / "as everyone knows...") or abstract emotion words | WARN |
| **E15** | Monologue/narration appears in the first 3 seconds | FAIL |

The validator checks only countable items (count, length, position). Whether a given monologue actually writes a concrete ledger is a judgment call, handled by the issue cards in `script-doctor-protocol.md`.

---

## X. Migration Scope and Sources

- Factual basis for the whitelist and quotas: the Douyin hit-drama timelines live-searched in 2026-09 (*So What If I'm Old* at 1:13 / 2:10 / Act Four; *Superhuman Wife of the Seventies*, opening line).
- The prohibitions inherit the "reverse-exposition death penalty" from `dialogue-doctor-anti-ai.md`.
- **Note**: popularity figures come from a live-search snapshot and serve only as trend references. This library's quotas and placement discipline are **engineering constraints** (preventing padding and validator evasion), **not official platform rules**. If a future upgrade finds a new hit using a stable pattern that exceeds the quotas, decompose it using the three-layer method in `mechanism-imitation.md`, backfill this table, and log one line in the CHANGELOG.
