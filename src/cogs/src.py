from typing import Union

from discord.ext import commands
from discord.ext.commands.context import Context
from discord.ext.commands.cooldowns import Cooldown

from bot import SRBpp, run_and_output

PREFIX: str = "srcom/bin"
RATE: int = 5


class Src(commands.Cog):
	def __init__(self, bot: SRBpp) -> None:
		self.bot: SRBpp = bot
		self._cd = commands.CooldownMapping.from_cooldown(
			RATE, 60, commands.BucketType.user
		)

	async def cog_check(self, ctx: Context) -> bool:
		"""
		Fuck you Khalooody.
		"""
		if ctx.invoked_with == "help":
			return True

		BUCKET: Cooldown = self._cd.get_bucket(ctx.message)
		RETRY_AFTER: float = BUCKET.update_rate_limit()
		if RETRY_AFTER:
			raise commands.CommandOnCooldown(BUCKET, RETRY_AFTER)
		return True

	@commands.command(name="categories", aliases=("cats",))
	async def categories(_, ctx: Context, GAME: str = None) -> None:
		"""
		Get a list of all of a games categories.
		"""
		await run_and_output(ctx, f"{PREFIX}/categories", GAME)

	@commands.command(name="categoriesplayed", aliases=("catsplayed",))
	async def categoriesplayed(_, ctx: Context, PLAYER: str = None) -> None:
		"""
		Get the number of unique categories a player has submit runs to.
		"""
		await run_and_output(
			ctx,
			f"{PREFIX}/categoriesplayed",
			PLAYER,
			TITLE=f"Categories Played: {PLAYER}",
		)

	@commands.command(name="games")
	async def games(_, ctx: Context, PLAYER: str = None) -> None:
		"""
		Get the number of unique games a player has submit runs to.
		"""
		await run_and_output(
			ctx, f"{PREFIX}/games", PLAYER, TITLE=f"Games Played: {PLAYER}"
		)

	@commands.command(name="leaderboard", aliases=("lb",))
	async def leaderboard(
		_, ctx: Context, GAME: str = None, CAT: str = None, SUBCAT: str = None
	) -> None:
		"""
		Get the top 10 runs for a game, with an optional category and subcategory.
		"""
		await run_and_output(ctx, f"{PREFIX}/leaderboard", GAME, CAT, SUBCAT)

	@commands.command(name="modcount", aliases=("mc",))
	async def modcount(_, ctx: Context, PLAYER: str = None) -> None:
		"""
		Get the number of games and series a player moderates.
		"""
		await run_and_output(
			ctx,
			f"{PREFIX}/modcount",
			PLAYER,
			TITLE=f"Leaderboards Moderated {PLAYER}",
		)

	@commands.command(name="runqueue", aliases=("queue",))
	async def runqueue(_, ctx: Context, GAME: str = None) -> None:
		"""
		Get the number of runs awaiting verification for a given game
		"""
		await run_and_output(ctx, f"{PREFIX}/runqueue", GAME)

	@commands.command(name="runs")
	async def runs(
		_, ctx: Context, PLAYER: str = None, GAME: str = None
	) -> None:
		"""
		Get the amount of runs a player has submit.
		"""
		await run_and_output(ctx, f"{PREFIX}/runs", PLAYER, GAME)

	@commands.command(name="verified")
	async def verified(
		_, ctx: Context, PLAYER: str = None, GAME: str = None
	) -> None:
		"""
		Get the amount of runs a player has verified or rejected.
		"""
		await run_and_output(
			ctx,
			f"{PREFIX}/verified",
			PLAYER,
			GAME,
			TITLE=f"Runs Verified: {PLAYER}",
		)

	@commands.command(name="worldrecord", aliases=("wr",))
	async def worldrecord(
		_, ctx: Context, GAME: str = None, CAT: str = None, SUBCAT: str = None
	) -> None:
		"""
		Get the world record for a game, with an optional category and subcategory.
		"""
		await run_and_output(ctx, f"{PREFIX}/worldrecord", GAME, CAT, SUBCAT)

	@commands.command(name="worldrecords", aliases=("wrs",))
	async def worldrecords(
		_, ctx: Context, PLAYER: str = None, GAME: str = None
	) -> None:
		"""
		Get the number of world records a player currently holds.
		"""
		await run_and_output(ctx, f"{PREFIX}/worldrecords", PLAYER, GAME)

	@commands.command(name="pending")
	async def pending(_, ctx: Context, GAME: str = None) -> None:
		"""
		Get all pending runs for a game.
		"""
		await run_and_output(
			ctx, f"{PREFIX}/pending", GAME, TITLE=f"Pending runs for {GAME}"
		)

	@commands.command(name="verifierleaderboard", aliases=("vlb",))
	async def verifierleaderboard(_, ctx, *, GAMES=None):
		"""
		Get a leaderboard of a game's verifier and how many runs each has verified
		"""
		GAMES = GAMES.split(" ") if GAMES else []
		await run_and_output(
			ctx,
			f"{PREFIX}/verifierleaderboard",
			*GAMES,
			TITLE=f"Verifier Leaderboard for games: {', '.join(GAMES) if GAMES else GAMES}",
		)


def setup(bot: SRBpp) -> None:
	bot.add_cog(Src(bot))
