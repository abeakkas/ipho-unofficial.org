# Scans participants.csv for likely duplicate people: participants from the same
# country, one or two years apart, whose names look similar without being
# identical. Catches reordered names, added/dropped middle names, and spelling
# variants (e.g. Ahmed vs Akhmed). Run by hand every now and then:
#
#   python3 name_analysis.py

from difflib import SequenceMatcher
from itertools import permutations
from asciify import asciify
from database_participants import participants_by_code

THRESHOLD = 0.7
MAX_YEAR_GAP = 2

def name_tokens(name):
  return asciify(name).lower().replace("-", " ").split()

def similarity(tokens1, tokens2):
  shorter, longer = sorted((tokens1, tokens2), key=len)
  return max(
    min(SequenceMatcher(None, a, b).ratio() for a, b in zip(shorter, chosen))
    for chosen in permutations(longer, len(shorter))
  )

def find_similar_names():
  """Return (score, row1, row2) triples above THRESHOLD, best matches first."""
  matches = []
  for rows in participants_by_code.values():
    tokenized = [(row, name_tokens(row.name)) for row in rows]
    for i in range(len(tokenized)):
      row1, tokens1 = tokenized[i]
      for j in range(i + 1, len(tokenized)):
        row2, tokens2 = tokenized[j]
        if row1.year == row2.year or row1.name == row2.name:
          continue
        if int(row2.year) - int(row1.year) > MAX_YEAR_GAP:
          break
        score = similarity(tokens1, tokens2)
        if score >= THRESHOLD:
          matches.append((score, row1, row2))
  matches.sort(key=lambda match: match[0], reverse=True)
  return matches

def run():
  for score, row1, row2 in find_similar_names():
    country = row1.country.name
    print(f"{score:.2f}  {country}: ({row1.year}) {row1.name}  ~  ({row2.year}) {row2.name}")

if __name__ == "__main__":
  run()
