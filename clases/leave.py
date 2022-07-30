async def onleave(ctx: Context):
    profile = await ctx.client.get_user_info(ctx.msg.uid)
    leave = """[c] ¡Adios usuario! Esperamos verte pronto.
[c]Gracias por    haberte unido               ₍ᐢ. .ᐢ₎ """
    embed = Embed(
        title=profile.nickname,
        object_type=0,
        object_id=ctx.msg.uid,
        content="No soporto el estilo Drev. unu"
    )
    await ctx.send(leave, embed=embed)
