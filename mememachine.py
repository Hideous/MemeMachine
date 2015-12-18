import discord
import commands
import config
import utility

client = discord.Client()
channel = "General"
voice = None

#We've logged in!
@client.async_event
def on_ready():
	print('Logged in as')
	print(client.user.name)
	print(client.user.id)
	print('-----')
	
#Text message posted, do command processing here
@client.async_event
def on_message(message):
	m = message.content
	
	if ( not m.startswith("!")): #Not a command
		return
	
	options = {'hello' : commands.hello,
           'quit' : commands.quit,
		   'flickr' : commands.flickr
	}
	
	command = m.split()[0].strip('!')
	arguments = m.split()[1:]
	msg = m[len(command)+2:]
	
	print(command + " command received from USER:" + message.author.name)
	#options[command](arguments, msg, client, message.author, message.channel)
	method = getattr(commands, command, commands.default)
	yield from method(arguments, msg, client, message.author, message.channel)
	
	return
	
@client.async_event
def main_task():
	return

#Message Deleted
@client.async_event
def on_message_delete():
	return
	
@client.async_event
def on_member_join(member):
	print("Member "+member.name+" has joined")
	return
	
client.run(config.EMAIL, config.PASSWORD)