import random
import cProfile

POSITIONS = [
        [38, 25, 13, 12, 6, 3, 3],
        [25, 22, 17, 16, 10, 6, 4],
        [76, 7, 6, 3, 3, 3, 2],
        [19, 18, 17, 16, 15, 12, 3],
        [33, 32, 13, 11, 4, 4, 3],
      ]

def draft_position(position):
  players = POSITIONS[position]
  rand = random.randint(1,100)

  cumulative_chance = 0

  for player_index, player_chance in enumerate(players):
    cumulative_chance += player_chance
    if rand <= cumulative_chance:
      return player_index 

class Team():
  def __init__(self, scores):
    self.positions = self.draft()
    self.score = self.calc_score(scores)

  def draft(self):
    positions = [draft_position(i) for i in range(len(POSITIONS))]
    return positions

  def calc_score(self, scores):
    score = 0

    for pos in range(len(self.positions)):
      player = self.positions[pos]
      player_score = scores[pos][player]
      score += player_score

    return score

  def __repr__(self):
    return "Score: %s -- Players: %s" % (self.score, self.positions)

def generate_random_scores():
  return [ [random.randint(10, 60) for i in range(len(POSITIONS[0]))] for i in range(len(POSITIONS))]


def percentile_for_score(teams, score):
  sorted_teams = sorted(teams, key=lambda x: x.score)
  num_teams_beat = 0

  for team in sorted_teams:
    if team.score < score:
      num_teams_beat += 1
    else:
      break

  decimal_p = num_teams_beat / float(len(sorted_teams))
  int_p = int(decimal_p * 100)
  return int_p


def calc_owned_for_pos(teams, pos):
  players = [0] * len(POSITIONS[0])

  for team in teams:
    player = team.positions[pos]
    players[player] += 1

  return players

def team_with_most_owned_players(teams):
  team = [0] * len(POSITIONS)

  for pos in range(len(POSITIONS)):
    ownage = calc_owned_for_pos(teams, pos)
    most_owned_player = ownage.index(max(ownage))
    team[pos] = most_owned_player

  return team

def score_for_players(scores, players):
  score = 0

  for pos, pos_scores in enumerate(scores):
    score += pos_scores[players[pos]]

  return score

def run_week(num_teams=1000):
  scores = generate_random_scores()
  teams = [Team(scores) for i in range(num_teams)]

  most_owned_players = team_with_most_owned_players(teams)
  score_for_most_owned_team = score_for_players(scores, most_owned_players)
  percentile = percentile_for_score(teams, score_for_most_owned_team)

  return percentile

  '''
  team_count_by_score = {}
  for team in teams:
    if not team.score in team_count_by_score:
      team_count_by_score[team.score] = 1
    else:
      team_count_by_score[team.score] += 1
  '''



  ''' 
  print "Score -- Count"
  for k,v in team_count_by_score.iteritems():
    print "%s -- %s" % (k, v)

  score = score_for_most_owned(scores)
  print "Score for most owned team: %s" % score
  print "Percentile: %s" % percentile_for_score(teams, score)
  ''' 

def run_season(num_weeks=1000):
  percentiles = []

  for week in range(num_weeks):
    print "Week: %s" % week
    percentiles.append(run_week())

  percentile_counts = [0] * 100
  for p in percentiles:
    percentile_counts[p] += 1

  print "Percentile Counts: %s" % percentile_counts

if __name__ == "__main__":
  print "Starting Sim"

  run_season(100000)
  #cProfile.run('run_season(2000)')

