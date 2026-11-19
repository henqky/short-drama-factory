# Dramatic Craft Layer (Universal Quality Base · Hongguo-Adapted · v4.9 Upgrade)

> **Purpose**: This file covers the layer that **machine checks cannot see**: "structurally compliant but the drama is fake, no visual support, pacing spins in place, dialogue wanders and is hard to follow." The machine check (`validate_episode.py`) handles the hard-metric safety net; this layer targets dramatic causality, visual-support density, the 15-second shift-and-advance, and zero-barrier plain-language delivery.
>
> **Triggers**: **Must read** before writing the body of a new episode; when a scene reads as flat narration / has no visual support / has the wrong pacing / the lines take a while to understand / characters only execute tasks; when two consecutive revisions of the same item still show no improvement; and when a long-tier two-round arc reads like two parallel events.
>
> **Sources**: Integrated from the external package JYY v3.8's quality-baseline and dramatic-generation references, plus the product-pattern section of jyy-script-creation-v2 (these are **external source files, not included in this package**; do not look for them at in-package paths). Fused with the three battle-tested rules from real viewer feedback in v4.9: "strong visual support + 15-second shift + plain language delivered in the same round." Items not adopted are listed in the "Migration Boundary" at the end.

---

## §0 Layering Principle (most important, read this first)

This skill has two layers of rules. **When they conflict, the hard constraint always wins**:

| Layer | Content | Nature |
|---|---|---|
| **Outer · Hongguo platform adaptation** | Volume tier, scene cap, golden first 3 seconds, per-episode cliffhanger, paywall range, single-line cap, compliance red lines, talking-only dead-air cap | **Hard constraints**, enforced by machine check; cannot be bypassed in the name of "quality first" |
| **Inner · Dramatic craft** | Everything in this file: whether causality holds, whether images have support, whether pacing shifts gears, whether a line is understood on first hearing | **Quality layer**, used for diagnosis and generation |

**In one sentence**: the outer layer guarantees "this is a short drama that can run on Hongguo," and the inner layer guarantees "this is a good drama with visuals, rhythm, and instant comprehension, not an expansion of outline labels." Both layers are needed, but the outer layer may not be overturned by the inner one.

---

## §1 Find the Real Bottleneck First: Five Questions

When a user or viewer says "no visuals, wrong pacing, the lines take forever to make sense, no tension," **do not blindly add words, adjectives, or arguments**. Run these five questions in order and locate which link broke:

1. **Does the character have a clear immediate goal right now?** (Not "wants revenge," but "in this scene he needs the other person to do / hand over / keep something")
2. **Does the obstacle act directly on that goal?** (The opponent has their own chips to play; they are not standing there waiting for the protagonist to perform)
3. **Is the character forced to make a choice and carry it out in visible action?** (Not standing still and relying purely on talk)
4. **Does the outcome change the situation within every 15–30 seconds?** (Information / relationship / resources / position / danger / body / eligibility / cognition)
5. **Is the next scene directly triggered by this outcome?** (Strictly forbidden: scene 1 argues about X in the living room, and scene 2 is back in the living room arguing the same thing)

- If any one of the five is missing → **fix causality, shift-of-gears, and scene function first**.
- If all five hold but the read is still dry or hard to follow → immediately check **§4·Supplement (the three strong-visual anchors)** and **§6·Supplement (plain language delivered in the same round)**.

---

## §2 Drama Generation Chain (run internally before writing a scene; not part of the body)

For load-bearing scenes, use this line to find the drama:

```text
Pressure caused by the previous outcome
  ➔ Character's current judgment / misjudgment (may include self-deception, luck, stubbornness)
  ➔ The method they believe will work (must be playable on screen, not a mood)
  ➔ The counter-effect from the opponent or the rules
  ➔ Visible cost or unexpected gain
  ➔ The character recognizes, denies, or misreads the outcome
  ➔ The next choice
```

**This is a causal diagnostic line, not a seven-part body template.** Calm togetherness, caregiving, waiting, pure comedy, and emotional aftershocks do not need every item filled in. But **if a load-bearing scene only has "the character does something" — with no basis, no counter-effect, no change, and no follow-up — the scene is not finished.**

Check especially for three high-frequency failures: **a well-meant bad outcome / an impulsive counterattack / a wrong choice**:

