#!/usr/bin/env python

import discord
import asyncio

TOKEN = open("./token", "r", encoding="UTF-8").read()
AUTH_URL = "https://discord.com/oauth2/authorize?client_id=1446412675281326202"
AUDIO_FILE_PATH = "./simian_segue.wav"
SERVER_ID = 1239764510873489419
CHANNEL_ID = 1446414760009535548

intents = discord.Intents.default()
intents.voice_states = True 
discord_client = discord.Client(intents=intents)
discord_command_tree = discord.app_commands.CommandTree(discord_client)
discord_server = discord.Object(SERVER_ID)

def voice_client_callback(voice_client: discord.VoiceClient, ex: Exception = None):
    if ex != None:
        print(ex)
        return
    
    source = discord.FFmpegPCMAudio(AUDIO_FILE_PATH)
    voice_client.play(source, after=lambda ex: voice_client_callback(voice_client, ex))

@discord_command_tree.command(name="play_song", description="Joins the voice channel and plays simian segue.", guild=discord_server)
async def play_song(interaction: discord.Interaction):
    try:
        if interaction.user.voice == None:
            await interaction.response.send_message("You must be in a voice channel to use this command.", ephemeral=True)
            return
        voice_channel = interaction.user.voice.channel

        voice_client = interaction.guild.voice_client
        if voice_client == None:
            voice_client = await voice_channel.connect()
        elif voice_client.channel.id != voice_channel.id:
            await voice_client.move_to(voice_channel)

        if voice_client.is_playing():
            voice_client.stop()

        source = discord.FFmpegPCMAudio(AUDIO_FILE_PATH)
        voice_client.play(source, after=lambda ex: voice_client_callback(voice_client, ex))
        await interaction.response.send_message("Started playing simian segue.", ephemeral=True)
    except Exception as ex:
        print(ex)

@discord_command_tree.command(name="stop_song", description="Stops playing simian segue and leaves the voice channel.", guild=discord_server)
async def stop_song(interaction: discord.Interaction):
    try:
        voice_client = interaction.guild.voice_client
        if voice_client != None:
            await voice_client.disconnect()
        await interaction.response.send_message("Stopped playing simian segue.", ephemeral=True)
    except Exception as ex:
        print(ex)

@discord_client.event
async def on_ready():
    await discord_command_tree.sync(guild=discord_server)
    await discord_client.change_presence(activity=discord.CustomActivity("Playing simian segue..."), status=discord.Status.online)
    print(f"Online as {discord_client.user}...")

async def main():
    await discord_client.start(TOKEN)
asyncio.run(main())