* [Ejemplos](#example)
    * [Ejemplo mínimo](#min-example)
    * [Enviar imagen](#send-image)
    * [Enviar gif](#send-gif)
    * [Enviar sticker](#send-sticker)
    * [Enviar embed](#send-embed)
    * [Esperar por](#wait-for)
    * [Escritura y grabación simuladas](#typing-bot)
    * [Cómo mencionar a un usuario en una sala de chat](#mention-chat)

* [Eventos](#event)
    * [on_ready](#on-ready-event)
    * [on_mention](#on-ready-event)
    * [Selección de un tipo de mensaje (Messagetype) o tipo de multimedia (Mediatype)](#select-type)

* [Capacidades de comando del decorador](#command)
    * [Parámetros Adicionales](#command-parameters)
    * [Puedes reservar varios comandos](#command-reserve)
    * [Prefijo (Prefix)](#prefix)

<br><br>

# Ejemplos <a id=example>

## Ejemplo Minimo <a id=min-example>

```py
from edamino import Bot, Context

bot = Bot('correo', 'contraseña', 'prefix')


@bot.command('ping')
async def on_ping(ctx: Context):
    await ctx.reply('Pong!')


bot.start()
```

## Enviar imagen <a id=send-image>

```py
from edamino import Bot, Context
from edamino.api import File

bot = Bot('correo', 'contraseña', 'prefix')


@bot.command('image')
async def on_image(ctx: Context):
    image = File.load('path_to_file')
    await ctx.send_image(image)

    # También puede cargar una imagen de forma asíncrona

    image = await File.async_load('path_to_file')
    await ctx.send_image(image)

    # También puedes cargarlo tú mismo

    with open('path_to_file', 'rb') as file:
        image = file.read()

    await ctx.send_image(image)

    # Incluso puedes descargar una imagen de Internet

    image = await ctx.download_from_link('link_to_image')
    await ctx.send_image(image)


bot.start()
```

## Enviar sticker <a id=send-sticker>

```py
from edamino import Bot, Context

bot = Bot('correo', 'contraseña', 'prefix')


@bot.command('sticker')
async def on_gif(ctx: Context):
    await ctx.send_sticker('Id del Sticker (StickerId)')


bot.start()
```

## Enviar embed <a id=send-embed>

```py
from edamino import Bot, Context
from edamino.api import Embed

bot = Bot('correo', 'contraseña', 'prefix')


@bot.command('embed')
async def on_embed(ctx: Context):
    embed = Embed(
        title=ctx.msg.author.nickname,
        object_type=0,
        object_id=ctx.msg.author.uid,
        content="Pon el texto de tu preferencia."
    )
    await ctx.send(embed=embed)


bot.start()
```

## Espera por <a id=wait-for>

**NOTA: El `bot.wait_for` es necesario si desea recibir el siguiente mensaje..**

```py
from edamino import Bot, Context
from edamino.objects import Message

bot = Bot('correo', 'contraseña', 'prefix')


@bot.command('check')
async def on_check(ctx: Context):
    def check(m: Message):
        return m.content == 'Sh'

    msg = await bot.wait_for(check=check)
    await ctx.send('Ok', reply=msg.messageId)


bot.start()
```

## Escritura y grabación simuladas <a id=typing-bot>
```py
from edamino import Bot, Context
from edamino.objects import Message
from asyncio import sleep

bot = Bot('correo', 'contraseña', 'prefix')

@bot.command('typing')
async def on_typing(ctx: Context):
    async with ctx.typing():
        await sleep(3)
        await ctx.reply('✔')

@bot.command(['rec', 'recording'])
async def on_ping(ctx: Context):
    async with ctx.recording():
        await sleep(3)
        await ctx.reply('🎁')

bot.start()
```

## Cómo mencionar a un usuario en una sala de chat <a id=mention-chat>
```py
from edamino import Bot, Context

bot = Bot('email', 'password', 'prefix')

@bot.command('mention')
async def on_m(ctx: Context):
    await ctx.reply(f'<$@{ctx.msg.author.nickname}$>', mentions=[ctx.msg.uid])

bot.start()
```

# Eventos <a id=event>

## `on_ready` <a id=on-ready-event>

**NOTA: El evento `on_ready` está diseñado para averiguar cuándo el bot comenzará a funcionar. Toma el perfil global del bot
como parámetro.**

```py
from edamino import Bot, logger
from edamino.objects import UserProfile

bot = Bot(correo='correo', contraseña='contraseña', prefix="/")


@bot.event()
async def on_ready(profile: UserProfile):
    logger.info(f'{profile.nickname} ready')


bot.start()
```

## `on_mention` <a id=on-mention-event>

**NOTA: El evento `on_mention` se activa si se menciona o se responde al bot.**

```py
from edamino import Bot, Context

bot = Bot(correo='correo', contraseña='contraseña', prefix="/")


@bot.event()
async def on_mention(ctx: Context):
    await ctx.reply('Lo que quieras.')


bot.start()
```

## Selección de un tipo de mensaje (Messagetype) o tipo de multimedia (Mediatype) <a id=select-type>

**NOTA: Puede configurar a qué tipos de mensajes reaccionará el evento.**

```py
from edamino import Bot, Context, logger
from edamino import api

bot = Bot(correo='correo', contraseña='contraseña', prefix="/")


# Este evento aceptará absolutamente todo tipo de mensajes.
@bot.event(message_types=api.MessageType.ALL, media_types=api.MediaType.ALL)
async def on_message(ctx: Context):
    print(ctx.msg)


# Este evento se activará si alguien ha ingresado a la sala de chat.
@bot.event([api.MessageType.GROUP_MEMBER_JOIN])
async def on_member_join(ctx: Context):
    embed = api.Embed(
        title=ctx.msg.author.nickname,
        object_type=0,
        object_id=ctx.msg.author.uid,
    )
    await ctx.send("Bienvenido al chat!", embed=embed)


bot.start()
```

# Capacidades del decorador de comando <a id=command>

## Parametros de comando <a id=command-parameters>

```py
from edamino import Bot, Context

bot = Bot(correo='correo', contraseña='contraseña', prefix="/")


@bot.command('say')
async def on_say(ctx: Context, args: str)
    await ctx.reply(args)


@bot.command('get')
async def on_get(ctx: Context, link: str):
    """
    User: get https://aminoapps/c/anime
    Bot: Community id
    """
    info = await ctx.get_info_link(link)

    await ctx.reply(str(info.community.ndcId))


bot.start()
```

## Puedes reservar varios comandos <a id=command-reserve>

```py
from edamino import Bot, Context

bot = Bot(email='email', password='password', prefix="/")

@bot.commnad(['play', 'p'])
async def on_example(ctx: Context):
    await ctx.reply('Good! 🎉')

bot.start()
```


## Prefijo (Prefix) <a id=prefix>
**NOTA: Puede hacer un prefijo separado para su comando.**
```py
from edamino import Bot, Context

bot = Bot(email='email', password='password', prefix="/")

@bot.commnad('println(', prefix='System.out.')
async def on_print(ctx: Context, args: str):
    """
    User: System.out.println(lala)
    Bot: lala
    """
    await ctx.reply(args.replace(')'))

bot.start()
```
