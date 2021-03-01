from subprocess import CompletedProcess

import discord
from discord.ext import commands

from bot import SRBpp

Context = commands.context.Context
PREFIX: str = "srcom/bin"


class Src(commands.Cog):
	def __init__(self, bot: SRBpp) -> None:
		self.bot: SRBpp = bot

	@commands.command(name="wrs")
	async def wrs(self, ctx: Context, PLAYER: str = None) -> None:
		if not PLAYER:
			await ctx.send("Usage: `!wrs [PLAYER NAME]`")
			return

		RET: CompletedProcess = self.bot.execv(f"{PREFIX}/wrs", PLAYER)
		embed = discord.Embed(
			title=f"World Record Count: {PLAYER}", description=RET.stdout
		)
		await ctx.send(embed=embed)

	@commands.command(name="runs")
	async def runs(self, ctx: Context, PLAYER: str = None) -> None:
		if not PLAYER:
			await ctx.send("Usage: `!runs [PLAYER NAME]`")
			return

		RET: CompletedProcess = self.bot.execv(f"{PREFIX}/runs", PLAYER)
		embed = discord.Embed(title=f"Run Count: {PLAYER}", description=RET.stdout)
		await ctx.send(embed=embed)

	@commands.command(name="games")
	async def games(self, ctx: Context, PLAYER: str = None) -> None:
		if not PLAYER:
			await ctx.send("Usage: `!games [PLAYER NAME]`")
			return

		RET: CompletedProcess = self.bot.execv(f"{PREFIX}/games", PLAYER)
		embed = discord.Embed(title=f"Games Played: {PLAYER}", description=RET.stdout)
		await ctx.send(embed=embed)

	@commands.command(name="modcount", aliases=("mc",))
	async def modcount(self, ctx: Context, PLAYER: str = None) -> None:
		if not PLAYER:
			await ctx.send("Usage: `!modcount [PLAYER NAME]`")
			return

		RET: CompletedProcess = self.bot.execv(f"{PREFIX}/modcount", PLAYER)
		embed = discord.Embed(
			title=f"Leaderboards Moderated: {PLAYER}", description=RET.stdout
		)
		await ctx.send(embed=embed)

	@commands.command(name="categories", aliases=("cats",))
	async def categories(self, ctx: Context, GAME: str = None) -> None:
		if not GAME:
			await ctx.send("Usage: `!categories [GAME]`")
			return

		RET: CompletedProcess = self.bot.execv(f"{PREFIX}/categories", GAME)
		TITLE, CATS = RET.stdout.split("\n", 1)
		embed = discord.Embed(title=TITLE, description=CATS)
		await ctx.send(embed=embed)

	@commands.command(name="leaderboard", aliases=("lb",))
	async def leaderboard(
		self, ctx: Context, GAME: str = None, CAT: str = None
	) -> None:
		if not GAME:
			await ctx.send("Usage: `!leaderboard [GAME] [CATEGORY (Optional)]`")
			return

		RET: CompletedProcess = self.bot.execv(f"{PREFIX}/leaderboard", GAME, CAT)
		TITLE, LB = RET.stdout.split("\n", 1)
		embed = discord.Embed(title=TITLE, description=LB)
		await ctx.send(embed=embed)

	@commands.command(name="worldrecord", aliases=("wr",))
	async def worldrecord(
		self, ctx: Context, GAME: str = None, CAT: str = None
	) -> None:
		if not GAME:
			await ctx.send("Usage: `!worldrecord [GAME] [CATEGORY (Optional)]`")
			return

		RET: CompletedProcess = self.bot.execv(f"{PREFIX}/worldrecord", GAME, CAT)
		TITLE, WR = RET.stdout.split("\n", 1)
		embed = discord.Embed(title=TITLE, description=WR)
		await ctx.send(embed=embed)

	@commands.command(name="verified")
	async def verified(self, ctx: Context, PLAYER: str = None) -> None:
		if not PLAYER:
			await ctx.send("Usage: `!verified [PLAYER NAME]`")
			return

		RET: CompletedProcess = self.bot.execv(f"{PREFIX}/verified", PLAYER)
		embed = discord.Embed(title="Runs verified: {PLAYER}", description=RET.stdout)
		await ctx.send(embed=embed)


def setup(bot: SRBpp) -> None:
	bot.add_cog(Src(bot))
