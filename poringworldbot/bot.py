from discord.ext import commands

from . import poringworld

PRICE_CHECK_ITEM_LIMIT = 5

bot = commands.Bot(command_prefix='$pw ')


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command()
async def echo(ctx, *, arg):
    await ctx.send(arg)


@bot.command(name='pc')
async def price_check(ctx, *, arg):
    items = await poringworld.get(query=arg, in_stock=1, modified=0, limit=PRICE_CHECK_ITEM_LIMIT, order='price')
    if not items:
        items = await poringworld.get(query=arg, in_stock=0, modified=0, limit=PRICE_CHECK_ITEM_LIMIT, order='price')

    if not items:
        await ctx.send(f"Unable to find a price for: {arg}")
    else:
        msg = "```\n"
        for item in items[:1]:
            price = '{:20,d}'.format(item.price).lstrip()
            msg += f"Name: {item.name}\nPrice: {price}\nStock: {item.stock}\n"
        for item in items[1:]:
            msg += '\n'
            price = '{:20,d}'.format(item.price).lstrip()
            msg += f"Name: {item.name}\nPrice: {price}\nStock: {item.stock}\n"
        msg += "```"
        await ctx.send(msg)
