"""Monday, reviewed in a single line.

Entry for the make.fun bounty "Monday, Reviewed in One Line"
(slug u-zeroxfive-monday-reviewed-in-one-line-e55de3c1). The brief asks
for one review of the entrant's own Monday, under 200 characters, and
nothing else. This script keeps six hand-written drafts, marks each one
on five counts, keeps the best of the six, and writes it to
/output/entry.txt. The drafts never change at run time and the arithmetic
never changes either, so the same draft wins on every run and the file
comes out byte-identical each time.
"""

from hashlib import sha256
from pathlib import Path

DESTINATION = Path("/output/entry.txt")
LIMIT = 199
FINGERPRINT = "f00cb4fe04c49d677c40849e35a0a768" "9f84fe1707d4007376fa06d605870d08"

# Marks run in this order: on-brief, laugh, specific, lean, repeatable.
# Each draft is a fixed string plus its five marks; the total decides,
# and a tie goes to the shorter draft.
DRAFTS = [
    # 10, 10, 10, 10, 9 = 49. A one-star review of a stand-up that never
    # stands: the meeting lends its own name to the joke, and the payoff
    # word is the last word in the line.
    ("My Monday earned one star: the 9 a.m. stand-up sat down for two hours, and the only thing that stood up was my blood pressure.", (10, 10, 10, 10, 9)),
    # 10, 9, 9, 9, 9 = 46. Ninety minutes, nobody on their feet, and the
    # only thing the meeting produces is itself again next week.
    ("I rated my Monday one star \u2014 the stand-up ran 90 minutes, nobody stood, and the only action item was the same meeting, again, next week.", (10, 9, 9, 9, 9)),
    # 10, 9, 9, 9, 8 = 45. Forty-seven unread before nine, then a meeting
    # about the emails that outnumbers the emails themselves.
    ("Monday, one star: my inbox hit 47 unread before 9 a.m., and the meeting to discuss the emails outnumbered the emails.", (10, 9, 9, 9, 8)),
    # 10, 8, 9, 9, 8 = 44. An hour of updates, a meeting about the
    # meeting, and HR asking afterwards how it went.
    ("Monday review: my laptop updated for an hour, my boss booked a meeting about the meeting, and HR sent a survey asking how it went.", (10, 8, 9, 9, 8)),
    # 10, 8, 8, 9, 8 = 43. On-time commute, cold coffee, and a quick sync
    # that runs longer than the weekend it follows.
    ("I reviewed my Monday: the commute was on time, the coffee was cold, and the 'quick sync' lasted longer than my weekend.", (10, 8, 8, 9, 8)),
    # 10, 8, 8, 8, 8 = 42. Alarm, train and calendar surrendering in
    # turn, the calendar last.
    ("My Monday: the alarm gave up, the train gave up, and by 10 a.m. my calendar had given up pretending the meetings were meetings.", (10, 8, 8, 8, 8)),]


def vet(text):
    """Refuse anything the gate would refuse, before it is written."""
    if not isinstance(text, str):
        raise TypeError("draft is not text")
    if "\n" in text or "\r" in text:
        raise ValueError("draft must stay on a single line")
    if not text.strip():
        raise ValueError("draft is blank")
    if len(text) > LIMIT:
        raise ValueError(
            f"draft is {len(text)} characters, past the {LIMIT} cap"
        )
    text.encode("utf-8")
    return text


def total(draft):
    """Add a draft's five marks into its single deciding number."""
    return sum(draft[1])


def choose(drafts):
    """Best total wins; the shorter draft wins a tie."""
    ranked = sorted(drafts, key=lambda draft: (total(draft), -len(draft[0])), reverse=True)
    return ranked[0][0]


def fingerprint(text):
    """Hex digest of a line, for the tamper check below."""
    return sha256(text.encode("utf-8")).hexdigest()


def deliver(text):
    """Write the winning line, then prove the disk holds that line."""
    vet(text)
    if fingerprint(text) != FINGERPRINT:
        raise ValueError(f"winner fingerprint mismatch: {fingerprint(text)}")
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    DESTINATION.write_text(text, encoding="utf-8")
    DESTINATION.chmod(0o644)
    back = DESTINATION.read_text(encoding="utf-8")
    if back != text:
        raise ValueError("entry.txt on disk is not the chosen line")
    if fingerprint(back) != FINGERPRINT:
        raise ValueError("entry.txt fingerprint drifted after writing")
    return back


def run():
    """Vet every draft, pick the winner, write it, print it."""
    for draft in DRAFTS:
        vet(draft[0])
    chosen = choose(DRAFTS)
    deliver(chosen)
    print(chosen)


if __name__ == "__main__": run()
