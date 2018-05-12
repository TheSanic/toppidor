import discord
import asyncio
from aiohttp import ClientSession
from sys import exc_info
from re import findall
from time import sleep
from os import environ
from random import randrange
from discord.ext import commands
from discord import Embed

dreamfinity_admins = ["Rainbowtaves", "Noire", "Primali", "Farianit", "fox1488", "Hallowt", "cleveron24", "Dancho",
                      "Herobrine1_YT", "CrashBox", "BlackDiver", "D_lorian", "Integral"]
#            ----Саник----------------EveryMe----------------Noki--------------ONE1SIDE----------------Аква-------------
wlist = ['267297442318254090', '252438598081708033', '366340820049199105', '320596679394852866', '170467542907879425',
         '401449359247409152', '278286357334589440', '235996669013917698', '256887303450918912', '292797130249207808']
#           ----sevith-------------БУХАРИНЪ-----------непонятные_символы--------Нинтендо---------------4epB9lk----------
help_message = ("```Список команд: \n\n !t - список игроков сервера Technocracy\n !m - список игроков сервера Mageweave"
                "\n !a - список игроков сервера ArcaneFactory\n !s - список игроков сервера Spacecross \n !remove [числ"
                "о] - удалить данное количество сообщений \n !echo [сообщение] - сказать от имени бота данное сообщение"
                "\n !choice [один, два] - выбрать между несколькими аргументами \n !o - показать статистику серверов Dr"
                "eamfinity\n !cmds - вывести это сообщение\n © 2018 PIDORASSIMUS TEAM```")
bot_prefix = "!"
client = commands.Bot(command_prefix=bot_prefix)
client_token = environ.get('client_token', None)
PORT_arcane = environ.get('PORT_arcane', None)
PORT_techno = environ.get('PORT_techno', None)
PORT_magic = environ.get('PORT_magic', None)
PORT_space = environ.get('PORT_space', None)
package_1 = environ.get('package_1', None)
package_2 = environ.get('package_2', None)
Client = discord.Client()


