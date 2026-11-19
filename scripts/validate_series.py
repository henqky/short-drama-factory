#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""short-drama-factory v4.9 series ledger validator

Usage:
    python validate_series.py <ledger.md> [--episodes 80] [--script-dir scripts-dir]
    python validate_series.py --self-test
    (Windows: use python; macOS / Linux: use python3)

The ledger is a markdown file of tables (templates/ledger.md format) with four ledgers:
    Foreshadowing Ledger / Character Ledger / Prop Ledger / World Rules Ledger

--episodes sets the paywall ranges: standard tier 60/80/100 eps; long tier (about 3 min/ep) 30/40/50 eps
(1 long ep ≈ 2 standard eps, so wall episodes are halved; see references/hongguo-beat-sheet.md, sections 2 and 4).

Checks:
    S1  Foreshadowing overdue: status Planted/Nurturing/Unresolved and current ep > planned resolution + 3      WARN
    S2  Foreshadowing discarded: status "Discarded" but no reason given in the notes column                    WARN
    S3  Dead character speaks: Character Ledger status Dead/Perished/Missing but a later script has their dialogue  FAIL
    S4  Character not in roster: speaker in the scripts is not in the Character Ledger                        WARN (needs --script-dir)
    S5  Missing cliffhanger: with --script-dir, check each episode for 【Episode Cliffhanger】                   FAIL (missing)
    S6  Paywall placement: no "wall" marker line inside the wall range for each of the three totals            WARN
    S7  Four required ledger tables present                                                                    FAIL (missing table)
    S8  Twist rotation: same [A-I] tag reused within 3 episodes in the Twist Rotation Matrix                   WARN
        (A Identity Suppression / B Ironclad Evidence / C Ally Betrayal / D Dimensional Crackdown /
         E Heart-Piercing Collapse / F Pure Force / G Emotional Deprivation / H Public Social Death /
         I Borrowed-Knife Self-Consumption; G/H/I are additions for female-lead dramas)
