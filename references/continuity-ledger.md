# Cross-Episode Continuity Ledger (Continuity Ledger)

> ★ Authoritative (new in v3.0): the only safeguard that keeps multi-episode serial writing from collapsing. **No ledger, no writing**: `/episode-plan`, `/write-episode`, and `/serial-write` must read the ledger before writing each episode and update it afterward. The ledger is the single source of truth. If the script body and the ledger conflict, stop and ask the user which one to change.

---

## I. Four Ledgers (one set per project; template in `templates/ledger.md`)

### 1. Foreshadowing Ledger (register of seeded threads)
| ID | Seeded element | Planted in Episode | Planned payoff Episode | Status (Seed/Nurture/Resolve/Drop) | Notes |
|---|---|---|---|---|---|
| FB-01 | Bloodstained old pocket watch | 3 | 28 | Nurture | Physical evidence of the Lin family's old accounts |

- Every episode plan **must register the new seeds planted in that episode** (IDs numbered consecutively);
- When a seed is paid off, change its status to "Resolve" and record how. If a seed goes unresolved 3 episodes past its planned payoff, `validate_series.py` reports it as overdue;
- Density guide: at least 2 seeds planted and 1 resolved every 10 episodes. Seeds that are planted but never paid off leave the audience cold; seeds paid off instantly leave no aftertaste.

### 2. Character Ledger (survival and relationship state machine)
| Character | First appearance | Current state (Alive/Dead/Missing/Identity) | Current relationship to protagonist | Last changed (Episode) |
|---|---|---|---|---|

- **The dead cannot speak again** (including direct dialogue outside flashback memories). Every state change must have an episode number and a triggering event;
- New characters must be entered in `character-bible.md` when registered. No dialogue for anyone without a bible entry.

### 3. Prop Status Ledger
| Prop | Holder | Current status | Changed (Episode) |
|---|---|---|---|
| Nine-Dragon Iron Token | Lin Chen | Slammed down in public in Episode 12, then returned to his chest | 12 |

- Key props (those involved in cliffhangers, paywalls, or twists) get one line every time they change hands, are damaged, or are shown;
- Before writing a cliffhanger that uses a close-up of a prop, check the prop's current holder.

### 4. World-Rule Ledger
| Rule | Established (Episode) | Referenced (Episode) | Broken? |
|---|---|---|---|

- Rebirth, system, and rule-horror stories must register: capability limits, costs, and taboos, each on its own line;
- Each time a character uses a set-up ability, log one reference. Breaking a rule → validator FAIL.

---

## II. Read/Write Procedure (main loop of /serial-write mode)

```text
for N in episode range:
  1. Read the ledger (all four ledgers)
  2. Read the Episode N plan + round table to locate this episode's round and which evidence/rebuttal tier it hits
  3. Write the single-episode script (with first 3 seconds, one round-trip beat, cliffhanger; long tier = two rounds + mid-episode hook)
  4. Run validate_episode.py; fix any FAIL
  5. Update the ledger: log new seeds / character changes / prop handovers / rule references line by line
  6. After every 5 episodes written, run validate_series.py once
```

- Updating the ledger is not optional. If step 5 is skipped, the episode counts as unfinished;
- The "previous-episode bridge" within an episode follows the ledger, not a recap from memory.

---

## III. Ledger Differences for Long-Tier Projects (150-195 s per episode)

- The ledger header's "Tier" row is marked long tier, and the total episode count is 30, 40, or 50. Episode ranges are converted at "1 long-tier episode ≈ 2 standard episodes";
- Unit division is halved to match: 10-15 long-tier episodes per unit (40 episodes = 3 units: A 1-13 / B 14-27 / C 28-40);
- A long-tier episode contains two beats, Round A + Round B, plus one mid-episode hook. Round-end cliffhangers are still logged per round, not per episode.

### §3 Supplement: Logging Semantics for Action-Persistence (②)

Action-type round tables do not fill in "evidence tier / rebuttal tier" (that is the battlefield of language). Replace those two columns with the following:

| Dialogue-type column | Action (②) equivalent column |
|---|---|
| Evidence tier (external pressure) | **Omen-Evidence Tier** (power cut / price hike / weather forecast / random incident; hardens tier by tier) |
| Rebuttal tier (protagonist pushes back) | **Preparation-Verification Tier** (each preparation action gets verified once: the blackout really happened / the price really went up) |

- The ledger's "round-end cliffhanger" entry is kept, but Action-type cliffhangers land on "the second before verification."
- 【Skeptic Supporting Character】 is required for Action (no opponent slot = an action log; validator E23 FAIL).
- The paywall and four-act ranges follow the long-tier tables in `hongguo-beat-sheet.md` §2 / §4.3.
- Pass the long-tier total episode count to the series validator: `python scripts/validate_series.py <ledger.md> --episodes 40`. Passing the wrong value (e.g., 80) produces a false S6 report.

---

## IV. Reversal-Method Rotation Matrix (A-I, all tracks)

> v4.2 addition: during serial writing, log each episode's main reversal method to prevent payoff sameness. Validator check **S8**. Register template: `templates/ledger.md`, §Reversal-Method Rotation Matrix.

Nine reversal tags (all tracks):

- `[A]` Identity suppression (true status / hidden Dragon King / top tycoon exposed)
- `[B]` Ironclad evidence (recordings / surveillance / original contract / proof of blood ties)
- `[C]` Ally turns (the opponent's key backer or core patron defects on the spot and submits)
- `[D]` Dimension-dropping sanction (cross-level law / industry rules / financial assets frozen outright)
- `[E]` Heart-piercing breakdown (hypocritical mask torn off / core lie exposed on the spot)
- `[F]` Pure force (physical domination / thugs taken out in seconds / breaking the door to take control)
- `[G]` Emotional deprivation (cutting off mother-child or adoptive ties, stripping inheritance, tearing up an engagement on the spot) ★ new for female-led dramas
- `[H]` Public humiliation (screen exposé at a press event / livestreamed doxxing / media swarm breaks them) ★ new for female-led dramas
- `[I]` Backfire (the villain's own trap and scheme turn back on themselves) ★ new for female-led dramas

- **Red line**: the same reversal tag may not be reused within 3 adjacent episodes (i.e., if two matrix entries are 2 or fewer episodes apart, their tags must differ);
- Violation → `validate_series.py` reports **S8 WARN** (format: `S8 reversal-tag repeat: EP{ep1} and EP{ep2} reuse [{tag}] within 3 adjacent episodes`);
- G/H/I are new for the female-led drama track. Male-led payoff-heavy projects may use them less, but each episode's main reversal method must still get a matrix row and can never be left blank.

---

## V. Hot/Cold Ledger Tiering (Context Control)

During batch serial writing, to keep context usage tight, the ledger is mounted in two zones by activity:

- **Hot zone**: active seeds from the last 5 episodes, plus character states (alive / location / tokens held). Serial writing mounts **only the hot zone**: read before writing, update after;
- **Cold archive**: closed seeds (status = Resolve or Drop with no further follow-up) and retired or dead characters. During serial writing it is **not returned and not loaded into context**; it is pulled manually only when re-checking old threads.

- After each episode is written, move "closed seeds / retired characters" from the hot zone to the cold archive. The archive only grows, never deletes, and stays on record;
- The hot zone keeps only rows still active within the last 5-episode window. Anything outside the window and already closed sinks to the cold archive;
- Hot/cold tiering does not replace the four ledgers. The four ledgers remain the single source of truth. The hot zone is the active view of the four ledgers within the last 5-episode window, and the cold archive is their closed-out view.