async def get_online(ctx, port, server):
    info = None
    string = "\n"
    players_server = []
    reader, writer = await asyncio.open_connection(host='mc.dreamfinity.org', port=port)
    print(type(package_1, package_2)
    print(package_1, package_2)
    writer.write(package_1)
    writer.write(package_2)
    while not info:
        info = await reader.read(1024)
    online_players = findall(r'"online":(\w+)', str(info))
    online_players = int(online_players[0])
    writer.close()
    if 12 < online_players:
        await client.send_message(ctx.message.channel,
                                  embed=Embed(color=discord.Color.orange(), description="Сейчас может быть задержка!"))
    while len(players_server) < online_players:
        info = None
        reader, writer = await asyncio.open_connection(host='mc.dreamfinity.org', port=port)
        writer.write(package_1)
        sleep(0.5)
        writer.write(package_2)
        while not info:
            info = await reader.read(2048)
        info = str(info)
        writer.close()
        online_players = findall(r'"online":(\w+)', info)
        online_players = int(online_players[0])
        result_1 = findall(r'("id":"\w+-\w+-\w+-\w+-\w+","name":"\w+)', info)
        players_server += result_1
        players_server = list(set(result_1[:]))
    n = 1
    for p in players_server:
        k = len(p) - 51
        one = "{0}. {1} [{2}]".format(str(n), p[-k:], p[:43]).replace("id", "UUID").replace('"', "").replace("_", "\_")
        n += 1
        if one in dreamfinity_admins:
            one = "\n**{0}**".format(one)
        else:
            one = "\n{0}".format(one)
        string += one
    await client.send_message(ctx.message.channel,
                              "В данный момент на {2} **{0}** человек: {1}".format(online_players, string, server))


@client.event
async def on_ready():
    await client.change_presence(
        game=discord.Game(name="!cmds - команды", url="https://www.twitch.tv/dreamfinitycasts", type=1))


@client.command(name="echo", description="Написать от имени бота", pass_context=True)
async def echo(ctx, *, msg: str):
    # noinspection PyBroadException
    try:
        await client.delete_message(ctx.message)
        await client.send_message(ctx.message.channel, msg)
    except discord.Forbidden:
        await client.send_message(ctx.message.channel, msg)


@client.command(pass_context=True, description="Выбрать между несколькими аргументами")
async def choice(ctx, *, choices: str):
    choicesArr = choices.split(",")
    chosen = choicesArr[randrange(len(choicesArr))]
    await client.send_message(ctx.message.channel, ctx.message.author.mention + ", я выбираю `" + chosen + "`")


@client.command(pass_context=True)
async def cmds(ctx):
    await client.send_message(ctx.message.channel, help_message)


@client.command(pass_context=True, description="Удалить от 2 до 100 сообщений")
async def remove(ctx, number: str):
    # noinspection PyBroadException
    try:
        if not discord.Channel.permissions_for(ctx.message.channel, ctx.message.author).manage_messages and \
                        ctx.message.author.id not in wlist:
            await client.send_message(ctx.message.channel,
                                      embed=Embed(color=discord.Color.red(), description="В доступе - отказано!"))
            await client.add_reaction(ctx.message, "❎")
            return
        mgs = []
        number = int(number)
        async for x in client.logs_from(ctx.message.channel, limit=number):
            mgs.append(x)
        await client.delete_messages(mgs)
        await client.send_message(ctx.message.channel, ":heavy_check_mark: Было удалено {0} сообщений"
                                                       ".".format(str(number)))
    except discord.ClientException:
        await client.send_message(ctx.message.channel,
                                  embed=Embed(color=discord.Color.red(),
                                              description="Ошибка! Количество сообщений должно быть не меньше,"
                                              " чем 2 и не должно превышать 100"))
    except discord.Forbidden:
        await client.send_message(ctx.message.channel, embed=Embed(color=discord.Color.red(),
                                                                   description="Ошибка! У бота недостаточно прав"))
    except:
        await client.send_message(ctx.message.channel,
                                  embed=Embed(color=discord.Color.red(), description=str(exc_info()[0])))


@client.command(pass_context=True, description="Показать статистику серверов Dreamfinity")
async def o(ctx):
    # noinspection PyBroadException
    try:
        async with ClientSession() as session:
            async with session.get('http://dreamfinity.org/monAJAX/ajax.php') as resp:
                i = await resp.json()
                await client.send_message(ctx.message.channel, content="**Статистика состояния серверов Dreamfinity:**"
                                          "\n\n**Статус Technocracy**: {0}**   | Игроков**: {1} из {2}\n**Статус "
                                          "Mageweave**: {3} **    | Игроков**: {4} из {5}\n**Статус Spacecross**: {6}**"
                                          "      | Игроков**: {7} из {8}".format(i["servers"]["Technocracy"]["status"],
                                          str(i["servers"]["Technocracy"]["online"]),
                                          str(i["servers"]["Technocracy"]["slots"]),
                                          i["servers"]["Mageweave"]["status"], str(i["servers"]["Mageweave"]["online"]),
                                          str(i["servers"]["Mageweave"]["slots"]), i["servers"]["Spacecross"]["status"],
                                          str(i["servers"]["Spacecross"]["online"]),
                                          str(i["servers"]["Spacecross"]["slots"])))
    except:
        await client.send_message(ctx.message.channel,
                                  embed=Embed(color=discord.Color.red(), description="Нойра пидор, всё сломал " +
                                              str(exc_info()[0])))


@client.command(pass_context=True, description="Показать игроков ArcaneFactory")
async def a(ctx):
    await get_online(port=PORT_arcane, server="ArcaneFactory", ctx=ctx)


@client.command(pass_context=True, description="Показать игроков Technocracy")
async def t(ctx):
    await get_online(port=PORT_techno, server="Technocracy", ctx=ctx)


@client.command(pass_context=True, description="Показать игроков Mageweave")
async def m(ctx):
    await get_online(port=PORT_magic, server="Mageweave", ctx=ctx)


@client.command(pass_context=True, description="Показать игроков Spacecross")
async def s(ctx):
    await get_online(port=PORT_space, server="Spacecross", ctx=ctx)

client.run(client_token)
