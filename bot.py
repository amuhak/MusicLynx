#getting tokens
import os
from dotenv import load_dotenv

#getting yt audio and searching youtube
import yt_dlp
from youtube_search import YoutubeSearch

#regex
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

#functional
import asyncio
import random
import typing

#genius client
from lyricsgenius import Genius

#spotify client
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

#meme
import requests
import urllib

#Getting tokens
load_dotenv()
TOKEN = os.environ.get('TOKEN')
client_id = os.environ.get('client_id')
client_secret = os.environ.get('client_secret')
genius_token = os.environ.get('genius_token')

#discord client imports
import discord
from discord.ext import commands
from discord import app_commands
from discord.utils import get
from discord import FFmpegPCMAudio
from discord import TextChannel
from typing import List
from typing import Optional

#Setting up discord client
intents = discord.Intents.all()
client = discord.Client(intents = intents)
activity = discord.Game(name="Music", type=discord.ActivityType.playing)
bot = commands.Bot(command_prefix='!', intents = intents, activity=activity)
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
#DISCORD

#setting up spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

#setting up genius client
genius = Genius(genius_token)
skip = False

#run when bot is ready
@bot.event
async def on_ready():
    #log to console
    print("Lynx online")
    try:
        #sync application commands
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)

#setting up imgflip for /meme
username = 'MusicLynx'
password = os.environ.get('imgflip')
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) \ AppleWebKit/537.36 (KHTML, like Gecko) \ Chrome/120.0.0.0 Safari/537.36"

data = requests.get('https://api.imgflip.com/get_memes').json()['data']['memes']
images = [{'name':image['name'],'url':image['url'],'id':image['id']} for image in data]
meme_names = []
for image in images:
     meme_names.append(image['name'])

#get command help
@bot.tree.command(name = "lynx_help")
async def help(interaction: discord.Interaction):
     await interaction.response.send_message(f"""
**Disclaimer**: the player disconnects frequently from YT's end, so there's little i can do to fix that. sorry.
`/link` links to a song.
`/join` you have to get the bot to join a voice channel before it can play. if it's having errors, always try to run this first.
`/play song:` plays the song you enter. ideal format: [artist] [song] [explicit/clean]. queues song if something's already playing.
`/queue action:[clear/view]` prints or clears the queue.
`/resume` resumes playing song.
`/pause` pauses song.
`/skip` skips song.
`/stop` stops playing and leaves the vc.\n
`!sing` sends the lyrics of the song you enter one-by-one. use carefully, or you might get banned :D
`!shout` SHOUTS the lyrics of the song you enter one-by-one. use carefully, or you might get banned :D
`!stop_lyrics` stops sending lyrics.
`!time` adjusts the time between each line\n
`!preach` spits straight facts.
`!nerd user` when someone is being far too much of a nerd, nerd them.
`/doggo` summons a random doggo pic.
`/8ball` answers questions by harnessing the peak reasoning abilities of a UGA student.\n
`/bradley_hate` disables/enables the bradley-hate features if you have perms.\n
`!updates` gets the latest updates and new features!\n
pls use me responsibly.
""")
     