Exit codes: 0=passed, 1=FAIL, 2=usage error
"""
import re
import sys
import pathlib

WALL_RANGES = {60: [(8, 11), (21, 24), (41, 44)], 80: [(10, 15), (28, 32), (55, 58)], 100: [(13, 19), (35, 40), (68, 73)],
               # Long tier (about 3 min/ep): episode counts halved, wall ranges scaled to match
               30: [(4, 6), (10, 12), (20, 22)], 40: [(5, 8), (14, 16), (27, 29)], 50: [(7, 10), (17, 20), (34, 37)]}
TABLE_KEYS = {"Foreshadowing": "Foreshadowing Ledger", "Character": "Character Ledger",
              "Prop": "Prop Ledger", "Rules": "World Rules Ledger"}


def _rows(text, section_kw):
    """Return the markdown table data rows under a ledger section"""
    m = re.search(r"^#+[^\n]*?" + section_kw + r"[^\n]*\n(.*?)(?=^#+\s|\Z)", text, re.S | re.M | re.I)
    if not m:
        return None
    rows = []
    for line in m.group(1).splitlines():
        s = line.strip()
        if s.startswith("|") and not re.match(r"^\|[\s\-:|]+\|$", s):
            cells = [c.strip() for c in s.strip("|").split("|")]
            rows.append(cells)
    return rows[1:] if rows else []  # drop header


def _reversal_entries(text):
    """Parse the 'Twist Rotation Matrix' table; return [(ep:int, tag:str)] sorted by episode."""
    m = re.search(r"#+.*?Twist Rotation Matrix.*?\n(.*?)(?=\n#+\s|\Z)", text, re.S | re.I)
    out = []
    if not m:
        return out
    for line in m.group(1).splitlines():
        s = line.strip()
        if not s.startswith("|"):
            continue
        if re.match(r"^\|[\s\-:|]+\|$", s):
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if not cells or "Episode" in cells[0]:
            continue
        em = re.search(r"(\d+)", cells[0])
        tm = re.search(r"\[([A-I])\]", s)
        if em and tm:
            out.append((int(em.group(1)), tm.group(1)))
    out.sort()
    return out


def validate_ledger(text, total_eps=80, scripts=None):
    fails, warns = [], []
    for kw in TABLE_KEYS.values():
        if not re.search(r"#+.*?" + kw, text, re.I):
            fails.append(f"S7 Ledger is missing the 「{kw}」 table")
    mm = re.search(r"Current Episode[:：]\s*(\d+)", text, re.I)
    cur = int(mm.group(1)) if mm else (max(scripts) if scripts else total_eps)

    # S1/S2 Foreshadowing Ledger
    fb = _rows(text, "Foreshadowing Ledger") or []
    for r in fb:
        if len(r) < 5:
            continue
        plan, state = r[3], r[4].strip()
        low = state.lower()
        try:
            pn = int(plan)
        except ValueError:
            warns.append(f"S1 foreshadowing 「{r[1][:24]}」 planned resolution is not a number: {plan}"); continue
        is_open = any(w in low for w in ("planted", "nurturing", "unresolved")) and not low.startswith("resolved")
        if is_open and cur > pn + 3:
            warns.append(f"S1 foreshadowing 「{r[1][:24]}」 overdue (planned ep {pn}, now ep {cur}, status {state})")
        if low.startswith("discarded") and (len(r) < 6 or not r[5]):
            warns.append(f"S2 foreshadowing 「{r[1][:24]}」 marked discarded but no reason given")

    # S3 dead character speaks
    dead = {}
    for r in (_rows(text, "Character Ledger") or []):
        if len(r) < 3:
            continue
        if re.search(r"\b(dead|perished|missing)\b", r[2], re.I):
            mm2 = re.search(r"(\d+)", r[4] if len(r) > 4 else r[2])
            dead[r[0].strip()] = int(mm2.group(1)) if mm2 else cur
    if scripts:
        for ep in sorted(scripts):
            for name, at in dead.items():
                if ep > at:
                    body = scripts[ep]
                    if re.search(r"^" + re.escape(name) + r"\s*(\(|（|[:：])", body, re.M):
                        fails.append(f"S3 「{name}」 is dead/missing from ep {at}, but ep {ep} has dialogue from them")

    # S4 speaker not on roster
    roster = {r[0].strip() for r in (_rows(text, "Character Ledger") or []) if len(r) > 0}
    if scripts and roster:
        NOISE = {"Episode", "Ep", "Scene", "Cast", "This Episode", "Stage", "Golden", "Emotion", "Note", "Continued",
                 "Sound", "Narration", "Voiceover", "Inner Monologue", "Monologue", "Inner Voice", "Shot",
                 "Caption", "On-screen Caption", "Hint", "SFX"}
        for ep in sorted(scripts):
            seen = set()
            for m2 in re.finditer(r"^([A-Za-z][A-Za-z .'-]{0,24})(?:（[^）]*）|\([^)]*\))?\s*[:：]", scripts[ep], re.M):
                nm = m2.group(1).strip()
                if nm in NOISE or nm in seen:
                    continue
                seen.add(nm)
                if nm not in roster and not any(nm in x or x in nm for x in roster):
                    warns.append(f"S4 Ep {ep} dialogue speaker 「{nm}」 is not in the Character Ledger")

    # S5 missing cliffhanger
    if scripts:
        for ep in sorted(scripts):
            if not re.search(r"[【\[]Episode Cliffhanger", scripts[ep]):
                fails.append(f"S5 Episode {ep} is missing 【Episode Cliffhanger】")

    # S6 paywall markers
    ranges = WALL_RANGES.get(total_eps, WALL_RANGES[80])
    marks = []
    for m in re.finditer(r"\bwall\b[^\n]{0,12}?(\d+)\s*(?:[-~]|to)?\s*(\d+)?", text, re.I):
        marks.append(int(m.group(1)))
        if m.group(2):
            marks.append(int(m.group(2)))
    for lo, hi in ranges:
        if not any(lo <= x <= hi for x in marks):
            warns.append(f"S6 no paywall found in Ep {lo}~{hi} (each of the three tiers needs one 'Tier-X wall, Ep N' marker)")

    # S8 twist rotation: same [A-I] tag within 3 episodes (difference <= 2) -> WARN
    rev = _reversal_entries(text)
    for i in range(len(rev)):
        e1, t1 = rev[i]
        for j in range(i + 1, len(rev)):
            e2, t2 = rev[j]
            if e2 - e1 > 2:
                break
            if t1 == t2:
                warns.append(f"S8 twist tag repeated: EP{e1} and EP{e2} within 3 episodes both use [{t1}]")
    return fails, warns, cur


LEDGER_GOOD = """# Ledger: Demo Project
Current Episode: 30

## Foreshadowing Ledger
| ID | Content | Planted In | Planned Resolution | Status | Notes |
|---|---|---|---|---|---|
| FB-01 | Old pocket watch | 3 | 28 | Resolved | Revealed publicly |
| FB-02 | Mystery call | 12 | 31 | Nurturing | Rival infighting thread |

