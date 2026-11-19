# Script Review and Repair Protocol (Reviewer / Repairer Dual Roles)

> **Purpose**: This file is the **operating standard** for the "script doctor" stage. The original `dialogue-doctor-anti-ai.md` only treats the AI flavor of dialogue and is **local surgery**; this file covers the **complete review-repair loop**: how to diagnose, how to grade, whether a note should be accepted, how far a revision must go to count as done, and when to stop.
>
> **Triggers**: The user asks to "review / check whether this draft works / help revise it / script doctor / this episode is close but not there / recheck"; or the pipeline reaches Step 4 (polish) or Step 8 (compliance recheck). **Must read** in those cases.
>
> **Sources**: Integrated from the evidence-based issue cards and repair discipline of JYY v3.8 `jyy-script-review` / `jyy-script-repair`, mapped onto Hongguo tier and paywall standards.

---

## §1 Two Roles, Don't Mix Them

| Role | Does only | Never does |
|---|---|---|
| **Reviewer** (`/script-review`) | Judges whether the draft delivers the agreed viewing experience, and gives **verifiable problems** and revision targets | **Does not rewrite on the author's behalf** (unless the user explicitly asks for edits) |
| **Repairer** (`/script-revise`) | Makes the **minimum sufficient edits** within the **authorized scope**, and delivers a complete draft that can be swapped in directly | Does not expand scope on its own, does not rewrite unauthorized sections, does not "beautify in passing" |

Process principle: **review first, then repair.** Once a draft is written, run the review first; the review's issue cards then go to the repairer. Skipping review and editing straight away most easily produces a "flat draft with no specific defects but also no flavor."

> Diagnosis and revision are **output separately**. The review report must not smuggle in revised body text; the repair delivery must not carry a long self-assessment.

---

## §2 Three Review Intensities

| Mode | Used for | How much is read | Output |
|---|---|---|---|
| `quick` (default) | A freshly written first draft | Only the range the user specifies | 3–5 problems that most affect viewing + **strengths that must be kept**; **do not fill out the full table** |
| `focused` | Rechecking one item (dialogue / cliffhangers / continuity / paywall placement) | The affected adjacent segments + necessary prior facts | Conclusion for that item; other dimensions marked **Not tested** |
| `final` | Delivery acceptance, before the full set is submitted | Read through the agreed delivery range, verifying in batches | Full dimension status + reading coverage + major unresolved cross-unit items |

**If it can't all be read, say so**: when the actual readable amount is exceeded, state clearly "read episodes X, did not read episodes Y," deliver partial conclusions, and **do not claim a full pass**. A focused pass **does not equal** a pass of the whole draft.

---

## §3 Issue Card (eleven fields)

Every important problem uses this set of fields. They may be merged into natural language, but **evidence and impact must not be omitted**:

```text
id                  / Problem ID (merge the same root cause into one entry; do not double-count)
scope               / Scope (which episode, which scene, which round)
severity_by_impact  / Severity by impact: P0/P1/P2
evidence            / Evidence: draft version + episode/scene + verbatim short quote
observation         / What is observed (describe only what is in the text)
interpretation      / Why it may damage the goal
target              / The audience experience to improve (not "change it to ...")
protected_effects   / Existing strengths that must be preserved (may not be lost after the edit)
allowed_edit        / Permitted scope of edits (give a sufficiently small suggested range)
downstream_checks   / What to recheck downstream (same-period dialogue, later episodes, ledger)
status              / open / resolved / rejected / to-verify
```

Iron rules:
- **`evidence` must be checked verbatim against the source text**; never quote from memory;
- If support cannot be found, mark **`to-verify`**; **do not pad the problem count**;
- Run a **minimal check** on plausible alternative explanations before passing judgment;
- `target` states "what experience to improve," and **never "change line 3 to ..."** — the fix is a candidate, not a command.

---

## §4 Severity: By Impact, Not by Category

| Level | Criterion | Typical Hongguo Cases |
|---|---|---|
| **P0 Blocking** | The core viewing promise or an explicit delivery requirement fails | Winning or losing is incomprehensible; the ending holds up only through unsourced information; dialogue across the whole episode stays hard to follow; the agreed core emotion never happens; no cliffhanger hook at the paywall point |
| **P1 Major** | An important section or a recurring problem significantly weakens the experience, but does not make the core delivery fail overall | A whole episode of attack-and-defense spinning in place; the protagonist lacks ownership of results; a unit closes but only adds hooks without payoff |
| **P2 Local** | Affects local flow or expression and can be fixed within a limited range | Single-scene information repetition; inconsistent forms of address; a line that doesn't fit the speaker's identity |

**Key points**:
- **A single critical error can also be P0**; a high count **does not automatically** make something P0;
- If dialogue, comedy, or aftertaste is itself the core product of this project (for example, the "warmth" of a heartfelt project), **it can also block delivery**;
- **No critical failure may be offset by other strengths**, and "not tested" must not pass for "passed";
- Do not output **S/A grades, total scores, or hit predictions**.

