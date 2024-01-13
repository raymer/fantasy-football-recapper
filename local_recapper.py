from espn_api.football import League
import openai
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
import Function.TimedRecapper.recapper as recapper

settingsData = open("recapper_settings.txt", "r")
settings = settingsData.readlines()

swid = settings[0].split("=")[1].replace('\n', '').strip()
espn_s2 = settings[1].split("=")[1].replace('\n', '').strip()
openAiKey = settings[2].split("=")[1].replace('\n', '').strip()
slackBotToken = settings[3].split("=")[1].replace('\n', '').strip()
slackChannelId = settings[4].split("=")[1].replace('\n', '').strip()
leagueId = settings[5].split("=")[1].replace('\n', '').strip()

recapper.generateRecap(swid, espn_s2, openAiKey, slackBotToken, slackChannelId, leagueId)
