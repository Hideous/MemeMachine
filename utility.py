import discord
import asyncio

## UTILITY FUNCTIONS
@asyncio.coroutine
def check_mod(user):
	for role in user.roles:
		p = role.permissions
		if (p == p.all() or p == p.all_channel()):
			return True
	return False
###-----