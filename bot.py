import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import os
import random
import time

os.system('color 0A')

bot = commands.Bot(command_prefix = "?")
@bot.event
async def on_ready():
	print ("BOT ON")

@bot.event
async def on_member_join(member):
    channel = bot.get_channel("567634481238900736")
    rules_channel = bot.get_channel("567633107851673601")
    await bot.send_message(channel, "Welcome to The GD Kingdom ! {} please read {} so that you don't get a warn immediately, have a great time on this server !".format(member.mention, rules_channel.mention))
    print ("New member : {}".format(member))
    role = discord.utils.get(member.server.roles, name="Newbie")
    await bot.add_roles(member, role)
    print ("Role Newbie has been added to : {}".format(member))

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel("567634481238900736")
    await bot.send_message(channel, "Sorry to see you leaving {} :(". format(member))
    print ("Member left : {}".format(member))


@bot.command(pass_context = True)
async def ping(ctx):
    resp = await bot.say('Ping :')
    diff = resp.timestamp - ctx.message.timestamp
    await bot.say(f"{1000*diff.total_seconds():.1f}ms")
    print ("Ping")

@bot.command(pass_context = True)
async def warn(ctx, member: discord.Member, arg1):
	roles = [role.name for role in member.roles]
	mod_roles = [role.name for role in ctx.message.author.roles]
	channel = bot.get_channel("570286158777679873")
	bchannel = bot.get_channel("570532951687823371")
	if "Helper" in mod_roles:
		warning1 = False
		warning2 = False

		for role in member.roles:
			if role.name == "Warning 2" and "Warning 1":
				warn3 = discord.utils.get(member.server.roles, name="Warning 3")
				await bot.add_roles(member, warn3)
				await bot.send_message(channel, "{} got warned (Warning 3) by {} in {} for : {}".format(member.mention, ctx.message.author.mention, ctx.message.channel.mention,arg1))
				print ("{} got Warning 3 for : {}".format(member, arg1))
				warning1 = True
				warning2 = True
				break

		for role in member.roles:
			if role.name == "Warning 1":
				if role.name == "Warning 2" and warning2 == True:
					pass
				elif warning2 == False:
					warn2 = discord.utils.get(member.server.roles, name="Warning 2")
					await bot.add_roles(member, warn2)
					await bot.send_message(channel, "{} got warned (Warning 2) by {} in {} for : {}".format(member.mention, ctx.message.author.mention, ctx.message.channel.mention,arg1))
					print ("{} got Warning 2 for : {}".format(member, arg1))
					warning1 = True
					break

		if warning1 == False:
			warn1 = discord.utils.get(member.server.roles, name="Warning 1")
			await bot.add_roles(member, warn1)
			await bot.send_message(channel, "{} got warned (Warning 1) by {} in {} for : {}".format(member.mention, ctx.message.author.mention, ctx.message.channel.mention,arg1))
			print ("{} got Warning 1 for : {}".format(member, arg1))

		if "Warning 3" in roles:
			await bot.ban(member)
			await bot.send_message(bchannel, "{} got banned (Warning 4) by {} in {} for : {}".format(member, ctx.message.author.mention, ctx.message.channel.mention, arg1))
	else:
		await bot.send_message(ctx.message.channel, "You don't have permission to warn members".format(ctx.message.author.mention))

@bot.command(pass_context=True)
async def remove_warn(ctx, member: discord.Member, args):
	roles = [role.name for role in member.roles]
	mod_roles = [role.name for role in ctx.message.author.roles]
	channel = bot.get_channel("570301894321504261")
	if "Helper" in mod_roles:
		r_warn1 = True
		r_warn2 = True
		if "Warning 1" in roles:
			print("test")
			if "Warning 3" not in roles and "Warning 2" not in roles:
				role = discord.utils.get(ctx.message.server.roles, name='Warning 1')
				await bot.remove_roles(member, role)
				await bot.send_message(channel, "{} got warning 1 removed by {} : {}".format(member.mention, ctx.message.author.mention, args))
			if "Warning 2" in roles:
				if "Warning 3" not in roles:
					role = discord.utils.get(ctx.message.server.roles, name='Warning 2')
					await bot.remove_roles(member, role)
					await bot.send_message(channel, "{} got warning 2 removed by {} : {}".format(member.mention, ctx.message.author.mention, args))
					r_warn1 = False
				if "Warning 3" in roles:
					role = discord.utils.get(ctx.message.server.roles, name='Warning 3')
					await bot.remove_roles(member, role)
					await bot.send_message(channel, "{} got warning 3 removed by {} : {}".format(member.mention, ctx.message.author.mention, args))
		elif "Warning 1" not in roles:
			await bot.send_message(ctx.message.channel, "{} has no warning {}".format(member, ctx.message.author.mention))
	else:
		await bot.send_message(ctx.message.channel, "You don't have permission to remove warnings".format(ctx.message.author.mention))

@bot.command(pass_context=True)
async def ban(ctx, member: discord.Member, args):
	mod_roles = [role.name for role in ctx.message.author.roles]
	bchannel = bot.get_channel("570532951687823371")
	try:
		if "Helper" in mod_roles:
			await bot.ban(member)
			await bot.send_message(bchannel, "{} got banned by {} for : {}".format(member, ctx.message.author.mention, arg1))
		else:
			await bot.send_message(ctx.message.channel, "You don't have permission to ban members")
	except:
		await bot.send_message(ctx.message.channel, "You can't ban a staff member")


@bot.command(pass_context = True)
async def clear(ctx, number):
	mod_roles = [role.name for role in ctx.message.author.roles]
	try :
		if "Helper" in mod_roles:
		    mgs = []
		    number = int(number)
		    number = number + 1
		    async for x in bot.logs_from(ctx.message.channel, limit = number):
		        mgs.append(x)
		    await bot.delete_messages(mgs)
		else:
			await bot.send_message(ctx.message.channel, "You don't have permission to delete messages")
	except :
		await bot.send_message(ctx.message.channel, "You can't delete more than 99 messages")





bot.run(os.getenv('TOKEN'))
