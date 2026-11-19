# Five Conflict Modes: The Battlefield Sets the Engine (Conflict Modes)

> **Purpose**: this library answers "which battlefield is the conflict fought on?" Until now, the exchange rules across the library (the turn-taking in `dialogue-doctor-anti-ai.md` Dimension 3, and the round trips in `emotion-flow-roundtrip.md`) assumed the conflict happens in language. That covers only one of the five modes. Identifying the mode means choosing the right skeleton tools and cliffhanger formula. **Only when dialogue is naturally sparse is the validator relaxed.**
>
> **Trigger**: before greenlighting, episode planning, or writing an episode, set the 【Conflict Mode】 first. Writing "the protagonist quietly works and gets mocked" (②) requires reading this file.

---

## 〇 Shared Engine (both drive all five modes)

1. **Information gap**: the audience and the people in the scene know different amounts (audience omniscient / protagonist foresees / each side knows half). The hook is the gap.
2. **Every beat must shift the balance of power, the state, or the understanding**: standing still = leakage.

> The five modes differ only in where the battlefield is: language / behavioral mismatch / identity perception / relationship emotion / puzzle information.

---

## I. Five-Mode Comparison Table

| # | Mode | Battlefield | Hook | Beat | Cliffhanger | Validator |
|---|---|---|---|---|---|---|
| ① | **Dialogue** (blood on the lips) | Language | One line at the peak | Turn-based exchange (pressure → rebuttal → probing → final blow) | Formula 3 contrast punchline / public face-slap | **No relaxation** |
| ② | **Action-Persistence** (blood on the hands, lips shut) | Behavior × mismatched doubt | **Abnormal action** + "why is he doing this?" | Preparation → obstruction escalation loop | **The second before verification** (the omen pays off) | **Relaxed** (see §IV) |
| ③ | **Identity-Gap** (perception ≠ truth) ★ largest mainstream | Identity vs. perception | An omen of an identity reversal | When will he be exposed / will they accept him | **Formula 1: the second before the reveal** | No relaxation (dialogue is normal) |
| ④ | **Relationship-Emotion** (emotional-debt tug-of-war) | Emotional debt in the relationship | The breaking-point image of the relationship | Forgive or not / dare to get close | **Formula 5: Emotion Contrast Landing** | No relaxation (lots of dialogue) |
| ⑤ | **Rule-Puzzle** (information ladder) | Puzzle and solution | An anomalous rule | New clue → misjudgment → case reversed → bigger mystery | Mid-episode hook = the misjudgment confirmed for half a beat; cliffhanger = half the truth revealed | No relaxation (plot-driven) |

**Mnemonic**: ① blood on the lips | ② blood on the hands, lips shut | ③ who is he, really? | ④ do I still want him? | ⑤ what is going on here?

**Mixed**: **action shell + dialogue firepower**. The protagonist, under siege, doesn't explain and just acts. He speaks only at the key beat, with cutting lines (2-3 hard lines per episode). This is a common combination of ② and ① (e.g., "a hoarder gets mocked by the whole building and closes with one cold line on the final beat").

> ⚠️ Identifying the mode ≠ relaxing the validator. ③④⑤ have normal dialogue volume and need no relaxation switches. The mode tag is only there to choose the right skeleton tools and cliffhanger formula. Only ② (naturally sparse dialogue) is relaxed.

---

## II. The Action-Persistence (②) Loop Skeleton

```text
Abnormal preparation (hook: why is he doing this?)
  ➔ Doubt / obstruction ① (neighbors / relatives / family; reasons: embarrassing / wasteful / in the way)
  ➔ Protagonist doesn't explain, keeps preparing ② (escalation: scale / precision / irreversibility)
  ➔ Doubt / obstruction ② (escalate one tier: from mouth to action — reporting / secretly filming / cutting water and power)
  ➔ Preparation ③ (lock down the lifelines: keys / water / power / doors)
  ➔ Verification moment (the omen pays off; the skeptic is stunned)
  ➔ Cliffhanger: lands on the "second before verification" (a bigger catastrophe / the generator doesn't start)
```

**Three iron rules**: ① explaining = losing steam (answer with action, never excuse). ② Each obstruction escalates one tier (repetition = a dead beat). ③ Preparation must be **filmable** (every preparation action changes the situation).

---

## III. Long-Tier (3-Minute) Implementation Formulas

| Mode | Skeleton | Dialogue / action ratio (reference) |
|---|---|---|
| ① Dialogue | Two rounds: Round A shouting match ➔ mid-episode hook ➔ Round B escalated shouting match ➔ cliffhanger punchline | Dialogue-led (E9 ≥8 lines, 25-70% share) |
| ② Action | Preparation ×2 + doubt/obstruction ×2 + **verification segment** (the final-stretch hook drops an omen; the cliffhanger lands on "the second before verification") | **Spoken dialogue ≥300 words + 15-22 action lines ≈150 s** (can stretch to 195 s) |
| Mixed | Action shell + dialogue firepower | 6-8 dialogue lines, ≥15% share |
| ③④⑤ | Keep each one's own skeleton (identity / relationship / puzzle) | Dialogue is normal; judged by the dialogue standard |

> E16 for ②: the validator counts each action beat as ×4.0 s (×1.5 s for Dialogue, ×2.5 s for Mixed). Preparation actions carry the narrative and take up more time. Otherwise the Action type gets squeezed from both sides: "tagged long → reported as inflated; tagged short → reported as downgraded."

---

## IV. Validator Rules (**only ② is relaxed**)

- Required field per episode: 【Conflict Mode】: Dialogue / Action-Persistence / Identity-Gap / Relationship-Emotion / Rule-Puzzle / Mixed (default = Dialogue).
- **② Action**: E9 dialogue-line floor halved (long tier 8→4); E21 dialogue-share floor 25%→**10%**; E16 action-beat weight ×4.0 s; E23 requires 【Skeptic Supporting Character】 (no opponent slot = action log, FAIL); N13 action-padding exemption.
- **Mixed**: E9 long tier 8→**6**; E21 floor **15%**; E16 action-beat weight ×2.5 s; N13 exempt.
- **③④⑤**: always judged by the dialogue standard (the mode tag alone is enough; no relaxation needed).
- **Scene cap scales with episode length**: for custom durations (>195 s), scene cap = max(tier value, about 1 scene per 75 seconds). Example: 300 s → 4 scenes.
- **E4 first 3 seconds**: ② Action hooks are "abnormal actions" (stockpile / move / weld / seal / lock / generator, etc.). These are now part of the E4 signal words, so they are not falsely flagged as the shouting-match type.
- The rest (E19 consecutive dialogue ≤63 words, E2 single line ≤17 words, E16 duration match, E17 long-tier floor, E22 terminology) applies as usual.

---

## V. Post-Writing Self-Check

1. What is the information gap between the audience and the people in the scene? (Can't answer = no engine.)
2. Does every beat in this episode shift the balance of power or the understanding? (No change = cut it.)
3. ②: Does the protagonist make excuses? (Excuses = the runner type.) | Does the skeptic escalate one tier each time? | Is there a verification segment?
4. ③: Is he cut off at "the second before the reveal"? | ④: Is there an emotion contrast landing? | ⑤: Is a misjudgment confirmed?
5. Did the mode identification select the right skeleton tools and cliffhanger formula? (That is the main purpose of identifying the mode. It is **not** to relax the validator.)
