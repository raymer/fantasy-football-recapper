from espn_api.football import League
import json

def getWeeklyWinner(league, week):
  box_scores = league.box_scores(week)
  if week == 2:
    return getWeek2Winner(league, week)
  elif week == 3:
    return getWeek3Winner(league, week)
  return ""

def getWeek2Winner(league, week):
  topScore = 0
  box_scores = league.box_scores(week)
  for box_score in box_scores:
    if box_score.away_score > topScore:
      topScore = box_score.away_score
    if box_score.home_score > topScore:
      topScore = box_score.home_score

  topScoringBoxScore = list(filter(lambda x: x.home_score == topScore or x.away_score == topScore, box_scores))
  highTeam = topScoringBoxScore[0].home_team if topScoringBoxScore[0].home_score == topScore else topScoringBoxScore[0].away_team
  highRoster = topScoringBoxScore[0].home_lineup if topScoringBoxScore[0].home_score == topScore else topScoringBoxScore[0].away_lineup
  message = "\n\nWeekly Challenge\nWeek 2: Hot Start - The team that scores the most points wins.\n"
  message += f"The winner was {highTeam.team_name} who scored {str(topScore)} points"
  return message


def calculateTouchdowns(player):
  playerDict = json.loads(str(player.stats).replace("{3:", "{\"3\":").replace("'", "\""))
  if "breakdown" not in playerDict["3"]:
    return 0
  
  breakdown = playerDict["3"]["breakdown"]
  # print(breakdown)

  touchDowns = 0
  if "passingTouchdowns" in breakdown:
    touchDowns += breakdown["passingTouchdowns"]
  if "rushingTouchdowns" in breakdown:
    touchDowns += breakdown["rushingTouchdowns"]
  if "receivingTouchdowns" in breakdown:
    touchDowns += breakdown["receivingTouchdowns"]

  print(player.name, touchDowns)
  return touchDowns

def getWeek3Winner(league, week):

  touchDownCount = 0
  box_scores = league.box_scores(week)
  playerDict = {}
  for box_score in box_scores:
    for player in box_score.home_lineup:
      if ("deebo" in player.name.lower()):
        calculateTouchdowns(player)
    for player in box_score.away_lineup:
      if ("deebo" in player.name.lower()):
        calculateTouchdowns(player)


  # topScoringBoxScore = list(filter(lambda x: x.home_score == topScore or x.away_score == topScore, box_scores))
  # highTeam = topScoringBoxScore[0].home_team if topScoringBoxScore[0].home_score == topScore else topScoringBoxScore[0].away_team
  # highRoster = topScoringBoxScore[0].home_lineup if topScoringBoxScore[0].home_score == topScore else topScoringBoxScore[0].away_lineup
  message = "\n\nWeekly Challenge\nWeek 3: Endzone Celebration - The team that scores the most offensive touchdowns wins.\n"
  return message