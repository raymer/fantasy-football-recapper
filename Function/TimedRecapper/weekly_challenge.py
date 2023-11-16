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
  elif week == 6:
    return getWeek6Winner(league, week)
  elif week == 7:
    return getWeek7Winner(league, week)
  elif week == 8:
    return getWeek8Winner(league, week)
  elif week == 9:
    return getWeek9Winner(league, week)
  elif week == 10:
    return getWeek10Winner(league, week)
  elif week == 11:
    return getWeek11Winner(league, week)
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
    
    sortedPoints = list(filter(lambda x: x.calculatedPoints >= 0, sorted(playerPoints, key=lambda item: item.calculatedPoints)))
    closestTo21.append(sortedPoints[0])

    playerPoints = []
    for player in list(filter(lambda x: x.slot_position != 'BE' and x.slot_position != 'IR', box_score.away_lineup)):
      playerPoints.append(Object(teamName=box_score.away_team.team_name, playerName=player.name, actualPoints=player.points, calculatedPoints=(21 - player.points)))
    
    sortedPoints = list(filter(lambda x: x.calculatedPoints >= 0, sorted(playerPoints, key=lambda item: item.calculatedPoints)))
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

def getWeek6Winner(league, week):
  loserPoints = []
  box_scores = league.box_scores(week)
  for box_score in box_scores:
    if box_score.away_score < box_score.home_score:
      loserPoints.append(Object(teamName=box_score.away_team.team_name, points=box_score.away_score))
    elif box_score.home_score < box_score.away_score:
      loserPoints.append(Object(teamName=box_score.home_team.team_name, points=box_score.home_score))

  sortedLosers = sorted(loserPoints, key=lambda item: item.points, reverse=True)

  message = "\n\nWeekly Challenge\nWeek 6: Biggest Loser- The team that scores the most points in a losing matchup wins.\n"
  if sortedLosers[0].points == sortedLosers[1].points:
    message += f"Uh oh, there was a tie. Multiple losing teams scored {str(sortedLosers[0].points)} points"
  else:
    message += f"The winner was {sortedLosers[0].teamName} who scored {str(sortedLosers[0].points)} points"

  message += f"\n\nHere's the full breakdown:\n"
  for team in sortedLosers:
    message += f"{team.teamName.strip()} who scored {team.points} points\n"

  return message

def getWeek7Winner(league, week):
  marginsOfVictory = []
  box_scores = league.box_scores(week)
  for box_score in box_scores:
    if box_score.away_score >= box_score.home_score:
      marginsOfVictory.append(Object(teamName=box_score.away_team.team_name, marginOfVictory=box_score.away_score - box_score.home_score))
    else:
      marginsOfVictory.append(Object(teamName=box_score.home_team.team_name, marginOfVictory=box_score.home_score - box_score.away_score))

  sortedMarginsOfVictory = sorted(marginsOfVictory, key=lambda item: item.marginOfVictory, reverse=True)

  message = "\n\nWeekly Challenge\nWeek 7: Like a Boss - The team that wins its matchup by the biggest margin of victory wins.\n"
  if sortedMarginsOfVictory[0].marginOfVictory == sortedMarginsOfVictory[1].marginOfVictory:
    message += f"Uh oh, there was a tie. Multiple teams had a margin of victory of {str(round(sortedMarginsOfVictory[0].marginOfVictory, 2))} points"
  else:
    message += f"The winner was {sortedMarginsOfVictory[0].teamName} who had a margin of victory of {str(round(sortedMarginsOfVictory[0].marginOfVictory, 2))} points"

  message += f"\n\nHere's the full breakdown:\n"
  for team in sortedMarginsOfVictory:
    message += f"{team.teamName.strip()} who had a margin of victory of {str(round(team.marginOfVictory, 2))} points\n"
  
  return message


def calculateRushYards(player):
  playerDict = json.loads(str(player.stats).replace("{8:", "{\"8\":").replace("'", "\""))
  if "breakdown" not in playerDict["8"]:
    return 0
  
  breakdown = playerDict["8"]["breakdown"]

  rushYards = 0
  if "rushingYards" in breakdown:
    rushYards = breakdown["rushingYards"]

  return rushYards

def getWeek8Winner(league, week):
  box_scores = league.box_scores(week)
  teamRushYards = []
  for box_score in box_scores:

    numRushYards = 0
    for player in list(filter(lambda x: x.slot_position == 'RB', box_score.home_lineup)):
      numRushYards += calculateRushYards(player)
    
    teamRushYards.append(Object(teamName=box_score.home_team.team_name, rushYards=numRushYards))

    numRushYards = 0
    for player in list(filter(lambda x: x.slot_position == 'RB', box_score.away_lineup)):
      numRushYards += calculateRushYards(player)
    
    teamRushYards.append(Object(teamName=box_score.away_team.team_name, rushYards=numRushYards))

  sortedRushYards = sorted(teamRushYards, key=lambda item: item.rushYards, reverse=True)

  message = "\n\nWeekly Challenge\nWeek 8: Rushing Attack- The team with the most RB rushing yards wins.\n"
  if sortedRushYards[0].rushYards == sortedRushYards[1].rushYards:
    message += f"Uh oh, there was a tie. Multiple teams had {str(sortedRushYards[0].rushYards)} rush yards"
  else:
    message += f"The winner was {sortedRushYards[0].teamName} who had {str(sortedRushYards[0].rushYards)} rush yards"

  message += f"\n\nHere's the full breakdown:\n"
  for team in sortedRushYards:
    message += f"{team.teamName.strip()} {team.rushYards}\n"
  
  message += "\n\nNext week's challenge is: Nailed It - The team that scores closest to its projected point total (over or under) wins.\n"
  return message

