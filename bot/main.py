# bot class
import discord
from discord.ext import commands
import asyncio
import threading
from scripts import logging
import time
from colorama import Fore, Style
import os

@logging.LogClass
class ThreeBot(commands.Bot):
    def __init__(
        self,
        token,
        application_id,
        logger
    ) -> None:
        self.token = token
        self.logger = logger
        super().__init__(
            command_prefix="/",
            intents=discord.Intents.all(),
            application_id=application_id
        )
        
    async def on_ready(self):
        self.logger.info(f"Connected to discord as {self.user}. Latency: {round(self.latency*1000)}ms")
        await self.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="CS:GO"))
        
        await self.load_extensions()
        while not self.loaded:
            pass
        # clearscreen()
        took = f'{(time.time()-self.last_restart):,.1f}'.replace(",", " ")
        self.logger.info(f"Loading extensions done (took {took}s)")

    async def close(self):
        try:
            self.logger.info("Closing gateway...")
            await super().close()
            self.logger.info("Connection to Discord closed, bot shut down")
        except:
            self.logger.error("Closing session failed")
            
    def run_bot(self):
        self.loaded = False
        self.part_loaded = False
        self.last_restart = round(time.time())
        self.run(self.token, log_handler=None)
        
    async def load_extension_(self, ext):
        self.current_ext_loading = ext
        self.current_ext_idx += 1
        await self.load_extension(ext)

    async def extload(self, extensions):
        for extension in extensions:
            await self.load_extension_(extension)
        self.part_loaded = True

    async def update_progressbar(self):
        progress_running_icons: list = ["|", "/", "-", "\\", "|", "/", "-", "\\"]
        i = 0
        while not self.part_loaded:
            cur = self.current_ext_loading or "NoExtension"
            cur_idx = self.current_ext_idx or 0
            leng = self.ext_len
            total = 40
            perc = (cur_idx/leng)*total
            print(f" {Fore.WHITE}{Style.BRIGHT}{'█'*round(perc)}{Fore.RESET}{Style.DIM}{'█'*(total-round(perc))}{Style.RESET_ALL} Loading extension {Fore.CYAN}{cur}{Fore.RESET} [{Fore.YELLOW}{cur_idx}{Fore.WHITE}/{Fore.GREEN}{leng}{Fore.RESET} {perc*2.5:.1f}%] {progress_running_icons[i%len(progress_running_icons)]}             ", end="\r")
            await asyncio.sleep(0.15)
            i += 1
        print(f" {Fore.WHITE}{Style.BRIGHT}{'█'*40}{Fore.RESET}{Style.RESET_ALL} Loaded extensions [{Fore.YELLOW}{leng}{Fore.WHITE}/{Fore.GREEN}{leng}{Fore.RESET} {100.0}%] {progress_running_icons[i%len(progress_running_icons)]}                       ")

    # loading extensions
    async def load_extensions(self):
        try:
            extensions = []
            self.ext_len = 0
            self.current_ext_loading = None
            self.current_ext_idx = 0
            for cog in os.listdir(os.path.join(os.path.dirname(
             os.path.abspath(__file__)), "cogs")):    
                if cog.endswith('.py'):
                    extensions.append("bot.cogs." + cog[:-3])
                    
            self.ext_len = len(extensions)
            self.logger.info(f"Loading {Fore.GREEN}{self.ext_len}{Fore.RESET} extensions...")
            
            thread_loader = threading.Thread(target=asyncio.run, args=(self.update_progressbar(),))
            thread_loader.start()
            ext_loader = threading.Thread(target=asyncio.run, args=(self.extload(extensions),))
            ext_loader.start()
            thread_loader.join()
            ext_loader.join()
            
            while not self.part_loaded:
                pass
            self.logger.info("Extensions loaded successfully, syncing with guilds...")
            
            for guild in list(self.guilds):
                await self.tree.sync(guild=guild)
            self.logger.info(f"Extensions synced with {len(self.guilds)} guilds")
            self.loaded = True
        except:
            pass
