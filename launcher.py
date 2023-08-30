"""
3bot
===================
Bot do librusa na dc

:copyright: Copyright (c) @konradsic @ArgoTeam 2023-present
:license: MIT, see LICENSE file for more details
"""

__version__ = "0.0.1"
__author__ = "@konradsic, @ArgoTeam"
__license__ = "Licensed under the MIT License"
__copyright__ = "Copyright 2023-present konradsic, ArgoTeam"

import scripts
from scripts import logging
from colorama import Fore, init, Style
import discord
import asyncio
import platform
import getpass
import os
from bot.main import KonradooBot
import time
from dotenv import load_dotenv

load_dotenv()

start_time = time.time()

# const
TOKEN = os.environ.get("TOKEN")
APP_ID = int(os.environ.get("APPLICATION_ID", 0))

init(autoreset=True)

logger = logging.Logger("launcher")
figlet = scripts.show_figlet()
print(Fore.CYAN + figlet + "\n")
figlet_len = len(figlet.split("\n")[-1])//2 + 1
print("~="*figlet_len)
print(scripts.table(
    ("Version", __version__),
    ("Author(s)", __author__),
    ("License", __license__),
    ("discord.py", discord.__version__),
    center_leng=figlet_len
))

logger.info("Initializing...")

device = platform.node()
pid = os.getpid()
path_to = os.path.abspath("./main.py")
try:
    effective_user = getpass.getuser()
except:
    effective_user = "Unknown"

logger.info(f"Initializing 3bot on device [{device}], PID: {pid}")
logger.info(f"{path_to} started by {effective_user}")

bot = KonradooBot(TOKEN, APP_ID)
bot.run_bot()