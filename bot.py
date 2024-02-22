# getting tokens
import os
from dotenv import load_dotenv

# getting yt audio and searching youtube
import yt_dlp
from youtube_search import YoutubeSearch

# regex
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

import json

# functional
import asyncio
import random
import typing
from io import BytesIO
from datetime import datetime

# genius client
from lyricsgenius import Genius

# spotify client
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# meme
import requests
import urllib

# Getting tokens
load_dotenv()
TOKEN = os.environ.get('TOKEN')
client_id = os.environ.get('client_id')
client_secret = os.environ.get('client_secret')
genius_token = os.environ.get('genius_token')
flieger_token = os.environ.get('flieger_token')

# discord client imports
import discord
from discord.ext import commands
from discord import app_commands
from discord.utils import get
from discord import FFmpegPCMAudio
from discord import TextChannel
from typing import List
from typing import Optional

# Setting up discord client
intents = discord.Intents.all()
client = discord.Client(intents=intents)
activity = discord.Game(name="Music", type=discord.ActivityType.playing)
bot = commands.Bot(command_prefix='!', intents=intents, activity=activity)
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
# DISCORD

# setting up spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# setting up genius client
genius = Genius(genius_token)
skip = False

logging = {}
ping_info = {}


# run when bot is ready
@bot.event
async def on_ready():
    global logging
    # log to console
    print("Lynx online")
    try:
        # sync application commands
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as e:
        print(e)
    try:
        with open("logginginfo.json", "r") as read_file:
            global logging
            logging = json.load(read_file)
            for info in logging:
                logging[info]["log"]

                # logging[info]["logging_channel"] = logging[info]["logging_channel"].replace("#","")
                # logging[info]["logging_channel"] = logging[info]["logging_channel"].replace("<","")
                # logging[info]["logging_channel"] = logging[info]["logging_channel"].replace(">","")

                logging[info]["logging_channel"] = int(logging[info]["logging_channel"])
    except Exception as e:
        print("logging file empty", e)
    try:
        with open("pinginfo.json", "r") as read_file:
            global ping_info
            ping_info = json.load(read_file)
        to_delete = []
        for word in ping_info:
            if ping_info[word] == None:
                to_delete.append(word)
        for delete in to_delete:
            del ping_info[delete]
    except Exception as e:
        print("ping file empty", e)


# setting up imgflip for /meme
username = 'MusicLynx'
password = os.environ.get('imgflip')
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) \ AppleWebKit/537.36 (KHTML, like Gecko) \ Chrome/120.0.0.0 Safari/537.36"

data = requests.get('https://api.imgflip.com/get_memes').json()['data']['memes']
images = [{'name': image['name'], 'url': image['url'], 'id': image['id']} for image in data]
meme_names = []
for image in images:
    meme_names.append(image['name'])


# get command help
@bot.tree.command(name="lynx_help", description="lists the bot's commands")
async def lynx_help(interaction: discord.Interaction):
    await interaction.response.send_message(f"""
**Disclaimer**: the player disconnects frequently from YT's end, so there's little i can do to fix that. sorry.
`/link [song]` links to a song.
`/join` you have to get the bot to join a voice channel before it can play. if it's having errors, always try to run this first.
`/play [song]` plays the song you enter. ideal format: [artist] [song] [explicit/clean]. queues song if something's already playing.
`/queue [clear/view]` prints or clears the queue.
`/resume` resumes playing song.
`/pause` pauses song.
`/skip` skips song.
`/stop` stops playing and leaves the vc.\n
`!sing` sends the lyrics of the song you enter one-by-one. use carefully, or you might get banned :D
`!shout` SHOUTS the lyrics of the song you enter one-by-one. use carefully, or you might get banned :D
`!stop` stops sending lyrics.
`!time` adjusts the time between each line\n
`!preach` spits straight facts.
`!rickroll` rickrolls.
`!hype` sends GT hype.
`!nerd user` when someone is being far too much of a nerd, nerd them.
`/doggo` summons a random doggo pic.
`/8ball [question]` answers questions by harnessing the peak reasoning abilities of a UGA student.
`/meme [template] [public] [line1] [line2] [line3 (opt.)] [line4 (opt.)]` generates meme\n

if you want to delete a reply i sent to your message, react with 🗑️
pls use me responsibly.
""", ephemeral=True)


