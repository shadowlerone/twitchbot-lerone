import logging
import re
import sys
import threading
import time
import traceback
import types
import typing
import webbrowser
import twitch
import requests

from bottle import Bottle, request, response, route, template


class Bot():
	def __init__(self, prefix: str, channel: str, nickname: str, oauth: str, client_id: str, client_secret: str, use_cache=True):
		self.commands = {}
		self.pattern = re.compile(f"^{prefix}(\w*) ?(.*)")
		self.prefix = prefix
		self.channel = channel
		self.nickname = nickname
		self.oauth = oauth
		self.client_id = client_id
		self.client_secret = client_secret
		self.scopes = ['moderation:read', 'channel:manage:broadcast','channel:manage:redemptions','channel:read:hype_train', 'channel:read:subscriptions','']
		self.token = None
		self.code = None
		self.code_available = threading.Event()
		self.app = Bottle()
		@self.app.route('/')
		def get_code():
			self.code = request.query.code
			self.code_available.set()
			# sys.exit(0)
			return "<script>close();</script>"

	def get_oauth(self):
		req = requests.post('https://id.twitch.tv/oauth2/token', {
			'client_id':self.client_id,
			'client_secret':self.client_secret,
			'grant_type':'client_credentials',
			'scope': " ".join(self.scopes)
		})
		self.token = req.json()['access_token']

	def command(self, name: str, desc: str):
		def c(f):
			def g(*args, **kwargs):
				out = f(*args, **kwargs)
				print(f"command output: {out}")
				return(out)
			self.commands[name] = g
		return c

	def handle_message(self, message: twitch.chat.Message) -> None:
		print(f"Recieved message: {message.text}")
		match = self.pattern.fullmatch(message.text)
		print(message.sender)
		if match != None:
			try:
				response = self.commands[match.group(1)](match.group(2), message= message)
				if response != None:
					message.chat.send(response)
			except KeyError:
				print("Command not found. Moving on...")
			except:
				print("Unexpected error:", sys.exc_info()[0])
				print(traceback.format_exc())

	def shut_down(self):
		pass

	def __call__(self):
		# pass
		print("bot starting")
		print("Getting Token")
		# self.get_oauth()
		# webbrowser.open(f"https://id.twitch.tv/oauth2/authorize?response_type=code&client_id={self.client_id}&redirect_uri=http://localhost&scope={'%20'.join(self.scopes)}")
		# print(f"Please go to https://id.twitch.tv/oauth2/authorize?response_type=code&client_id={self.client_id}&redirect_uri=http://localhost&scope={'%20'.join(self.scopes)}")
		
		# self.server = threading.Thread(target=self.app.run, kwargs={'port':80}, daemon=True)
		# self.server.start()
		# self.code_available.wait()
		# self.server.join()
		print("Code Obtained")
		print(f"Code: {self.code}")
		self.helix = twitch.Helix(client_id=self.client_id, client_secret=self.client_secret, use_cache=True, bearer_token=self.token) #, code=self.code)
		self.chat = twitch.Chat(channel=self.channel, nickname=self.nickname, oauth=self.oauth, helix=self.helix)
		self.chat.subscribe(self.handle_message)
