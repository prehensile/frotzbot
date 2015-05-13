#!/usr/bin/env python

from botkit import botkit
import frotzbot
import os

# instantiate botkit
last_mention_id = os.environ.get( "last_mention_id" )
if last_mention_id is not None:
    last_mention_id = int(last_mention_id)
bot = botkit.BotKit( "frotzbot", tweet_interval=60, last_mention_id=last_mention_id )

# instantiate frotzbot
frotz_binary = "/app/frotz/dfrotz"
story_file = "/app/stories/zork1.dat"
save_path = "/app/saves"
fb = frotzbot.ZorkBot( frotz_binary, story_file, save_path )

# go!
bot.run( fb )