1. Can the audience, from information and emotion already on the page, understand why he believes this method will work?
2. Does the safer method carry a cost he is unwilling to bear right now, or is it simply outside his awareness?
3. Did his action actually change other people, resources, risk, relationships, or information — rather than only proving the author wrote an action?
4. After the outcome appears, did he see something that should affect his next step? **He may keep being stubborn or mistaken, but he cannot act as if the outcome never happened.**

> **Characters need not be rational or optimal.** Credibility comes from "why this person would choose this right now," not from choosing correctly. A second-best but psychologically understandable choice plays far better than a correct choice with no motivation.

---

## §3 Seven Questions for a Single Scene

Run this on every load-bearing scene:

1. Who is trying to get what?
2. Why must they try **right now**? (What is the cost of delay?)
3. Who or what is blocking them?
4. What **specific tactic** do they use?
5. How does the block **counter-act**?
6. Where does the outcome **deviate** from their expectation?
7. **By the end of the scene, what has changed from the start?** (Information / relationship / resources / position / danger / eligibility / body / commitment / next choice)

Question 7 is the lifeline. If the character starts in doubt, argues it out, and leaves with **the same doubt and the same method**, the scene is an empty scene. Fix the action relationship first; **do not use louder voices as a substitute for progress.**

**Exception (not an empty scene)**: atmosphere-lingering, caregiving, daily-life, and emotional-aftershock scenes may have no explicit attack-and-defense, but they must have a clear emotional point of view and must change at least one of: the relationship, its meaning, the body state, a decision, or the audience's expectation.

---

### §3·Supplement Episode Settlement (the single-episode emotional release valve)

A vertical single episode must give the audience a **visible "exhale"**: the protagonist strikes back at least once, and the villain **pays a visible price** for this round of pressure (public loss of face / a scheme that falls through / being pinned in a dilemma).

- Piling on humiliation alone (no matter how dense the conflict or how much evidence) without a settlement blocks the audience's emotional release and ends in a cliff;
- **Density is set by the scene, not by a threshold**: density is a by-product of scene function — attack-and-defense scenes should say it all, crisis/action scenes let the image speak, transitions and aftershocks can be minimal; within one episode, density naturally rises and falls. The machine prevents talk-only padding through a wide reference band of volume and imbalance valves (E19 consecutive dialogue ≤63 words / E21 dialogue share ≤70% / **E24 more than 6 consecutive dialogue lines must be backed by a △ action**);
- One-sentence test: read this episode from start to finish — **did the villain pay for their pressure?** If not, it is "a straight line of humiliation";
- **Signal closure (hard rule)**: foreshadowing, powers, and mystical signals also need settlement — they must deliver the three steps **signal → instantly verifiable on the spot → has an effect**. **Strictly forbidden: using a code the audience can't decode to decide who wins** (e.g., "the paper cried / stopped crying"). If the rule has not been established inside the story, using it to judge outcomes only confuses viewers. How to write it: make the signal point to a **specific, instantly verifiable fact**, then have the protagonist verify it publicly and use it as a weapon. (Example: Mia says "that paper is reading my name" → Ellie flips the paper, and the header reads "Respondent: Mia.")

---

## §4 Three-Line Visible Change and the "Strong Visual Support" Three Anchors (v4.9 key reinforcement)

Vertical screens carry little information, so viewers track status through **visible objects**. Maintain three lines throughout, so each has a changeable point within this episode:

| Line | What it tracks | This episode must answer at least |
|---|---|---|
| **Body line** | Injuries, breathing, stance, whether they can stand up, distance and contact | Whose physical state changed? After it changed, what can they do and what can't they do? |
| **Space line** | Relative to the exit, sources of danger, key landmarks, who stands where | Has the shift in power landed in position (who retreats, who closes in, who is shut outside the door)? |
| **Prop line** | Where key objects came from, who holds them, how their state changes, where they end up | At the end of this episode, whose hands is the "hard evidence / token / note / passbook" in? |

### §4·Supplement Fully Fix "No Visual Support": Insert a Strong Visual `△` Every 2–4 Lines (machine check E24/E26)

Why do many scripts read like a "radio drama"? Because the writer describes the setting in one line at the top of the scene and then piles up a dozen lines of pure dialogue beneath it — or writes only `△ His eyes flicker`, `△ She pushes the cup half an inch`, which the camera cannot capture as effective micro-actions!

