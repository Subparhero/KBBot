import sys
import os
from os.path import dirname
sys.path.append('../')
import youtube_dl
import pafy
import discord
import ffmpeg
import asyncio
from discord.ext import commands

#Shuts up general bug report messages
youtube_dl.utils.bug_reports_message = lambda: ''

#Help Command
help_command = commands.DefaultHelpCommand(
    no_category = 'Commands'
)

#Bot Description, most bots will have this exact setup
intents = intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='!', 
                   description="KB Test Bot", 
                   help_command=help_command, 
                   intents=intents
                  )

#General class for code so its readable
voicechat = None

#Holds queue until its time to be played
music_playlist = []
music_playlist_titles = []

#Posts to Console when running fully
@bot.event
async def on_ready():
    print('Up and Running!')

#Keeps bot in a loop until new song is played
async def CheckForNewSong(ctx):
    if len(music_playlist) > 0:
        voicechat.play(discord.FFmpegPCMAudio(source=music_playlist[0]))
        while ctx.voice_client.is_playing():
            await asyncio.sleep(1)
        music_playlist.pop(0)
        await CheckForNewSong(ctx)
    

#Kicks bot from Voice Chat
@bot.command(brief='Disconnect Bot', description='Disconnects Bot from Voice')
async def leave(ctx):
    global voicechat
    if voicechat is not None:
        await voicechat.disconnect()
        voicechat = None
    else:
        await ctx.send("Bot is not in a Voice Channel")

#Prints the queue to chat
@bot.command(brief='Playlist Queue', description='Shows a list of the queue')
async def queue(ctx):
    global voicechat
    global music_playlist_titles
    if len(music_playlist_titles) > 0:
        await ctx.send(music_playlist_titles)
    else:
        await ctx.send("Playlist is empty")

#Plays audio from Youtube
@bot.command(brief='Play from a Youtube Link', description='Plays audio from a YouTube URL')
async def play(ctx, arg):
    global voicechat
    global music_playlist_titles
    isConnected = ctx.message.author.voice
    if isConnected != None:
        voice_channel = ctx.message.author.voice.channel
        if voicechat is None:
            voicechat = await voice_channel.connect()
        url = arg
        video = pafy.new(url)
        music_playlist_titles.append(video.title + '\n')
        best = video.getbest()
        playurl = best.url
        if ctx.voice_client.is_playing():
            music_playlist.append(playurl)
        else:
            music_playlist.append(playurl)
            await CheckForNewSong(ctx)
        
    else:
        await ctx.send("You are not in a voice channel.")

#Stops playback        
@bot.command(brief='Stops playback', description='Stop the current song')
async def stop(ctx):
    global voicechat
    isConnected = ctx.message.author.voice
    if isConnected != None:
        global music_playlist
        music_playlist = []
        voicechat.stop()
    else:
        await ctx.send("You are not in a voice channel.")

#Skips the current song
@bot.command(brief='Skip current song', description='Skip current song and play the next in queue')
async def skip(ctx):
    global voicechat
    isConnected = ctx.message.author.voice
    if isConnected != None:
        voicechat.stop()
    else:
        await ctx.send("You are not in a voice channel.")


bot.run('YOURTOKEN')