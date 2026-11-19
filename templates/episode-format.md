# Single-Episode Script Standard Layout (Episode Format · v4.9 upgrade)

> Delivery format template. After writing, the file must pass `python scripts/validate_episode.py <file>` (`--format standard|long|comic`, auto-detected by default).

**Pick the tier before drafting** (length format, choose one of three; spec in `references/hongguo-beat-sheet.md` §3):

| Tier | Duration (typical; adjustable) | Body Length 【Reference · Scaled to Length】 (words) | Scenes | Beats per Episode | Machine Check |
|---|---|---|---|---|---|
| Standard (default) | 90~120 s | 320~570 / 220~415 | ≤2 | 1 beat (internal 15-s four-step pacing) | `--format standard` |
| Long | 150~195 s | 550~930 / 440~765 | ≤3 | 2 beats + mid-episode hook | `--format long` |
| Comic-drama | 60~90 s | 220~415 | ≤2 | 1 beat | `--format comic` |

## 1. Standard / Comic-Drama Tier Template

```text
Episode 【XX】: 【Episode Title / Core Payoff Tag】
【Stage】: Act X · (Ep X/80 | back-and-forth Round N · Evidence Slot X / Rebuttal Slot X)
【Golden 3-Second Hook】: one of six archetypes (Life-or-Death Crisis / Extreme Humiliation / Sudden Identity Surge / Physical-Evidence Betrayal / Rule Mystery / Cute-Healing Contrast)
【Conflict Mode】: Dialogue / Action-Persistence / Identity-Mismatch / Relationship-Emotion / Rule-Puzzle / Mixed (choose the right skeleton and cliffhanger formula; **only Action-Persistence gets relaxed machine checks**, see references/conflict-modes.md)
【Emotion Shift】: A ➔ B ➔ C ➔ Last-Gasp Cliffhanger
【Episode Evidence】: 1~2 physical objects that run through this episode (emotional anchor: bowl / ledger / fishing rod / group-chat screenshot / payment-received page; close-ups shoot well and are AI-image friendly, emotion lands on the evidence)  ← new in v4.1
【Skeptic Supporting Character】: the character slot that voices the audience's anger/questions in this episode (let a supporting character say what viewers are holding back so the protagonist stays cool; write "None" if absent)  ← new in v4.1
【Episode Obsession】: one sentence — the thing this unit/episode must hold onto or win back (same source as the series Emotion Contract)
【What the Opponent Wants】: the villain's immediate goal in this episode (what he wants, what chips he puts up) — prevents a floating motive
【Protagonist Active Goal】: the **choice/action** the protagonist takes this episode (not passively taking hits; a hard requirement of the beat sheet)
【What Changes This Episode】: at least one visible change in information / relationship / resources / position / danger
【Episode Payoff】: the protagonist's visible counterstrike this episode + the villain's visible cost for this pressure (no "humiliation with no payoff"; post-write gate · see SKILL Step 3)
【Episode Length】: __ seconds (back-calculate from dialogue volume: pure dialogue ÷ **3.0 words/s (Reference Speech Rate)** + △ action lines × action-beat weight (①Dialogue 1.5s / Mixed 2.5s / ②Action 4.0s) + pauses; E16 tolerance ±20%, no padding or inflated labels)

[Scene]: Interior/Exterior · Location · Day/Night        ← max 2 per episode
[Cast]: Name (status tag), Name (tag)      ← names must be in the Character Ledger

△ Close-up/Medium shot: write only the three visual anchors (physical result / identity-contrast action / evidence-reveal confrontation); no abstract psychological words or ineffective micro-gestures (E26).
Character Name (expression phrase: visual cue｜vocal tone):
"Line."                              ← vary the pace (2~4-word quick-cut lines + 5~11-word direct, account-settling lines); max 17 words per breath (E2); every 2~4 dialogue lines must interleave a △ action line, no more than 6 consecutive pure-dialogue lines (E24); evidence and plain-language conclusions in the same turn, no untranslated jargon (E25)

(Optional, ≤1) Inner Monologue: ≤17 words, write the concrete tally, not abstract emotion
(Optional, ≤1) Narration: ≤8 words, only for theme-pointing turns / time anchors
                                      ← monologue does not count as a dialogue line; banned in the first 3 seconds and at cliffhangers; two monologues may not be adjacent

【Episode Cliffhanger】: Freeze-frame description. (Black screen: swipe down to unlock Episode XX at once)
```

## 2. Long Tier Template (150~195 s flexible)