fax = ["CS majors should get free deodorant", "It's not immoral if you make six figures", "To Hell With Georgia",
       "I don't talk to UGA grads often, but when I do, I ask for large fries", "MIT is GT of the North",
       "Touch grass, buddy",
       "mods are nepo smh", "The art and the artist are separate", "Dobby is a free elf", "PJO >>",
       "The laws of physics don't apply to SRK",
       "The 'clay' in 'Mlepclaynos' is silent", "You heard about Pluto? That's messed up right?",
       "You the king, burger king",
       "I have two rules. Rule one: I'm always right. Rule two: If I'm wrong, refer to rule one…",
       "I just love the smell of C4 in the morning.", "It smell like gaaas, I think somebody poo",
       "I take my shirt off and all the hoes stop breathin'",
       "Deutschland > France", "SLATT", "Fuck UGA ong", "Fuck UGA ong", "Fuck UGA ong", "Fuck UGA", "Fuck UGA", "GT>>",
       "GT>>",
       "Pickup trucks are for idiots", "Bhupendra Jogi", "The best racism is Formula 1",
       "Lewis Hamilton is the greatest racist of all time",
       "Messi is the :goat:", "Messi > Ronaldo", "LeBron is my pookie", "LeBron GOAT",
       "Real football is played with the feet", "American Eggball != Football",
       "Lucas Luwa teaches CS1331", "Georgia _ech is _he bes_ ", "OJ is innocent- orange juice can't commit crimes",
       "The Superbowl was scripted",
       "OO is a myth.", "It's pronounced 'Chad' Starner", "you = :nerd:", ":nerd:", "you = :nerd:", ":moyai:",
       ":moyai:",
       "I'm really happy for you, Imma let you finish, but Beyoncé had one of the best videos of all time!",
       "Man U will always be dogshit", "Barca > Madrid",
       "Bayern cheat", "Animal testing is a crime", "Math majors have no life purpose",
       "The existence of Ivan Allen is a myth", "East Campus is better",
       "Willage is overrated", "Coffee is a performance drug\nPerformance drugs are the best!", "Willage is overrated",
       "Everyone secretly wishes they were in CS",
       "OOS students worked harder to get here ¯\_(ツ)_/¯", "Georgia > Florida", "Bigotry is **not** cool",
       "If I get bleach on my t-shirt, Imma feel like an asshole",
       "992 > 991", "Macans are not Porsches", "SUVs are dumb", "SAT > ACT"]


# utility function to get urls from search term
def get_links(query):
    # spotify

    results = sp.search(q=query, type="track", limit=1)
    # basic conditional to handle search failure
    if results["tracks"]["items"]:
        spotify_url = results["tracks"]["items"][0]["external_urls"]["spotify"]
    else:
        raise Exception("Search Failed!")

    # genius
    hits = genius.search_songs(query)
    # if the search is successful, this'll get changed later
    genius_song = "Genius Search Failed"
    hits = hits["hits"]

    # making sure that the two results match closely. genius search can be weird.
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

    # return the genius url, the spotify url, and the genius song object
    return genius_url, spotify_url, genius_song


# get links to a song query
@bot.tree.command(name="link", description="links to the song given in the query")
@app_commands.describe(song="I'll link to this song!")
async def link(interaction: discord.Interaction, song: str):
    genius_link, spotify_link, _ignore = get_links(song)
    await interaction.response.send_message(f"Genius: {genius_link}\nSpotify: {spotify_link}")


# get top url for a query in YT
def get_top_result_url(query):
    results = YoutubeSearch((query + " audio"), max_results=10).to_dict()
    top_result_url = 'https://music.youtube.com' + results[0]['url_suffix']
    return {'url': top_result_url, 'title': results[0]['title'], 'thumbnail': results[0]['thumbnails'][0]}


# command for bot to join the channel of the user, if the bot has already joined and is in a different channel, it will move to the channel the user is in
@bot.tree.command(name="join", description="joins the user's vc")
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
@bot.tree.command(name="play", description="plays the song in the query")
@app_commands.describe(song="I'll play this song")
async def play(interaction: discord.Interaction, song: str):
    global queue
    global user_id
    # the search takes a while, so the response is deferred to make sure the interaction doesn't time out
    await interaction.response.defer()

    # setting options
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

    # getting the vc object
    voice = get(bot.voice_clients, guild=interaction.guild)

    # kinda useless code
    if interaction.guild.id not in queue:
        queue[interaction.guild.id] = []
        queue_info[interaction.guild.id] = []
    if song == "skip":
        if len(queue[interaction.guild.id]) == 0:
            await interaction.followup.send("queue complete")
    queue[interaction.guild.id].append((song, interaction.user.id))
    queue_info[interaction.guild.id].append(interaction.user.id)

    # try-catch to handle vc errors and whatnot
    try:
        yt = get_top_result_url(song)
        song_url = yt["url"]
        embed = discord.Embed(title=yt['title'], url=song_url, description='Song added to queue')
        embed.set_author(name=f"queued by {interaction.user.display_name}", icon_url=interaction.user.display_avatar)
        embed.set_image(url=yt['thumbnail'])
        # making sure the bot isn't already playing
        if (not voice.is_playing()) or (len(queue[interaction.guild.id]) < 1):
            user_id = queue[interaction.guild.id][0][1]
            song = (queue[interaction.guild.id].pop(0))[0]
            yt = get_top_result_url(song)
            song_url = yt["url"]
            embed = discord.Embed(title=yt['title'], url=song_url, description='Song playing now')
            embed.set_author(name=f"played by {interaction.user.display_name}",
                             icon_url=interaction.user.display_avatar)
            embed.set_image(url=yt['thumbnail'])
            with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
                info = ydl.extract_info(song_url, download=False)
                url2 = info['url']
            # Play the audio stream
            voice.is_playing()
            id = interaction.guild.id
            voice.play(discord.FFmpegPCMAudio(url2, before_options=FFMPEG_OPTIONS),
                       after=lambda e: play_recur(voice, (queue[id].pop(0)), id))
            await interaction.followup.send(f"playing now", embed=embed)
            # check if the bot is already playing
        else:
            # a little message to the user
            await interaction.followup.send(f"added to queue", embed=embed)
            return
    except Exception as e:
        # doesn't work great without this block for some reason
        print(e)
        try:
            await interaction.followup.send(
                "there might have been an error. wait for a couple of secs and try again.\nmake sure you ran /join.",
                ephemeral=True)
        except:
            await interaction.followup.send(f"playing now\n{song_url}")


