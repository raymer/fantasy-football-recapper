from espn_api.football import League

def getWeeklyWinner(league, week):
  box_scores = league.box_scores(week)
  if week == 2:
    return getWeek2Winner(league, week)
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


def getWeek3Winner(league, week):
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
    message = "\n\nWeekly Challenge\nWeek 3: Endzone Celebration - The team that scores the most offensive touchdowns wins.\n"
    message += f"The winner was {highTeam.team_name} who scored {str(topScore)} points"
    return message