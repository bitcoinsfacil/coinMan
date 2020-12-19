import os
import discord
from tipper.tipper import *
from dotenv import load_dotenv

load_dotenv()
TOKEN=os.getenv('DISCORD_TOKEN')

client = discord.Client()


@client.event
async def on_message(message):
    #make sure bot doesnt reply to himself
    if message.author == client.user:
        return

    if message.content.startswith('/help'):
        helpmsg = "```/deposit - your deposit address.``````/balance - your balance``````/send [user] [amount] - tips another user coins.``````/withdraw [amount] [address] - withdraws funds to an external address.\n``````/donate [amount] - donation to myce community```"
        #return await client.send_message(message.channel,helpmsg)
        await message.channel.send(helpmsg)

    if message.content.startswith('/deposit'):

        account = message.author.id
        address = getAddress(str(account))

        msg = '{0.author.mention}, your address is %s.'.format(message)%address
        await message.channel.send(msg)

    if message.content.startswith('/balance'): #0conf balance
        account = message.author.id
        balance = getBalance(account)
        msg = '{0.author.mention}, you have %f YCE.'.format(message)%balance
        await message.channel.send(msg)

    if message.content.startswith('/send '):
        tipper = message.author.id
        content = message.content.split()[1:]
        toTipMention = content[0]
        toTip = toTipMention.replace('<@','').replace('>','') #remove <@> from ID
        amount = content[1]

        #catching errors
        if not toTipMention[:2]=='<@':
            await message.channel.send("{0.author.mention}, invalid account.".format(message))
        try:
            amount = float(amount)
        except ValueError:
            await message.channel.send("{0.author.mention}, invalid amount.".format(message))

        try:
            tip(tipper,toTip,amount)
            #price = getPrice(float(amount))
            await message.channel.send("{0.author.mention} has tipped %s %f YCE.".format(message)%(toTipMention,amount))
        except ValueError:
            await message.channel.send("{0.author.mention}, insufficient balance.".format(message))

    if message.content.startswith('/withdraw '):
        account = message.author.id
        amount = message.content.split()[1]
        address = message.content.split()[2]

        #catching errors again
        if not validateAddress(address):
            await message.channel.send("{0.author.mention}, invalid address.".format(message))

        try:
            amount = float(amount)
        except ValueError:
            await message.channel.send("{0.author.mention}, invalid amount.".format(message))

        try:
            txid = withdraw(account,address,amount)
            await message.channel.send("{0.author.mention}, withdrawal complete, TXID %s".format(message)%txid)
        except ValueError:
            await message.channel.send("{0.author.mention}, insufficient balance.".format(message))

    if message.content.startswith('/rain '):
        account = message.author.id
        amount = float(message.content.split()[1])

        if amount < 0.01:
            await message.channel.send("{0.author.mention}, the amount must be bigger than 0.01 YCE.".format(message))
        #catching errors again
        try:
            amount = float(amount)
        except ValueError:
            await message.channel.send("{0.author.mention}, invalid amount.".format(message))

        try:
            eachtip = rain(account,amount) #the function returns each individual tip amount so this just makes it easier
            await message.channel.send("{0.author.mention} has tipped %f ammo to everyone on this server!".format(message)%eachtip)
        except ValueError:
            await message.channel.send("{0.author.mention}, insufficient balance.".format(message))


    if message.content.startswith('/donate'):
        account = message.author.id
        address = "YCEMarketing"#YCE marketing donation account
        amount = message.content.split()[1]

        #catching errors
        if not validateAddress(address):
            await message.channel.send("{0.author.mention}, invalid address.".format(message))

        try:
            amount = float(amount)
        except ValueError:
            await message.channel.send("{0.author.mention}, invalid amount.".format(message))

        try:
            txid = withdraw(account,address,amount)
            await message.channel.send("{0.author.mention}, Thank you for your donation! TXID: %s".format(message)%txid)
        except ValueError:
            await message.channel.send("{0.author.mention}, insufficient balance.".format(message))


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


client.run(TOKEN)
