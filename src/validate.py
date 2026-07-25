import sys
from database_participants import participants
from database_participants import participants_by_year

# How many problems to print per check before truncating the rest
LIMIT = 10

def check_score_rank_consistency():
  """
  Check if someone with a higher score is below in rank than someone else.
  """
  n = 0
  for year in participants_by_year:
    if not participants_by_year[year][0].total:
      continue
    last_rank = 0
    last_score = 1e10
    for participant in participants_by_year[year]:
      if not participant.total or participant.rank_geq:
        break
      rank = int(participant.rank)
      score = float(participant.total)
      if rank < last_rank:
        n += 1
        if n <= LIMIT:
          print("Rank should not decrease:")
          print(participant)
      if score > last_score or (score == last_score and rank != last_rank):
        n += 1
        if n <= LIMIT:
          print("Participant should have higher rank:")
          print(participant)
      last_rank = rank
      last_score = score
  if n > LIMIT:
    print(f"... and {n - LIMIT} more")
  return n

def check_score_sums():
  n = 0
  for year in participants_by_year:
    for participant in participants_by_year[year]:
      if not participant.theoretical or not participant.experimental or not participant.total:
        continue
      th = float(participant.theoretical)
      ex = float(participant.experimental)
      to = float(participant.total)
      if abs(th + ex - to) > .0001:
        n += 1
        if n <= LIMIT:
          print("Points don't add up:")
          print(participant)
  if n > LIMIT:
    print(f"... and {n - LIMIT} more")
  return n

def check_score_precision():
  n = 0
  for year in participants_by_year:
    for participant in participants_by_year[year]:
      for score in [participant.theoretical, participant.experimental, participant.total]:
        if score and ("." not in score or len(score.split(".")[1]) != 2):
          n += 1
          if n <= LIMIT:
            print("Score precision should be two digits after decimal:")
            print(f"{score} in {participant}")
  if n > LIMIT:
    print(f"... and {n - LIMIT} more")
  return n

def check_combining_characters():
  n = 0
  for participant in participants:
    for c in participant.name:
      if 768 <= ord(c) < 880:
        n += 1
        if n <= LIMIT:
          print(f"Combining character {c} detected in {participant}")
          print("Please replace with a single character. See unicodedata.normalize")
    if '\xa0' in participant.name:
      n += 1
      if n <= LIMIT:
        print(f"Non-breaking space \\xa0 detected in {participant}")
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
