#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""short-drama-factory v4.9 per-episode script validator (by tier)

Usage:
    python validate_episode.py <episode-script.md> [--format auto|standard|long|comic] [--prev prev.md ...]
    python validate_episode.py --self-test
    (Windows: use python; macOS / Linux: use python3)

Tier profiles (--format; default auto = detect from the script header, i.e. its first 3 lines:
    the header contains "long tier" -> long ; contains "comic-drama" -> comic ; otherwise standard):
    standard  standard tier 90~120 s     body words real-shoot 320~570 / comic 220~415   scenes <=2   dialogue lines >=4
    long      long tier 150~195 s        body words real-shoot 550~930 / comic 440~765   scenes <=3   dialogue lines >=8   must set 【Mid-Episode Hook】
    comic     comic-drama tier 60~90 s   body words 220~415                             scenes <=2   dialogue lines >=4
    (shorthands: --long = --format long ; --comic = --format comic)

Checks (FAIL = blocking, must fix; WARN = warning, review; NOTE = protective counterexample hint, explicitly NOT a defect):
    E1  body word count vs the [Reference Band] = dialogue + action lines + cliffhanger frame
          (excludes 【】 field lines and [Scene] / [Cast]).
          The band is derived from 【Episode Length】 (~3.3~5.1 words/s incl. action); without a length, the tier default is used.
          WARN (outside band, not blocking) / FAIL (below 0.5x the band = extreme empty draft)
    E2  single dialogue clause (normal 8~12 words / punchy 5~8) cap 17 words (over-long = WARN, not blocking)   WARN (clause > 17)
          note: monologue / narration are not judged here (they use E12 os_len / vo_len)
    E3  scene count <= 2 (count of [Scene] markers)                FAIL (>2)
    E4  golden first 3 seconds: the first content line must contain a conflict signal (Action mode may also use an unusual-action word)   FAIL (none)
    E5  banned opener clichés (wakes up / draws the curtains / sun rises / walking down the street, etc.)   WARN
    E6  cliffhanger: 【Episode Cliffhanger】 exists and contains black screen / suspense   FAIL (missing)
    E7  emotion-shift chain: 【Emotion Shift】 exists with an arrow (-> or ➔)   WARN (missing)
    E8  repetition check: protagonist line repeats a prior episode passed in (--prev)   WARN (repeated line)
    E9  dialogue line count: >= tier minimum (standard/comic 4 lines, long 8 lines)   WARN (too few)
          note: monologue / narration lines do not count as dialogue lines (so they cannot be used to pad past the structure check)
    E10 compliance red-line words (dismember / disembowel / lingchi etc., one-strike graphic depictions)   FAIL
    E11 long-tier midpoint hook: 【Mid-Episode Hook】 exists (long tier)      FAIL (long tier missing)
    E12 monologue / narration quota: inner monologue 1 (standard) / 2 (long) / 1 (comic) per episode (single line 17/20/13 words);
        narration <= 1 use, <= 8 words                                       FAIL (over quota)
    E13 monologue / narration back-to-back: two adjacent, or right before the cliffhanger closing   FAIL
    E14 monologue carrying exposition or abstract emotion                    WARN
    E15 monologue / narration in the first 3 seconds (should be on-scene conflict)   FAIL
    E16 inflated duration (v4.9.1, all tiers): 【Episode Length】 > dialogue-derived duration x 1.20      FAIL
          (v4.9.1: the seconds unit is optional; old "：180" without a unit used to bypass the check)
          derivable duration = pure dialogue words / 3.0 (reference speech rate) + action lines x action-beat credit + 5 s padding;
          action-line words do not count toward duration
    E17 long-tier downgrade (v3.4.2, long tier): 【Episode Length】 < 150 s (long-tier floor)   FAIL
    E18 tone-cue supply (v3.4.3, aligns with director-side V6.9.3 C16 / model-adapters §5.2):
        E18a parenthetical contains a vague emotion word (happy / angry, etc.)   WARN
        E18b no dialogue line in the whole script has a tone cue (extreme case: voice / delivery info missing for the episode)   WARN
    E19 15-second dialogue density (v4.0, WARN production-side suggestion): consecutive dialogue block > 63 words   WARN
    E20 single action segment <= 27 words (v4.2, WARN soft limit): one △ shot with > 27 words   WARN
    E21 dialogue / action word ratio 25%~70% (v4.2, WARN): dialogue / (dialogue + △ action)   WARN
    E22 dialogue wording / typos (common misuse table, e.g. could of / alot / irregardless)   WARN (hint only, not blocking)
    E23 conflict-mode fit: Action-Persistence mode must set 【Skeptic Supporting Character】   FAIL
    E24 dry-talk gap detection (v4.9, WARN strong-visual support): more than 6 consecutive pure-dialogue lines with no △ action line   WARN
          addresses the "standing-still radio drama" pain point; suggest a strong-visual △ every 2~4 dialogue lines
    E25 riddle-jargon detection (v4.9, WARN plain-language delivery): dialogue contains untranslated obscure jargon / riddle terms   WARN
          addresses the "takes forever to understand what is being said" pain point; proper nouns and jargon must be translated
          into plain consequences (money / life / status)
    E26 invalid micro-action detection (v4.9, WARN strong-visual anchor): a △ contains an unfilmable micro-action / psychological word
          with no strong action marker                                       WARN
          bans fake actions like "△ eyes flicker / slightly stunned / pushed half an inch" that pad the count; requires one of the
          three visual anchors (v4.9.1: a weak micro-action wrapped in a long atmosphere description still warns; a combined △
          with a strong action such as an evidence smash or physical clash does not false-positive)

Protective counterexamples (NOTE level -- hints that you may have over-corrected; no change required; see references/protective-counterexamples.md):
    N12 fragmenting: >= 5 consecutive dialogue lines with each line <= 3 words      NOTE (may be chopping full sentences to dodge E2)
    N13 action padding: >= 12 action lines, each averaging <= 9 words, and dialogue lines <= tier minimum   NOTE (may be padding E1 volume)
    N14 hugging the floor: volume <= floor + 10 and cliffhanger frame < 13 words     NOTE (may have cut needed process or made the cliffhanger too thin)