1. **Hard discipline on interleaving density**: **between every 2–4 lines of dialogue, insert at least one substantive `△` action line!** Once **7 lines** of consecutive pure dialogue appear with no `△` action support, machine check `E24` raises a warning!
2. **Three strong visual anchors (every `△` must hit at least one, so that the story can be followed by reading only the `△` lines in silence)**:
   - **Anchor A · Physical result and visual spectacle**: the action must produce a visible physical change or physiological reaction (e.g., `△ He grinds the cigar hard into a collar washed white, smoke curling up`, `△ Herbal soup splashes onto the potted plant, leaves instantly blacken and wilt`, `△ One kick topples the long ladder, the bruiser crashes into a bamboo basket`).
   - **Anchor B · Identity contrast and busy hands**: no standing still while talking! Have the character speak while doing a highly contrasting, concrete action (e.g., `△ A six-foot-three bruiser in a floral apron chops firewood, scolded by his seven-year-old niece until he hides the axe behind his back`, `△ The chairman wipes his fingers clean with a damp towel, unhurriedly, without even glancing at the vice president kneeling on the floor`).
   - **Anchor C · Evidence reveal and physical confrontation**: whatever physical evidence a line mentions, the frame must immediately show a concrete action on that evidence (e.g., `△ She grabs a coarse ceramic bowl, flips it over, and rubs her finger across the dry bottom, leaving a film of white flour`, `△ He catches the wrist of the hand swinging at him and slams the divorce papers into the other man's face`).
3. **Blacklist of ineffective micro-actions (machine check E26 blocks them)**: never use `eyes flicker / gaze shifts slightly / pauses for a moment / looks thoughtful / corner of mouth lifts / sighs / pushes the cup half an inch` as a standalone action line!

---

## §5 Causal Relay and Preventing Spinning in Place

Write each transition as one sentence:

> Because the previous scene produced X, the character must now go to Y and do Z, or they will lose W.

- **Strictly forbidden: spinning in place within the same episode and same scene.** Never allow scene 1 to argue about a matter in one room, and then scenes 2/3 to still be in the same room (or another room) arguing the same thing with the same lines;
- **When one transition changes three or more of: time, place, characters, goal, key prop, event type, it must keep at least one relay cue**: a continuing action / the same prop / the same injury / the same sound / the same question / one explicit motive line.

---

## §6 Minimum Concept-Load Register and "Plain Language Delivered in the Same Round" (v4.9 key reinforcement)

A densely worldbuilt episode must convey era/world background, organizational relations, forms of address, prices, or rule terms. Make a minimal register entry for each new name:

```text
Name / Must the audience know the name right now? / The effect or consequence they see first / How it differs from old concepts / Expected reuse / Handling
```

`Handling` takes exactly one of: **name it now / plain language first / show first, name later / merge with an old concept / defer / delete**.

### §6·Supplement Fully Fix "Lines That Take Forever to Understand" (machine check E25)

1. **Physical evidence + plain-language conclusion delivered in the same round**: strictly forbidden to write only an obscure detail and leave the audience to guess (e.g., just saying "today I set out a seventh pair of chopsticks" or "no water ring on the bowl rim"). Whenever physical evidence or an abnormal detail is pointed out, **the same round of dialogue must state the conclusion in plain language** ("This bowl is coated in dry flour — you didn't eat breakfast at all, you saved everything for us!").
2. **Jargon and setting words translated into everyday speech in the same or next line**: whenever industry terms, business concepts, medical terms, archaic phrasing, or mystical setting words appear, **the same or the next line must immediately translate them into plain worldly stakes (how much money, how many years in prison, who lives and who dies)**. Strictly forbidden: throwing out hard-to-parse words like `rule-gap / fate-anchor / causal-loop / dimension-collapse` that make people think for ages (machine check `E25` blocks them).
3. **Self-test after drafting**: cover all proper names. If you can still understand at a glance "who is about to do what, who has the upper hand, and what the cost is in money or lives," the draft passes.

---

## §7 Writing State Pack for Long Batches (keep distant episodes brief, near ones detailed; prevents drift over 60–100 episodes)

When writing in batch, **each episode carries only the information needed for its current range**. Do not stuff the full set of character biographies, review checklists, and future answers into every episode at once:

- The series' story engine + immutable facts (era, city, family makeup, golden-finger setup);
- A brief direction for more distant stages (not expanded);
- **The actual outcomes of the last one or two episodes**, key original lines, and the body / prop / relationship states that have not yet resolved;
- Both sides' goals, knowledge, concealments, and expected twists for the current episode;
- The dominant change of this episode, stage payoff, and the next pressure.

