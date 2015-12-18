import discord
import asyncio
import urllib.request
import urllib.error
import config
import os.path
import os
import utility
import random
from ctypes.util import find_library

tts = False

playing = False
gPlayer = None

@asyncio.coroutine	
def help(arguments, message, client, author, channel):
	yield from client.send_typing(channel)
	helptext = """
	This is my current list of commands:```
	!help
!flickr [keywords]
!soundboard/!sb/!s [sound name]
!nicememe```
!roll [number]
	"""
	yield from client.send_message(channel, helptext)
	return

@asyncio.coroutine	
def default(arguments, message, client, author, channel):
	return
	
@asyncio.coroutine
def hello(arguments, message, client, author, channel):
	print("hello! you said:" + message)

@asyncio.coroutine
def quit(arguments, message, client, author, channel):
	if (utility.check_mod(author)):
		raise SystemExit
	return
	
#Retreives a random flicker pic of specified tag
@asyncio.coroutine
def flickr(arguments, message, client, author, channel):
	yield from client.send_typing(channel)
	message = "http://loremflickr.com/640/480"
	keywords = ""
	for arg in arguments:
		if (arg == ""):
			break
		keywords = keywords + "/" + arg
		keywords = keywords + "/"
	message = message + keywords
	
	title = "Random Flickr Image.jpg"
	print("Sending message:" + message + " to channel " + channel.name)
	
	try:
		image = urllib.request.urlopen(message)
	except urllib.error.HTTPError:
			print("HTTP Error!")
			yield from client.send_message(channel, "Sorry, I couldn't find any images with those keywords.")
			return
	if (image.getcode() == 200 or image.getcode() == "200"):
		yield from client.send_file(channel, image, title)
	
	else:
		yield from client.send_message(channel, "Sorry, I couldn't find any images with those keywords.")
	
	image.close()
	
	return


#THE CROWN JEWEL OF THIS BOT:
#Soundboard! sb is set up as alias function.
@asyncio.coroutine
def soundboard(arguments, message, client, author, channel):
	global playing
	global gPlayer
	
	c = author.voice_channel
	
	if (c == None):
		return
	
	userchannel = None
	
	if (not discord.opus.is_loaded()):
		discord.opus.load_opus("C:\\Users\\Andreas\\Documents\\MemeMachine\\libopus-0.dll")
	
	files_list = os.listdir(config.SOUNDS)
	files_list = map(lambda each:each.rstrip(".mp3"), files_list)
	files = " - ".join(files_list)
	
	print (len(arguments))
	if (len(arguments) == 0):
		emptymessage = """
		Use command with: ```!soundboard [sound name]
!sb [sound name]
!s [sound name]```
		
		"""+"This is my current list of sounds:\n```"+files+"```"
		yield from client.send_typing(channel)
		yield from client.send_message(channel, emptymessage)
		return
	
	filename=config.SOUNDS+'\\'+arguments[0].lower()+'.mp3'
	
	print(filename)
	if (not os.path.isfile(path=filename)):
		yield from client.send_typing(channel)
		yield from client.send_message(channel, "I don't have that sound! This is my current list:\n```"+files+"```")
		return
	
	if (gPlayer is not None and gPlayer.is_playing()):
		return
	
	for s in client.servers:
		for m in s.members:
			if m.id == author.id:
				userchannel = m.voice_channel
				print("User is in channel " + str(userchannel))
			if m.id == client.user.id:
				mychannel = m.voice_channel
				print("I'm in channel "+str(mychannel))
	
	if (userchannel is not mychannel):
		print("I'm in "+str(c)+", so I will join"+str(userchannel)+"instead.")
		if (client.is_voice_connected()):
			yield from client.voice.disconnect()
		yield from client.join_voice_channel(c)

	if (client.is_voice_connected()):
		player = client.voice.create_ffmpeg_player(filename)
		player.start()
		gPlayer = player
	return
	
@asyncio.coroutine
def sb(arguments, message, client, author, channel):
	yield from soundboard(arguments, message, client, author, channel)
	return
	
@asyncio.coroutine
def s(arguments, message, client, author, channel):
	yield from soundboard(arguments, message, client, author, channel)
	return
	
@asyncio.coroutine
def nicememe(arguments, message, client, author, channel):
	yield from soundboard(["nicememe"], message, client, author, channel)
	return
	
@asyncio.coroutine
def roll(arguments, message, client, author, channel):
	yield from client.send_typing(channel)
	if (len(arguments) == 0):
		yield from client.send_message(channel, "To use this command, please say ```!roll [number]```")
		return

	try:
		die = int(arguments[0])
	except ValueError:
		yield from client.send_message(channel, "Not a valid number!")
		return
		
	result = random.randint(0, die)
		
	yield from client.send_message(channel, "Your d"+str(die)+" die has rolled a "+str(result)+"!")
	return
