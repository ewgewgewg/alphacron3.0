import random

async def guessNumber(client, message):
  channel = message.channel
  await channel.send("Guess the number from 0-10 by writing number in this channel!")

  number1 = str(random.randint(1,10))

  def check(m):
      return m.content == number1 and m.channel == channel
  
  msg = await client.wait_for('message', check=check)
  await channel.send("Correct answer from far action, {.author}" .format(msg))