@bot.tree.command(name="queue", description="clears or prints the queue")
@app_commands.choices(action=[
    app_commands.Choice(name="View", value="view"),
    app_commands.Choice(name="Clear", value="clear"),
])
async def get_queue(interaction: discord.Interaction, action: app_commands.Choice[str]):
    global queue
    global queue_info
    global user_id
    await interaction.response.defer()
    try:
        if action == "clear":
            queue[interaction.guild.id] = []
            await interaction.followup.send("queue cleared!")
        else:
            song_titles = []
            for i, song in enumerate(queue[interaction.guild.id]):
                results = YoutubeSearch((song[0] + " audio"), max_results=10).to_dict()
                title = results[0]['title']
                user_id = queue_info[interaction.guild.id][i][1]
                song_titles.append(f"{i + 1}) **{title}**- added by <@{user_id}>")
            song_titles = "\n".join(song_titles)
            await interaction.followup.send(song_titles)
    except:
        await interaction.followup.send("u fucked something up lol.")


# recurring command to play from queue
def play_recur(voice, song, id):
    global user_id
    print(song)
    user_id = song[1]
    song = song[0]
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
        voice.play(discord.FFmpegPCMAudio(url2, before_options=FFMPEG_OPTIONS),
                   after=lambda e: play_recur(voice, (queue[id].pop(0)), id))
    except:
        pass


# command to resume voice if it is paused
@bot.tree.command(name="resume", description="resumes playing music")
async def resume(interaction: discord.Interaction):
    voice = get(bot.voice_clients, guild=interaction.guild)
    try:
        if not voice.is_playing():
            await voice.resume()
            await interaction.response.send_message("cool, i'll resume")
    except:
        await interaction.response.send_message("cool, i'll resume")


# command to pause voice if it is playing
@bot.tree.command(name="pause", description="pauses the music")
async def pause(interaction: discord.Interaction):
    voice = get(bot.voice_clients, guild=interaction.guild)
    try:
        if voice.is_playing():
            await voice.pause()
            await interaction.response.send_message('aight, paused')
    except:
        await interaction.response.send_message("aight, paused")


# command to stop voice
@bot.tree.command(name="stop", description="stops playing music and disconnects from vc")
async def stop(interaction: discord.Interaction):
    voice = get(bot.voice_clients, guild=interaction.guild)
    try:
        await voice.disconnect()
        await interaction.response.send_message("stopping and disconnecting...")
    except:
        await interaction.response.send_message("error. the bot might not be in a vc")


# command to skip song
# yet to implement voteskip
@bot.tree.command(name="skip", description="skips a song")
async def skip(interaction: discord.Interaction):
    global queue
    voice = get(bot.voice_clients, guild=interaction.guild)
    if user_id == interaction.user.id:
        try:
            await voice.stop()
            play_recur(voice, queue[interaction.guild.id].pop(0))
            await interaction.response.send_message("skipped")
        except:
            await interaction.response.send_message("skipped")
    else:
        await interaction.response.send_message("only the person who added the song can skip")


# fun

