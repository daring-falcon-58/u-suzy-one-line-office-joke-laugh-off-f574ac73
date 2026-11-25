#!/usr/bin/env python3
"""One-Line Office Joke Laugh-Off -- entry program.

Method (full record: README.md and candidates.md in this repo):
  1. Read the soal first: the judge compares two one-line office jokes
     pairwise, weighing in order -- (a) really a one-line office joke,
     (b) a sharp, surprising punchline that earns a real laugh, (c) clear
     on one read, (d) fresh, avoiding office cliches, (e) tight wording.
  2. Generated 36 original candidates, avoiding the saturated premises in
     the live field (office plant, printer, "per my last email",
     meetings-that-should-have-been-emails, standup/Jira, reply-all,
     out-of-office replies, "we're a family here").
  3. Scored each candidate 0-5 on punchline / clarity / freshness /
     tightness; total = 3P + 2C + 2F + T (max 40). Top 8 scored 34-35.
  4. Ran a full pairwise tournament over the top 8 (28 pairs, decided by
     the judge's own sequential rule: first differing criterion decides).
     Winner: candidate #3, 7-0. Runner-up: candidate #35, 6-1.
  5. This program re-derives the pick from the scored shortlist and the
     tournament record, then writes the winning line to /output/entry.txt.

Gate (competition.yaml): /output/entry.txt must be UTF-8 text of 1-200
characters, not only whitespace. The winning line is 68 characters.
"""

import os
import sys

# Shortlist: the top 8 of 36 candidates, with rubric scores.
# (n, text, punchline, clarity, freshness, tightness)
SHORTLIST = [
    (3, "I've been on mute so long my own reflection stopped listening to me.",
     4, 5, 4, 5),
    (25, "I said 'you're on mute' so many times today that my dreams now "
         "come with a red microphone icon.", 4, 5, 4, 5),
    (1, "My performance review said I 'exceed expectations,' so I asked if "
        "that included the expectation that I'd still be here.", 4, 5, 4, 4),
    (12, "My onboarding buddy quit on day two, which HR called 'accelerated "
         "independence training.'", 4, 5, 4, 4),
    (15, "The wellness webinar on burnout was scheduled during lunch, so I "
         "burned out eating a sandwich.", 4, 5, 4, 4),
    (18, "The trust fall at the team offsite failed because Legal caught me "
         "first -- with a waiver.", 4, 5, 4, 4),
    (23, "The employee-of-the-month parking spot is empty, because the winner "
         "quit for a job with a parking lot.", 4, 5, 4, 4),
    (35, "The open floor plan means everyone can hear me sigh, which HR now "
         "tracks as 'engagement.'", 4, 5, 4, 4),
]

# Pairwise tournament over the top 8: (winner_n, loser_n), 28 pairs.
# Decided by the judge's sequential rule; full reasons in candidates.md.
TOURNAMENT = [
    (3, 25), (3, 1), (3, 12), (3, 15), (3, 18), (3, 23), (3, 35),
    (25, 1), (25, 12), (25, 15), (18, 25), (23, 25), (35, 25),
    (12, 1), (15, 1), (18, 1), (23, 1), (35, 1),
    (15, 12), (18, 12), (23, 12), (35, 12),
    (15, 18), (15, 23), (35, 15),
    (18, 23), (35, 18),
    (35, 23),
]


def weighted_score(entry):
    """Rubric total: 3*punchline + 2*clarity + 2*freshness + tightness."""
    _, _, p, c, f, t = entry
    return 3 * p + 2 * c + 2 * f + t


def tournament_wins(entry_n):
    """Games won in the 28-pair tournament over the top 8."""
    return sum(1 for w, _ in TOURNAMENT if w == entry_n)


def pick_winner(shortlist):
    """Rank by tournament wins, then weighted score; return the top text."""
    ranked = sorted(
        shortlist,
        key=lambda e: (tournament_wins(e[0]), weighted_score(e)),
        reverse=True,
    )
    return ranked[0][1], ranked


def gate_ok(text):
    """The sealed gate: UTF-8, 1-200 chars, not only whitespace, one line."""
    if not text or text != text.strip():
        return False
    if not 1 <= len(text) <= 200:
        return False
    if text.strip() == "":
        return False
    if "\n" in text or "\r" in text:
        return False
    text.encode("utf-8")
    return True


# Premises saturated in the live field at build time (see candidates.md):
# the judge's freshness criterion punishes them, so the winner must avoid
# every one. Checked as substrings, case-insensitive.
BANNED_PREMISES = [
    "plant", "printer", "per my last email",
    "should have been an email", "standup", "reply-all",
    "out of office", "we're a family",
]


def freshness_ok(text):
    """True when the line uses none of the saturated premises."""
    lowered = text.lower()
    return all(banned not in lowered for banned in BANNED_PREMISES)


def main():
    winner, ranked = pick_winner(SHORTLIST)
    if not gate_ok(winner):
        print("gate FAILED for winning line", file=sys.stderr)
        return 1
    if not freshness_ok(winner):
        print("freshness FAILED: winning line uses a saturated premise",
              file=sys.stderr)
        return 1
    out_dir = "/output"
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, "entry.txt"), "w", encoding="utf-8") as f:
        f.write(winner)
    print("winner: #%d (tournament %d-0, score %d/40, %d chars)" % (
        ranked[0][0], tournament_wins(ranked[0][0]),
        weighted_score(ranked[0]), len(winner)))
    print(winner)
    return 0


if __name__ == "__main__":
    sys.exit(main())
