import sys
from database_participants import database
from database_participants import year_grouped

# How many problems to print per check before truncating the rest
LIMIT = 10

def check_score_rank_consistency():
  """
  Check if someone with a higher score is below in rank than someone else.
  """
  n = 0
  for year in year_grouped:
    if not year_grouped[year][0].total:
      continue
    last_rank = 0
    last_score = 1e10
    for row in year_grouped[year]:
      if not row.total or row.rank_geq:
        break
      rank = int(row.rank)
      score = float(row.total)
      if rank < last_rank:
        n += 1
        if n <= LIMIT:
          print(f"Rank should not decrease: {row}")
      if score > last_score or (score == last_score and rank != last_rank):
        n += 1
        if n <= LIMIT:
          print(f"Row should have higher rank: {row}")
      last_rank = rank
      last_score = score
  if n > LIMIT:
    print(f"... and {n - LIMIT} more")
  return n

def check_score_sums():
  n = 0
  for year in year_grouped:
    for row in year_grouped[year]:
      if not row.theoretical or not row.experimental or not row.total:
        continue
      th = float(row.theoretical)
      ex = float(row.experimental)
      to = float(row.total)
      if abs(th + ex - to) > .0001:
        n += 1
        if n <= LIMIT:
          print(f"Points don't add up: {row}")
  if n > LIMIT:
    print(f"... and {n - LIMIT} more")
  return n

def check_score_precision():
  n = 0
  for year in year_grouped:
    for row in year_grouped[year]:
      for score in [row.theoretical, row.experimental, row.total]:
        if score and ("." not in score or len(score.split(".")[1]) != 2):
          n += 1
          if n <= LIMIT:
            print("Score precision should be two digits after decimal:")
            print(f"{score} in {row}")
  if n > LIMIT:
    print(f"... and {n - LIMIT} more")
  return n

def check_combining_characters():
  n = 0
  for row in database:
    for c in row.name:
      if 768 <= ord(c) < 880:
        n += 1
        if n <= LIMIT:
          print(f"Combining character {c} detected in {row}")
          print("Please replace with a single character. See unicodedata.normalize")
    if '\xa0' in row.name:
      n += 1
      if n <= LIMIT:
        print(f"Non-breaking space \\xa0 detected in {row}")
        print("Please replace with a regular space")
  if n > LIMIT:
    print(f"... and {n - LIMIT} more")
  return n

checks = [
  check_score_rank_consistency,
  check_score_sums,
  check_score_precision,
  check_combining_characters,
]

def run():
  total = 0
  for check in checks:
    total += check()

  if not total:
    print("All checks passed.")
  return 1 if total else 0

if __name__ == "__main__":
  sys.exit(run())
