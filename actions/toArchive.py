import discord

async def toArchive(message):
  channels = message.guild.channels
  newcategory = None
  for channel in channels:
    if channel.type == discord.ChannelType.category and channel.name == 'archive':
      newcategory = channel

  await message.channel.edit(category = newcategory)