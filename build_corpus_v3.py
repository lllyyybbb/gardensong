#!/usr/bin/env python3
"""build_corpus_v3.py — rebuild the corpus, rebalanced, de-numbered, and slur-filtered.

Changes from v1:
  * DROPPED Paul Laurence Dunbar's Complete Poems (#18338). It was ~72% of the
    corpus, so it drowned out the other poets, pushed the dialect register, and
    (via its alphabetical index of first lines) was the main source of stray
    numbers. Dunbar is still present — the anthology below includes a selection
    of his work — just no longer dominant.
  * ADDED two more public-domain volumes, both standard-English, to rebalance:
    Claude McKay's Harlem Shadows and Frances E. W. Harper's Poems.
  * STRIP any line containing a digit, to remove page numbers, contents/index
    entries, and similar cruft.

Edit BOOKS to curate. Re-run:  python3 build_corpus_v2.py
Code generated with Claude.
"""

import re
import urllib.request

BOOKS = {
    11986: "The Book of American Negro Poetry (ed. James Weldon Johnson, 1922) - 31 poets",
    64989: "Claude McKay - Harlem Shadows (1922)",
    679:   "Frances E. W. Harper - Poems",
    # Removed: 18338 Dunbar Complete Poems (too dominant / dialect-heavy / index of numbers).
    # Easy to add more standard-English PD volumes here, e.g.:
    # 69248: "Frances E. W. Harper - Atlanta Offering: Poems",
}

OUT = "corpus.txt"
UA = {"User-Agent": "Mozilla/5.0 (personal corpus builder)"}
HAS_DIGIT = re.compile(r"\d")
# Drop any line containing the racial slur, in any period/dialect spelling (root match).
# NOTE: this root also catches the unrelated words "niggardly"/"niggling"; that is
# intentional here — for a public poem generator we don't want either surfacing.
# It does NOT touch "Negro" (the period term in these texts, incl. the anthology title).
SLUR = re.compile(r"nigg", re.I)


def fetch(book_id):
    url = f"https://www.gutenberg.org/cache/epub/{book_id}/pg{book_id}.txt"
    req = urllib.request.Request(url, headers=UA)
    raw = urllib.request.urlopen(req, timeout=60).read()
    for enc in ("utf-8", "latin-1"):
        try:
            return raw.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw.decode("utf-8", errors="replace")


def strip_boilerplate(text):
    start = text.find("*** START OF")
    start = text.find("\n", start) + 1 if start != -1 else 0
    end = text.find("*** END OF")
    if end == -1:
        end = len(text)
    return text[start:end].strip()


def strip_numbers(text):
    """Drop any line with a digit — page numbers, index/contents entries, etc."""
    return "\n".join(ln for ln in text.split("\n") if not HAS_DIGIT.search(ln))


def strip_slurs(text):
    """Drop any line containing the slur so the word never enters the model."""
    return "\n".join(ln for ln in text.split("\n") if not SLUR.search(ln))


def main():
    pieces = []
    for book_id, label in BOOKS.items():
        try:
            body = strip_slurs(strip_numbers(strip_boilerplate(fetch(book_id))))
            pieces.append(body)
            print(f"  ok   #{book_id}: {len(body):>8,} chars  {label}")
        except Exception as e:
            print(f"  FAIL #{book_id}: {e}")

    if not pieces:
        print("\nNothing downloaded - corpus.txt not written.")
        return

    corpus = "\n\n\n".join(pieces)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(corpus)

    words = len(corpus.split())
    lines = corpus.count("\n") + 1
    print(f"\nWrote {OUT}: {len(corpus):,} chars, ~{words:,} words, {lines:,} lines")


if __name__ == "__main__":
    main()