fax = ["CS majors should get free deodorant", "It's not immoral if you make six figures", "To Hell With Georgia",
       "I don't talk to UGA grads often, but when I do, I ask for large fries", "MIT is GT of the North", "Touch grass, buddy", 
       "mods are nepo smh", "The art and the artist are separate", "Dobby is a free elf", "PJO >>", "The laws of physics don't apply to SRK", 
       "The 'clay' in 'Mlepclaynos' is silent", "You heard about Pluto? That's messed up right?", "You the king, burger king", 
       "I have two rules. Rule one: I'm always right. Rule two: If I'm wrong, refer to rule one…",
       "I just love the smell of C4 in the morning.", "It smell like gaaas, I think somebody poo", "I take my shirt off and all the hoes stop breathin'",
       "Deutschland > France", "SLATT", "Fuck UGA ong", "Fuck UGA ong", "Fuck UGA ong", "Fuck UGA", "Fuck UGA", "GT>>", "GT>>",
       "Pickup trucks are for idiots", "Bhupendra Jogi", "The best racism is Formula 1", "Lewis Hamilton is the greatest racist of all time",
       "Messi is the :goat:", "Messi > Ronaldo", "LeBron is my pookie", "LeBron GOAT", "Real football is played with the feet", "American Eggball != Football",
       "Lucas Luwa teaches CS1331", "Georgia _ech is _he bes_ ", "OJ is innocent- orange juice can't commit crimes", "ತೆಲುಗು ವಿಚಿತ್ರ ಭಾಷೆ ಫ್ರ",
       "OO is a myth.", "It's pronounced 'Chad' Starner", "you = :nerd:", ":nerd:", "you = :nerd:", ":moyai:", ":moyai:",
       "I'm really happy for you, Imma let you finish, but Beyoncé had one of the best videos of all time!", "Man U will always be dogshit", "Barca > Madrid",
       "Bayern cheat", "Animal testing is a crime", "Math majors have no life purpose" , "The existence of Ivan Allen is a myth", "East Campus is better",
       "Willage is overrated", "Coffee is a performance drug\nPerformance drugs are the best!", "Willage is overrated", "Everyone secretly wishes they were in CS",
       "OOS students worked harder to get here ¯\_(ツ)_/¯", "Georgia > Florida", "Bigotry is **not** cool", "If I get bleach on my t-shirt, Imma feel like an asshole",
       "992 > 991", "Macans are not Porsches", "SUVs are dumb", "SAT > ACT"]

#utility function to get urls from search term
def get_links(query):
     #spotify

     results = sp.search(q=query, type="track", limit=1)
     #basic conditional to handle search failure
     if results["tracks"]["items"]:
          spotify_url = results["tracks"]["items"][0]["external_urls"]["spotify"]
     else:
          raise Exception("Search Failed!")

     #genius
     hits = genius.search_songs(query)
     #if the search is successful, this'll get changed later
     genius_song = "Genius Search Failed"
     hits = hits["hits"]

     #making sure that the two results match closely. genius search can be weird.
     try:
          for hit in hits:
               genius_title = hit['result']['title']
               spotify_title = results['tracks']['items'][0]['name']
               if fuzz.ratio(str(genius_title), str(spotify_title)) > 60:
                         genius_song = hit
                         break
          genius_url = genius_song['result']['url']
     except Exception as e:
          print(e)
          genius_url = "genius search failed, sry"
     
     #return the genius url, the spotify url, and the genius song object
     return genius_url, spotify_url, genius_song

#get links to a song query
@bot.tree.command(name = "link")
@app_commands.describe(song = "I'll link to this song!")
async def link(interaction: discord.Interaction, song: str):
    genius_link, spotify_link, _ignore = get_links(song)
    await interaction.response.send_message(f"Genius: {genius_link}\nSpotify: {spotify_link}")

#get top url for a query in YT
def get_top_result_url(query):
     results = YoutubeSearch((query + " audio"), max_results=10).to_dict()
     top_result_url = 'https://music.youtube.com' + results[0]['url_suffix']
     return {'url' : top_result_url, 'title' : results[0]['title'], 'thumbnail' : results[0]['thumbnails'][0]}

# command for bot to join the channel of the user, if the bot has already joined and is in a different channel, it will move to the channel the user is in
@bot.tree.command(name = "join")
async def join(interaction: discord.Interaction):
     try:
          channel = interaction.user.voice.channel
          voice = get(bot.voice_clients, guild=interaction.guild)
          if voice and voice.is_connected():
               await voice.move_to(channel)
          else:
               voice = await channel.connect()
          await interaction.response.send_message("joined channel.")
     except:
          await interaction.response.send_message("you might have to join a vc first.")

queue = {}
queue_info = {}
nerded = {}

