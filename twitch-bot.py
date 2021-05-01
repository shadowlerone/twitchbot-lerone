import sys

import twitch

from shadowlerone.twitch_bot.bot import Bot
from shadowlerone.twitch_bot.creds import channel, nickname, oauth, client_id, client_secret
bot = Bot(prefix="!",
				channel=channel,
				nickname=nickname,
				oauth=oauth,
				client_id=client_id,
				client_secret=client_secret,
				use_cache=True)

@bot.command('stream', 'get stream info')
def stream(*args, **kwargs):
	return bot.helix.stream().viewer_count

@bot.command('socials', 'get my social media')
def socials(*args, **kwargs):
	return "You can find me at http://shadowlerone.ca/socials/"

@bot.command('discord', 'discord')
def discord(*args, **kwargs):
	return "Join our discord server! http://shadowlerone.ca/r/discord/"

@bot.command('id', 'id')
def id(*args, **kwargs):
	return bot.helix.user(args[0]).id

@bot.command('so', 'shoutouts a user')
def shoutout(*args, **kwargs):
	user = bot.helix.user(args[0])
	# print(f"printing users: {user}")
	mods = list(map(lambda x: x['user_name'],bot.helix.api.get('/moderation/moderators', {'broadcaster_id':71100896})['data']))
	mods.append(bot.channel[1:])
	print(mods)
	if kwargs['message'].sender in mods:
		game_id = bot.helix.api.get('/search/channels', {'query':user.display_name})['data'][0]['game_id']
		game = bot.helix.api.get('games', {'id':game_id})['data'][0]['name']
		# print(f"Printing mods: {mods}")
		return f"Shoutout to {user.login}! They were last playing {game}. Check them out at https://twitch.tv/{user.login}"

@bot.command('raid', 'inits raid if online')
def raid(*args, **kwargs):
	if bot.helix.user(args[0]).is_live:
		if bot.helix.user(bot.nickname).is_live:
			return f"/raid {args[0]}"
		else:
			return f"/host {args[0]}"
	else:
		return f"{args[0]} is currently offline."

@bot.command('shutdown', '')
def shutdown(*args, **kwargs):
	if kwargs['message'].sender == 'shadowlerone':
		sys.exit(0)


bot()