def getWeek9Winner(league, week):
  projectedActualDifferential = []
  box_scores = league.box_scores(week)
  for box_score in box_scores:
    projectedActualDifferential.append(Object(teamName=box_score.away_team.team_name, points=abs(box_score.away_score - box_score.away_projected)))
    projectedActualDifferential.append(Object(teamName=box_score.home_team.team_name, points=abs(box_score.home_score - box_score.home_projected)))

  sortedProjectedActualDifferential = sorted(projectedActualDifferential, key=lambda item: item.points)

  message = "\n\nWeekly Challenge\nWeek 9: Nailed It - The team that scores closest to its projected point total (over or under) wins.\n"
  if sortedProjectedActualDifferential[0].points == sortedProjectedActualDifferential[1].points:
    message += f"Uh oh, there was a tie. Multiple teams were {str(round(sortedProjectedActualDifferential[0].points), 1)} points away from their projected score"
  else:
    message += f"The winner was {sortedProjectedActualDifferential[0].teamName} who was {str(round(sortedProjectedActualDifferential[0].points, 1))} points away from their projected score"

  message += f"\n\nHere's the full breakdown:\n"
  for team in sortedProjectedActualDifferential:
    message += f"{team.teamName.strip()} who was {round(team.points, 1)} points away from their projected score\n"

  message += "\n\nNext week's challenge is: Dead Weight - The team that wins its matchup with the week's lowest-scoring starting player wins.\n"
  return message

def getWeek10Winner(league, week):
  box_scores = league.box_scores(week)
  lowestScoringPlayers = []
  for box_score in box_scores:

    if box_score.away_score > box_score.home_score:
      lowestPoints = list(filter(lambda x: x.slot_position != 'BE' and x.slot_position != 'IR', sorted(box_score.away_lineup, key=lambda item: item.points)))[0]
      lowestScoringPlayers.append(Object(teamName=box_score.away_team.team_name, points=lowestPoints.points, playerName=lowestPoints.name))
    elif box_score.home_score > box_score.away_score:
      lowestPoints = list(filter(lambda x: x.slot_position != 'BE' and x.slot_position != 'IR', sorted(box_score.home_lineup, key=lambda item: item.points)))[0]
      lowestScoringPlayers.append(Object(teamName=box_score.home_team.team_name, points=lowestPoints.points, playerName=lowestPoints.name))

  sortedlowestScoringPlayers = sorted(lowestScoringPlayers, key=lambda item: item.points)

  message = "\n\nWeekly Challenge\nWeek 10: Dead Weight -The team that wins its matchup with the week's lowest-scoring starting player wins.\n"
  if sortedlowestScoringPlayers[0].points == sortedlowestScoringPlayers[1].points:
    message += f"Uh oh, there was a tie. Multiple teams had players who scored {str(sortedlowestScoringPlayers[0].points)} points"
  else:
    message += f"The winner was {sortedlowestScoringPlayers[0].teamName} who had {sortedlowestScoringPlayers[0].playerName} score {str(sortedlowestScoringPlayers[0].points)} points"

  message += f"\n\nHere's the full breakdown:\n"
  for team in sortedlowestScoringPlayers:
    message += f"{team.teamName.strip()} who had {team.playerName} score {team.points} points\n"

  message += "\n\nNext week's challenge is: Hot Flex -The team with the highest-scoring FLEX position wins.\n"
  return message

def getWeek11Winner(league, week):
  box_scores = league.box_scores(week)
  highestScoringFlexes = []
  for box_score in box_scores:

    flexPlayer = list(filter(lambda x: x.slot_position == 'RB/WR/TE', box_score.away_lineup))[0]
    highestScoringFlexes.append(Object(teamName=box_score.away_team.team_name, points=flexPlayer.points, playerName=flexPlayer.name))

    flexPlayer = list(filter(lambda x: x.slot_position == 'RB/WR/TE', box_score.home_lineup))[0]
    highestScoringFlexes.append(Object(teamName=box_score.home_team.team_name, points=flexPlayer.points, playerName=flexPlayer.name))

  sortedHighestScoringFlexes = sorted(highestScoringFlexes, key=lambda item: item.points, reverse=True)

  message = "\n\nWeekly Challenge\nWeek 11: Hot Flex - The team with the highest-scoring FLEX position wins.\n"
  if sortedHighestScoringFlexes[0].points == sortedHighestScoringFlexes[1].points:
    message += f"Uh oh, there was a tie. Multiple teams had players who scored {str(sortedHighestScoringFlexes[0].points)} points"
  else:
    message += f"The winner was {sortedHighestScoringFlexes[0].teamName} who had {sortedHighestScoringFlexes[0].playerName} score {str(sortedHighestScoringFlexes[0].points)} points"

  message += f"\n\nHere's the full breakdown:\n"
  for team in sortedHighestScoringFlexes:
    message += f"{team.teamName.strip()} who had {team.playerName} score {team.points} points\n"

  message += "\n\nNext week's challenge is: Gotta Catch Em All - Team with the most WR receptions (WR 1&2, flex not included).\n"
  return message
