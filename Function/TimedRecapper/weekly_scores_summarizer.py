from espn_api.football import League

def getSummary(league, currentWeek):
  espnMessage = ''
  topScore = 0
  lowScore = 1000

  box_scores = league.box_scores(currentWeek)
  for box_score in box_scores:
    espnMessage += f" {box_score.away_team.team_name} who scored {str(box_score.away_score)} vs. {box_score.home_team.team_name} who scored {str(box_score.home_score)};"
    if box_score.away_score > topScore:
      topScore = box_score.away_score
    if box_score.home_score > topScore:
      topScore = box_score.home_score

    if box_score.away_score < lowScore:
      lowScore = box_score.away_score
    if box_score.home_score < lowScore:
      lowScore = box_score.home_score

  topScoringBoxScore = list(filter(lambda x: x.home_score == topScore or x.away_score == topScore, box_scores))
  highTeam = topScoringBoxScore[0].home_team if topScoringBoxScore[0].home_score == topScore else topScoringBoxScore[0].away_team
  highRoster = topScoringBoxScore[0].home_lineup if topScoringBoxScore[0].home_score == topScore else topScoringBoxScore[0].away_lineup

  bottomScoringBoxScore = list(filter(lambda x: x.home_score == lowScore or x.away_score == lowScore, box_scores))
  lowTeam = bottomScoringBoxScore[0].home_team if bottomScoringBoxScore[0].home_score == lowScore else bottomScoringBoxScore[0].away_team
  lowRoster = bottomScoringBoxScore[0].home_lineup if bottomScoringBoxScore[0].home_score == lowScore else bottomScoringBoxScore[0].away_lineup

  sortedHighRoster = list(filter(lambda x: x.slot_position != 'BE' and x.slot_position != 'IR', sorted(highRoster, key=lambda item: item.points, reverse=True)))
  sortedLowRoster = list(filter(lambda x: x.slot_position != 'BE' and x.slot_position != 'IR', sorted(lowRoster, key=lambda item: item.points)))

  espnMessage += f" The highest scoring team was {highTeam.team_name} who scored {str(topScore)} points, thanks to {sortedHighRoster[0].name} who scored {str(sortedHighRoster[0].points)}"
  espnMessage += f". The lowest scoring team was {lowTeam.team_name} who scored {str(lowScore)} points, thanks to {sortedLowRoster[0].name} who scored {str(sortedLowRoster[0].points)}"
  
  return espnMessage
