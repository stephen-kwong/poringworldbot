import logging

from discord import Embed
from discord.ext import commands

from . import poringworld

PRICE_CHECK_ITEM_LIMIT = 5

bot = commands.Bot(command_prefix='$pw ')

logger = logging.getLogger(__name__)


@bot.event
async def on_ready() -> None:
    logger.info('We have logged in as {0.user}'.format(bot))


@bot.command()
async def echo(ctx: commands.Context, *, msg: str) -> None:
    """
    Test command to see if the bot is alive.
    """
    await ctx.send(msg)


@bot.command(name='pc')
async def price_check(ctx: commands.Context, *, item_name: str) -> None:
    """
    Price check an item.
    """
    # Try in stock items first as the query is faster.
    logger.info("Checking price for %s", item_name)
    try:
        items = await poringworld.get(
            query=item_name,
            in_stock=1,
            modified=0,
            limit=PRICE_CHECK_ITEM_LIMIT,
            order='price',
        )

        # If we don't find any items in stock then try out of stock
        if not items:
            items = await poringworld.get(
                query=item_name,
                in_stock=0,
                modified=0,
                limit=PRICE_CHECK_ITEM_LIMIT,
                order='price',
            )
    except poringworld.PoringWorldApiException:
        await ctx.send("Unable to retrieve data from poring.world. Please try again later :(")
        return

    if not items:
        await ctx.send(f"Unable to find a price for: {item_name}")
    else:
        for item in items:
            await ctx.send(embed=to_embed(item))


def to_embed(item: poringworld.Item) -> Embed:
    """
    Convert an poring world Item into a Discord embed.
    """
    def get_color_from_price_change():
        if item.price_change_1d > 0:
            return 0x00ff00  # green
        if item.price_change_1d < 0:
            return 0xff0000  # red
        return 0x000000  # black

    return Embed(
        title=item.name,
        description=f"Price: {'{:20,d}'.format(item.price).lstrip()}"
                    f"\nStock: {item.stock}"
                    f"\nChange(1d): {item.price_change_1d:.1f}%",
        color=get_color_from_price_change(),
    ).set_thumbnail(url=item.icon_url)
