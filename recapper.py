from espn_api.football import League
import openai
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

settingsData = open("recapper_settings.txt", "r")
settings = settingsData.readlines()

swid = settings[0].split("=")[1].replace('\n', '').strip()
espn_s2 = settings[1].split("=")[1].replace('\n', '').strip()
openai.api_key = settings[2].split("=")[1].replace('\n', '').strip()
slackBotToken = settings[3].split("=")[1].replace('\n', '').strip()

league = League(league_id=428433, year=2022, espn_s2=espn_s2, swid=swid)

espnMessage = ''
topScore = 0
lowScore = 1000

box_scores = league.box_scores()
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

sortedHighRoster = list(filter(lambda x: x.slot_position != 'BE', sorted(highRoster, key=lambda item: item.points, reverse=True)))
sortedLowRoster = list(filter(lambda x: x.slot_position != 'BE', sorted(lowRoster, key=lambda item: item.points)))

espnMessage += f" The highest scoring team was {highTeam.team_name} who scored {str(topScore)} points, thanks to {sortedHighRoster[0].name} who scored {str(sortedHighRoster[0].points)}"
espnMessage += f". The lowest scoring team was {lowTeam.team_name} who scored {str(lowScore)} points, thanks to {sortedLowRoster[0].name} who scored {str(sortedLowRoster[0].points)}"

print(espnMessage)

#stats
#print(league.teams)
#print(league.standings())
#print(league.top_scorer())
#print(league.least_scorer())
#print(league.most_points_against())
#print(league.top_scored_week())
#print(league.least_scored_week())



# Chat GPT
# messages = [ {"role": "system", "content": "You are a intelligent assistant."} ]
# message = f"User : Pretending to be a guy named RickyGPT, write a funny/condescending summary of this week's (week {league.current_week}) results in the fantasy football league given this data about the teams and scores: {espnMessage}"

# messages.append({"role": "user", "content": message})
# chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
# chatGPTResponse = chat.choices[0].message.content
# print(chatGPTResponse)


# Post to Slack
# client = WebClient(token=slackBotToken)
# testingChannelId = "C05QADBPZQW"
# fantasyFootballChannelId = "G53UF4PC4"
# try:
#   result = client.chat_postMessage(channel=testingChannelId, text=chatGPTResponse)
#   print(result)

# except SlackApiError as e:
#   print(f"Error: {e}")

