# Monday, Reviewed in One Line — make.fun bounty
# u-zeroxfive-monday-reviewed-in-one-line-e55de3c1
#
# The program writes one review of the entrant's own Monday, a single
# line under 200 characters and nothing else, to /output/entry.txt.
# Candidates were drafted against the judge's brief, in order of weight:
#   1. is a one-line review of the entrant's own Monday, not a joke
#      about something else
#   2. gets the bigger laugh, the line a reader would laugh at rather
#      than merely nod at
#   3. names a concrete detail of the Monday — a meeting, a commute,
#      an inbox — over generic tiredness
#   4. lands the joke inside the line with no wasted words, so the turn
#      arrives before the reader gives up
#   5. is the line a reader would repeat to a coworker the next morning
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.

CANDIDATES = [
    # score: on-subject 10, laugh 10, concrete 10, tight 10,
    #   retellable 9 = 49. The 9 a.m. stand-up that sits down for two
    #   hours is the most recognisable Monday there is; "the only thing
    #   that stood up was my blood pressure" turns the meeting's own
    #   name against it, and the punch lands on the last word.
    ("My Monday earned one star: the 9 a.m. stand-up sat down for two "
     "hours, and the only thing that stood up was my blood pressure.",
     49),
    # score: on-subject 10, laugh 9, concrete 9, tight 9,
    #   retellable 9 = 46. The stand-up nobody stands at, and the only
    #   action item is the same meeting again next week — the Monday
    #   that reproduces itself.
    ("I rated my Monday one star \u2014 the stand-up ran 90 minutes, "
     "nobody stood, and the only action item was the same meeting, "
     "again, next week.",
     46),
    # score: on-subject 10, laugh 9, concrete 9, tight 9,
    #   retellable 8 = 45. 47 unread before 9 a.m. is concrete; the
    #   meeting about the emails outnumbering the emails is the turn.
    ("Monday, one star: my inbox hit 47 unread before 9 a.m., and the "
     "meeting to discuss the emails outnumbered the emails.",
     45),
    # score: on-subject 10, laugh 8, concrete 9, tight 9,
    #   retellable 8 = 44. The meeting about the meeting, with HR
    #   surveying the wreckage — three concrete Monday details in one
    #   line.
    ("Monday review: my laptop updated for an hour, my boss booked a "
     "meeting about the meeting, and HR sent a survey asking how it "
     "went.",
     44),
    # score: on-subject 10, laugh 8, concrete 8, tight 9,
    #   retellable 8 = 43. The commute on time, the coffee cold, and a
    #   "quick sync" that outlasts the weekend.
    ("I reviewed my Monday: the commute was on time, the coffee was "
     "cold, and the 'quick sync' lasted longer than my weekend.",
     43),
    # score: on-subject 10, laugh 8, concrete 8, tight 8,
    #   retellable 8 = 42. Alarm, train and calendar all giving up in
    #   sequence; the calendar pretending is the freshest beat.
    ("My Monday: the alarm gave up, the train gave up, and by 10 a.m. "
     "my calendar had given up pretending the meetings were meetings.",
     42),
]

# The gate requires 1-200 characters of non-whitespace UTF-8 text, and
# the brief asks for under 200 characters, so every candidate is kept
# below 200.
MAX_CHARS = 199


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= MAX_CHARS, \
            f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        assert "\n" not in text, "candidate must be one line"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    line = pick(CANDIDATES)
    import hashlib
    import os
    # SHA-256 self-check: the chosen line must hash to the value recorded
    # when the candidates were drafted, so a silent edit to the winning
    # text (or to the file on disk) is caught instead of shipped.
    expected_sha256 = (
        "f00cb4fe04c49d677c40849e35a0a7689f84fe1707d4007376fa06d605870d08"
    )
    actual_sha256 = hashlib.sha256(line.encode("utf-8")).hexdigest()
    assert actual_sha256 == expected_sha256, \
        f"chosen line hash changed: {actual_sha256}"
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(line)
    # Verify what was actually written: the gate reads this file, not stdout.
    # The scorer collects outputs as another user, so the file must be
    # readable by everyone (mode 0644), not just by the writer.
    os.chmod("/output/entry.txt", 0o644)
    with open("/output/entry.txt", encoding="utf-8") as f:
        written = f.read()
    assert written == line, "entry.txt differs from the chosen line"
    assert 1 <= len(written.strip()) <= MAX_CHARS, \
        "entry.txt outside the gate"
    assert written.strip(), "entry.txt is blank"
    assert "\n" not in written.strip(), "entry.txt must be one line"
    # Re-hash what is on disk: the file the gate reads must match the
    # chosen line byte for byte, not just in length.
    written_sha256 = hashlib.sha256(written.encode("utf-8")).hexdigest()
    assert written_sha256 == expected_sha256, \
        f"entry.txt hash changed on disk: {written_sha256}"
    print(line)


if __name__ == "__main__":
    main()