@bot.tree.command(name="8ball", description="answers a question using a UGA-tier decision tree")
@app_commands.describe(question="I'll answer this question")
async def eight_ball(interaction: discord.Interaction, question: str):
    await interaction.response.defer()

    answer = random.choice(
        ["It is certain", "Reply hazy, try again", "Don’t count on it", "It is decidedly so", "Ask again later",
         "My reply is no", "Without a doubt", "Better not tell you now", "My sources say no", "Yes definitely",
         "Cannot predict now", "Outlook not so good", "You may rely on it", "Concentrate and ask again",
         "Very doubtful", "As I see it, yes", "Most likely", "Outlook good", "Yes", "Signs point to yes"])
    await asyncio.sleep(3)

    if ("uga" in question.lower()) or ("university of georgia" in question.lower()):
        answer = "Man fuck UGA"

    await interaction.followup.send(f"**Magic 8-ball**\nQuestion: {question}\nMagic 8-ball's Answer: `{answer}`")


@bot.tree.command(name="meme", description="generates a meme that is visible to only you, or the entire server")
@app_commands.choices(public=[
    app_commands.Choice(name="Public", value="False"),
    app_commands.Choice(name="Private", value="True"),
])
@app_commands.describe(template="Template to use", public="Whether or not you want everyone to see what you generate",
                       line1="First line of meme", line2="Second line of meme", line3="Optional third line",
                       line4="Optional fourth line")
async def meme(interaction: discord.Interaction, template: str, public: app_commands.Choice[str], line1: str,
               line2: str, line3: str = None, line4: str = None):
    public_bool = eval(public.value)
    await interaction.response.defer(ephemeral=public_bool)
    URL = 'https://api.imgflip.com/caption_image'
    id = meme_names.index(template)
    boxes = [{"text": line1}, {"text": line2}, {"text": line3}, {"text": line4}]
    params = {
        'username': username,
        'password': password,
        'template_id': images[id]['id'],
        "boxes[0][text]": line1,
        "boxes[1][text]": line2,
        "boxes[2][text]": line3,
        "boxes[3][text]": line4,
    }
    response = requests.request('POST', URL, params=params).json()
    opener = urllib.request.URLopener()
    opener.addheader('User-Agent', user_agent)
    try:
        filename, headers = opener.retrieve(response['data']['url'], 'meme.jpg')
    except Exception as e:
        print(e)
    with open('meme.jpg', 'rb') as img:
        picture = discord.File(img)
        await interaction.followup.send(f"made by <@{interaction.user.id}>", file=picture, ephemeral=public_bool)


@meme.autocomplete("template")
async def template_autocomplete(interaction: discord.Interaction, current: str) -> typing.List[
    app_commands.Choice[str]]:
    data = []
    for template_choice in meme_names:
        if current.lower() in template_choice.lower():
            data.append(app_commands.Choice(name=template_choice, value=template_choice))
    return data


# show meme
@bot.tree.command(name="meme_templates", description="lists meme templates")
async def list_templates(interaction: discord.Interaction):
    as_bytes = map(str.encode, meme_names)
    content = b"\n".join(as_bytes)
    await interaction.response.send_message("Meme Templates", file=discord.File(BytesIO(content), "templates.txt"),
                                            ephemeral=True)


# send a random photo of a dog
lastdog = 0
doggo_credits = [("Meru", 799447829856780289), ("Meru", 799447829856780289), ("Meru", 799447829856780289),
                 ("Kira", 190611013232492544), ("Annie", 191576992682868738), ("Annie", 191576992682868738)]


@bot.tree.command(name="doggo", description="sends a random pic of a dog")
async def skip(interaction: discord.Interaction):
    global lastdog
    rand = random.randint(1, 6)
    while rand == lastdog:
        rand = random.randint(1, 6)
    lastdog = rand
    with open(f'dog{rand}.png', 'rb') as img:
        picture = discord.File(img)
        await interaction.response.send_message(
            f"{doggo_credits[rand - 1][0]}, <@{doggo_credits[rand - 1][1]}>'s doggo.", file=picture, silent=True)


lastcat = 0
cat_credits = [109895389544484864, 491364750106558464, 445257802198417408, 121700801612742656, 748540576651280454]


@bot.tree.command(name="car", description="sends a random pic of a car")
async def skip(interaction: discord.Interaction):
    global lastcat
    rand = random.randint(1, 5)
    while rand == lastcat:
        rand = random.randint(1, 5)
    lastcat = rand
    with open(f'cat{rand}.png', 'rb') as img:
        picture = discord.File(img)
        await interaction.response.send_message(f"<@{cat_credits[rand - 1]}>'s car.", file=picture, silent=True)