```text
Episode 【XX】: 【Episode Title / Core Payoff Tag】 (Long tier · 150~195 s flexible)
【Stage】: Act X · (Ep X/40 | Unit A | back-and-forth Round N · Evidence Slot X / Rebuttal Slot X)
【Golden 3-Second Hook】: one of six archetypes
【Conflict Mode】: Dialogue / Action-Persistence / Identity-Mismatch / Relationship-Emotion / Rule-Puzzle / Mixed (see references/conflict-modes.md)
【Emotion Shift】: A ➔ B ➔ C ➔ D ➔ Last-Gasp Cliffhanger
【Episode Evidence】: 1~2 physical objects that run through this episode (same as standard tier; long tier should run the evidence through both rounds)  ← new in v4.1
【Skeptic Supporting Character】: the character slot that voices the audience's anger/questions in this episode (long tier may set one in Round A and one in Round B)  ← new in v4.1
【Episode Obsession】: one sentence — the thing this unit/episode must hold onto or win back
【What the Opponent Wants】: the villain's immediate goal in this episode (what he wants, what chips he puts up)
【Protagonist Active Goal】: the **choice/action** the protagonist takes this episode (not passively taking hits)
【What Changes This Episode】: at least one visible change in information / relationship / resources / position / danger  ← four pre-write gates; if any is missing, do not start writing (see SKILL Step 3)
【Episode Payoff】: the protagonist's visible counterstrike this episode + the villain's visible cost for this pressure (no "humiliation with no payoff")
【Episode Length】: __ seconds   ← must be back-calculated from dialogue volume (pure dialogue ÷ **3.0 words/s (Reference Speech Rate, including action/pause share)** + △ action lines × action-beat weight (①1.5s / Mixed 2.5s / ②Action 4.0s) + pauses 3~5s; E16 tolerance ±20%); no inflating via total word count. Quantified 【Reference Median】: pure dialogue ≈ **447** words (150 s) / ≈ **533** words (180 s) / ≈ **580** words (195 s cap) + 12~15 action lines (②Action: pure dialogue ≥300 words + 15~22 action lines) (machine check E16 blocks inflated labels; E17 blocks "labeling short to downgrade" — long tier may not drop below 150 s)
【Episode Structure】: Two rounds (Round A ____ ➔ Round B ____)    ← time skeleton (flexible, scales with content): hook 0~8s / Round A 8~80s / mid-episode hook ≈90s / Round B 95~170s / cliffhanger 170~195s

[Scene]: Interior/Exterior · Location · Day/Night        ← max 3 per episode; scenes 2 and 3 must be escalation scenes (new space / new opponent / new pressure level)
[Cast]: Name (status tag), Name (tag)

△ Close-up/Medium shot: hook — cut straight into the conflict's peak; no setup.
Character Name (expression phrase: visual cue｜vocal tone):
"Line."                              ← Round A: pressure ➔ rebuttal; the rebuttal must carry a cost or new information; ≥8 dialogue lines; interleave a strong-visual △ every 2~4 lines (no more than 6 consecutive dialogue lines, E24)

【Mid-Episode Hook】: at ≈90 s, new information / a new threat / half a twist; raise the stakes, don't detonate the payoff yet. (Machine-checked)

△ Medium shot: Round B — escalated pressure (new evidence / new cost / new witness).
Character Name (expression phrase: visual cue｜vocal tone):
"Line."                              ← escalated rebuttal / failed reversal; do not repeat Round A's lines; expression-phrase spec see §4
(Optional, ≤2) Inner Monologue: ≤20 words, write the concrete tally, not abstract emotion
(Optional, ≤1) Narration: ≤8 words, only for theme-pointing turns / time anchors
                                      ← monologue does not count as a dialogue line; banned in the first 3 seconds and at cliffhangers; two monologues may not be adjacent
△ Medium shot: emotional peak lands + silent reaction shot

【Episode Cliffhanger】: Freeze-frame description. (Black screen: swipe down to unlock Episode XX at once)
```

**Production check · 15-second window dialogue ≤63 words + consecutive dialogue ≤6 lines** (v4.0 E19 + v4.9 E24): within any consecutive 15-second span, net dialogue words may not exceed 63 (E19), and consecutive pure dialogue may not exceed 6 lines without a `△` action beat (E24). A substantive `△` action line inside a dialogue block counts as a visual break and resets the count.

**Realistic healing slow tier (long sub-variant, new in v4.0)**: 150~195 s / **320~570 words** (not 550~930), for healing tracks (adult divorce-healing, adult emotional/healing, silver-age romance). Low dialogue density, lots of white space and empty shots; cliffhangers are softer and emotional density is higher. Cliffhangers use Formula 5, "Emotion Contrast Landing" (restrained emotional cut-to-black), not a strong-suspense formula. **The standard/long word caps do not apply**; measure volume independently under this variant.

**Before writing**: read the ledger + round table to locate this episode's tier and beat count; **after writing**: update the four ledgers and run the machine check for the tier.

---

## 3. Monologue / Narration Quotas (quota tool; spec in `references/inner-monologue-vo.md`)

| Tier | Inner Monologue | Narration / Caption | Hard Constraints |
|---|---|---|---|
| Standard | ≤1 instance · ≤17 words | ≤1 instance · ≤8 words | first 3 s banned · cliffhangers banned · no back-to-back placement · not counted as dialogue lines |
| Long | ≤2 instances · ≤20 words | ≤1 instance · ≤8 words | same as above |
| Comic-drama | ≤1 instance · ≤13 words | ≤1 instance · ≤8 words | same as above |

