# Skill Upgrade Evaluation Protocol (Skill Eval Protocol)

> **Purpose**: after every upgrade of this skill, how to **prove it actually got better**, rather than "it feels smoother after the edit."
> This protocol extends the "five-layer re-check" of `skill-package-upgrade-review` to the output layer. The five layers check the package's own consistency. This protocol checks whether output quality actually improved.

---

## I. Five Iron Rules (violate any one and the evaluation conclusion is void)

1. **Fixed cases first**: before the upgrade, freeze a case set (genre, tier, episode number, requirements). Run the same set before and after, and compare item by item.
2. **Don't treat a sample used for rule-tuning as independent acceptance**: any sample you repeatedly reviewed while tuning rules is already leaked, and it cannot prove generalization. You must keep holdout questions.
3. **Blind review over self-review**: reviewers (human or another model) must not know which draft is pre- or post-upgrade. They judge only "does the drama hold up" using the issue cards in `script-doctor-protocol.md`.
4. **Layered evidence labels**: every conclusion must state its source level: **programmatic** (validator-reproducible) > **model judgment** (consistency across two runs of the same prompt) > **human feedback**. Never blend the three into one sentence like "works better."
5. **No bare regressions**: some scores may drop, but you must explain why that is acceptable. (E.g., a new rule tightened the quota, so a sample now FAILs. If that sample really was padded, it is an improvement.)

---

## II. Case-Set Composition (three parts)

| Type | Count | Purpose | Allowed for rule-tuning? |
|---|---|---|---|
| **Fixed cases** (regression) | 5-8 | Run on every upgrade to prevent backsliding | Yes (the whole point is to watch them for regressions) |
| **Holdout questions** (holdout) | 2-3 | Run once, at final acceptance only, to test generalization | **No**. They must not be viewed during the upgrade |
| **Adversarial cases** (adversarial) | 3-5 | Designed to test whether the rules can be circumvented | Yes |

**Directions for building adversarial cases** (real pitfalls this project has hit):
- Using monologue to pad dialogue-line counts and bypass the exchange-structure check (closed in v3.4; see `inner-monologue-vo.md`)
- Stuffing body text into field lines to inflate volume (closed in v3.2)
- Chopping long sentences to dodge the single-line length cap (covered by the N12 protective counterexample)
- Piling up low-information action lines to pad volume (covered by N13)
- Long tier: writing the mid-episode hook as a climax, or filling three minutes with Round A rhetoric (covered by E11 + red line 9)

**Where the case set lives**: fixed and adversarial cases ship with the package (`examples/` can be extended to `examples/eval-cases/`). Holdout questions are kept by the user and are **not** written into the package.

---

## III. Evaluation Workflow (six steps)

```text
Freeze case set → run baseline (old version) → run candidate (new version) → validator regression (programmatic) → blind review (model / human) → produce comparison report
```

1. **Freeze the case set**: specify genre, tier, episode number, input (premise / source-novel summary), and delivery requirements.
2. **Run the baseline**: run the full case set on the old version and archive it. This becomes the anchor for all later comparisons.
3. **Run the candidate**: run the same set on the new version and archive it likewise.
4. **Validator regression (programmatic evidence)**: both scripts' `--self-test` must PASS. Run `validate_episode.py` on all cases and record changes in FAIL / WARN / NOTE counts. This layer is hard evidence and takes no part in scoring.
5. **Blind review (judgment layer)**: strip identifiers from the old and new drafts and shuffle their order. Reviewers score using the issue cards: P0/P1 issue counts, whether the causal chain holds, and whether emotion lands. Never give a "hit prediction" or total score at this layer.
6. **Produce the comparison report**: one page, three sections: programmatic differences (reproducible), blind-review differences (level-labeled), and the holdout conclusion (given only once).

---

## IV. Judging Criteria (no total score)

**Don't ask "which is better." Ask only four answerable questions:**

| Question | How to judge |
|---|---|
| What did the new version **fix**? | Issue cards present in the old version but absent in the new (list each item) |
| What did the new version **introduce**? | Issue cards present in the new version but absent in the old (this is the cost of the upgrade and must be listed explicitly) |
| Does the new version still hold on the **holdout** questions? | Holds / partly holds / doesn't hold (doesn't hold = this upgrade is not a success) |
| Can the new rules **be circumvented**? | Were all adversarial cases blocked? Log any misses for the next round |

**Forbidden outputs**: total scores, star ratings, "hit rate up X%." Numbers create false precision, and this project has no platform-level feedback data to back them. Popularity metrics are inconsistent and serve only as trend references.

---

## V. Boundaries with Source Material

- The "blind review / holdout / evidence layering" in this protocol comes from evaluation practice in the external JYY v3.8 package. It is a transferred method, not a measured conclusion of this project.
- This protocol does **not** adopt "replace validators with model scoring." Countable items the validator can judge (volume / counts / length / position) always go through the script. The model judges only "does the drama hold up."
- A holdout question is burned after one run (once seen, it is no longer a holdout). The next upgrade must use new questions.
