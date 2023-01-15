import requests
import json
import os
import discord
import asyncio
import pyblox3
from pyblox3 import Users
from discord.ext import commands
from dotenv import load_dotenv
load_dotenv()




bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


importpeopleids = []
def botowners(ctx):
    return ctx.author.id in importpeopleids
apikey = os.getenv('apikey')
token = os.getenv('token')
idlist = os.getenv('idlist')
bottoken = os.getenv('bottoken')
webhook = os.getenv('webhook')





@bot.listen('on_ready')
async def on_ready():

    print(f'bot online- {bot.user} - {bot.user.id}')
    for s in bot.guilds:
      print(f'Guild - {s} - {s.id}')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=" Idiots get banned, "))
      

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------



def sendlog(msg):
    json = {
        "content": msg,
        "embeds": None,
        "attachments": []
    }
    requests.post(webhook, json=json)






def getuser(userid):
  r = requests.get(f'https://users.roblox.com/v1/users/{userid}')
  response = r.json()
  plrusername = response["name"]
  print(plrusername)




@bot.command()
#@commands.has_role()
async def ban(ctx, user,*, reason=None):

    if reason == None:
      try:
        plrdata1 = Users.User(user)
        plrid1 = str(plrdata1.Id)
        plrusernamefunc = plrid1
        await ctx.send(f'{ctx.author} reason for banning {plrusernamefunc} (30 seconds to reply)')
      except:
        await ctx.send(f'{ctx.author} reason for banning {user} (30 seconds to reply)')

    def check(m):
        return m.channel == ctx.channel
    try:
      msg = await bot.wait_for('message', timeout=30, check=check)
    except:
      return await ctx.send('You either have typing issues or didnt say anything, aborting....')
    if msg.content == 'cancel'.lower():
      return await ctx.send('aborting...')
    reason=msg.content


    if user in ['P4IGER', 'KKTrendy', '4158901433', '1622425024']:
      return await ctx.send('no')

    if user.isnumeric():
      opuser = getuser(user)
      print('User id')
    else:
      plrdata = Users.User(user)
      plrid = str(plrdata.Id)
      user = plrid


    url = "https://api.trello.com/1/cards"

    headers = {
      "Accept": "application/json"
    }

    query = {
      'idList': idlist,
      'key': apikey,
      'token': token
    }

    response = requests.request(
      "POST",
      url,
      headers=headers,
      params=query
    )

    a = response.json()
    this = a['shortLink']


    url = f"https://api.trello.com/1/cards/{this}"
    query = {'key': apikey, 'token': token}
    payload = {'name': user}
    response = requests.request("PUT", url, params=query, data=payload)

    try:
      plrdata1 = Users.User(user)
      plrid1 = str(plrdata1.Id)
      plrusernamefunc = plrid1
      await ctx.send(f'```\nBANNED ({ctx.author}): {plrusernamefunc} | reason: {reason}```')
    except:
      await ctx.send(f'```\nBANNED ({ctx.author}): {user} | reason: {reason}```')

    print(f'Banned id: `{user}` with key `{this}` , {reason}')
    try:
      sendlog(f'Banned id: `{plrusernamefunc}` with key `{this}` - Reason: `{reason}`')
    except:
      sendlog(f'Banned id: `{user}` with key `{this}` - Reason: `{reason}`')
    await ctx.message.add_reaction('\N{WHITE HEAVY CHECK MARK}')





@bot.command()
#@commands.has_role()
async def unban(ctx, trelloident,*, reason=None):
  if reason==None:
    if trelloident.isnumeric():
      return await ctx.send(f'Thats no where near a key')
    else:
      await ctx.send(f'{ctx.author} reason for unbanning {trelloident} (30 seconds to respond)')

  def check(m):
      return m.channel == ctx.channel
  try:
    msg = await bot.wait_for('message', timeout=30, check=check)
  except:
    return await ctx.send('You either have typing issues or didnt say anything, aborting....')
  if msg.content == 'cancel':
    return await ctx.send('aborting...')
  reason=msg.content

  url = f"https://api.trello.com/1/cards/{trelloident}"

  query = {
    'key': apikey,
    'token': token
  }

  response = requests.request(
    "DELETE",
    url,
    params=query
  )
  
  chan = await bot.fetch_channel(1061583083863814266)
  #await chan.send(f'`Unbanned key `{trelloident}` for reason: `{reason}`')
  await ctx.send(f'```\nUN-BANNED ({ctx.author}): {trelloident} | reason: {reason}```')
  await ctx.message.add_reaction('\N{WHITE HEAVY CHECK MARK}')




@bot.command(aliases=['e', 'evaluate'])
@commands.check(botowners)
async def eval(ctx, *, code):
    """Evaluates customized code"""
    language_specifiers = ["python", "py", "javascript", "js", "html", "css", "php", "md", "markdown", "go", "golang", "c", "c++", "cpp", "c#", "cs", "csharp", "java", "ruby", "rb", "coffee-script", "coffeescript", "coffee", "bash", "shell", "sh", "json", "http", "pascal", "perl", "rust", "sql", "swift", "vim", "xml", "yaml"]
    loops = 0
    while code.startswith("`"):
        code = "".join(list(code)[1:])
        loops += 1
        if loops == 3:
            loops = 0
            break
    for language_specifier in language_specifiers:
        if code.startswith(language_specifier):
            code = code.lstrip(language_specifier)
    try:
        while code.endswith("`"):
            code = "".join(list(code)[0:-1])
            loops += 1
            if loops == 3:
                break
        code = "\n".join(f"    {i}" for i in code.splitlines())
        code = f"async def eval_expr():\n{code}"
        def send(text):
            bot.loop.create_task(ctx.send(text))
        env = {
            "bot": bot,
            "client": bot,
            "ctx": ctx,
            "print": send,
            "_author": ctx.author,
            "_message": ctx.message,
            "_channel": ctx.channel,
            "_guild": ctx.guild,
            "_me": ctx.me
        }
        env.update(globals())
        exec(code, env)
        eval_expr = env["eval_expr"]
        result = await eval_expr()
        await ctx.message.add_reaction("\N{WHITE HEAVY CHECK MARK}")
        if result:
            await ctx.send(result)
    except Exception as learntofuckingcode:
        await ctx.message.add_reaction("\N{WARNING SIGN}")
        await ctx.send(f'**Error**```py\n{learntofuckingcode}```')



bot.run(bottoken)