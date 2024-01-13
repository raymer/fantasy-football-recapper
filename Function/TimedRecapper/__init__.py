import datetime
import logging

import azure.functions as func
import os

from . import recapper

def main(mytimer: func.TimerRequest) -> None:
  utc_timestamp = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).isoformat()

  logging.info('Python timer trigger function ran at %s', utc_timestamp)

  swid = os.getenv("swid")
  espn_s2 = os.getenv("espn_s2")
  openAiKey = os.getenv("openai_key")
  slackBotToken = os.getenv("slack_token")
  slackChannelId = os.getenv("slack_channel_id")

  recapper.generateRecap(swid, espn_s2, openAiKey, slackBotToken, slackChannelId)