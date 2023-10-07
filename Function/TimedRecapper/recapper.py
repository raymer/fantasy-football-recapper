from espn_api.football import League
import openai
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import logging
from . import weekly_challenge

def generateRecap(_swid, _espn_s2, _openAiKey, _slackToken):
  swid = _swid
  espn_s2 = _espn_s2
  openai.api_key = _openAiKey
  slackBotToken = _slackToken

  league = League(league_id=428433, year=2023, espn_s2=espn_s2, swid=swid)

  currentWeek = league.current_week if league.current_week == 1 or league.current_week == 14 else league.current_week - 1
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

  # Chat GPT
  # messages = [ {"role": "system", "content": "You are a intelligent assistant."} ]
  # message = f"User : Pretending to be a guy named RickyGPT, write a funny/condescending summary of this week's (week {currentWeek}) results in the fantasy football league given this data about the teams and scores: {espnMessage}"

  # messages.append({"role": "user", "content": message})
  # chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
  # chatGPTResponse = chat.choices[0].message.content
  # logging.info("Chat GPT Response Generated")
  
  # slackMessage = chatGPTResponse + weekly_challenge.getWeeklyWinner(league, currentWeek)
  print(weekly_challenge.getWeeklyWinner(league, currentWeek))

  # Post to Slack
  # client = WebClient(token=slackBotToken)
  # testingChannelId = "C05QADBPZQW"
  # fantasyFootballChannelId = "G53UF4PC4"
  # try:
  #   result = client.chat_postMessage(channel=fantasyFootballChannelId, text=slackMessage)
  #   logging.info("Posted to Slack")

  # except SlackApiError as e:
  #   logging.info(f"Error: {e}")