## Character Ledger
| Character | First Appearance | Status | Current Relation | Changed In | Notes |
|---|---|---|---|---|---|
| Lin Chen | 1 | Alive | Protagonist | 30 | |
| Chen Feng | 1 | Dead | Enemy | 25 | Fell from the building in ep 25 |

## Prop Ledger
| Prop | Held By | Status | Changed In |
|---|---|---|---|
| Black Iron Token | Lin Chen | On person | 12 |

## World Rules Ledger
| Rule | Established In | Referenced In | Violated |
|---|---|---|---|
| The Dragon King's Token works only once | 12 | 25 | No |

Paywall placement: Tier-1 wall, Ep 12 (midpoint turn) / Tier-2 wall, Ep 30 / Tier-3 wall, Ep 56
"""
EP_GOOD = """Episode 【3】
[Scene]: Interior · Great Hall
△ The slap stops halfway through the swing.
Chen Feng: Sign it.
Lin Chen: Are you sure?
【Episode Cliffhanger】: Outside, everyone kneels; "Your Highness" is cut off mid-shout. (Blackout)
"""
EP_BAD = """Episode 【4】
[Scene]: Interior · Great Hall
△ Standoff.
Lin Chen: Get lost.
Chen Feng: Fine.
"""


def self_test():
    ok = 1
    scripts = {3: EP_GOOD, 4: EP_BAD}
    f, w, cur = validate_ledger(LEDGER_GOOD, 80, scripts)
    if not any("S5" in x and "Episode 4" in x for x in f):
        print("FAIL self-test: Episode 4 lacks a cliffhanger, should report S5:", f); ok = 0
    if any("S1" in x for x in w):
        print("FAIL self-test: not overdue, should not report S1:", w); ok = 0
    scripts2 = {3: EP_GOOD, 4: EP_BAD, 30: "Episode 【30】\n[Scene]: Interior · Mansion\n△ Standoff.\nChen Feng (sneering): I'm back.\n【Episode Cliffhanger】: Lights out. (Blackout)\n"}
    f2, _, _ = validate_ledger(LEDGER_GOOD, 80, scripts2)
    if not any("S3" in x for x in f2):
        print("FAIL self-test: dead character speaking should report S3:", f2); ok = 0
    if any("S5" in x and "Episode 30" in x for x in f2):
        print("FAIL self-test: Episode 30 has a cliffhanger, should not report S5"); ok = 0
    f3, _, _ = validate_ledger("Empty ledger", 80)
    if len([x for x in f3 if x.startswith("S7")]) < 4:
        print("FAIL self-test: empty ledger should report 4 S7 entries:", f3); ok = 0

    led2 = LEDGER_GOOD.replace("| FB-02 | Mystery call | 12 | 31 | Nurturing | Rival infighting thread |",
                               "| FB-02 | Mystery call | 12 | 8 | Already planted | Rival infighting thread |")
    f4, w4, _ = validate_ledger(led2, 80, scripts)
    if not any("S1" in x and "FB" not in x or "Mystery call" in x for x in w4):
        print("FAIL self-test: status 'Already planted' past due should report S1:", w4); ok = 0
    ep_noise = {5: "Episode 【5】\n[Scene]: Interior\n△ Slam the table.\nSound: Rumbling.\nLin Chen: Who?\nChen Feng: Me.\n【Episode Cliffhanger】: Black screen. (Blackout)\n"}
    _, w5, _ = validate_ledger(LEDGER_GOOD, 80, ep_noise)
    if any("「Sound」" in x for x in w5):
        print("FAIL self-test: 'Sound:' narration line should not report S4:", w5); ok = 0

    ep_dup = {9: "Episode 【9】\n[Scene]: Interior\n[Cast]: A\n△ Standoff.\nStranger: Who are you?\nStranger: Talk!\nStranger: Talk now or I'll move.\nLin Chen: Hold on.\n【Episode Cliffhanger】: Black screen. (Blackout)\n"}
    _, w6, _ = validate_ledger(LEDGER_GOOD, 80, ep_dup)
    dup_cnt = sum(1 for x in w6 if "「Stranger」" in x)
    if dup_cnt != 1:
        print(f"FAIL self-test: S4 same unknown speaker should report only once, got {dup_cnt}", w6); ok = 0

    led_long = LEDGER_GOOD.replace(
        "Paywall placement: Tier-1 wall, Ep 12 (midpoint turn) / Tier-2 wall, Ep 30 / Tier-3 wall, Ep 56",
        "Paywall placement: Tier-1 wall, Ep 6 (midpoint turn) / Tier-2 wall, Ep 15 / Tier-3 wall, Ep 28")
    _, w7, _ = validate_ledger(led_long, 40)
    if any("S6" in x for x in w7):
        print("FAIL self-test: long-tier 40-ep wall placement should not report S6:", w7); ok = 0
    _, w8, _ = validate_ledger(LEDGER_GOOD, 40)
    if not any("S6" in x for x in w8):
        print("FAIL self-test: standard-tier wall placement checked against 40 eps should report S6:", w8); ok = 0

    led_s8_bad = LEDGER_GOOD + """
