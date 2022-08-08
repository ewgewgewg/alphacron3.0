import discord
import os
import datetime
import urllib.request
import requests
import inspect
from actions.guessNumber import guessNumber
from actions.toArchive import toArchive
from actions.stale import stale
from lookup import activeCategoryNames

token = os.environ['TOKEN']

client = discord.Client()

thresholdDays = 30
lastDays = 6


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$whatcategory'):
        print(message.channel.category)
        await message.channel.send(message.channel.category)
        return

    if message.content.startswith('$callbotstring'):
        date = datetime.datetime.now()
        await message.channel.send(
            f'alphacron says hello to {message.author} on {date} in channel at position {message.channel.position}!'
        )
        return

    if message.content.startswith('$staleprintdebug'):
        staleList = await stale(message, thresholdDays)
        print('these are stale channels')
        await message.channel.send('these are stale channels')
        for staleItem in staleList:
            print(staleItem.name)
            await message.channel.send(
                f'alphacron thinks {staleItem.name} is a stale channel!')
        return

    if message.content.startswith('Weekly cleanup check!'):
        staleList = await stale(message, thresholdDays)
        print('these are stale channels')
        for staleItem in staleList:
            print(staleItem.name)
            await staleItem.send(
                f'Inactivity Warning! This is a stale channel in the category --{message.channel.category.name}--, and has been inactive for greater than the following number of days: {thresholdDays}. In about {lastDays+1} days this channel will be moved to Archive unless new activity appears. Channels with new activity restore to their old category. This is an automatic message.'
            )

        channels = message.guild.channels
        for channel in channels:
            print(channel.name)
            try:
                last = channel.last_message_id
                if last:
                    now = datetime.datetime.now()
                    curmessage = await channel.fetch_message(last)
                    created = curmessage.created_at
                    since = now - created
                    text = curmessage.content
                    if text.startswith(
                            'Inactivity Warning! This is a stale channel, and'
                    ) and since.days >= lastDays:
                        await toArchive(curmessage)
                else:
                    pass
            except:
                print('no messages possible in this channel type!')

    if message.content.startswith('$_toarchive'):
        await toArchive(message)

    if message.content.startswith('$get-hacker-news'):
        # get top stories IDS
        with urllib.request.urlopen(
                'https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty'
        ) as response:
            top_story_ids = response.read()
            # only_five = top_story_ids[0:4]
            # use IDS to fetch top story URLS (and blurbs?)
            print(top_story_ids)

    if message.content.startswith('$test-get'):
        tester = requests.get(
            'https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty'
        )
        top_story_ids = tester[0:4]
        print(top_story_ids)

    if message.content.startswith("?guess a number"):
        await guessNumber(client, message)

    if message.content.startswith("?test-writing-Text Channels"):
        await message.channel.send("writing--Text Channels")

    bot_id = 832792242782863401
    if message.channel.category.name == "archive" and message.author.id != bot_id:
        last_messages = await message.channel.history(limit=2).flatten()
        restored_category_name = None
        if last_messages[1].author.id == bot_id and len(last_messages[1].content.split('--')) > 1:
          restored_category_name = last_messages[1].content.split('--')[1]

        elif(activeCategoryNames[message.channel.name]):
          restored_category_name = activeCategoryNames[message.channel.name]
          print(restored_category_name)
        if not restored_category_name:
          return

        all_categories = message.guild.categories
        for selected_category in all_categories:
          if (selected_category.name == restored_category_name):
              await message.channel.edit(category=selected_category)
              after = False
              for selected_channel in selected_category.channels:
                if after:
                  await selected_channel.edit(positon=selected_channel.position+1)
                elif selected_channel.name > message.channel.name:
                  await message.channel.edit(position=selected_channel.position)
                  await selected_channel.edit(position=selected_channel.position+1)
                  after = True
                  
              await message.channel.send(
                  f'Restored channel to {restored_category_name} based on activity!'
              )
          
client.run(token)