# command to play sound from a youtube URL
@bot.tree.command(name = "play")
@app_commands.describe(song = "I'll play this song")
async def play(interaction: discord.Interaction, song: str):
     global queue
     #the search takes a while, so the response is deferred to make sure the interaction doesn't time out
     await interaction.response.defer()

     #setting options
     YDL_OPTIONS = {
        'format': 'bestaudio/best',
        'extractaudio': True,
        'audioformat': 'mp3',
        'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'logtostderr': False,
        'quiet': True,
        'no_warnings': True,
        'default_search': 'auto',
        'source_address': '0.0.0.0',
    }
     FFMPEG_OPTIONS = {
          'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

     #getting the vc object
     voice = get(bot.voice_clients, guild=interaction.guild)

     #kinda useless code
     if interaction.guild.id not in queue:
          queue[interaction.guild.id] = []
          queue_info[interaction.guild.id] = []
     if song == "skip":
      if len(queue[interaction.guild.id]) == 0:
        await interaction.followup.send("queue complete")
     queue[interaction.guild.id].append(song)
     queue_info[interaction.guild.id].append(interaction.user.id)
     
     #try-catch to handle vc errors and whatnot
     try:
          yt = get_top_result_url(song)
          song_url = yt["url"]
          embed = discord.Embed(title = yt['title'], url = song_url, description = 'Song added to queue')
          embed.set_author(name = f"queued by {interaction.user.display_name}", icon_url=interaction.user.display_avatar)
          embed.set_image(url = yt['thumbnail'])
          #making sure the bot isn't already playing
          if (not voice.is_playing()) or (len(queue[interaction.guild.id])<1):
               song = queue[interaction.guild.id].pop(0)
               yt = get_top_result_url(song)
               song_url = yt["url"]
               embed = discord.Embed(title = yt['title'], url = song_url, description = 'Song playing now')
               embed.set_author(name = f"played by {interaction.user.display_name}", icon_url=interaction.user.display_avatar)
               embed.set_image(url = yt['thumbnail'])
               with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                    info = ydl.extract_info(song_url, download=False)
                    url2 = info['url']
               # Play the audio stream
               voice.is_playing()
               id = interaction.guild.id
               voice.play(discord.FFmpegPCMAudio(url2,before_options=FFMPEG_OPTIONS), after = lambda e: play_recur(voice, (queue[id].pop(0)), id))
               await interaction.followup.send(f"playing now", embed=embed)
               # check if the bot is already playing
          else:
               #a little message to the user
               await interaction.followup.send(f"added to queue", embed=embed)
               return
     except Exception as e:
          #doesn't work great without this block for some reason
          print(e)
          try:
               await interaction.followup.send("there might have been an error. wait for a couple of secs and try again.\nmake sure you ran /join.")
          except:
               await interaction.followup.send(f"playing now\n{song_url}")

@bot.tree.command(name = "queue")
@app_commands.choices(action=[
     app_commands.Choice(name="View", value="view"),
     app_commands.Choice(name="Clear", value="clear"),
])
async def get_queue(interaction: discord.Interaction, action: app_commands.Choice[str]):
     global queue
     global queue_info
     await interaction.response.defer()
     if action == "clear":
          queue[interaction.guild.id] = []
          await interaction.followup.send("queue cleared!")
     else:
          song_titles = []
          for i, song in enumerate(queue[interaction.guild.id]):
               results = YoutubeSearch((song + " audio"), max_results=10).to_dict()
               title = results[0]['title']
               user_id = queue_info[interaction.guild.id][i]
               song_titles.append(f"{i+1}) **{title}**- added by <@{user_id}>")
          song_titles = "\n".join(song_titles)
          await interaction.followup.send(song_titles)

#recurring command to play from queue
def play_recur(voice, song, id):
     print(song)
     url = get_top_result_url(song)["url"]
     YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist': 'True'}
     FFMPEG_OPTIONS = {
          'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'}
     with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
          info = ydl.extract_info(url, download=False)
          url2 = info['url']
     # Play the audio stream
     voice.is_playing()
     try:
          voice.play(discord.FFmpegPCMAudio(url2,before_options=FFMPEG_OPTIONS), after = lambda e: play_recur(voice, queue[id].pop(0), id))
     except:
          pass

# command to resume voice if it is paused
@bot.tree.command(name = "resume")
async def resume(interaction: discord.Interaction):
     voice = get(bot.voice_clients, guild=interaction.guild)
     try:
          if not voice.is_playing():
               await voice.resume()
               await interaction.response.send_message("cool, i'll resume")
     except:
          await interaction.response.send_message("cool, i'll resume")


# command to pause voice if it is playing
@bot.tree.command(name = "pause")
async def pause(interaction: discord.Interaction):
     voice = get(bot.voice_clients, guild=interaction.guild)
     try:
          if voice.is_playing():
               await voice.pause()
               await interaction.response.send_message('aight, paused')
     except:
          await interaction.response.send_message("aight, paused")


# command to stop voice
@bot.tree.command(name = "stop")
async def stop(interaction: discord.Interaction):
     voice = get(bot.voice_clients, guild=interaction.guild)
     try:
          await voice.disconnect()
          await interaction.response.send_message("stopping and disconnecting...")
     except:
          await interaction.response.send_message("error. the bot might not be in a vc")

#command to skip song
#yet to implement voteskip
@bot.tree.command(name = "skip")
async def skip(interaction: discord.Interaction):
     global queue
     voice = get(bot.voice_clients, guild=interaction.guild)
     try:
          await voice.stop()
          play_recur(voice, queue[interaction.guild.id].pop(0))
          await interaction.response.send_message("skipped")
     except:
          await interaction.response.send_message("skipped")

#fun

@bot.tree.command(name = "8ball")
@app_commands.describe(question = "I'll answer this question")
async def skip(interaction: discord.Interaction, question: str):

     await interaction.response.defer()

     answer = random.choice(["It is certain", "Reply hazy, try again", "Don’t count on it", "It is decidedly so", "Ask again later", 
                             "My reply is no", "Without a doubt", "Better not tell you now", "My sources say no", "Yes definitely", 
                             "Cannot predict now", "Outlook not so good", "You may rely on it", "Concentrate and ask again", 
                             "Very doubtful", "As I see it, yes", "Most likely", "Outlook good", "Yes", "Signs point to yes"])
     await asyncio.sleep(3)
     
     await interaction.followup.send(f"**Magic 8-ball**\nQuestion: `{question}`\nMagic 8-ball's Answer: `{answer}`")

@bot.tree.command(name = "meme")
@app_commands.describe(template = "Template to use", line1 = "First line of meme", line2 = "Second line of meme", line3 = "Optional third line", line4 = "Optional fourth line")
async def meme(interaction: discord.Interaction, template : str, line1 : str, line2 : str, line3 : str = None, line4 : str = None):
     await interaction.response.defer()
     URL = 'https://api.imgflip.com/caption_image'
     id = meme_names.index(template)
     boxes = [{"text":line1},{"text":line2},{"text":line3},{"text":line4}]
     params = {
     'username':username,
     'password':password,
     'template_id':images[id]['id'],
     "boxes[0][text]": line1,
     "boxes[1][text]": line2,
     "boxes[2][text]": line3,
     "boxes[3][text]": line4,
     }
     response = requests.request('POST',URL,params=params).json()
     opener = urllib.request.URLopener()
     opener.addheader('User-Agent', user_agent)
     try:
          filename, headers = opener.retrieve(response['data']['url'], 'meme.jpg')
     except Exception as e:
          print(e)
     with open('meme.jpg','rb') as img:
          picture = discord.File(img)
          await interaction.followup.send(f"made by <@{interaction.user.id}>",file = picture)

@meme.autocomplete("template")
async def template_autocomplete(interaction: discord.Interaction, current: str) -> typing.List[app_commands.Choice[str]]:
     data = []
     for template_choice in meme_names:
          if current.lower() in template_choice.lower():
               data.append(app_commands.Choice(name = template_choice, value = template_choice))
     return data

#show meme templates
@bot.tree.command(name = "meme_templates")
async def list_templates(interaction : discord.Interaction):
     template_names = "\n".join(meme_names)
     await interaction.response.send_message(f"# Templates\n{template_names}", ephemeral=True)


#send a random photo of a dog
doggo_credits = [("Meru", 799447829856780289), ("Meru", 799447829856780289), ("Meru", 799447829856780289)]
@bot.tree.command(name = "doggo")
async def skip(interaction: discord.Interaction):
     rand = random.randint(1,4)
     with open(f'dog{rand}.png', 'rb') as img:
          picture = discord.File(img)
          await interaction.response.send_message(f"{doggo_credits[rand-1][0]}, <@{doggo_credits[rand-1][1]}>'s doggo.", file=picture)

#SINGING FUNCTIONALITY#
 
#Setting default varables
singing = False
current_line = ""
time = float(8)
skipped = False

#Find a song's lyrics
def find_song(song_in):
     #using the get_links to simplify code
     url = get_links(song_in)[0]
     #retrieving the genius song object
     genius_song = get_links(song_in)[2]

     #handling a search failure from get_links
     if genius_song == "Genius Search Failed":
          lines, title = ["search failed"], "sorry"
          return(lines, title)
     else:
          #getting the lyrics
          song_lyrics = genius.lyrics(song_url=url)
          #cleaning the lyrics
          lines = clean(song_lyrics)
          #getting the title
          title = genius_song['result']['title']
          return(lines, title)

#Clean a song
def clean(lyrics):
     #getting line breaks when there are ad-libs
     lyrics = lyrics.replace("(","\n(")
     lyrics = lyrics.replace(")",")\n")

     #splitting lines
     lyrics = lyrics.split("\n")

     #creating a new list to save lyrics over to
     return_lyrics = []
     for line in lyrics:
          #if it has a square bracket, it's not actually a lyrics
          if "[" not in line:
               #getting rid of the bits that aren't lyrics
               if "Embed" in line:
                    line = line.replace("Embed","")
                    ine = ''.join((x for x in line if not x.isdigit()))
               if "contributor" in line.lower():
                    continue
               #i don't have an n-word pass
               if "nigga" in line.lower():
                    line = line.replace("Nigga", "Ni**a")
                    line = line.replace("nigga", "ni**ga")
               return_lyrics.append(line)
        
     return return_lyrics

bradley_hate = False

@bot.tree.command(name = "bradley_hate")
@app_commands.choices(choices=[
     app_commands.Choice(name="Disable", value="disable"),
     app_commands.Choice(name="Enable", value="enable"),
])
async def control_bradley_hate(interaction: discord.Interaction, choices: app_commands.Choice[str]):
     global bradley_hate
     global fax
     authorized = [286225309773070336, 799447829856780289, 651632296440365087, 694310264295915560, 549393343583485962, 946196592074031165]
     if interaction.user.id in authorized:
          if choices.value == "enable":
               bradley_hate = True
               await interaction.response.send_message("Bradley hate set to `enabled`")
               fax.extend(("Bradley is a loser", "Bradley is a loser", "Bradley is a loser", "Bradley is a loser"))
          else:
               await interaction.response.send_message("Bradley hate set to `disabled`")
               if bradley_hate:
                    fax = fax[0:len(fax)-4]
               bradley_hate = False
     else:
          await interaction.response.send_message("you don't have the perms for that buddy")

#checking if the next line should skipping
@bot.event
async def on_message(message):
     global bradley_hate

     #line-skipping
     global current_line
     global skip
     if not message.author.bot:
          if fuzz.ratio(message.content, current_line) > 50:
               skip = True
               #logging the skip to console
               print(f"Skipping!: '{message.content}' as '{current_line}'")

     #checking if the sender of a message has been "nerded"
     if message.author.id in nerded:
          #incrementing number of messages sent while nerded
          nerded[message.author.id] += 1
          #adding reaction
          await message.add_reaction("🤓")
          #rremoving from nerd directory if the 4 messages have already been reacted to
          if nerded[message.author.id] >= 2:
               del nerded[message.author.id]
     
     #responding to pings
     mention = f'<@{1196931379129241600}>'
     if mention in message.content:
          remark = random.choice(["wassup?", "you called?", "ayyy, what's good?", "yo", ":moyai:", "ay yo", "aiyyooo... why ping me", "yeah?"])
          await message.reply(f'{remark} use /lynx_help to get to know me better.')

     #bradley hate
     if bradley_hate:
          insult = random.randint(0,2)
          message_core = message.content.lower().strip()
          if (("bradley" in message_core) or ("🅱️radley" in message_core) or ("🇧 radley" in message_core ) or ("748540576651280454" in message_core)) and (not message.author.bot) and (insult != 2):
               await message.reply(random.choice(["Bradley? lol, what a loser","Bradley? lol, what a loser","lmao bradley L","don't summon bradley, he'll start talking about rust or something",
                                                  "bradley hate is the best hate","bradley? that guy's a bozo","Bradley? lol what a doofus"]))
     await bot.process_commands(message)

@bot.command(name = "sing", help = "Sings songs!")
async def sing(ctx, *, song_name):
     global singing
     global current_line
     global skip
     global skipped
     global time

     if singing:
          await ctx.send("i'm alr singing smh. you haven't even told me to stop yet")

     singing = True
    
     #"""
     print("singing now")
     try:
          lines, title = find_song(song_name)
     except:
          await ctx.send("sorry, I had trouble pulling that up. pls try again")

     await ctx.send(title+":")
     for line in lines:

          #Updating current line
          current_line = line

          #Waiting for 8 seconds while typing if a line hasn't already been skipped
          if (not skipped) and singing:
               async with ctx.typing():
                    await asyncio.sleep(time)
          skipped = False

          if (not skip) and singing:
               skip = False
               if line != "":
                    await ctx.send(f"🗣️{line}")
               if not singing:
                    break
          elif skip:
               print("Skipped!")
               skipped = True
               skip = False
               continue
          else:
               break
     singing = False
     #"""

@bot.command(name = "shout", help = "SHOUTS songs!")
async def shout(ctx, *, song_name):
     global singing
     global current_line
     global skip
     global skipped
     global time

     if singing:
          await ctx.send("i'm alr singing smh. you haven't even told me to stop yet")

     singing = True
    
     #"""
     print("singing now")
     while True:
          try:
               lines, title = find_song(song_name)
               break
          except:
               await ctx.send("sorry, I had trouble pulling that up. lemme try again")
               continue

     await ctx.send(title+":")
     for line in lines:

          #Updating current line
          current_line = line

          #Waiting for 8 seconds while typing if a line hasn't already been skipped
          if (not skipped) and singing:
               async with ctx.typing():
                    await asyncio.sleep(time)
          skipped = False

          if (not skip) and singing:
               skip = False
               if line != "":
                    await ctx.send(f"🗣️{line}")
               if not singing:
                    break
          elif skip:
               print("Skipped!")
               skipped = True
               skip = False
               continue
          else:
               break
     singing = False
     #"""

@bot.command(name = "time")
async def time_set(ctx, time_in):
     global time
     try:
          time = float(time_in.strip())
          await ctx.send(f"ok. time interval set to {time}s")
     except:
          await ctx.send(f"bruh idk what you mean by '{time_in}'.")

@bot.command(name = "stop_lyrics")
async def stop_lyrics(ctx):
     global singing
     singing = False
     await ctx.send("ok. I'll stop 😕")

@bot.command(name = "preach")
async def preach(ctx):
     global fax
     await ctx.send(random.choice(fax))

#send reaction when bean
@bot.command(name = "bean")
async def bean_lynx(ctx):
     await ctx.send(random.choice(["bruh why bean","get beaned lol"]))

#send reaction when ben
@bot.command(name = "ban")
async def ban_lynx(ctx):
     await ctx.send("🙀")

#command to nerd someone
@bot.command(name = "nerd")
async def nerd(ctx, member: discord.Member):
     #global dictionary of people who have been "nerded"
     global nerded
     #initializing how many messages they have sent while nerded
     if (member.id == 799447829856780289):
          nerded[ctx.author.id] = 0
          await ctx.send(f"# <@{ctx.author.id}> = :nerd:\nlmao get nerded noob")
     elif (member.id == 1196931379129241600):
          await ctx.send("you dare use my own spells against me?")
     else:
          nerded[member.id] = 0
          await ctx.send(f"# <@{member.id}> = :nerd:")

@bot.command(name = "aarush")
async def aarush(ctx):
     server_members = ctx.guild.members
     tags = []
     for member in server_members:
          if "aarush" in (member.display_name.strip()).lower():
               tags.append(member.id)
     chosen_aarush = random.choice(tags)
     await ctx.send(f"an aarush -> <@{chosen_aarush}>")

@bot.command(name = "updates")
async def updates_message(ctx):
     updates_str = ("""**Update 3.0! by <@799447829856780289>**\n
Added `!aarush`, which randomly pings an aarush from the server.
Added `/skip`, which enables skipping a currently playing a song.
Added `/bradley_hate` which allows mods and my creator to disable or enable the Bradley-hating features. They will be disabled by default from now on :(
Added `/8ball` which replicates the peak logical prowess of a UGA student to help you make decisions.
Added `/doggo` which posts a random pic of a doggo! Pls share yours.
Added a placeholder function for `\meme`. in the future, this command will allow you to generate your own memes!
""")
     await ctx.send(updates_str)
     
bot.run(TOKEN)
