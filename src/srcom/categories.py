#!/usr/bin/env python3.9

from sys import argv

import requests
from utils import *

GAME, GID = game(argv[1])
r: dict = requests.get(f"{API}/games/{GID}/categories").json()

FULLGAME: tuple[str] = tuple(
    c["name"]
    for c in r["data"]
    if c["miscellaneous"] == False and c["type"] == "per-game"
)
MISC: tuple[str] = tuple(
    c["name"] for c in r["data"] if c["miscellaneous"] == True
)
IL: tuple[str] = tuple(
    c["name"]
    for c in r["data"]
    if c["miscellaneous"] == False and c["type"] == "per-level"
)

print(
    f"Categories - {GAME}\n"
    + (
        "No Categories"
        if len(FULLGAME + MISC + IL) == 0
        else (
            (("Fullgame: " + ", ".join(FULLGAME)) if len(FULLGAME) > 0 else "")
            + (("\nMiscellaneous: " + ", ".join(MISC)) if len(MISC) > 0 else "")
            + (("\nIndividual Level: " + ", ".join(IL)) if len(IL) > 0 else "")
        )
    )
)