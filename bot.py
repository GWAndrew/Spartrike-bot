import discord
from discord.ext import commands
from discord.ext.commands import Bot
import asyncio
import os
import random
import time
import json
from time import sleep

bot = commands.Bot(command_prefix = "s!")

@bot.event
async def on_ready():
	print ("Le bot est online")

@bot.event
async def on_member_join(member):

	channel = bot.get_channel("535522119401078784")
	await bot.send_message(channel, "Bienvenu(e) sur le serveur de Spar_Trike :smile: Mais je te conseil de d'abord lire les regles {} :joy:". format(member.mention))
	print ("Nouveau membre : {}".format(member))

	role = discord.utils.get(member.server.roles, name="GirlZ and BoyZ")
	await bot.add_roles(member, role)
	print ("Role GirlZ and BoyZ a été ajouté à : {}".format(member))

	with open("users.json", "r") as f:
		users = json.load(f)

	await update_data(users, member)

	with open("users.json", "w") as f:
		json.dump(users, f)

async def update_data(users, user):
	if not user.id in users:
		users[user.id]= {}
		users[user.id]["experience"] = 0
		users[user.id]["level"] = 1

async def add_experience(users, user, exp):
	users[user.id]["experience"] += exp

async def level_up(users, user, channel):
	experience = users[user.id]["experience"]
	lvl_start = users[user.id]["level"]
	level = users[user.id]["level"]
	lvl_end_first = 250
	lvl_end = int(lvl_end_first * ((level+level)*1.5))
	int(level)

	if experience >= lvl_end:
		level = level + 1
		await bot.send_message(channel, "{} a augmenter au level {}".format(user.mention, level))
		print ("{} a augmenter au level {}".format(user.mention, level))
		users[user.id]["level"] = level


async def say_rank(users, user, channel):
	experience = users[user.id]["experience"]
	level = users[user.id]["level"]
	await bot.send_message(channel, "XP : {} ; LEVEL : {}".format(experience, level))

async def got_role_xp(users, user, member):
	level = users[user.id]["level"]
	int(level)
	if level >= 5:
		role = discord.utils.get(member.server.roles, name="Les ptits bros")
		await bot.add_roles(member, role)

	if level >= 15:
		role = discord.utils.get(member.server.roles, name="Les Maîtres")
		await bot.add_roles(member, role)

	if level >= 30:
		role = discord.utils.get(member.server.roles, name="Les seigneurs youtubes")
		await bot.add_roles(member, role)



async def show_xp(ctx, users, user, channel):
    experience = users[user.id]["experience"]
    level = users[user.id]["level"]
    username = ctx.message.author.name
    lvl_end_first = 250
    xp_next_level = int(lvl_end_first * ((level+level)*1.5))
    xp_last_level = xp_next_level - 750
    xp_needed = xp_next_level - experience
    pourcent = int((100*(xp_last_level + xp_needed))/750)
    pourcent = pourcent-(level*100)
    pourcent = pourcent+100
    pourcent_real = 100 - pourcent
    pourcent_bar_diff = int((100-pourcent)/2.4)
    pourcent_bar = int(pourcent/2.4)
    complete = "█"*pourcent_bar_diff
    not_complete = " -"*pourcent_bar
    Embed = discord.Embed(colour = discord.Colour.blue())
    Embed.set_author(name='SYSTEME DE LEVELS')
    Embed.add_field(name='LEVEL :', value='{}'.format(level), inline=True)
    Embed.add_field(name='XP TOTAL :', value='{}'.format(experience), inline=True)
    Embed.add_field(name='PROGRESSION :', value='| {}{} | {} %'.format(complete, not_complete, pourcent_real), inline=False)
    Embed.add_field(name='RESTANT :', value='{} % ({}xp) Restant | {}xp/{}xp'.format(pourcent, xp_needed, experience, xp_next_level), inline=False)
    Embed.set_footer(text="Informations : Pour gagner de l'experience, il faut tchater. A chaque message, vous pouvez gangner entre 6 et 8 d'experience. Il faut 750xp pour augmenter d'un niveau.")
    await bot.send_message(channel, embed=Embed)
    print ("LEVEL : {} ; XP : {}".format(level,experience))

@bot.event
async def on_message(message):
	if message.content.upper() == ('SPARTRIKE'):
		await bot.send_message(message.channel, "Spartrike c'est le sang :100: :fire:")
		print ("Spartrike c'est le sang :100: :fire:")

	with open("users.json", "r") as f:
		users = json.load(f)

	if message.author != bot.user:
		await update_data(users, message.author)
		await add_experience(users, message.author, random.randint(6,8))
		await level_up(users, message.author,message.channel)
	else :
		pass

	with open("users.json", "w") as f:
		json.dump(users, f)

	if message.content == message.content and message.author != bot.user:
		await got_role_xp(users, message.author, message.author)

	await bot.process_commands(message)

@bot.command(pass_context = True)
async def ping(ctx):
    resp = await bot.say('Ping du bot :')
    diff = resp.timestamp - ctx.message.timestamp
    await bot.say(f"{1000*diff.total_seconds():.1f}ms")
    print ("Ping :", f"{1000*diff.total_seconds():.1f}ms")

@bot.command(pass_context = True)
async def effacer(ctx, amount=100):
	if ctx.message.author.server_permissions.administrator:
	    channel = ctx.message.channel
	    messages = []
	    async for message in bot.logs_from(channel, limit=int(amount)):
	    	messages.append(message)
	    await bot.delete_messages(messages)
	else :
		await bot.send_message(ctx.message.channel, "Tu n'as pas la permission pour effacer un message")

@bot.command(pass_context = True)
async def rank(ctx):
	with open("users.json", "r") as f:
		users = json.load(f)
	await show_xp(ctx, users, ctx.message.author,ctx.message.channel)


bot.run(os.getenv('TOKEN'))
