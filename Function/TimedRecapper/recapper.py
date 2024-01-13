from espn_api.football import League
import openai
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import logging
from . import weekly_scores_summarizer
import datetime

def generateRecap(swid, espn_s2, openAiKey, slackBotToken, slackChannelId, leagueId):
  openai.api_key = openAiKey

  lastYear = datetime.date.today().year - 1
  league = League(league_id=leagueId, year=lastYear, espn_s2=espn_s2, swid=swid)

  currentWeek = league.current_week if league.current_week == 1 else league.current_week - 1

  weeklySummary = weekly_scores_summarizer.getSummary(league, currentWeek)

  messages = [ {"role": "system", "content": "You are a intelligent assistant."} ]
  message = f"User : Pretending to be the commissioner of our fantasy football league, write a funny/condescending summary of this week's (week {currentWeek}) results in the fantasy football league given this data about the teams and scores: {weeklySummary}"
  messages.append({"role": "user", "content": message})
  chat = openai.ChatCompletion.create(model="gpt-4-1106-preview", messages=messages)
  chatGPTResponse = chat.choices[0].message.content

  client = WebClient(token=slackBotToken)
  try:
    result = client.chat_postMessage(channel=slackChannelId, text=chatGPTResponse)
    logging.info("Posted to Slack")
  except SlackApiError as e:
    logging.info(f"Error: {e}")