**Three-channel split**: dialogue = in-scene offense/defense rounds; inner monologue = grievances and thoughts only the audience hears, establishing the character; narration = theme-pointing turns and time anchors.
**Two hard lines**: monologue **does not carry exposition** (Red Line 2 also covers monologue, and governs it more strictly); △ action lines **still describe only physiologically observable actions**, and psychological description may not be stuffed into action lines to pad them.
**Three usable forms**: a grievance tally (I bore him five children) / a theme-pointing line (the honest man finally fought back) / a character-establishing line (can take down a wild boar on the mountain).

---

## 4. Expression Phrase Spec (visual cue｜vocal tone · new in v3.4.3)

> The parentheses on a dialogue line `Character Name (expression phrase):` are not a junk drawer. They are the **performance-direction source** for downstream AI production.
> Seedance's official three dialogue elements = **who speaks + what they say + how they say it** (HOW THEY SOUND). The first two come naturally with the line;
> the third depends entirely on the expression phrase. Without tone, the model's generated **voice and expression both flatten**.
> The downstream director side (short-drama-director V6.9.3 §5.2 routing table) routes mechanically by this spec: vocal-tone words are moved verbatim into the line's tone slot, visual words go into the visual segment. **So the more regular the writing here, the less loss in downstream translation.**

### 4.1 Binary Rule (one-line test: what the microphone picks up → vocal tone; what the camera sees → visual cue)

**Visual cue comes first, vocal tone second, separated by a fullwidth `｜`; terms are joined with `·`.**

| Form | Format | Example |
|---|---|---|
| Visual only | `(visual·visual)` | `(leans in·smile not reaching the eyes)` |
| Tone only | `(tone·tone)` | `(breathy·trembling)` |
| Mixed | `(visual｜tone·tone)` | `(leans in, turning a jade pendant｜sweet smile·soft voice·knife in every word)` |

Old forms (`(hoarse)`, `(leans in, toys with a jade pendant, smiles)`) **remain valid**: pure tone or pure visual needs no `｜`;
only **the mixed form must use `｜`** as the separator (the one marker downstream can recognize mechanically). Comma separation is also valid, but `·` is recommended.

### 4.2 Vocal Tone List (how the voice is produced, narrowed to four dimensions; same basis as director-side §5.2)

| Dimension | Usable Terms |
|---|---|
| Voice texture | hoarse / husky / breathy / trembling / sobbing / choking / barely audible / weak and faint |
| Force | whisper / soft / gentle / sharp-toned / roaring / low growl / word by word / drawn-out / lowered voice |
| Manner | coldly sneering (modifies "say") / scoffing / sardonic / sarcastic / teeth-gritted / says through gritted teeth |
| Rhythm | rushed / word by word / each word a blade |

**Dual-class words** (coldly sneering / scoffing): when modifying "say", they are vocal tone; when modifying facial expression, they are visual cue.
**Banned: vague emotion-result words**: happy / sad / angry / excited / seductive, etc. These are "result words" the model cannot execute.
Write four-dimension executable words instead (`suppressed anger·low murmur`, not `angry`). Machine check E18a blocks them.
**A script with zero vocal-tone words across all dialogue** triggers E18b. Every episode must give key lines (hook, confrontation, just before the cliffhanger) a tone.

### 4.3 Visual-Cue Boundaries (aligned with existing rules)

Visual cues remain bound by the same discipline as △ lines: write only physiologically observable **actions and expression changes** (pupils contract / knuckles whiten / throat bobs),
no abstract psychological words. Example: `Lin Weiwei (leans in, fingertip turning a jade pendant, smile not reaching the eyes｜sweet smile·soft voice): "Sis, your mother didn't die of illness back then."`

---

## 5. Strong-Visual Support + 15-Second Pacing + Plain-Language Quick Reference (new in v4.9 · E24~E26)

1. **Strong-visual support (prevents E24 talk-only gaps / E26 ineffective micro-gestures)**:
   - Every **2~4 dialogue lines** must include 1 `△` action line; consecutive pure dialogue must never exceed **6 lines**;
   - each `△` must hit one of the three visual anchors: ① **physical results and visual spectacle**; ② **identity contrast and hands-on busywork**; ③ **evidence reveal and physical confrontation**;
   - never write standalone `△ His eyes flicker` / `△ She stiffens slightly` / `△ Pushes the cup half an inch` or other ineffective micro-gestures (triggers E26 WARN).
2. **Plain language, same turn (prevents E25 riddling jargon)**:
   - whenever evidence is pointed to, the conclusion must be stated in plain language in the same dialogue turn; never "mention the evidence without stating the conclusion";
   - whenever professional terms, archaic phrasing, or mystical setting words appear, the same sentence must be followed by a worldly translation (converted into how much money, how many years, who lives or dies).
3. **15-second four-beat pacing shift**:
   - `0~15s` strong visual to grab attention + state a number/deadline to set the stakes ➔ `15~45s` head-on confrontation and pressure ➔ `45~85s` trump card revealed, the reversal completes【Episode Payoff】 ➔ `85~110s` aftershock throws a new crisis, cut to cliffhanger.