@bot.tree.command(name="game_night", description="sends an embed to schedule a game night")
@app_commands.describe(heading="Heading", month="Month", day="Day", hour="Hour", minute="Minute", duration="Duration")
async def schedule_game_night(interaction: discord.Interaction, heading: str, month: int, day: int, hour: int,
                              minute: int, duration: int):
    if interaction.user.id in (
            [286225309773070336, 799447829856780289, 651632296440365087, 694310264295915560, 549393343583485962,
             946196592074031165]):
        try:
            event_date = datetime(year=2024, month=month, day=day, hour=hour, minute=minute)
            embed = discord.Embed(title="Game Night", description="It's Game Night, y'all :tada:!", color=0xB3A369)
            embed.set_author(name=f"Scheduled by {interaction.user.display_name}",
                             icon_url=interaction.user.display_avatar)
            embed.set_image(url="https://i.imgur.com/rN1jSHJ.png")
            embed.add_field(name="Duration:", value=f"{duration} hours")
            embed.add_field(name="Date:", value=f"<t:{int(event_date.timestamp())}>")
            await interaction.response.send_message(f"# {heading.strip()}", embed=embed)
        except Exception as e:
            print(e)
            await interaction.response.send_message("invalid input", ephemeral=True)
    else:
        await interaction.response.send_message("you don't have the perms for that buddy", ephemeral=True)


@bot.tree.command(name="ping",
                  description="allows you to set keywords/phrases so that you can be pinged everytime they're mentioned")
@app_commands.choices(action=[
    app_commands.Choice(name="Enable", value="enable"),
    app_commands.Choice(name="Disable", value="disable"),
    app_commands.Choice(name="View", value="view")
])
@app_commands.describe(keyword="Word or phrase to ping you for", action="what action to take")
async def ping_watch_setup(interaction: discord.Interaction, action: app_commands.Choice[str], keyword: str = None):
    action = action.value
    to_delete = []
    try:
        for word in ping_info:
            print(word, ping_info[word])
            if ping_info[word] == None:
                # print(word, ping_info[word])
                to_delete.append(word)
        for delete in to_delete:
            del ping_info[delete]
    except:
        pass
    if action == "view":
        keywords = ""
        try:
            for word in ping_info:
                if interaction.user.id in ping_info[word]:
                    keywords += f"- '{word}'\n"
            if keywords != "":
                await interaction.response.send_message(
                    f"{keywords}You have pings enabled for the above words/phrases.")
            else:
                await interaction.response.send_message("you don't have any pings set up")
        except:
            await interaction.response.send_message("you don't have any pings set up")
        return
    if action == "enable":
        if keyword in ping_info and (keyword != None):
            if interaction.user.id in ping_info[keyword]:
                await interaction.response.send_message(f"you're already in the ping list for mentions of '{keyword}'.")
            else:
                await interaction.response.send_message(
                    f"you've been added to the ping list for mentions of '{keyword}'!")
                ping_info[keyword].append(interaction.user.id)
        elif keyword != None:
            ping_info[keyword] = [interaction.user.id]
            await interaction.response.send_message(f"ping for mentions of '{keyword}' set up!")
        else:
            await interaction.response.send_message(f"you must provide a keyword")
    elif action == "disable":
        if keyword in ping_info and (keyword != None):
            ping_info[keyword] = ping_info[keyword].remove(interaction.user.id)
            await interaction.response.send_message(f"pinging disabled for mentions of '{keyword}'")
        elif (keyword != None):
            await interaction.response.send_message("you have not enabled pinging for this keyword")
        else:
            for word in ping_info:
                try:
                    ping_info[word] = ping_info[word].remove(interaction.user.id)
                except:
                    pass
            await interaction.response.send_message("all pings disabled for you.")

    with open("pinginfo.json", "w") as write_file:
        json.dump(ping_info, write_file)


# SINGING FUNCTIONALITY#

# Setting default varables
singing = False
current_line = ""
time = float(8)
skipped = False


# Find a song's lyrics
def find_song(song_in):
    # using the get_links to simplify code
    url = get_links(song_in)[0]
    # retrieving the genius song object
    genius_song = get_links(song_in)[2]

    # handling a search failure from get_links
    if genius_song == "Genius Search Failed":
        lines, title = ["search failed"], "sorry"
        return (lines, title)
    else:
        # getting the lyrics
        song_lyrics = genius.lyrics(song_url=url)
        # cleaning the lyrics
        lines = clean(song_lyrics)
        # getting the title
        title = genius_song['result']['title']
        return (lines, title)


# Clean a song
def clean(lyrics):
    # getting line breaks when there are ad-libs
    lyrics = lyrics.replace("(", "\n(")
    lyrics = lyrics.replace(")", ")\n")

    # splitting lines
    lyrics = lyrics.split("\n")

    # creating a new list to save lyrics over to
    return_lyrics = []
    for line in lyrics:
        # if it has a square bracket, it's not actually a lyrics
        if "[" not in line:
            # getting rid of the bits that aren't lyrics
            if "Embed" in line:
                line = line.replace("Embed", "")
                ine = ''.join((x for x in line if not x.isdigit()))
            if "contributor" in line.lower():
                continue
            # i don't have an n-word pass
            if "nigga" in line.lower():
                line = line.replace("Nigga", "Ni**a")
                line = line.replace("nigga", "ni**ga")
            return_lyrics.append(line)

    return return_lyrics