Companion discipline: **the ledger records facts; the state pack records what must be carried when generating** — the two have different jobs, so do not use the ledger as a substitute for the state pack.

---

## §8 Seven-Level Revision Order

When several problems are found, rank them by impact, not by "easiest to fix first":

1. Interface with preceding material and hard facts (era, names, timeline, prop ownership);
2. Character motives, information access, spatial continuity;
3. Single-scene function and single-episode 15-second shift / unit closure;
4. Enemy and protagonist strategy and cost;
5. Strong-visual `△` support density (eliminate continuous talk-only padding and ineffective micro-actions);
6. Plain-language directness of dialogue, pace variation, character speech fingerprint;
7. Format, typos, markers, on-screen text list.

---

## §9 Vertical Landing (turning the craft layer into filmable images)

This layer is a script layer and does not do shot breakdowns, but **writing to the point of being performable** is the baseline:

- Write actions that **can be performed**: keep the objects that determine understanding, the resistance, the result, and the reaction;
- Interleave one strong visual `△` every 2–4 lines of dialogue, using actions to cut up long exchanges;
- Micro-expressions should be written only as **physiologically observable actions** (Adam's apple bobbing, fingernails digging into a palm, ears flushing red), never as "his heart is in turmoil."

> **Boundary with the monologue channel (v3.4)**: the constraint above against writing "inner turmoil" applies to **△ action lines** — psychological description may not be stuffed into action lines. It does **not** constitute a ban on monologue: monologue is an independent channel, written in `Inner Monologue:` / `Narration:` format lines; its quota and writing method are in `references/inner-monologue-vo.md`. The test in one sentence: **△ does not write feelings; monologue writes only concrete accounts.**

---

## §10 Prohibitions (craft-layer specific)

1. Using the author's conclusion ("the atmosphere is oppressive," "he understood") in place of visible reaction;
2. More than 7 consecutive lines of pure dialogue with no `△` action support (the standing radio-drama);
3. Giving physical evidence without a plain-language conclusion, or speaking in riddles through a literary "A asks, B answers" pattern;
4. Throwing out untranslated industry jargon or made-up mystical terms that leave the audience guessing for ages;
5. Spinning in place within the same episode and same scene, or repeatedly chewing on the same line;
6. Padding with ineffective micro-actions the camera cannot shoot, like `eyes flicker / pauses for a moment / pushes half an inch`;
7. Pushing every emotional layer to its peak (the character stays at the same volume all the way, and the climax disappears).

---

## Migration Boundary (what was not adopted, and why)

| JYY Original Item | Disposition | Reason |
|---|---|---|
| "At least three effective scenes per episode" | **Not adopted** | This item is actually a **personal project convention** of one user inside the JYY package (its file states "this is not a general rule of the short-drama industry"), and it directly conflicts with the Hongguo standard-tier cap of ≤2 scenes per episode |
| "Do not mandate a slap in the first episode, the first 3 seconds, or a stimulus every three seconds" | **Not adopted** | Hongguo's hard thresholds are backed by real platform search data on hit dramas, and belong to the **platform-adaptation layer** |
| "Do not set paywalls at episodes 10/20/30" | **Not adopted** | We have the three-tier paywall ranges in `hongguo-beat-sheet.md`; only recalculate under the new basis when **changing platform or changing total episode count** |
| North American English / full multi-language localization | **Not adopted** | Not needed for Hongguo scenes; only borrow its "region-uncalibrated working draft" downgrade discipline when doing dialect projects |
| Three-tier emotional structure (series-level promise / episode-level emotional debt / key-scene design) | **Partially merged** | At series level we already have the emotion contract in `emotion-flow-roundtrip.md`; this layer takes only the pre-writing diagnosis for key scenes |
| Concept-load minimal register, distant-brief / near-detailed state pack | **Adopted and reinforced** | Directly addresses the pain points of "high setting density" and "batch writing 60–100 episodes," and v4.9 adds "plain language delivered in the same round" |
| Drama generation chain, seven questions per scene, three-line change, causal relay, seven-level revision order | **Adopted and reinforced** | Closes the gap of "passes all machine checks but the drama is fake," and v4.9 adds the "three strong visual anchors" |
