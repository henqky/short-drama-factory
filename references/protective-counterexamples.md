# Protective Counterexamples (Keeping Machine Checks from Failing Good Drafts · v4.9 Upgrade)

> **Purpose**: The validators (`validate_episode.py` / `validate_series.py`) are deterministic rules; they only count. Counting correctly is not the same as judging correctly. **Every hard metric can wrongly penalize a scene that works.** This file lists what is explicitly *not* a defect, and provides **NOTE-level** hints (explicitly labeled "not a failure") as counter-signals for the validators.
>
> **Trigger**: read this before running the validators, before revising based on validator results, and before grading review comments. Read here before acting on any FAIL/WARN, so you can tell which items are rule prompts and which are real defects.
>
> **Source**: the "counterexamples that must not be auto-failed" column of the jyy-script-eval scoring rubric in the external JYY v3.8 package (an external source file, **not included in this package**; do not look for it by in-package path). Mapped item by item to the Hongguo validator checks, with v4.9 adding boundary counterexamples for `E24-E26`.

---

## §1 Three Output Levels: FAIL / WARN / NOTE

Validator results have three levels, and each is handled differently:

| Level | Meaning | Handling |
|---|---|---|
| **FAIL** | A hard constraint is not met (volume far out of range, missing cliffhanger, missing mid-episode hook, compliance red line, scene cap exceeded, duration inflated or downgraded) | **Must fix**, then rerun |
| **WARN** | A suspicious point needing **human review** (over-long line, banned opener words, too few dialogue lines, talking-only gap, untranslated jargon, ineffective micro-gesture) | After review it may be judged "valid" and passed, but in normal production it should be eliminated first |
| **NOTE** | Protective-counterexample hint: **explicitly not a defect**; a reminder not to over-correct | **No change required**; if it really is over-correction, roll it back |

> ⚠️ **Treating a NOTE as a FAIL is the number-one error this document exists to prevent.** Seeing a NOTE and rushing to edit will break good drafts.

---

## §2 Item-by-Item Counterexample Table

| Check | What it's likely to wrongly penalize | Counterexample (cases not to fail) | Correct handling |
|---|---|---|---|
| **E1 body volume range** | Cutting necessary process to hit the target / padding to hit the target | Some episodes are naturally short (aftermath, pivot); some episodes genuinely need long process | First merge repeated explanations, let one action serve several purposes, and adjust event load. **Never cut a decision or reaction whose removal would make causality jump.** |
| **E2 single line ≤17 words** | Forcibly chopping complete direct speech into fragments | **Complete, accurate, polite direct speech is valid**; long sentences under power pressure, procedural talk in formal settings, professional handling | If sentences are broadly chopped just to pass the check → revert to full phrasing (see N12) |
| **E3 scene-count cap** | Splitting one continuous action into multiple scenes artificially to meet the count | One continuous scene can contain several changes of action; a single event may span scenes | Split scenes for real time-and-place reasons, not for count targets |
| **E4 golden first 3 seconds** | — | None (this is a red line; **no counterexamples**. Action-Persistence episodes may open on an "abnormal action") | Every tier must cut straight into conflict or an abnormal action |
| **E6 cliffhanger** | Cutting off an answer for no reason just to manufacture a hook | When the episode's payoff is already delivered, the hook only needs to be an unmade choice, a guess about to be tested, or a new cost | A hook may not erase the payoff the episode owes |
| **E7 emotion shift** | Every episode written at the same volume and the same direction | **Quiet, aftermath, and build-up scenes are valid**; emotion need not be pushed to an extreme every episode | A quiet scene only needs a clear emotional point of view and must change the relationship, meaning, or state |
| **E9 minimum dialogue lines** | Forcing in filler dialogue | **A brief reaction with no dialogue can still carry weight**; silence, care, or a single action can drive the scene | When short, check the exchange structure first, rather than adding dialogue |
| **E8 repetition detection** | Flagging functional repetition as a defect | **Repetition that works**: requests, mockery, accusation, confirmation, retraction, mishearing, small talk | If a repetition carries a new function, keep it and note the reason |
| **E10 compliance red line** | — | None (**automatic veto**; no counterexamples) | Depict violence impressionistically: "thrown back by the force," "bones crack," "falls to the ground" |
| **E11 long-tier mid-episode hook** | Writing the mid-episode hook as the episode's climax | The mid-episode hook is a **single release** of new information or a new threat, not a second climax | Round B must escalate twice, but the hook stays at about the 90-second mark |
| **E24 talking-only gap (more than 6 consecutive lines with no △)** | Stuffing in filler gestures like "he nods" or "she blinks" just to clear the alert | Rare cases: a fast courtroom volley of questions, or telegraphic rapid-fire interruptions (total under 10 seconds, and backstopped by the E19 63-word window) | **Never fill the gap with ineffective micro-gestures (this triggers E26).** Insert real visual anchors instead: show a physical exhibit, a body movement forward or back, or a contrasting hands-on action |
| **E25 riddle/jargon alert** | A villain deliberately speaks mystical jargon and the protagonist exposes it on the spot | When the villain uses jargon and the very next line has the protagonist mock and expose it in plain speech (e.g., "Stop with the fate-anchor nonsense, you just want me to sign a slave contract") | As long as plain-speech exposure follows immediately, human review can pass it. If the protagonist is also speaking in riddles, rewrite to plain, direct speech |
| **E26 ineffective micro-gesture alert** | Restrained expressions in a quiet, healing scene | If the same △ line contains both an expression and a concrete physical exhibit or body action (e.g., "She startles slightly; the medicine bowl in her hand shatters on the flagstones"), the validator does not false-flag it | Only when the whole △ line contains nothing but "eyes flicker / lost in thought / moves forward half an inch" with no filmable physical result must it be replaced with a visible action |