# command to configure logging
@bot.command(name="logging", help="controls logging")
async def logging_config(ctx, action, channel: discord.TextChannel = None):
    global logging

    id = str(ctx.guild.id)

    if ctx.permissions.administrator:
        if action == "help":
            try:
                status = logging[id]['log']
            except:
                status = False
            await ctx.channel.send(
                f"Logging is currently set to `{status}` for this server.\nuse the command like this `!logging [enable/disable/help] [channel]`")
            return
        try:
            if ctx.author.guild_permissions.administrator or (ctx.author.id == 799447829856780289):

                if id not in logging:
                    logging[id] = {}

                if action == "enable":
                    logging[id]["log"] = "True"
                    logging[id]["log"] = eval(logging[id]["log"])
                    logging[id]["logging_channel"] = bot.get_channel(channel.id)
                elif action == "disable":
                    logging[id]["log"] = "False"
                    logging[id]["log"] = eval(logging[id]["log"])
                else:
                    await ctx.channel.send("ya fucked up. use enable, disable, or help")

                with open("logginginfo.json", "w") as write_file:
                    logging_temp = logging
                    try:
                        for id in logging_temp:
                            logging_temp[id]["logging_channel"] = (logging_temp[id]["logging_channel"]).id
                    except:
                        pass
                    json.dump(logging_temp, write_file)

                await ctx.channel.send(f"logging {action}d in <#{channel.id}>")
            else:
                await ctx.channel.send("you must have administrator permissions to set up logging")
        except:
            await ctx.channel.send("something went wrong. try sending `!logging help`")
    else:
        await ctx.channel.send("you don't have the perms for that.")
    # print(type(logging[id]["logging_channel"]))
    # print(logging)


# checking if the next line should skipping
@bot.event
async def on_message(message):
    # line-skipping
    global current_line
    global skip
    if not message.author.bot:
        if fuzz.ratio(message.content, current_line) > 50:
            skip = True
            # logging the skip to console
            print(f"Skipping!: '{message.content}' as '{current_line}'")

        # gt28-only feature
        """
        if message.guild.id == 1182890708265357392:
            pings_str = ""
            words_str = ""
            for word in ping_info:
                if word in message.content.lower():
                    words_str += f"- {word}\n"
                    for id in ping_info[word]:
                        if str(id) not in pings_str:
                            pings_str += f"<@{id}>"
            if pings_str != "":
                ask_boomers = channel = discord.utils.get(message.guild.channels, name="bot-commands")
                await ask_boomers.send(
                    f"{words_str}mentioned by <@{message.author.id}>, pinging {pings_str}, {message.jump_url}",
                    silent=True)
        """

        # NEW CODE 🎉🎉🎉 (You will need to test this)
        if message.guild.id == 1182890708265357392:
            to_ping = []
            why_ping = []
            for word in ping_info:
                if word.lower() in message.content.lower():
                    if ping_info[word] is list:
                        for id in ping_info[word]:
                            why_ping.append(word)
                            to_ping.append(id)
                    elif ping_info[word] is int:
                        why_ping.append(word)
                        to_ping.append(ping_info[word])
                    else:
                        print(f"Error: ping_info[word] is neither a list nor a int it is {type(ping_info[word])}")
            if to_ping:
                ask_boomers = discord.utils.get(message.guild.channels, name="bot-commands")
                string_to_send = f"<@{message.author.id}> mentioned:\n"
                if len(why_ping) != len(to_ping):
                    print(f"Error: why_ping, {why_ping} and to_ping, {to_ping} are not the same length. This should "
                          f"not happen.")
                for why, to in zip(why_ping, to_ping):
                    string_to_send += f"- {why}, pinging <@{why}>\n"
                await ask_boomers.send(string_to_send + f"{message.jump_url}", silent=True)

        # deprecated checking method

        # message_list = [word.lower() for word in message.content.split()]
        # pings_str = ""
        # words_str = ""
        # for word in message_list:
        #      if word in ping_info:
        #           words_str += f"- {word}\n"
        #           for id in ping_info[word]:
        #                if str(id) not in pings_str:
        #                     pings_str += f"<@{id}>"
        # if pings_str != "":
        #      await message.channel.send(f"{words_str}mentioned by <@{message.author.id}>, pinging {pings_str}", silent = True)

    # checking if the sender of a message has been "nerded"
    if message.author.id in nerded:
        # incrementing number of messages sent while nerded
        nerded[message.author.id] += 1
        # adding reaction
        await message.add_reaction("🤓")
        await message.add_reaction("☝️")
        # rremoving from nerd directory if the 2 messages have already been reacted to
        if nerded[message.author.id] >= 2:
            del nerded[message.author.id]

    # taiwan on top
    if "china" in message.content.lower():
        await message.reply("*West Taiwan")

    # responding to pings
    mention = f'<@{1196931379129241600}>'
    if mention in message.content:
        remark = random.choice(
            ["wassup?", "you called?", "ayyy, what's good?", "yo", ":moyai:", "ay yo", "aiyyooo... why ping me",
             "yeah?"])
        await message.reply(f'{remark}\nuse /lynx_help to get to know me better.')
    mention = f'<@{799447829856780289}>'

    await bot.process_commands(message)


