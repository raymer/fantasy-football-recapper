from espn_api.football import League
import openai
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import logging
from . import weekly_challenge
from . import weekly_scores_summarizer

def generateRecap(_swid, _espn_s2, _openAiKey, _slackToken, _slackChannelId):
  swid = _swid
  espn_s2 = _espn_s2
  openai.api_key = _openAiKey
  slackBotToken = _slackToken
  slackChannelId = _slackChannelId

  league = League(league_id=428433, year=2023, espn_s2=espn_s2, swid=swid)

  currentWeek = league.current_week if league.current_week == 1 else league.current_week - 1

  # Get weekly score summary.
  weeklySummary = weekly_scores_summarizer.getSummary(league, currentWeek)

  # Use weekly score summary to get ChatGPT summary.
  messages = [ {"role": "system", "content": "You are a intelligent assistant."} ]
  message = f"User : Pretending to be the commissioner of our fantasy football league, write a funny/condescending summary of this week's (week {currentWeek}) results in the fantasy football league given this data about the teams and scores: {weeklySummary}"

  messages.append({"role": "user", "content": message})
  chat = openai.ChatCompletion.create(model="gpt-4-1106-preview", messages=messages)
  chatGPTResponse = chat.choices[0].message.content
  logging.info("Chat GPT Response Generated")
  
  slackMessage = chatGPTResponse + weekly_challenge.getWeeklyWinner(league, currentWeek)

  # Post to Slack
  client = WebClient(token=slackBotToken)
  try:
    result = client.chat_postMessage(channel=slackChannelId, text=slackMessage)
    logging.info("Posted to Slack")

  except SlackApiError as e:
    logging.info(f"Error: {e}")

