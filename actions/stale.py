import datetime

async def stale(message, thresholdDays):
  staleList = []
  channels = message.guild.channels

  for channel in channels:
    print(channel.name)
    try:
      last = channel.last_message_id
      now = datetime.datetime.now()
      if last:

        #categories exempt from cleanup
        exempt = ['admin','archive']
        if channel.category.name in exempt:
          continue
        if 'SERVER' in channel.category.name:
          continue

        curmessage = await channel.fetch_message(last)
        created = curmessage.created_at
        since = now - created
        print(since)
        print(since.days)
        if (since.days > thresholdDays):
          staleList.append(channel)
      else:
        created = channel.created_at
        since = now - created
        print(since)
        print(since.days)
        if (since.days > thresholdDays):
          staleList.append(channel)
    except:
      print('no messages possible in this channel type!')
  
  return staleList