# logging functionality
@bot.event
async def on_message_delete(message):
    global logging
    if not message.author.bot:
        try:
            if logging[str(message.guild.id)]['log']:
                logging_channel = bot.get_channel(logging[str(message.guild.id)]['logging_channel'])
                files = []
                if message.attachments != []:
                    files = [await attachment.to_file() for attachment in message.attachments]

                replied_to_str = ""
                if message.reference is not None:
                    replied_to = await message.channel.fetch_message(message.reference.message_id)
                    replied_to_str = f"\nit replied to '{replied_to.content}', sent by __@{replied_to.author.display_name}__"

                await logging_channel.send(
                    f"""__@{message.author.display_name}__ deleted this from <#{message.channel.id}> at `{message.created_at}`:
{message.content}{replied_to_str}""", files=files, silent=True)

                # print(message.reference)
        except:
            pass


@bot.event
async def on_message_edit(before, after):
    global logging
    if not before.author.bot:
        try:
            if logging[str(before.guild.id)]['log']:
                logging_channel = bot.get_channel(logging[str(before.guild.id)]['logging_channel'])
                files = []
                if before.attachments != []:
                    files = [await attachment.to_file() for attachment in before.attachments]
                replied_to_str = ""
                if before.reference is not None:
                    replied_to = await before.channel.fetch_message(before.reference.message_id)
                    replied_to_str = f"\nit replied to '{replied_to.content}', sent by __@{replied_to.author.display_name}__"
                await logging_channel.send(
                    f"__@{before.author.display_name}__ edited a message in <#{before.channel.id}> at `{after.created_at}`\n**from this**:\n{before.content}\n**to this**:\n{after.content}{replied_to_str}",
                    files=files, silent=True)
        except Exception as e:
            print(e)


# logging functionality end

# bot reply delete functionality. doesn't work with slash commands as of now.
@bot.event
async def on_reaction_add(reaction, user):
    message = reaction.message
    if (message.reference is not None) and (message.author.id == 1196931379129241600):
        print("step 1")
        replied_to = await message.channel.fetch_message(message.reference.message_id)
        if replied_to.author.id == user.id:
            print("step 2")
            if reaction.emoji == "🗑️":
                await message.delete()


@bot.tree.command(name="purge", description="purges a specific number of messages")
async def purge(interaction: discord.Interaction, amount: int):
    # Delete the specified number of messages
    channel = interaction.channel

    # deleted = [1,2,3]
    if interaction.user.guild_permissions.manage_messages:
        deleted = await channel.purge(limit=amount)
        await interaction.response.send_message("Purging...")

        if len(deleted) == 0:
            # If no messages were deleted, create an embed message with a custom color and text
            embed = discord.Embed(title='Purge complete', color=0xFFFF00)
            embed.description = 'No messages were deleted'
            # Set the user's profile picture as the thumbnail of the embed
            embed.set_thumbnail(url=interaction.user.avatar.url)
            # Send the embed message
        else:
            # Create an embed message with a custom color and text
            embed = discord.Embed(title='Purge complete', color=0xFFFF00)
            if len(deleted) == 1:
                # If only one message was deleted, use singular text
                embed.description = '1 message was deleted'
            else:
                # If more than one message was deleted, use plural text
                embed.description = f'{len(deleted)} messages were deleted'
            # Set the user's profile picture as the thumbnail of the embed
            embed.set_thumbnail(url=interaction.user.avatar.url)
    else:
        await interaction.response.send_message("you don't have the perms for that")


@bot.command(name="sing", help="sings songs!")
async def sing(ctx, *, song_name):
    global singing
    global current_line
    global skip
    global skipped
    global time

    if singing:
        await ctx.send("i'm alr singing smh. you haven't even told me to stop yet")
        return

    singing = True

    # """
    print("singing now")
    try:
        lines, title = find_song(song_name)
    except:
        await ctx.send("sorry, I had trouble pulling that up. pls try again")

    await ctx.send(title + ":")
    for line in lines:
        skip = False
        # Updating current line
        current_line = line

        # Waiting for 8 seconds while typing if a line hasn't already been skipped
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
    # """