Exit codes: 0 = pass (may contain WARN / NOTE), 1 = FAIL, 2 = usage error
"""
import re
import sys

# Body-volume thresholds in words (body only: dialogue lines + △ action lines + cliffhanger frame description)
# Converted from the original character counts at 1 English word ~= 1.5 Chinese characters (chars / 1.5, rounded).
NET_MIN, NET_MAX = 320, 570          # real-shoot short drama (wide reference band: only catches extremely thin / thick scripts)
NET_MIN_ANIME, NET_MAX_ANIME = 220, 415  # comic-drama / vertical animation
NET_LONG_MIN, NET_LONG_MAX = 550, 930        # long tier (150~195 s flexible) real-shoot
NET_LONG_ANIME_MIN, NET_LONG_ANIME_MAX = 440, 765  # long tier comic-drama / vertical animation
SENT_MAX = 17                        # single dialogue clause cap in words (WARN level, not blocking; normal 8~12)

# ---- Long-tier duration anchors (v4.3, recalibrated to measured speech rate: 15 s ~= 63-word cap, target 3.0 words/s) ----
LONG_MIN_SEC = 150                   # long-tier 【Episode Length】 floor (seconds): below this = "long tier label, standard-tier volume"
DLG_PER_SEC = 3.0                    # dialogue -> duration reference rate (words/s), used by E16 (tolerance +/-20%)
DLG_TARGET = {90: 267, 120: 360, 150: 447, 180: 533, 195: 580}   # reference median pure-dialogue words per target duration; not a hard gate
WIN15_MAX_WORDS = 63                 # E19: max net words in any consecutive dialogue block (~15 s x 4.2 words/s ceiling)
DRY_DLG_RUN_MAX = 6                  # E24 (v4.9): max consecutive pure-dialogue lines with no △ action line (>6 = dry-talk gap warning)
ACT_SEG_MAX = 27                     # E20: max words in one △ action shot (WARN)

# ---- Dialogue tone-cue supply (v3.4.3 · aligns with director-side V6.9.3 C16 / model-adapters §5.2 dialogue triad) ----
# Matched case-insensitively at a word start (prefix), so "whisper" also hits "whispered".
TONE_WORDS = ("hoarse", "husky", "breathy", "trembl", "shaky", "tearful", "sobb", "choked", "cracking",
              "barely", "weak", "whisper", "softly", "gently", "sharply", "bark", "snarl", "roar", "growl",
              "shout", "word by word", "drawn-out", "sarcas", "mock", "sneer", "scoff", "cold",
              "gritted", "lowered voice", "low voice", "hushed", "rapid", "calmly", "very low",
              "loudly", "shrill", "voice", "tone", "stammer", "slurr")
# Vague emotion words in a parenthetical (E18a); matched as whole words.
E18_VAGUE_WORDS = ("happy", "happily", "sad", "sadly", "angry", "angrily", "furious", "sorrowful",
                   "heartbroken", "glad", "seductive", "melancholy", "excited")

# ---- E22 dialogue wording / typos (common misuse table, WARN level: hint only, not blocking) ----
# (wrong, right); matched case-insensitively as whole words.
TYPO_LITERALS = (
    ("could of", "could have"), ("would of", "would have"), ("should of", "should have"),
    ("might of", "might have"), ("must of", "must have"),
    ("alot", "a lot"), ("irregardless", "regardless"),
    ("for all intensive purposes", "for all intents and purposes"),
    ("definately", "definitely"), ("seperate", "separate"), ("occured", "occurred"), ("untill", "until"),
    ("could care less", "couldn't care less"), ("free reign", "free rein"),
    ("one in the same", "one and the same"), ("nip it in the butt", "nip it in the bud"),
    ("pass judgement", "pass judgment"), ("taken for granite", "taken for granted"),
)
TYPO_REGEX = (
    (r"\bborrow(?:ed|ing)? (?:me|us|him|her|them|you) (?:some |the |a )?(?:money|cash|bucks|dollars)\b",
     "'borrow' takes money from someone; to hand money to someone, use 'lend' or 'give'"),
)

# ---- E25 riddle jargon and untranslated setting terms (v4.9 · WARN level: stop viewers from puzzling over lines) ----
OBSCURE_JARGON_WORDS = (
    "law rift", "fortune anchor", "karmic loop", "dimensional collapse", "higher-dimensional projection",
    "closed logic loop", "empowerment matrix", "ember leak", "mute jade", "seventh shard", "eighth shard",
    "tilt the oil lamp toward",
)

# ---- E26 invalid micro-actions (v4.9 · WARN level: stop fake actions that the camera cannot show from padding) ----
WEAK_MICRO_ACTIONS = (
    "eyes flicker", "eyes twitch", "gaze flickers", "gaze twitches", "slightly stunned",
    "lost in thought", "deep in thought", "pensive", "corner of the mouth twitches",
    "lips curl slightly", "faint smile", "pushed half an inch", "moved half an inch",
)

# Strong action markers (v4.9.1): if a △ line contains any of these, it has a visible physical result / evidence clash,
# so E26 lets it pass. Fixes the blind spot where a weak micro-action wrapped in a long atmosphere description slipped past.
# When a weak word hits but the line has no strong marker, it warns regardless of the line's length
# (so a combined "slightly stunned + teacup smashes" line does not false-positive).
STRONG_ACT_MARKERS = (
    "smash", "shatter", "slam", "throw", "fling", "hurl", "toss", "kick", "punch", "slap", "flip",
    "bump", "choke", "grab", "seize", "snatch", "drag", "yank", "tear", "rip", "splash", "burn",
    "ignite", "kneel", "collapse", "crumple", "fall", "drop", "stagger", "stumble", "step back",
    "back away", "retreat", "turn", "stand up", "rise", "crack", "spill", "pour", "roll off", "slide",
    "clench", "pinch", "press", "close-up", "close in", "lunge", "pounce", "rush", "block", "dodge",
    "pin", "pull", "push", "shove", "cover", "tie", "draw", "raise", "reveal", "flush", "knock",
    "overturn", "hit the ground", "spew",
)

# ---- Monologue / narration (non-spoken narrative channels) ----
VO_OS_TAGS = ("inner monologue", "monologue", "inner voice")          # only the audience hears the speaker's thoughts
VO_VO_TAGS = ("narration", "voiceover", "on-screen caption", "caption")  # third-person pointing-out / time anchors
VO_EXPO_WORDS = ["it all started", "it all began", "everything started", "as everyone knows", "backstory",
                 "let me explain", "flashback", "the background is"]
VO_ABSTRACT_WORDS = ["mixed feelings", "a flood of emotions", "a thousand thoughts", "my heart was breaking",
                     "beyond words", "so many emotions"]

PROFILES = {
    "auto":     {"scenes": 2, "lines": 4, "midhook": False, "os": 1, "os_len": 17, "vo": 1, "vo_len": 8, "label": "auto-detect tier"},
    "standard": {"scenes": 2, "lines": 4, "midhook": False, "os": 1, "os_len": 17, "vo": 1, "vo_len": 8, "label": "standard tier 90~120 s"},
    "long":     {"scenes": 3, "lines": 8, "midhook": True,  "os": 2, "os_len": 20, "vo": 1, "vo_len": 8, "label": "long tier 150~195 s (flexible)"},
    "comic":    {"scenes": 2, "lines": 4, "midhook": False, "os": 1, "os_len": 13, "vo": 1, "vo_len": 8, "label": "comic-drama tier 60~90 s"},
}

# Opener clichés that waste the first shot (E5 / E4), matched case-insensitively at a word start.
OPEN_BAN_WORDS = ["wakes up", "woke up", "wake up", "gets out of bed", "draws the curtains", "pulls the curtains",
                  "the sun rises", "sunrise", "walking down the street", "walking along the road",
                  "straightens his clothes", "straightens her clothes", "driving to work", "sipping coffee",
                  "a lazy morning", "a sunny morning"]

# E4 conflict signals in the first 3 seconds (punctuation is matched as plain substring).
CONFLICT_SIGNALS = ["!", "?", "gun", "knife", "slap", "throw", "smash", "shout", "kneel", "tear", "slam",
                    "shove", "kick", "curse", "humiliat", "divorce", "critical", "sign", "die", "dead", "kill",
                    "get out", "stop", "save", "break", "explod", "burn", "blood", "punch", "pin", "scream"]
# Extra action-mode openers (Action mode may open on an unusual action): prep / hoarding / physical work.
ACTION_SIGNALS = ["stock", "hoard", "carry", "haul", "lift", "weld", "seal", "lock", "bolt", "crate", "stack",
                  "barrel", "water", "generator", "steel plate", "reinforc", "rush-buy", "stockpile", "supplies",
                  "power cut", "outage", "dig", "brick", "drill", "twist", "nail", "strap", "tape", "tally"]

BREAK_WORDS = ["black screen", "suspense", "swipe", "unlock"]

# Red-line one-strike graphic words (E10), matched case-insensitively at a word start.
REDLINE_WORDS = ("dismember", "disembowel", "decapitat", "buried alive", "lingchi", "lethal injection",
                 "cook meth", "drug synthesis", "suicide method", "gu poison", "poison curse",
                 "real government agency")


_VO_LINE_RE = re.compile(
    r"^(inner monologue|monologue|inner voice|narration|voiceover|on-screen caption|caption)"
    r"(?:\([^)]*\)|（[^）]*）)?\s*[:：]\s*(.+)$", re.I)
_DIALOGUE_RE = re.compile(
    r"^([A-Za-z][A-Za-z .'-]{0,24})(?:\([^)]*\)|（[^）]*）)?\s*[:：]\s*(.+)$")
_PAREN_RE = re.compile(
    r"^[A-Za-z][A-Za-z .'-]{0,24}(?:\(([^)]*)\)|（([^）]*)）)?\s*[:：]")
_LABEL_RE = re.compile(r"\[[^\]]*\]|【[^】]*】")   # [Scene] / 【...】 labels and markers
_NON_WORD_RE = re.compile(r"[^A-Za-z0-9'’-]+")  # punctuation other than apostrophes and hyphens


def count_words(text):
    """Net word count: drop [..] / 【..】 labels and punctuation, then count whitespace-separated word tokens.
    Contractions and hyphenated words (don't, life-saving) count as one word."""
    text = _NON_WORD_RE.sub(" ", _LABEL_RE.sub(" ", text))
    return sum(1 for tok in text.split() if re.search(r"[A-Za-z0-9]", tok))


def _has(s, w, whole=False):
    """Case-insensitive phrase match. A word starting with a letter must begin at a word boundary
    (prefix match, so 'smash' hits 'smashed'); whole=True also requires a word end.
    Punctuation signals ('!', '?') are plain substring matches."""
    pre = r"(?<![A-Za-z])" if w[:1].isalpha() else ""
    post = r"(?![A-Za-z])" if whole else ""
    return re.search(pre + re.escape(w) + post, s, re.I) is not None


def _norm_line(s):
    return re.sub(r"\s+", " ", s).strip().lower()


_TYPO_LITERAL_RES = tuple((re.compile(r"\b" + re.escape(bad) + r"\b", re.I), bad, good)
                          for bad, good in TYPO_LITERALS)
_TYPO_REGEX_RES = tuple((re.compile(pat, re.I), note) for pat, note in TYPO_REGEX)


def _vo_line(line):
    """Monologue / narration line -> (kind, content); kind is 'os' (inner monologue) or 'vo' (narration / caption); None for other lines"""
    s = line.strip()
    if not s or s.startswith(("[", "△", "【", "#", ">")):
        return None
    m = _VO_LINE_RE.match(s)
    if not m:
        return None
    return ("os" if m.group(1).lower() in VO_OS_TAGS else "vo", m.group(2))


def _is_dialogue(line):
    """Dialogue line: Speaker (optional parenthetical): line -- does not start with [ △ 【 and is not a monologue / narration line"""
    s = line.strip()
    if not s or s.startswith(("[", "△", "【", "#", ">")):
        return None
    if _vo_line(s):
        return None
    m = _DIALOGUE_RE.match(s)
    return m.group(2) if m else None


def _paren_of(line):
    """Parenthetical (tone / action cue) of a dialogue line -> str; '' if no parenthetical or not a dialogue line"""
    s = line.strip()
    if not s or _vo_line(s) is not None:
        return ""
    m = _PAREN_RE.match(s)
    if not m:
        return ""
    return (m.group(1) or m.group(2) or "").strip()


def net_words(text):
    """Body word count: counts only dialogue lines + monologue / narration content + △ action content + 【Episode Cliffhanger】 frame description"""
    total = 0
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        d = _is_dialogue(s)
        v = _vo_line(s)
        if v is not None:
            body = v[1]
        elif d is not None:
            body = d
        elif s.startswith("△"):
            body = re.sub(r"^△\s*", "", s)
        elif s.startswith("【Episode Cliffhanger】"):
            body = re.sub(r"^【Episode Cliffhanger】\s*[:：]?\s*", "", s)
        else:
            continue
        total += count_words(body)
    return total


def _header_text(text):
    """Only the script header (first 3 lines: episode title / tier marker area)"""
    return "\n".join(text.splitlines()[:3])


def is_anime(text):
    """Comic-drama / vertical animation project: header contains 'comic-drama' -> judged against the comic body band in E1"""
    return re.search(r"comic[- ]drama", _header_text(text), re.I) is not None


def is_long(text):
    """Long-tier project: header contains 'long tier' -> judged against the long-tier body band in E1/E3/E9/E11"""
    return re.search(r"long[- ]tier", _header_text(text), re.I) is not None


def resolve_profile(text, profile="auto"):
    """auto: detect from the header -- 'long tier' -> long, 'comic-drama' -> comic, otherwise standard"""
    if profile != "auto":
        return profile if profile in PROFILES else "standard"
    if is_long(text):
        return "long"
    if is_anime(text):
        return "comic"
    return "standard"


def net_band(text, profile):
    """Body word count [Reference Band]. Preferentially derived from the script's declared 【Episode Length】, adjusted by conflict mode
    (rates are the original chars/s rates divided by 1.5)"""
    m = re.search(r"【Episode Length】[:：]\s*(\d+)", text)
    if m:
        t = int(m.group(1))
        if t > 0:
            _mode = conflict_mode(text)
            _lo, _hi = (2.3, 3.7) if _mode == "Action" else ((2.8, 4.3) if _mode == "Mixed" else (3.3, 5.1))
            return (round(t * _lo), round(t * _hi))
    if profile == "long":
        return (NET_LONG_ANIME_MIN, NET_LONG_ANIME_MAX) if is_anime(text) else (NET_LONG_MIN, NET_LONG_MAX)
    if profile == "comic":
        return NET_MIN_ANIME, NET_MAX_ANIME
    return (NET_MIN_ANIME, NET_MAX_ANIME) if is_anime(text) else (NET_MIN, NET_MAX)


def scene_count(text):
    return len(re.findall(r"^\[Scene\]|^【Scene】|^##?\s*Scene", text, re.M))


def first_content_lines(text, n=3):
    out = []
    for line in text.splitlines():
        s = line.strip().lstrip("﻿").strip()  # v4.9.1: strip BOM so it cannot take up the first-3-seconds window
        if not s or s.startswith(("#", ">", "Episode", "【", "[")):
            continue
        out.append(s)
        if len(out) >= n:
            break
    return out


def conflict_mode(text):
    """Conflict mode: Dialogue (verbal fight) / Action (prep x doubt) / Mixed; default = Dialogue.
    Action-Persistence also maps to Action."""
    m = re.search(r"【Conflict Mode】[:：]\s*([^\n【]{1,30})", text)
    if m:
        s = re.split(r"[/／\s,，、|｜]", m.group(1).strip())[0]
        if "action" in s.lower():
            return "Action"
        if "mixed" in s.lower():
            return "Mixed"
    return "Dialogue"


def validate(text, prev_texts=(), profile="auto"):
    profile = resolve_profile(text, profile)
    prof = PROFILES[profile]
    mode = conflict_mode(text)
    if mode == "Action":
        lines_min = max(3, prof["lines"] // 2)
    elif mode == "Mixed":
        lines_min = max(4, prof["lines"] - 2)
    else:
        lines_min = prof["lines"]
    act_credit = 4.0 if mode == "Action" else (2.5 if mode == "Mixed" else 1.5)
    fails, warns = [], []
    nc = net_words(text)
    lo, hi = net_band(text, profile)
    if nc < lo * 0.5:
        fails.append(f"E1 [{profile}] body word count {nc} too thin (reference band {lo}~{hi}; blocks only extreme empty drafts)")
    elif not (lo <= nc <= hi):
        warns.append(f"E1 body word count {nc} outside reference band {lo}~{hi} (band is advisory: judge by 【Episode Length】 or content; not blocking)")

    # E2 single clause <= 17 words: dialogue lines only, split by punctuation into clauses (one line may hold several), clause > 17 words -> WARN
    for line in text.splitlines():
        d = _is_dialogue(line)
        if not d:
            continue
        for clause in re.split(r"[,;!?.…—]", d):
            n = count_words(clause)
            if n > SENT_MAX:
                warns.append(f"E2 dialogue clause {n} words (>{SENT_MAX}): {clause.strip()[:30]}…")

    sc = scene_count(text)
    _cap = prof["scenes"]
    _md = re.search(r"【Episode Length】[:：]\s*(\d+)", text)
    if _md:
        _t = int(_md.group(1))
        if _t > 0:
            _cap = max(_cap, int(round(_t / 75.0)))
    if sc > _cap:
        fails.append(f"E3 [{profile}] scene count {sc} >{_cap}")
    if sc == 0:
        warns.append("E3 no [Scene] marker detected, cannot verify scene count")

    head = "\n".join(first_content_lines(text))
    banned_hit = any(_has(head, w) for w in OPEN_BAN_WORDS)
    _sig = CONFLICT_SIGNALS + (ACTION_SIGNALS if mode == "Action" else [])
    if banned_hit or not any(_has(head, w) for w in _sig):
        fails.append("E4 no conflict in the first 3 seconds, or hits an opener banned word "
                     "(must cut straight to the conflict peak, no setup; Action mode may open on an unusual action)")
    for w in OPEN_BAN_WORDS:
        if _has(head, w):
            warns.append(f"E5 opener may be a stock empty shot, banned word '{w}'")

    if not re.search(r"【Episode Cliffhanger】|\[Episode Cliffhanger", text):
        fails.append("E6 missing 【Episode Cliffhanger】 section")
    else:
        seg = re.search(r"【Episode Cliffhanger】(.{0,800})", text, re.S)
        if seg and not any(_has(seg.group(1), w) for w in BREAK_WORDS):
            warns.append("E6 cliffhanger lacks a black-screen / swipe-to-unlock landing word")

    if not re.search(r"【Emotion Shift】.*(->|➔|→)", text):
        warns.append("E7 missing 【Emotion Shift】 chain (should read: Humiliated ➔ … ➔ Deadly cliffhanger)")

    my_lines = [d for d in (_is_dialogue(l) for l in text.splitlines()) if d]
    rounds = len(my_lines)
    if prof["midhook"] and not re.search(r"【Mid-Episode Hook】|\[Mid-Episode Hook", text):
        fails.append("E11 long tier missing 【Mid-Episode Hook】 (set new information / a new threat at ~90 s to prevent drift)")
    if rounds < lines_min:
        warns.append(f"E9 [{profile}] only {rounds} dialogue lines (<{lines_min}), exchange structure too thin"
                     + (" (Action halved)" if mode == "Action" else ""))
    # E23 Action mode must have a 【Skeptic Supporting Character】 (the opposing seat of prep x doubt)
    if mode == "Action":
        _q = re.search(r"【Skeptic Supporting Character】[:：]\s*([^\n]*)", text)
        if _q and _q.group(1).strip().lower() in ("", "none", "none.", "n/a", "—", "-"):
            fails.append("E23 Action mode missing 【Skeptic Supporting Character】 (no opposing seat: prep x doubt needs a skeptic; "
                         "without one it is an action log)")

    # ---- Dialogue tone-cue supply (E18 · v3.4.3) ----
    if my_lines:
        for l in text.splitlines():
            p = _paren_of(l)
            if not p:
                continue
            v = [w for w in E18_VAGUE_WORDS if _has(p, w, whole=True)]
            if v:
                warns.append(f"E18a parenthetical has vague emotion word '{'/'.join(v)}': {p} -- "
                             "change it to an actionable tone / visual cue (e.g. jaw clenched, low voice | knuckles white), "
                             "spec in templates/episode-format.md §4")
                break
        tone_lines = sum(1 for l in text.splitlines()
                         if _is_dialogue(l) and any(_has(_paren_of(l), w) for w in TONE_WORDS))
        if tone_lines == 0:
            warns.append(f"E18b none of the {rounds} dialogue lines has a tone cue (voice / delivery info missing for the whole episode) -- "
                         "the third dialogue element, HOW THEY SOUND, has no upstream supply: add tone cues to key lines "
                         "(e.g. (breathy, trembling) / (leaning in | sweet smile, gentle)), spec in templates/episode-format.md §4")

    # ---- Monologue / narration channel (E12~E15) ----
    seq = []
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith(("#", ">", "[Scene", "[Cast", "Episode 【")):
            continue
        if s.startswith("【Episode Cliffhanger】") or s.startswith("[Episode Cliffhanger"):
            seq.append(("break", s)); continue
        if s.startswith("【"):
            continue
        v = _vo_line(s)
        if v is not None:
            seq.append((v[0], v[1])); continue
        if _is_dialogue(s) is not None:
            seq.append(("dia", s)); continue
        if s.startswith("△"):
            seq.append(("act", s)); continue

    os_cnt = sum(1 for c, _ in seq if c == "os")
    vo_cnt = sum(1 for c, _ in seq if c == "vo")
    if os_cnt > prof["os"]:
        fails.append(f"E12 [{profile}] inner monologue x{os_cnt} > {prof['os']}: monologue is a quota tool, excess is padding")
    if vo_cnt > prof["vo"]:
        fails.append(f"E12 [{profile}] narration / caption x{vo_cnt} > {prof['vo']}: narration only serves pointing out turns")
    for cls, body in seq:
        if cls in ("os", "vo"):
            cap = prof["os_len"] if cls == "os" else prof["vo_len"]
            n = count_words(body)
            if n > cap:
                fails.append(f"E12 {'inner monologue' if cls == 'os' else 'narration / caption'} single line {n} words >{cap} ({body[:30]}…)")

    for i in range(len(seq) - 1):
        if seq[i][0] in ("os", "vo") and seq[i + 1][0] in ("os", "vo"):
            fails.append("E13 two monologue / narration lines back to back (no back-to-back): separate them with action or dialogue")
            break
    bi = next((i for i, (c, _) in enumerate(seq) if c == "break"), None)
    if bi is not None and bi > 0 and seq[bi - 1][0] in ("os", "vo"):
        fails.append("E13 monologue / narration right before the cliffhanger: the cliffhanger must land on an image / event "
                     "(a monologue ending is a soft ending)")

    for cls, body in seq:
        if cls not in ("os", "vo"):
            continue
        for w in VO_EXPO_WORDS:
            if _has(body, w):
                warns.append(f"E14 monologue carries exposition / backstory signal '{w}': monologue must not deliver setup (red line 2)")
                break
        for w in VO_ABSTRACT_WORDS:
            if _has(body, w):
                warns.append(f"E14 monologue states abstract emotion '{w}': write a concrete ledger (I gave him five children), not abstract feelings")
                break

    for s in first_content_lines(text, 3):
        if _vo_line(s):
            fails.append("E15 monologue / narration in the first 3 seconds: the golden 3 seconds must be on-scene conflict "
                         "(a monologue opening is a soft open; breaks red line 1)")
            break

    # E16 inflated duration / E17 long-tier downgrade
    # v4.9.1 fix: (1) the seconds unit is optional in 【Episode Length】 (old "：180" without a unit bypassed the check);
    # (2) E16 applies to all tiers -- any tier that declares 【Episode Length】 is checked at 3.0 words/s to prevent inflation;
    # E17 (< 150 s blocked as a downgrade) still applies to the long tier only.
    m_dur = re.search(r"【Episode Length】[:：]?\s*(\d{2,4})(?:\s*(?:seconds?|secs?|s)\b)?", text, re.I)
    if m_dur:
        dlg_words = 0
        action_lines = 0
        for line in text.splitlines():
            s = line.strip()
            v = _vo_line(s)
            d = _is_dialogue(s)
            if v is not None:
                dlg_words += count_words(v[1])
            elif d is not None:
                dlg_words += count_words(d)
            elif s.startswith("△"):
                action_lines += 1
        est = dlg_words / DLG_PER_SEC + action_lines * act_credit + 5
        claimed = int(m_dur.group(1))
        if claimed > est * 1.20:
            fails.append(
                f"E16 inflated duration: labeled {claimed}s, but dialogue supports at most {est:.0f}s "
                f"(pure dialogue {dlg_words} words / 3.0 words/s reference rate + {action_lines} action beats x {act_credit}s [{mode}] + padding) -- "
                "reference rate 3.0 words/s (local ceiling 4.2 x dialogue share 0.7), tolerance +/-20%; add dialogue or label the true duration; "
                "action-line words do not count toward duration, so do not pad volume with atmosphere △ lines to inflate")

        if profile == "long" and claimed < LONG_MIN_SEC:
            fails.append(
                f"E17 long-tier downgrade: labeled {claimed}s is below the long-tier floor {LONG_MIN_SEC}s -- "
                f"long-tier label, standard-tier volume (pure dialogue only {dlg_words} words, supports {est:.0f}s). Two ways out: "
                "(1) add pure dialogue to make a real long tier (150s ~= 447 words / 180s ~= 533 / 195s ~= 580 pure dialogue, reference medians); "
                "(2) explicitly switch to --format standard (90~120 s). "
                "Do not pad with action lines and then label a short duration to dodge E16")

    for prev in prev_texts:
        prev_set = set(_norm_line(p) for p in (_is_dialogue(l) for l in prev.splitlines()) if p)
        for d in my_lines:
            dd = _norm_line(d)
            if dd in prev_set and count_words(dd) >= 5:
                warns.append(f"E8 dialogue repeats prior episode: {dd[:40]}…")

    for w in REDLINE_WORDS:
        if re.search(r"\b" + re.escape(w), text, re.I):
            fails.append(f"E10 compliance one-strike graphic depiction '{w}'")

    # ---- E19 15-second dialogue density + E24 consecutive dry-talk gap detection (v4.9) ----
    run_words = 0
    run_lines = 0
    max_dry_run = 0
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        d = _is_dialogue(s)
        if d is not None:
            run_words += count_words(d)
            run_lines += 1
            if run_lines > max_dry_run:
                max_dry_run = run_lines
            continue
        if run_words > WIN15_MAX_WORDS:
            warns.append(f"E19 15-second dialogue overload: {run_words} words in a row exceed the {WIN15_MAX_WORDS}-word cap "
                         f"(= {run_words / 15:.2f} words/s vs. a {WIN15_MAX_WORDS / 15:.2f} words/s ceiling); insert a △ action beat or split")
        run_words = 0
        run_lines = 0
    if run_words > WIN15_MAX_WORDS:
        warns.append(f"E19 15-second dialogue overload: {run_words} words in a row exceed the {WIN15_MAX_WORDS}-word cap "
                     f"(= {run_words / 15:.2f} words/s vs. a {WIN15_MAX_WORDS / 15:.2f} words/s ceiling); insert a △ action beat or split")
    if max_dry_run > DRY_DLG_RUN_MAX:
        warns.append(f"E24 dry-talk gap: {max_dry_run} dialogue lines in a row with no △ action support (limit {DRY_DLG_RUN_MAX} lines); "
                     "the scene risks becoming a static radio drama -- suggest a strong-visual △ every 2~4 dialogue lines "
                     "(physical result / identity contrast / evidence clash)")

    # ---- E20 single action <= 27 words + E21 dialogue/action ratio 25%~70% + E26 invalid micro-action (v4.9) ----
    act_total = 0
    dlg_total = 0
    weak_act_hit = None
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("△"):
            body = re.sub(r"^△\s*", "", s)
            n = count_words(body)
            if n > ACT_SEG_MAX:
                warns.append(f"E20 action segment {n} words (>{ACT_SEG_MAX}), consider splitting into two △ shots")
            # v4.9.1 fix: a weak micro-action still warns even when wrapped in a long atmosphere description (> 14 words);
            # but a combined △ that has a strong action marker (evidence smash / physical clash) does not false-positive
            if weak_act_hit is None:
                for w in WEAK_MICRO_ACTIONS:
                    if _has(body, w):
                        if not any(_has(body, m) for m in STRONG_ACT_MARKERS):
                            weak_act_hit = body
                        break
            act_total += n
        else:
            d = _is_dialogue(s)
            if d is not None:
                dlg_total += count_words(d)
    if weak_act_hit is not None:
        warns.append(f"E26 invalid micro-action: '△ {weak_act_hit}' has no visible physical result or evidence clash -- "
                     "rewrite it as one of the three visual anchors (physical destruction / identity-contrast action / evidence reveal), "
                     "see references/craft-quality-layer.md §4 addendum")

    denom = dlg_total + act_total
    if denom > 0:
        ratio = dlg_total / denom
        pct = int(round(ratio * 100))
        if ratio > 0.70:
            warns.append(f"E21 dialogue share {pct}%>70%, lacks physical conflict and audio-visual staging")
        else:
            _lo = 0.10 if mode == "Action" else (0.15 if mode == "Mixed" else 0.25)
            if ratio < _lo:
                warns.append(f"E21 dialogue share {pct}%<{int(_lo*100)}%, lacks verbal sparring" + (f" ({mode} relaxed)" if mode != "Dialogue" else ""))

    # ---- E22 dialogue wording / typos + E25 riddle jargon and untranslated setting terms (v4.9) ----
    _hit = set()
    _jargon_hit = set()
    for _raw in text.splitlines():
        _s = _raw.strip()
        if not _s or _s.startswith(("【", "[", "#", ">", "△")):
            continue
        for _pat, _bad, _good in _TYPO_LITERAL_RES:
            if _bad not in _hit and _pat.search(_s):
                _hit.add(_bad)
                warns.append(f"E22 dialogue wording: '{_bad}' is likely '{_good}'")
        for _pat, _note in _TYPO_REGEX_RES:
            _m = _pat.search(_s)
            if _m and _note not in _hit:
                _hit.add(_note)
                warns.append(f"E22 dialogue wording: '{_m.group(0)}' -- {_note}")
        for _jw in OBSCURE_JARGON_WORDS:
            if _jw not in _jargon_hit and _has(_s, _jw):
                _jargon_hit.add(_jw)
                warns.append(f"E25 jargon alert: dialogue contains obscure term '{_jw}' -- translate it on the spot into plain language "
                             "with concrete stakes (how much money / who lives or dies / what evidence)")

    return fails, warns, nc


FRAG_RUN = 5        # N12: consecutive short dialogue lines threshold (each line <= 3 words)
FRAG_LEN = 3        # N12: short-line cap in words (4 chars ~= 3 words)
DUMP_ACT = 12       # N13: action-line count threshold
DUMP_AVG = 9        # N13: average words per action line cap (14 chars ~= 9 words)
NEAR_LO = 10        # N14: "near the floor" tolerance in words (15 chars ~= 10 words)
BRK_MIN = 13        # N14: cliffhanger frame word floor (20 chars ~= 13 words)


def collect_notes(text, profile="auto"):
    """Protective counterexample hints (NOTE level) -- explicitly NOT defects; hint that you may have 'over-corrected'."""
    profile = resolve_profile(text, profile)
    prof = PROFILES[profile]
    mode = conflict_mode(text)
    notes = []

    # N12 fragmenting: >= FRAG_RUN consecutive dialogue lines, each <= FRAG_LEN words
    run, run_start = 0, ""
    for line in text.splitlines():
        d = _is_dialogue(line)
        if d is None:
            continue
        if count_words(d) <= FRAG_LEN:
            if run == 0:
                run_start = d.strip()
            run += 1
            if run >= FRAG_RUN:
                notes.append("N12 %d+ consecutive short dialogue lines (<= %d words), starting at '%s': may be chopping full sentences "
                             "to dodge the clause cap. Saying it in full is not a defect -- under power pressure, shame or formal settings "
                             "a character may speak more politely and more completely, not in fragments" % (FRAG_RUN, FRAG_LEN, run_start))
                break
        else:
            run = 0

    # N13 action padding: action lines >= DUMP_ACT, average <= DUMP_AVG words, and dialogue lines <= tier minimum
    act, dia = [], []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("△"):
            act.append(count_words(re.sub(r"^△\s*", "", s)))
        else:
            d = _is_dialogue(s)
            if d is not None:
                dia.append(d)
    if mode == "Dialogue" and act and len(act) >= DUMP_ACT and (sum(act) / len(act)) <= DUMP_AVG and len(dia) <= prof["lines"]:
        notes.append("N13 %d action lines averaging %.1f words, only %d dialogue lines: may be padding E1 volume with low-information action lines. "
                     "More action is not more drama -- merge repeated beats and let one action carry character, clue and emotion"
                     % (len(act), sum(act) / len(act), len(dia)))

    # N14 hugging the floor: volume <= floor + NEAR_LO and cliffhanger frame < BRK_MIN words
    nc = net_words(text)
    lo, _hi = net_band(text, profile)
    m = re.search(r"【Episode Cliffhanger】\s*[:：]?\s*(.*)", text)
    brk = count_words(m.group(1)) if m else 0
    if nc <= lo + NEAR_LO and brk < BRK_MIN:
        notes.append("N14 body %d is close to this tier's floor %d, cliffhanger frame only %d words: may be cutting necessary process "
                     "or making the cliffhanger too thin. Necessary process must not be cut just to hit the line; if this episode works on its "
                     "own (aftershock / fast-turn episode), state the reason in the delivery notes" % (nc, lo, brk))

    return notes


GOOD = """Episode 【1】: The Dragon King's Token · Opening Humiliation
【Golden 3-Second Hook】: Extreme humiliation
【Emotion Shift】: Publicly humiliated ➔ Swallows rage ➔ Reveals the token and strikes back ➔ Deadly cliffhanger
【Episode Length】: 105 s
[Scene]: INT. Private club · top floor · night
[Cast]: Lin Chen (hidden Dragon King), Chen Feng (arrogant rich heir), Su Qingxue (fiancée)

△ Close-up: A lit cigar is pressed hard into the collar of Lin Chen's faded shirt; smoke curls up, sparks fall.
△ Medium shot: Chen Feng holds Su Qingxue, sneering; bodyguards stand around the room.
Chen Feng (blowing out smoke): Kneel and drink this filthy water, and I'll transfer you the ten thousand for your life-saving money right here.
Su Qingxue (aloof): Lin Chen, don't be ungrateful. Know your place.
△ Close-up: Lin Chen's lowered eyes snap up; the fist at his side slowly clenches, knuckles going white.
Lin Chen (very low voice): Three years ago, when your Chen family was on its knees begging me to save them, did you wear this same face?
Chen Feng (flushed with rage): You're dead! Break his hands!
△ Four bodyguards lunge at once; Lin Chen catches the leader's wrist and twists it, bones crack, and a guard flies back to smash a whole liquor cabinet.
△ Glass shatters, liquor runs across the floor, the whole room goes silent; Chen Feng stumbles back and knocks over a tea table.
Chen Feng (weakly defiant): You... you dare touch me? Do you know who my father is?
△ Medium shot: The door swings open; the hotel manager, sweating, squeezes through the crowd and stands by, not daring to speak.
Su Qingxue (gripping her clutch): Lin Chen, if you walk out that door today, our engagement is over for good.
Lin Chen (brushing off his cuff): Engagement? When your Su family knelt and begged to cancel our wedding, did you remember to mention that word?
△ Su Qingxue's face flushes red, then pales; her fingers tighten on the strap of her bag, and she doesn't dare look up again.
Lin Chen: In Jiangcheng, the only ones who make me kneel are my late ancestors.
△ Lin Chen pulls a nine-dragon iron token from his coat and slams it on the table; the wine glasses all shatter.
Lin Chen (cold, every word a blade): Carry my Dragon King's Token: in ten minutes, Chen Group of Jiangcheng goes bankrupt.
△ Close-up: Chen Feng stares at the nine-dragon emblem on the token; his legs tremble violently, his phone buzzes nonstop, the caller ID reads "Father".
Lin Chen (very low voice): Three years. Every debt your family owes me is right here, line by line.
Chen Feng (hoarse): I... I was wrong. I'll go apologize to you right now.
Lin Chen: Save the apology for my lawyer.
△ Chen Feng's knees buckle; he grabs the table to keep from kneeling.
Su Qingxue (trembling voice): Lin Chen, we had a bond once. Don't wipe us out completely.
Lin Chen (calmly): A bond? Did you forget it when you climbed on top of it?
△ Not one bodyguard dares step forward; they all back away toward the door.
Lin Chen: Whoever walks out that door today, I won't chase.
△ The words have barely landed when the bodyguards scramble for the exit.
Chen Feng (anxious): You even bought them off?
Lin Chen: I didn't need to buy them. They just see more clearly which way the wind is blowing.
Su Qingxue: Lin Chen, for the sake of our past, spare the Chen family.
Chen Feng: Dad... Dad, where are you...
Su Qingxue: I don't know anything about any of this.
△ Chen Feng buries his face in his hands, shoulders shaking.
△ Chen Feng slumps to the floor; his phone screen is still lit, the call still flashing.

【Episode Cliffhanger】: Chen Feng trembles as he answers; a wail of despair comes through: "Rebel son, who on earth did you offend? The Chen family is finished!" Lin Chen steps forward and closes in, looking down at him. (Black screen: swipe to unlock Episode 2 now)
"""

BAD = """Episode 【1】
Morning. Lin Chen gets out of bed, draws the curtains, the sun rises. He walks slowly down the street.
Chen Feng: Lin Chen, you need to know that three years ago you killed my father, took thirty million from our family, and today I will make you pay in blood and return everything!
Lin Chen: Okay.
△ He picks up the dismembered limb.
"""


def self_test():
    ok = 1

    def _long_dlg(n):
        return "".join(f"Lin Chen: Line {i}, a back-and-forth that drops new information and raises the stakes.\n" for i in range(n))

    f, w, nc = validate(GOOD)
    if f:
        print("FAIL self-test: GOOD sample should not FAIL:", f); ok = 0
    if nc < 67:
        print("FAIL self-test: GOOD body word count abnormal", nc); ok = 0
    f, w, _ = validate(BAD)
    if not any("E1" in x for x in f):
        print("FAIL self-test: BAD should report E1 (or word count anomaly)"); ok = 0
    if not any("E4" in x for x in f):
        print("FAIL self-test: BAD should report E4 (no conflict in first 3 seconds)"); ok = 0
    if not any("E6" in x for x in f):
        print("FAIL self-test: BAD should report E6 (missing cliffhanger)"); ok = 0
    if not any("E10" in x for x in f):
        print("FAIL self-test: BAD should report E10 (red-line word)"); ok = 0
    if not any("E5" in x for x in w):
        print("FAIL self-test: BAD should report E5 (opener banned word)"); ok = 0

    # Regression 1: field lines must not feed E1 body volume
    hdr_only = ("Episode 【1】\n【Stage】: Act X · (Ep 1/80 | return round N)\n【Golden 3-Second Hook】: Extreme humiliation (wedding public shaming)\n"
                "【Emotion Shift】: Humiliated ➔ Swallows rage ➔ Strikes back ➔ Deadly cliffhanger\n【Episode Length】: 108 s\n"
                "[Scene]: INT. Club · night\n[Cast]: Lin Chen, Chen Feng\n")
    if net_words(hdr_only) != 0:
        print("FAIL self-test: pure field / marker lines should count 0 words, got", net_words(hdr_only)); ok = 0

    # Regression 2: a script opening with an empty △ shot must be blocked by E4
    boring = ("Episode 【1】\n[Scene]: INT. Living room · day\n[Cast]: Ann, Ben\n"
              "△ He slowly walks into the living room, picks up a teacup and takes a sip.\n"
              "△ He looks out the window.\nAnn: Nice weather today.\nBen: Yes.\nAnn: Well then, that's it.\nBen: Okay.\n"
              "【Episode Cliffhanger】: The two say goodbye. (Black screen)\n")
    f, w, _ = validate(boring)
    if not any("E4" in x for x in f):
        print("FAIL self-test: script opening with empty △ shots should report E4"); ok = 0

    # Regression 3: comic-drama tier body volume (220~415) must be usable
    anime = ("Episode 【1】: comic-drama\n【Emotion Shift】: Humiliated ➔ Swallows rage ➔ Strikes back ➔ Deadly cliffhanger\n"
             "[Scene]: INT. Hall · day\n[Cast]: Ann, Ben\n"
             + "".join(f"△ Concrete physical action beat number {i}, a camera-visible event that pushes the episode's conflict forward.\n" for i in range(18))
             + "Ann: Are you sure you want to do this?\nBen: I'm sure.\nAnn: Then don't blame me.\nBen: Come on.\n"
             "【Episode Cliffhanger】: Lights go out, people scatter, only one strike left. (Black screen: swipe to unlock)\n")
    f, w, _ = validate(anime)
    if any("E1" in x for x in f):
        print("FAIL self-test: comic tier should not report E1 conflict:", [x for x in f if 'E1' in x]); ok = 0

    # Regression 4: dialogue cap 17 words (WARN, not blocking)
    longline = ("Episode 【1】\n[Scene]: INT.\n[Cast]: Ann\n△ Slams the table.\n"
                "Ann: This is a long compound sentence with no pauses that is meant to trigger the warning check and confirm that the cap is actually working in practice today.\n"
                "【Episode Cliffhanger】: Black screen (black screen)\n")
    f, w, _ = validate(longline)
    if not any("E2" in x for x in w):
        print("FAIL self-test: dialogue over 17 words should report E2"); ok = 0

    # Regression 5: long tier (150~195 s flexible)
    long_body = ("".join(f"△ Force event {i}: a slap is caught mid-air and twisted back, the conflict climbs another level.\n" for i in range(10))
                 + _long_dlg(48))
    long_good = ("Episode 【1】: long-tier sample (long tier · about 3 minutes)\n【Episode Length】: 180 s\n"
                 "[Scene]: INT. Private club · night\n[Scene]: INT. Corridor · night\n[Cast]: Lin Chen, Chen Feng\n"
                 + long_body
                 + "【Mid-Episode Hook】: The phone lights up with a critical-condition notice, payment due tonight, and on the other end the caller hangs up.\n"
                 + "△ Lin Chen twists the wrist back, bones crack, and the iron bar rolls off.\n"
                 + "【Episode Cliffhanger】: A wail of despair comes from the other end of the line; Chen Feng's legs tremble. (Black screen: swipe to unlock Episode 2)\n")
    f, w, nc = validate(long_good)
    if f:
        print("FAIL self-test: long-tier sample should not FAIL:", f, "body", nc); ok = 0
    if not (NET_LONG_MIN <= nc <= NET_LONG_MAX):
        print(f"FAIL self-test: long-tier sample body {nc} should be within {NET_LONG_MIN}~{NET_LONG_MAX}"); ok = 0
    f, _, _ = validate(long_good.replace("【Mid-Episode Hook】", "【Midpoint】"))
    if not any("E11" in x for x in f):
        print("FAIL self-test: long tier missing midpoint hook should report E11"); ok = 0
    f, _, _ = validate(long_good.replace(_long_dlg(48), _long_dlg(16)))
    if not any("E16" in x for x in f):
        print("FAIL self-test: too few dialogue lines while labeling 180 s should report E16 inflated duration:", f); ok = 0
    f, _, _ = validate(long_good.replace("【Episode Length】: 180 s", "【Episode Length】: 110 s"), profile="long")
    if not any("E17" in x for x in f):
        print("FAIL self-test: long tier labeled 110 s should report E17 downgrade:", f); ok = 0
    for _d in (150, 180, 195):
        f, _, _ = validate(long_good.replace("【Episode Length】: 180 s", f"【Episode Length】: {_d} s"), profile="long")
        if any("E17" in x for x in f):
            print(f"FAIL self-test: long tier labeled {_d} s should not report E17:", [x for x in f if "E17" in x]); ok = 0
    f, w, _ = validate(GOOD, profile="long")
    if not any("E11" in x for x in f):
        print("FAIL self-test: standard sample checked explicitly as long should report E11"); ok = 0
    f, _, _ = validate(BAD, profile="long")
    if not any("E1" in x for x in f):
        print("FAIL self-test: extreme empty draft should report E1"); ok = 0
    f, _, _ = validate(long_good.replace("【Episode Length】: 180 s", "【Episode Length】: 60 s"), profile="comic")
    if any("E1" in x for x in f):
        print("FAIL self-test: exceeding the reference band upper limit should not FAIL:", [x for x in f if "E1" in x]); ok = 0
    f, _, _ = validate(long_good + "[Scene]: INT. Garage · night\n[Scene]: INT. Rooftop · night\n")
    if not any("E3" in x for x in f):
        print("FAIL self-test: long tier with 4 scenes should report E3"); ok = 0

    # ---- Protective counterexamples (NOTE level) regression ----
    n = collect_notes(GOOD)
    if n:
        print("FAIL self-test: GOOD sample should not produce NOTE:", n); ok = 0
    n = collect_notes(long_good)
    if n:
        print("FAIL self-test: long-tier sample should not produce NOTE:", n); ok = 0

    frag = ("Episode 【1】\n[Scene]: INT. Main hall · day\n[Cast]: Ann, Ben\n△ A slap is caught mid-air by the wrist.\n"
            "Ann: Kneel.\nBen: On what grounds?\nAnn: Shut up.\nBen: You dare?\nAnn: Say it again.\nBen: Fine.\n"
            "【Episode Cliffhanger】: The slap lands, the whole hall goes silent, footsteps rush outside, every head turns toward the door, the frame freezes. (Black screen: swipe to unlock Episode 2 now)\n")
    if not any("N12" in x for x in collect_notes(frag)):
        print("FAIL self-test: consecutive short dialogue should report N12 fragmenting"); ok = 0

    dump = ("Episode 【1】\n[Scene]: INT.\n[Cast]: Ann\n"
            + "".join("△ He raises a hand.\n" for _ in range(14))
            + "Ann: You're here.\n"
            + "【Episode Cliffhanger】: The door opens, light floods in, Ann slowly looks up, the frame freezes, swipe to unlock the next episode.\n")
    if not any("N13" in x for x in collect_notes(dump)):
        print("FAIL self-test: low-information action padding should report N13"); ok = 0

    thin = ("Episode 【1】\n[Scene]: INT.\n[Cast]: Ann\n△ He slams a knife on the table.\nAnn: Speak.\n"
            "【Episode Cliffhanger】: Black screen.\n")
    if not any("N14" in x for x in collect_notes(thin)):
        print("FAIL self-test: body hugging the floor with a thin cliffhanger should report N14"); ok = 0

    for sample in (frag, dump, thin, GOOD):
        f, _, _ = validate(sample)
        bad = [x for x in f if re.match(r"^N\d", x)]
        if bad:
            print("FAIL self-test: NOTE level should not appear in the FAIL list:", bad); ok = 0

    # ---- Monologue / narration (VO) regression ----
    vo_fill = ("Episode 【1】\n[Scene]: INT. Main hall · day\n[Cast]: Helen, Second Daughter-in-law\n"
               "△ A slap is caught mid-air by the wrist, the whole hall goes dead silent.\n"
               "Second Daughter-in-law: Helen, tell me the truth.\n"
               "△ Helen's hand tightens on her apron, knuckles white.\n"
               "Inner Monologue: I gave him five children.\n"
               "△ The daughter-in-law jabs a finger at her nose.\n"
               "Helen: I say yes.\n"
               "△ Everyone in the hall turns their heads at once.\n"
               "Narration: The meek one fought back.\n"
               "Second Daughter-in-law: Say it.\n"
               "【Episode Cliffhanger】: The door is kicked open, the hall falls dead silent. (Black screen: swipe to unlock Episode 2 now)\n")
    f, w, _ = validate(vo_fill)
    if not any("E9" in x for x in w):
        print("FAIL self-test: monologue should not count as a dialogue line (should report E9 too few)"); ok = 0
    if any("E12" in x or "E13" in x or "E15" in x for x in f):
        print("FAIL self-test: compliant monologue sample should not report E12/E13/E15:", f); ok = 0

    vo28 = "I gave him five children. The day he died, I was still sewing his jacket by the lamp."
    vo_long = ("Episode 【1】: long-tier sample (long tier · about 3 minutes)\n[Scene]: INT. Main hall · day\n[Cast]: Helen\n"
               "△ A slap is caught mid-air by the wrist, the whole hall goes silent.\n"
               "Helen: You're back.\n"
               "△ The daughter-in-law jabs a finger at her nose, and everyone turns to stare, eyes nailed to her face.\n"
               + f"Inner Monologue: {vo28}\n"
               + "【Mid-Episode Hook】: The phone lights up with a critical notice, payment due tonight.\n"
               + "△ Twist the wrist back, and the iron bar rolls off.\nAnn: Kneel.\n"
               + "【Episode Cliffhanger】: The door is kicked open, the hall falls dead silent. (Black screen: swipe to unlock Episode 2 now)\n")
    f, w, _ = validate(vo_long)
    if any(x.startswith("E2 ") for x in w):
        print("FAIL self-test: monologue should not hit the E2 dialogue cap:", [x for x in w if x.startswith("E2 ")]); ok = 0
    if any("E12" in x for x in f):
        print("FAIL self-test: 18-word long-tier monologue should not report E12 (cap 20):", [x for x in f if "E12" in x]); ok = 0

    f, _, _ = validate(vo_fill.replace("Narration: The meek one fought back.", "Inner Monologue: This life, I owe nobody anything anymore."))
    if not any("E12" in x for x in f):
        print("FAIL self-test: 2 inner monologues in standard tier should report E12"); ok = 0

    f, _, _ = validate("Episode 【1】\n[Scene]: INT. Main hall · day\n[Cast]: Ann\n△ A slap is caught mid-air by the wrist.\n"
                       "Inner Monologue: I gave him five children.\nNarration: The meek one fought back.\n"
                       "Ann: Are you saying so?\nBen: I say yes.\nCara: I say no.\n"
                       "【Episode Cliffhanger】: The door is kicked open, the hall falls dead silent. (Black screen: swipe to unlock Episode 2 now)\n")
    if not any("E13" in x for x in f):
        print("FAIL self-test: two monologue lines back to back should report E13"); ok = 0

    f, _, _ = validate("Episode 【1】\n[Scene]: INT. Main hall · day\n[Cast]: Ann\n△ A slap is caught mid-air by the wrist.\n"
                       "Ann: Are you saying so?\nBen: I say yes.\nCara: I say no.\nDan: I say yes.\n"
                       "Inner Monologue: This life, I owe nobody anything anymore.\n"
                       "【Episode Cliffhanger】: The door is kicked open, the hall falls dead silent. (Black screen: swipe to unlock Episode 2 now)\n")
    if not any("E13" in x for x in f):
        print("FAIL self-test: monologue right before the cliffhanger should report E13"); ok = 0

    f, _, _ = validate("Episode 【1】\n[Scene]: INT. Main hall · day\n[Cast]: Ann\n"
                       "Inner Monologue: I gave him five children.\n△ A slap is caught mid-air by the wrist.\n"
                       "Ann: Are you saying so?\nBen: I say yes.\n"
                       "【Episode Cliffhanger】: The door is kicked open, the hall falls dead silent. (Black screen: swipe to unlock Episode 2 now)\n")
    if not any("E15" in x for x in f):
        print("FAIL self-test: monologue in the first 3 seconds should report E15"); ok = 0

    f, w, _ = validate(vo_fill.replace("Inner Monologue: I gave him five children.", "Inner Monologue: It all started thirty years ago."))
    if not any("E14" in x for x in w):
        print("FAIL self-test: monologue carrying exposition should report E14"); ok = 0

    # ---- Dialogue tone-cue supply (E18 · v3.4.3) regression ----
    f, w, _ = validate(GOOD.replace("Su Qingxue (aloof):", "Su Qingxue (angry):"))
    if not any("E18a" in x for x in w):
        print("FAIL self-test: vague emotion word in parenthetical should report E18a:", [x for x in w if "E18" in x]); ok = 0
    t2 = GOOD
    for a, b in (("(blowing out smoke)", "(toying with a lighter)"), ("(aloof)", "(arms folded)"),
                 ("(very low voice)", "(staring at him)"), ("(cold, every word a blade)", "(pointing at the token)"),
                 ("(flushed with rage)", "(kicks over a chair)"), ("(weakly defiant)", "(steps back)"),
                 ("(hoarse)", "(clenches a fist)"), ("(trembling voice)", "(bows head)"), ("(calmly)", "(turns away)")):
        t2 = t2.replace(a, b)
    f, w, _ = validate(t2)
    if not any("E18b" in x for x in w):
        print("FAIL self-test: whole script with zero tone cues should report E18b:", [x for x in w if "E18" in x]); ok = 0
    t3 = GOOD.replace("Su Qingxue (aloof):", "Su Qingxue (arms folded, stepping back ｜ aloof and distant):")
    f, w, _ = validate(t3)
    if any("E18a" in x or "E18b" in x for x in w):
        print("FAIL self-test: compliant tone-cue supply should not report E18:", [x for x in w if "E18" in x]); ok = 0
    t4 = GOOD.replace("Lin Chen (very low voice): Three years ago, when your Chen family was on its knees begging me to save them, did you wear this same face?",
                      "Lin Chen: You could of walked away, but you didn't.")
    f, w, _ = validate(t4)
    if not any("E22" in x for x in w):
        print("FAIL self-test: typo should report E22:", [x for x in w if "E22" in x]); ok = 0

    _act_body = ("[Scene]: INT. Stairwell · night\n[Cast]: Ethan, Uncle Dave\n"
                 + "".join(f"△ Prep beat {i}: he bolts another steel plate on, sparks fly, the position gets one notch safer.\n" for i in range(14))
                 + "Uncle Dave (sneering): You're going to tear the whole building down and rebuild it?\n"
                 + "△ Ethan doesn't look up; he keeps turning the bolt.\n"
                 + "Uncle Dave (loudly): I already talked to the property office. They're coming to demolish it tomorrow.\n"
                 + "△ Ethan tightens the bolts to the end, the back of his hand corded with tendons.\n"
                 + "Uncle Dave (knocks on the steel plate): Night after night of this. What do you even want out of it?\n"
                 + "△ Ethan bends down and hammers the last rivet in.\n"
                 + "Ethan (calm): The power goes out tomorrow. You still have time to go downstairs now.\n"
                 + "△ Ethan turns and pushes the water barrel to the door.\n"
                 + "Uncle Dave (laughing loudly): Power outage? Only you would believe that, you lunatic.\n"
                 + "【Mid-Episode Hook】: The streetlights all go out; the whole compound sinks into darkness.\n"
                 + "【Episode Cliffhanger】: A second dull thud comes from downstairs, and the backup generator doesn't start. (Black screen: swipe to unlock)\n")
    _hdr = "Episode 【1】\n【Skeptic Supporting Character】: Uncle Dave\n【Episode Length】: 180 s\n"
    f1, w1, _ = validate(_hdr + "【Conflict Mode】: Action\n" + _act_body, profile="long")
    f2, w2, _ = validate(_hdr + _act_body, profile="long")
    if not any("E9" in x for x in w2) or not any("E21" in x for x in w2):
        print("FAIL self-test: dialogue-mode (no mode marker) sample should report E9/E21:", w2); ok = 0
    if any("E9" in x for x in w1) or any("E21" in x for x in w1):
        print("FAIL self-test: Action mode should not report E9/E21:", w1); ok = 0
    _t6 = ("Episode 【1】\n【Skeptic Supporting Character】: Uncle Dave\n【Episode Length】: 150 s\n[Scene]: INT. Rooftop\n[Cast]: Ethan, Uncle Dave\n"
           + "".join(f"△ Prep beat {i}: he bolts the steel plate on piece by piece, sparks fly, the position gets one notch safer.\n" for i in range(20))
           + "".join(f"Ethan: Line number {i}, about twelve words of argument goes right here now.\n" for i in range(20)))
    _fa, _, _ = validate(_t6, profile="long")
    _fb, _, _ = validate("【Conflict Mode】: Action\n" + _t6, profile="long")
    if not any("E16" in x for x in _fa):
        print("FAIL self-test: Dialogue mode with too few lines should report E16"); ok = 0
    if any("E16" in x for x in _fb):
        print("FAIL self-test: Action mode should not report E16 (action beat weight x2.5):", [x for x in _fb if "E16" in x]); ok = 0
    _t7 = ("Episode 【1】\n【Skeptic Supporting Character】: Uncle Dave\n【Episode Length】: 150 s\n[Scene]: INT. Rooftop\n[Cast]: Ethan, Uncle Dave\n"
           + "".join(f"△ Prep beat {i}: he bolts a steel plate on, sparks fly, the position gets one notch safer.\n" for i in range(14))
           + "".join("Ethan: Say it, then I'm straight back to work on the steel.\n" for _ in range(6)))
    _f7n, _w7n, _ = validate(_t7, profile="long")
    _f7m, _w7m, _ = validate("【Conflict Mode】: Mixed\n" + _t7, profile="long")
    if not any("E9" in x for x in _w7n) or not any("E21" in x for x in _w7n):
        print("FAIL self-test: Dialogue mode should report E9/E21:", _w7n); ok = 0
    if any("E9" in x for x in _w7m) or any("E21" in x for x in _w7m):
        print("FAIL self-test: Mixed mode should not report E9/E21:", _w7m); ok = 0
    _t8 = ("Episode 【1】\n【Skeptic Supporting Character】: Uncle Dave\n[Scene]: INT.\n[Cast]: Ethan, Uncle Dave\n"
           + "".join("△ He nods.\n" for _ in range(14))
           + "Uncle Dave: You're out of your mind.\nEthan: Mm.\nUncle Dave: Really out of your mind.\nEthan: Mm.\n"
           + "【Episode Cliffhanger】: The door blows open, the steel plate sways in the night, the light goes out. (Black screen: swipe to unlock)\n")
    if not any("N13" in x for x in collect_notes(_t8, "long")):
        print("FAIL self-test: Dialogue mode action padding should report N13"); ok = 0
    if any("N13" in x for x in collect_notes("【Conflict Mode】: Action\n" + _t8, "long")):
        print("FAIL self-test: Action mode should not report N13 (action padding exemption)"); ok = 0
    _t9 = ("Episode 【1】\n【Episode Length】: 150 s\n[Scene]: INT. Stairwell\n[Cast]: Ethan, Uncle Dave\n"
           "△ He hauls thirty crates of bottled water up the stairs one by one and stacks them at the door.\n"
           + "Ethan: Mm.\nUncle Dave: Mm.\nEthan: Mm.\nUncle Dave: Mm.\nEthan: Mm.\nUncle Dave: Mm.\nEthan: Mm.\nUncle Dave: Mm.\n"
           "【Episode Cliffhanger】: The lights go out, but the door is still lit. (Black screen: swipe to unlock)\n")
    _f9a, _, _ = validate(_t9, profile="long")
    _f9b, _, _ = validate("【Conflict Mode】: Action-Persistence\n" + _t9, profile="long")
    if not any("E4" in x for x in _f9a):
        print("FAIL self-test: no mode marker with an unusual-action opener should report E4"); ok = 0
    if any("E4" in x for x in _f9b):
        print("FAIL self-test: Action mode unusual-action opener should not report E4:", [x for x in _f9b if "E4" in x]); ok = 0

    # ---- E19 15-second dialogue density regression ----
    e19 = ("Episode 【1】\n[Scene]: INT. Hall · day\n[Cast]: Ann, Ben\n△ A slap is caught mid-air by the wrist.\n"
           + "".join(f"Ann: Round {i}, a continuous back-and-forth line that walks through new evidence, new cost and pressure, step by step.\n" for i in range(6))
           + "Ben: I know.\n"
           + "【Episode Cliffhanger】: The whole hall goes silent, the frame freezes. (Black screen: swipe to unlock Episode 2 now)\n")
    f, w, _ = validate(e19)
    if not any("E19" in x for x in w):
        print("FAIL self-test: consecutive dialogue over 63 words should report E19 WARN:", w); ok = 0
    e19_ok = ("Episode 【1】\n[Scene]: INT. Hall · day\n[Cast]: Ann, Ben\n△ A slap is caught mid-air by the wrist.\n"
              "Ann: First round of continuous back-and-forth, walking through new evidence, new cost and pressure step by step.\n△ Ann grips the other's wrist.\n"
              "Ben: Second round of continuous back-and-forth, carrying new cost and pressure step by step.\n△ Ben steps back half a pace.\n"
              "Ann: Third round of continuous back-and-forth, pressing new evidence on top step by step.\n"
              "【Episode Cliffhanger】: The whole hall goes silent, the frame freezes. (Black screen: swipe to unlock Episode 2 now)\n")
    f, w, _ = validate(e19_ok)
    if any("E19" in x for x in w):
        print("FAIL self-test: dialogue with action-beat breaks should not report E19:", w); ok = 0

    # ---- E20 single action <= 27 words / E21 dialogue-action ratio regression ----
    e20 = ("Episode 【1】\n[Scene]: INT. Hall · day\n[Cast]: Ann, Ben\n"
           "△ Close-up: Chen Feng stares hard at the nine-dragon emblem on the token on the table, his legs tremble violently, his phone buzzes nonstop, the caller ID reads Father, and he collapses onto the floor, unable to stand up again.\n"
           "Ann: Kneel.\nBen: You dare?\nAnn: Shut up.\nBen: Fine.\n"
           "【Episode Cliffhanger】: The door is kicked open, the hall falls dead silent. (Black screen: swipe to unlock Episode 2 now)\n")
    f, w, _ = validate(e20)
    if not any(x.startswith("E20 ") for x in w):
        print("FAIL self-test: single △ action over 27 words should report E20 WARN:", w); ok = 0
    bal_ok = ("Episode 【1】\n[Scene]: INT. Hall · day\n[Cast]: Ann, Ben\n△ Smack hits mid-air, caught by the wrist.\n"
              "Ann: You're going to settle this debt with me today.\n△ Ann grips the other's wrist.\n"
              "Ben: I've got nothing to settle with you.\n△ Ben steps back half a pace.\n"
              "Ann: Then don't blame me for turning on you.\n"
              "【Episode Cliffhanger】: The hall falls dead silent. (Black screen: swipe to unlock)\n")
    f, w, _ = validate(bal_ok)
    if any(x.startswith("E20 ") for x in w):
        print("FAIL self-test: short △ shots should not report E20:", w); ok = 0
    if any(x.startswith("E21 ") for x in w):
        print("FAIL self-test: balanced dialogue/action ratio should not report E21:", w); ok = 0
    e21_high = ("Episode 【1】\n[Scene]: INT. Hall · day\n[Cast]: Ann, Ben\n△ Slap.\n"
                + "".join(f"Ann: Round {i}, a lip-and-tongue duel that drops new evidence and new cost and presses the pressure step by step.\n" for i in range(8))
                + "【Episode Cliffhanger】: The hall falls dead silent. (Black screen: swipe to unlock)\n")
    f, w, _ = validate(e21_high)
    if not any(x.startswith("E21 ") and ">70%" in x for x in w):
        print("FAIL self-test: dialogue share over 70% should report E21 WARN:", w); ok = 0
    e21_low = ("Episode 【1】\n[Scene]: INT. Hall · day\n[Cast]: Ann, Ben\n"
               + "".join(f"△ Beat {i}: a concrete physical action, a camera-visible event that pushes conflict further.\n" for i in range(8))
               + "Ann: Come.\n"
               + "【Episode Cliffhanger】: The hall falls dead silent. (Black screen: swipe to unlock)\n")
    f, w, _ = validate(e21_low)
    if not any(x.startswith("E21 ") and "<25%" in x for x in w):
        print("FAIL self-test: dialogue share under 25% should report E21 WARN:", w); ok = 0

    # ---- v4.9 additions: E24 dry-talk gap / E25 riddle jargon / E26 invalid micro-action regression ----
    # T10: 7 consecutive dialogue lines with no △ support (under 63 words, so E19 does not fire) -> E24 WARN
    e24_dry = ("Episode 【1】\n[Scene]: INT. Hall · day\n[Cast]: Ann, Ben\n△ A slap is caught mid-air by the wrist.\n"
               "Ann (sharp): Hand over the money!\nBen (coldly): No money!\nAnn: You're dead!\nBen: You dare touch me?\n"
               "Ann: Look at whether I dare!\nBen: Come on then!\nAnn: Today you're not getting off easy!\n"
               "【Episode Cliffhanger】: The hall falls dead silent. (Black screen: swipe to unlock)\n")
    _, w24, _ = validate(e24_dry)
    if not any(x.startswith("E24 ") for x in w24):
        print("FAIL self-test: 7 consecutive dialogue lines with no △ should report E24 WARN:", w24); ok = 0
    if any(x.startswith("E24 ") for x in validate(GOOD)[1]):
        print("FAIL self-test: GOOD sample should not report E24"); ok = 0

    # T11: dialogue contains untranslated riddle jargon -> E25 WARN
    e25_jargon = GOOD.replace("Three years. Every debt your family owes me is right here, line by line.",
                              "Your fortune anchor has already triggered a karmic loop.")
    _, w25, _ = validate(e25_jargon)
    if not any(x.startswith("E25 ") for x in w25):
        print("FAIL self-test: riddle jargon should report E25 WARN:", w25); ok = 0

    # T12: a △ that is only an invalid micro-action -> E26 WARN
    _weak_line = "△ Chen Feng's knees buckle; he grabs the table to keep from kneeling."
    e26_weak = GOOD.replace(_weak_line, "△ Chen Feng's eyes flicker.")
    _, w26, _ = validate(e26_weak)
    if not any(x.startswith("E26 ") for x in w26):
        print("FAIL self-test: invalid micro-action should report E26 WARN:", w26); ok = 0

    # T13 (v4.9.1): a weak micro-action wrapped in a long atmosphere description still triggers E26
    e26_pad = GOOD.replace(_weak_line,
                           "△ Chen Feng's eyes flicker, the private room's lamplight is dim and yellow, everyone holds their breath.")
    _, w26b, _ = validate(e26_pad)
    if not any(x.startswith("E26 ") for x in w26b):
        print("FAIL self-test: long description wrapping eyes flicker should report E26:", w26b); ok = 0

    # T14 (v4.9.1): weak micro-action + strong physical-evidence action in one △ should NOT trigger E26
    e26_ok = GOOD.replace(_weak_line,
                          "△ Chen Feng is slightly stunned, and the teacup smashes on the floor into three pieces.")
    _, w26c, _ = validate(e26_ok)
    if any(x.startswith("E26 ") for x in w26c):
        print("FAIL self-test: weak micro-action + strong evidence action should not report E26:", w26c); ok = 0

    # T15 (v4.9.1): 【Episode Length】 without a unit must still trigger E16 (old version bypassed the check entirely)
    _t15 = long_good.replace("【Episode Length】: 180 s", "【Episode Length】: 180").replace(_long_dlg(48), _long_dlg(16))
    f, _, _ = validate(_t15)
    if not any("E16" in x for x in f):
        print("FAIL self-test: duration without a unit should still report E16:", f); ok = 0

    print("[+] self-test PASSED" if ok else "[-] self-test FAILED")
    return 0 if ok else 1


def parse_args(args):
    """Returns (path, profile, prev_paths); usage errors raise SystemExit(2)"""
    path, profile, prevs = None, "auto", []
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--prev":
            i += 1
            while i < len(args) and not args[i].startswith("--"):
                prevs.append(args[i]); i += 1
            continue
        if a == "--long":
            profile = "long"
        elif a == "--comic":
            profile = "comic"
        elif a == "--format" or a.startswith("--format="):
            val = a.split("=", 1)[1] if "=" in a else (args[i + 1] if i + 1 < len(args) else "")
            if "=" not in a:
                i += 1
            if val not in PROFILES:
                print(f"[-] --format only accepts {'/'.join(PROFILES)}, got '{val}'"); raise SystemExit(2)
            profile = val
        elif a.startswith("--"):
            print(f"[-] unknown argument '{a}'"); raise SystemExit(2)
        elif path is None:
            path = a
        i += 1
    return path, profile, prevs


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__); return 2
    if args[0] == "--self-test":
        return self_test()
    try:
        path, profile, prevs = parse_args(args)
    except SystemExit as e:
        return e.code or 2
    if not path:
        print(__doc__); return 2
    try:
        text = open(path, encoding="utf-8-sig").read()
    except FileNotFoundError:
        print(f"[-] script file not found: {path}"); return 2
    except IsADirectoryError:
        print(f"[-] path is a directory, not a script file: {path}"); return 2
    except UnicodeDecodeError:
        print(f"[-] file is not UTF-8 text, cannot read: {path}"); return 2
    except OSError as e:
        print(f"[-] cannot read script file: {path} ({e})"); return 2
    for p in prevs:
        try:
            open(p, encoding="utf-8-sig").read()
        except FileNotFoundError:
            print(f"[-] prev-episode file not found: {p}"); return 2
        except (UnicodeDecodeError, OSError):
            print(f"[-] cannot read prev-episode file: {p}"); return 2
    prev_texts = [open(p, encoding="utf-8-sig").read() for p in prevs]
    profile = resolve_profile(text, profile)
    fails, warns, nc = validate(text, prev_texts, profile)
    notes = collect_notes(text, profile)
    print(f"== {path}  [{profile} {PROFILES[profile]['label']}]  body word count≈{nc} ==")
    for x in fails:
        print("[-] FAIL:", x)
    for x in warns:
        print("[!] WARN:", x)
    for x in notes:
        print("[i] NOTE:", x, "  <- protective counterexample, no change required")
    if fails:
        print("Result: FAILED (fix and re-run)"); return 1
    tail = []
    if warns:
        tail.append("has WARN, please review")
    if notes:
        tail.append("has NOTE (not a defect; do not over-correct)")
    print("Result: PASSED" + ("(" + "; ".join(tail) + ")" if tail else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
