from edamino import Bot, Context, logger
from edamino.objects import UserProfile
from edamino.api import Embed
import re

bot = Bot(email='', password='', prefix="")

@bot.event()
async def on_ready(profile: UserProfile):
    logger.info(f'{profile.nickname} ha sido encendido')

@bot.command('ping', prefix="!")
async def on_ping(ctx: Context):
    await ctx.reply("pong")

@bot.command('embed')
async def on_embed(ctx: Context):
    embed = Embed(
        title=ctx.msg.author.nickname,
        object_type=0,
        object_id=ctx.msg.author.uid,
        content="Hola wapo."
    )
    await ctx.send("Interesante no? uwu", embed=embed)

@bot.command('join')
async def on_join_community(ctx: Context):
    msg = ctx.msg.content
    comu = re.search("http://aminoapps.com/c/", msg)
    cmd = ' '.join(ctx.msg.content.split()[1:])

    if comu:
        ide = await ctx.get_info_link(cmd)
        idlink = ide.community.ndcId
        with ctx.set_ndc(idlink):
            await ctx.join_community()
        await ctx.reply('Me he unido. :3')

bot.start()