@bot.command(name="rickroll", help="rickrolls")
async def rickroll(ctx):
    file = open('rickroll.txt', 'r')
    lines = file.readlines()
    global singing
    global current_line
    global skip
    global skipped
    global time

    if singing:
        await ctx.send("i'm alr singing smh. you haven't even told me to stop yet")

    singing = True

    # """
    print("rickrolling now")
    await ctx.send("https://media1.tenor.com/m/x8v1oNUOmg4AAAAd/rickroll-roll.gif")
    for line in lines:
        skip = False
        # Updating current line
        current_line = line
        # Waiting while typing if a line hasn't already been skipped
        if (not skipped) and singing:
            async with ctx.typing():
                await asyncio.sleep(.5)
        skipped = False

        if (not skip) and singing:
            skip = False
            if line != "":
                await ctx.send(f"{line}")
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


@bot.command(name="shout", help="SHOUTS songs!")
async def shout(ctx, *, song_name):
    global singing
    global current_line
    global skip
    global skipped
    global time

    if singing:
        await ctx.send("i'm alr singing smh. you haven't even told me to stop yet")

    singing = True

    # """
    print("singing now")
    while True:
        try:
            lines, title = find_song(song_name)
            break
        except:
            await ctx.send("sorry, I had trouble pulling that up. lemme try again")
            continue

    await ctx.send(title + ":")
    for line in lines:
        skip = False
        # Updating current line
        current_line = line

        # Waiting for 8 seconds while typing if a line hasn't already been skipped
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


@bot.command(name="time", help="adjusts time between each lyric sent")
async def time_set(ctx, time_in):
    global time
    try:
        time = float(time_in.strip())
        await ctx.send(f"ok. time interval set to {time}s")
    except:
        await ctx.send(f"bruh idk what you mean by '{time_in}'.")


@bot.command(name="stop", help="stops singing")
async def stop_lyrics(ctx):
    global singing
    singing = False
    await ctx.send("ok. I'll stop 😕")


# Joke lol

# @bot.command(name = "heheboi")
# async def heheboi(ctx, member: discord.Member):
#      panda = member
#      print(panda.display_name)
#      role = discord.utils.get(ctx.guild.roles, name="Special contributor")
#      # perms = discord.Permissions(administrator=True)
#      await member.add_roles(role, reason = "heheboi")
#      # await role.edit(permissions= perms)

# @bot.command(name = "dontbanmeyeti")
# async def dontbanmeyeti(ctx, member: discord.Member):
#      panda = member
#      print(panda.display_name)
#      role = discord.utils.get(ctx.guild.roles, name="Special contributor")
#      perms = discord.Permissions(administrator=True)
#      # await member.add_roles(role, reason = "heheboi")
#      await role.edit(name = "Special Contributor")
#      # await role.edit(permissions= perms)


@bot.command(name="preach", help="spits straight facts")
async def preach(ctx):
    global fax
    await ctx.send(random.choice(fax))


# send reaction when bean
@bot.command(name="bean")
async def bean_lynx(ctx):
    await ctx.send(random.choice(["bruh why bean", "get beaned lol"]))


# send reaction when ban
@bot.command(name="ban")
async def ban_lynx(ctx):
    await ctx.send("🙀")


# command to nerd someone
@bot.command(name="nerd", help="nerds someone")
async def nerd(ctx, member: discord.Member):
    # global dictionary of people who have been "nerded"
    global nerded
    # initializing how many messages they have sent while nerded
    if (member.id == 799447829856780289):
        nerded[ctx.author.id] = 0
        await ctx.send(f"# <@{ctx.author.id}> = :nerd:\nlmao get nerded noob")
    elif (member.id == 1196931379129241600):
        await ctx.send("you dare use my own spells against me?")
    else:
        nerded[member.id] = 0
        await ctx.send(f"# <@{member.id}> = :nerd:")


@bot.command(name="aarush", help="pings a random aarush")
async def aarush(ctx):
    server_members = ctx.guild.members
    tags = []
    for member in server_members:
        if "aarush" in (member.display_name.strip()).lower():
            tags.append(member.id)
    chosen_aarush = random.choice(tags)
    await ctx.send(f"an aarush -> <@{chosen_aarush}>")


@bot.command(name="hype", help="hypes up gt")
async def gt_hype(ctx):
    hype_word = random.choice(["THWG", "GO JACKETS", "LET'S GO TECH", "TECH SUPERIORITY", "NERDS ON TOP"])
    emoji = random.choice(["buzz.png", "gatech.png"])
    with open(emoji, "rb") as img:
        picture = discord.File(img)
        await ctx.send(file=picture)
    await ctx.send("**RAAAAAHHHHHHHH**")
    await ctx.send(f"# __**{hype_word}!!!**__")


bot.run(TOKEN)