---

## §5 Verify Notes First, Then Decide Whether to Accept

On receiving an issue card, the repairer's **first step is to verify whether it holds in the current version**, not to start editing. The following cases in particular require a recheck:

- The note comes from an **old version** (already overwritten by later edits);
- **No short source quote is given**;
- The note marks "direct speech / silence / a reasoned second-best choice" as bad across the board;
- The note **does not state its applicability conditions** (for example, it assumes "must be 9:16," "the paywall must be at episode 10," or "must be a female-lead drama");
- The note's **factual premise is already satisfied by the body text** — then it may no longer be treated as a defect; it can only be rejected, or rewritten as an optional enhancement with explicit conditions.

The disposition must be one of four: **Accepted / Partially accepted / Rejected / To verify**, with a brief statement of the basis for any important disagreement.

> **A reviewer's aesthetic preference is not a command.** Directness vs. restraint, strong payoff vs. warmth, serious vs. comedic are decided by the project's goals, not by whoever speaks loudest.

---

## §6 Conclusions in Three Layers, Don't Mix Them in Reporting

| Layer | Content | Scope of this skill |
|---|---|---|
| **Text quality** | Comprehension, characters, dialogue, emotion, process, aftertaste, continuity | Fully owned by this skill |
| **Platform fit** | Tier volume, scene count, golden first 3 seconds, cliffhanger placement, paywall ranges, compliance red lines | Fully owned by this skill (machine check as backstop) |
| **Production fit** | Aspect ratio, shot breakdown, assets, subtitle fonts, AI-generation feasibility | **Outside the scope of this skill**; explicitly mark as "not covered." Do not certify "filmability," "compliance," or "commercial success" from the script body |

Mark each dimension **Pass / Risk / Fail / Not tested**, and state its applicability; do not impose acceptance criteria on targets that were not agreed.

**Common misjudgments to correct**:
- Less dialogue **does not automatically** mean visual; more action **does not automatically** mean dramatic;
- Silence that works and empty flatness are **judged separately**: do not use "the dialogue is fine" to stand in for the whole segment being effective, and do not uniformly add arguments;
- Volume does not automatically mean poor quality just because it exceeds the target, and it must not be waved through because the numbers match when scenes are padded, filler is present, or episodes are split mechanically.

---

## §7 Repair Discipline and Regression Judgment

1. **First read the affected passage, necessary prior material, and downstream dependencies**, and settle the viewing effect to improve and the strengths that must be kept. Downstream content that is missing is marked as unverified; **do not fabricate facts**.
2. **Choose a sufficient repair level**: wording → scene → episode → core relationship / story drive → unit restructure.
   - If a local patch cannot solve a positioning or relationship failure → **regenerate the whole section from the upstream layer**; do not keep stacking patches;
   - But do not jump straight to restructuring — **if a fine adjustment works, make the fine adjustment**.
3. **Replace first; add only what is truly missing**: first check for repeated explanation, repeated proof of the same emotion, and unrelated procedure; run deletion / merge trials on complete passages, and if the loss affects understanding, characters, the genre experience, or necessary aftershocks, restore it or change the implementation.
4. **Recheck after every edit**: the target problem + affected continuity + **protected effects**. If a new problem comes from this edit, revert it.
5. **Sweep across episodes**: when you fix one line, sweep **all problems of the same kind within the same episode**, not just the one line that was pointed out.

### Regression judgment (signs the edit made things worse)

Any one of the following counts as a **repair regression**, and must be rolled back or re-implemented:

- The logic runs more smoothly, but **the characters have gone flat**;
- Jokes, pressure, intimacy, flaws, or aftertaste **have disappeared**;
- The emotion has been **resolved early** (no room is left for it to travel later);
- A stylized complete sentence has been **colloquialized** into uniform fragments;
- Padding has been added or necessary process has been **deleted** just to pass the machine check.

### Stop condition

If the same problem shows **no improvement after two consecutive edits** → change the implementation approach, narrow the unit of this revision, or return to upstream ideation. **Do not loop on self-checks indefinitely, and do not claim a pass**; for problems that truly cannot be solved, record the status honestly and deliver.

---

## §8 Delivery Format

**Review delivery**: first give the conclusion and biggest impact for the current scope, then list **preserved effects**, the issue cards in priority order, and next steps.

**Repair delivery**:
- A short change report (problems actually solved / notes rejected or unresolved / protected items / verification boundary);
- A **complete replacement draft** for the agreed scope — the body must **not** contain "rest unchanged," "same applies later," or "omitted";
- Mark **original → revised** and the episodes/scenes changed; when scenes are merged, split, or reordered, provide an **old-scene → new-scene mapping**, keeping the numbering and forms of address of unaffected parts;
- When a long draft is delivered in batches, the checklist must distinguish **completed** from **pending** scope; a batch's output must not be called completion of the whole series.

**Iron rule**: the body must stand on its own apart from the report; the report cannot substitute for the body.
