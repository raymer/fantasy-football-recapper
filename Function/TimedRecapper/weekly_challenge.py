from espn_api.football import League
import json

Object = lambda **kwargs: type("Object", (), kwargs)

def getWeeklyWinner(league, week):
  box_scores = league.box_scores(week)
  if week == 2:
    return getWeek2Winner(league, week)
  elif week == 3:
    return getWeek3Winner(league, week)
  elif week == 4:
    return getWeek4Winner(league, week)
  elif week == 5:
    return getWeek5Winner(league, week)
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

  touchDowns = 0
  if "passingTouchdowns" in breakdown:
    touchDowns += breakdown["passingTouchdowns"]
  if "rushingTouchdowns" in breakdown:
    touchDowns += breakdown["rushingTouchdowns"]
  if "receivingTouchdowns" in breakdown:
    touchDowns += breakdown["receivingTouchdowns"]

  return touchDowns

def getWeek3Winner(league, week):
  box_scores = league.box_scores(week)
  teamTouchdowns = []
  for box_score in box_scores:

    numTouchdowns = 0
    for player in list(filter(lambda x: x.slot_position != 'BE', box_score.home_lineup)):
      numTouchdowns += calculateTouchdowns(player)
    
    teamTouchdowns.append(Object(teamName=box_score.home_team.team_name, touchdowns=numTouchdowns))

    numTouchdowns = 0
    for player in list(filter(lambda x: x.slot_position != 'BE', box_score.away_lineup)):
      numTouchdowns += calculateTouchdowns(player)
    
    teamTouchdowns.append(Object(teamName=box_score.away_team.team_name, touchdowns=numTouchdowns))

  sortedTouchdowns = sorted(teamTouchdowns, key=lambda item: item.touchdowns, reverse=True)

  message = "\n\nWeekly Challenge\nWeek 3: Endzone Celebration - The team that scores the most offensive touchdowns wins.\n"
  if sortedTouchdowns[0].touchdowns == sortedTouchdowns[1].touchdowns:
    message += f"Uh oh, there was a tie. Multiple teams scored {str(sortedTouchdowns[0].touchdowns)} touchdowns"
  else:
    message += f"The winner was {sortedTouchdowns[0].teamName} who scored {str(sortedTouchdowns[0].touchdowns)} touchdowns"

  message += f"\n\nHere's the full breakdown:\n"
  for team in sortedTouchdowns:
    message += f"{team.teamName.strip()} {team.touchdowns}\n"
  
  return message

def getWeek4Winner(league, week):
  box_scores = league.box_scores(week)
  teamBenchPoints = []
  for box_score in box_scores:

    numBenchPoints = 0
    for player in list(filter(lambda x: x.slot_position == 'BE', box_score.home_lineup)):
      numBenchPoints += player.points
    
    teamBenchPoints.append(Object(teamName=box_score.home_team.team_name, benchPoints=numBenchPoints))

    numBenchPoints = 0
    for player in list(filter(lambda x: x.slot_position == 'BE', box_score.away_lineup)):
      numBenchPoints += player.points
    
    teamBenchPoints.append(Object(teamName=box_score.away_team.team_name, benchPoints=numBenchPoints))

  sortedBenchPoints = sorted(teamBenchPoints, key=lambda item: item.benchPoints, reverse=True)

  message = "\n\nWeekly Challenge\nWeek 4: Bench Warmer - Team with the most total points from their bench.\n"
  if sortedBenchPoints[0].benchPoints == sortedBenchPoints[1].benchPoints:
    message += f"Uh oh, there was a tie. Multiple teams scored {str(sortedBenchPoints[0].benchPoints)} bench points"
  else:
    message += f"The winner was {sortedBenchPoints[0].teamName} who scored {str(sortedBenchPoints[0].benchPoints)} bench points"

  message += f"\n\nHere's the full breakdown:\n"
  for team in sortedBenchPoints:
    message += f"{team.teamName.strip()} {str(round(team.benchPoints, 2))}\n"
  
  return message

def getWeek5Winner(league, week):
  box_scores = league.box_scores(week)
  closestTo21 = []
  for box_score in box_scores:

    playerPoints = []
    for player in list(filter(lambda x: x.slot_position != 'BE' and x.slot_position != 'IR', box_score.home_lineup)):
      playerPoints.append(Object(teamName=box_score.home_team.team_name, playerName=player.name, actualPoints=player.points, calculatedPoints=(21 - player.points)))
    
    sortedPoints = list(filter(lambda x: x.calculatedPoints > 0, sorted(playerPoints, key=lambda item: item.calculatedPoints)))
    closestTo21.append(sortedPoints[0])

    playerPoints = []
    for player in list(filter(lambda x: x.slot_position != 'BE' and x.slot_position != 'IR', box_score.away_lineup)):
      playerPoints.append(Object(teamName=box_score.away_team.team_name, playerName=player.name, actualPoints=player.points, calculatedPoints=(21 - player.points)))
    
    sortedPoints = list(filter(lambda x: x.calculatedPoints > 0, sorted(playerPoints, key=lambda item: item.calculatedPoints)))
    closestTo21.append(sortedPoints[0])

  sortedClosesTo21 = sorted(closestTo21, key=lambda item: item.actualPoints, reverse=True)

  message = "\n\nWeekly Challenge\nWeek 5: Blackjack!- The team with a player who scores the closest to 21 points without going over wins.\n"
  if sortedClosesTo21[0].actualPoints == 21:
    message += f"We had a blackjack!\n"
  if sortedClosesTo21[0].actualPoints == sortedClosesTo21[1].actualPoints:
    message += f"Uh oh, there was a tie. Multiple teams had players who scored {str(sortedClosesTo21[0].actualPoints)} points"
  else:
    message += f"The winner was {sortedClosesTo21[0].teamName} who had {sortedClosesTo21[0].playerName} score {str(sortedClosesTo21[0].actualPoints)} points"

  message += f"\n\nHere's the full breakdown:\n"
  for team in sortedClosesTo21:
    message += f"{team.teamName.strip()} who had {team.playerName} score {team.actualPoints} points\n"

  return message