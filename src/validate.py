import sys
from database_participants import database
from database_participants import year_grouped

def check_score_rank_consistency():
  """
  Check if someone with a higher score is below in rank than someone else.
  """
  problems = []
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
        problems.append(f"Rank should not decrease: {row}")
      if score > last_score or (score == last_score and rank != last_rank):
        problems.append(f"Row should have higher rank: {row}")
      last_rank = rank
      last_score = score
  return problems

def check_score_sums():
  problems = []
  for year in year_grouped:
    for row in year_grouped[year]:
      if not row.theoretical or not row.experimental or not row.total:
        continue
      th = float(row.theoretical)
      ex = float(row.experimental)
      to = float(row.total)
      if abs(th + ex - to) > .0001:
        problems.append(f"Points don't add up: {row}")
  return problems

def check_score_precision():
  problems = []
  for year in year_grouped:
    for row in year_grouped[year]:
      for score in [row.theoretical, row.experimental, row.total]:
        if score and ("." not in score or len(score.split(".")[1]) != 2):
          problems.append(
            "Score precision should be two digits after decimal:\n"
            f"{score} in {row}")
  return problems

def check_combining_characters():
  problems = []
  for row in database:
    for c in row.name:
      if 768 <= ord(c) < 880:
        problems.append(
          f"Combining character {c} detected in {row}\n"
          "Please replace with a single character. See unicodedata.normalize")
    if '\xa0' in row.name:
      problems.append(
        f"Non-breaking space \\xa0 detected in {row}\n"
        "Please replace with a regular space")
  return problems

checks = [
  check_score_rank_consistency,
  check_score_sums,
  check_score_precision,
  check_combining_characters,
]

# How many problems to print per check before truncating the rest
LIMIT = 10

def run():
  total = 0
  for check in checks:
    problems = check()
    total += len(problems)
    for problem in problems[:LIMIT]:
      print(problem)
    if len(problems) > LIMIT:
      print(f"... and {len(problems) - LIMIT} more from {check.__name__}")
    if problems:
      print()

  if total:
    print(f"{total} problem(s) found.")
    return 1
  else:
    print("All checks passed.")
    return 0

if __name__ == "__main__":
  sys.exit(run())
