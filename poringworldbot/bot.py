from discord import Embed
from discord.ext import commands

from . import poringworld

PRICE_CHECK_ITEM_LIMIT = 5

bot = commands.Bot(command_prefix='$pw ')


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))


@bot.command()
async def echo(ctx: commands.Context, *, arg: str):
    """
    Test command to see if the bot is alive.
    """
    await ctx.send(arg)


@bot.command(name='pc')
async def price_check(ctx: commands.Context, *, arg: str):
    """
    Price check an item.
    """
    items = await poringworld.get(query=arg, in_stock=1, modified=0, limit=PRICE_CHECK_ITEM_LIMIT, order='price')
    if not items:
        items = await poringworld.get(query=arg, in_stock=0, modified=0, limit=PRICE_CHECK_ITEM_LIMIT, order='price')

    if not items:
        await ctx.send(f"Unable to find a price for: {arg}")
    else:
        for item in items:
            await ctx.send(embed=to_embed(item))


def to_embed(item: poringworld.Item) -> Embed:
    return Embed(
        title=item.name,
        description=f"Price: {'{:20,d}'.format(item.price).lstrip()}\nStock: {item.stock}"
    ).set_thumbnail(url=item.icon_url)
