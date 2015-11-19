import random


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

#TODO: Make this calculate based on actual percent owned, and not assume its always player 0 although given the player matrix it always is
def score_for_most_owned(scores):
  score = 0

  for pos in scores:
    score += pos[0]

  return score

def percentile_for_score(sorted_teams, score):
  num_teams_beat = 0

  for team in sorted_teams:
    if team.score < score:
      num_teams_beat += 1
    else:
      break

  return num_teams_beat / float(len(sorted_teams))


def calc_owned_for_pos(teams, pos):
  players = [0] * len(POSITIONS[0])

  for team in teams:
    player = team.positions[pos]
    players[player] += 1

  return players

if __name__ == "__main__":
  print "Starting Sim"

  num_teams = 100000
  scores = generate_random_scores()
  teams = [Team(scores) for i in range(num_teams)]
  teams.sort(key=lambda x: x.score)

  team_count_by_score = {}
  for team in teams:
    if not team.score in team_count_by_score:
      team_count_by_score[team.score] = 1
    else:
      team_count_by_score[team.score] += 1

  print "Score -- Count"
  for k,v in team_count_by_score.iteritems():
    print "%s -- %s" % (k, v)

  score = score_for_most_owned(scores)
  print "Score for most owned team: %s" % score
  print "Percentile: %s" % percentile_for_score(teams, score)