---

## §3 Three Counter-Signal Hints (NOTE level)

The following three items are output automatically by `validate_episode.py`. **They are reminders that you may have over-corrected, not defects.**

### N12 Fragmented-dialogue hint
> Trigger: 5 or more consecutive dialogue lines, each with ≤3 words of net content.

Meaning: this may be a mechanical chopping of complete sentences into telegraphic riddles, done to dodge the "single line ≤17 words" cap. **Variable speed (2-3-word sharp lines alternating with 5-10-word ledger lines) is a good rhythm.** Five or more consecutive lines of two or three words each leave the audience unable to follow the cause and effect.
Handling: keep the 1-2 key short, sharp lines (e.g., "You dare!" "Look closely!"), and merge the rest of the fragments into complete plain-speech sentences that lay out the ledger clearly.

### N13 Action-line padding hint
> Trigger: ≥12 action lines with an average net length of ≤9 words, while dialogue lines are at or below this tier's floor.
> ⚠️ **Exemption**: scripts tagged 【Conflict Mode】: Action-Persistence / Mixed do **not** trigger N13. Many actions and few lines is simply the signature of the action form (preparation × doubt), not "padding volume with actions." (Types ③④⑤ and the default are still judged by the Dialogue standard.)

Meaning: this may be low-information action lines piled up to meet E1 volume. **More action does not mean more drama.**
Handling: return to event load. Merge repeated proofs, and let one action serve character, clue, and emotion at once, instead of adding more action lines.

### N14 Thin-episode-at-floor hint
> Trigger: body volume near this tier's floor (≤ floor + 10 words) and the net word count of the cliffhanger section <13.

Meaning: this may be necessary process cut to reach the floor, or a cliffhanger written too thin. **Necessary process must never be cut just to clear a threshold.**
Handling: if a decision or reaction whose removal would break causality was cut, restore it and explain why. If the episode itself holds up (an aftermath episode, or a fast-paced pivot episode), state the reason in the delivery notes and move on.

---

## §4 NOTE Handling Procedure

```text
NOTE raised
  ├─ Review: is this a "rule hint" or did we really break it?
  │    ├─ Original already holds up → leave it; log one line in delivery notes: "NOTE reviewed, judged valid"
  │    └─ Really broke it to pass the check → roll back to the previous version
  └─ Never run another round of "optimization" because of a NOTE
```

**Rollback criteria** (any one of these means the draft was broken and must be rolled back):

- The logic runs smoother, but the characters have become flatter;
- The laughs, the pressure, the intimacy, the flaws, or the aftertaste have disappeared;
- Emotion has been resolved early;
- Stylized full sentences have been uniformly chopped into fragments;
- Padding was added to pass the check, or necessary process was removed.

---

## §5 Connection to the Review Protocol

- NOTE belongs to the **validator layer** (`scripts/`); the review issue cards belong to the **human layer** (`script-doctor-protocol.md`). The two do not replace each other.
- A reviewer **must not** open an issue card just because the validator reported a WARN or NOTE. **Verify first** (see `script-doctor-protocol.md` §5).
- The reverse also needs guarding against: **do not treat "all validators pass" as a quality verdict.** Passing only shows that structure and on-screen density are compliant. Whether the drama actually works is judged by `craft-quality-layer.md`.