## Twist Rotation Matrix
| Episode | Twist Tag[A-I] | Core Conflict Event | Attacker vs Defender | Payoff |
|---|---|---|---|---|
| EP1 | [F] Pure Force | Kick the door in and floor the thugs | Hero vs villain | Physical suppression |
| EP2 | [A] Identity Suppression | Reveal true identity | Aide vs villain's family | Status reversal |
| EP3 | [F] Pure Force | Force control again | Hero vs villain | Repeated payoff |
"""
    _, w_s8b, _ = validate_ledger(led_s8_bad, 80)
    if not any(x.startswith("S8") and "EP1 and EP3" in x and "[F]" in x for x in w_s8b):
        print("FAIL self-test: [F] reused within 3 episodes should report S8:", w_s8b); ok = 0
    led_s8_good = LEDGER_GOOD + """
## Twist Rotation Matrix
| Episode | Twist Tag[A-I] | Core Conflict Event | Attacker vs Defender | Payoff |
|---|---|---|---|---|
| EP1 | [F] Pure Force | Kick the door in and floor the thugs | Hero vs villain | Physical suppression |
| EP2 | [A] Identity Suppression | Reveal true identity | Aide vs villain's family | Status reversal |
| EP3 | [B] Ironclad Evidence | Show the original black ledger | Hero vs ex-wife | Moral high ground collapses |
| EP4 | [C] Ally Betrayal | Core backer turns on them | Uncle vs villain | Betrayal on the spot |
"""
    _, w_s8g, _ = validate_ledger(led_s8_good, 80)
    if any(x.startswith("S8") for x in w_s8g):
        print("FAIL self-test: normal rotation should not report S8:", w_s8g); ok = 0

    print("[+] self-test PASSED" if ok else "[-] self-test FAILED")
    return 0 if ok else 1


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__); return 2
    if args[0] == "--self-test":
        return self_test()
    try:
        led = pathlib.Path(args[0]).read_text(encoding="utf-8-sig")
    except FileNotFoundError:
        print(f"[-] Ledger file not found: {args[0]}"); return 2
    except IsADirectoryError:
        print(f"[-] Path is a directory, not a ledger file: {args[0]}"); return 2
    except UnicodeDecodeError:
        print(f"[-] Ledger is not UTF-8 text: {args[0]}"); return 2
    except OSError as e:
        print(f"[-] Cannot read ledger file: {args[0]} ({e})"); return 2
    total = 80
    if "--episodes" in args:
        try:
            total = int(args[args.index("--episodes") + 1])
        except (IndexError, ValueError):
            print("[-] --episodes requires an integer"); return 2
    scripts = None
    if "--script-dir" in args:
        try:
            d = pathlib.Path(args[args.index("--script-dir") + 1])
        except IndexError:
            print("[-] --script-dir requires a directory path"); return 2
        if not d.is_dir():
            print(f"[-] Script directory not found: {d}"); return 2
        scripts = {}
        for p in sorted(d.glob("*.md")):
            if not (re.search(r"ep", p.stem, re.I) or re.fullmatch(r"\d+", p.stem)):
                continue
            m = re.search(r"(\d+)", p.stem)
            if m:
                try:
                    scripts[int(m.group(1))] = p.read_text(encoding="utf-8-sig")
                except (UnicodeDecodeError, OSError) as e:
                    print(f"[-] Skipping unreadable script: {p} ({e})")
    fails, warns, cur = validate_ledger(led, total, scripts)
    print(f"== {args[0]}  total eps={total} current ep={cur} ==")
    for x in fails:
        print("[-] FAIL:", x)
    for x in warns:
        print("[!] WARN:", x)
    if fails:
        print("Result: FAILED"); return 1
    print("Result: PASSED" + (" (with WARN)" if warns else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
