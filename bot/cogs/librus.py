from scripts import logging
import discord
from discord.ext import commands
from discord import app_commands
from librus import LibrusSession
from scripts import BASE_COLOR
import datetime

@logging.LogClass
class Librus(commands.GroupCog, name="librus"):
    def __init__(self, bot: commands.Bot, logger: logging.Logger):
        self.bot = bot
        self.logger = logger
        super().__init__()
        
    @app_commands.command(name="login", description="Login to your Librus account")
    async def librus_login_command(self, interaction: discord.Interaction):
        embed = discord.Embed(description="Please enter your Librus login and password, separated by space", color=BASE_COLOR)
        await interaction.response.send_message(embed=embed)
        
        def check(message):
            return str(message.author.id) == str(interaction.user.id)
        
        msg = await self.bot.wait_for("message", check=check)
        login, password = msg.content.split(" ")
        # librus session
        session = LibrusSession()
        session.login(login, password)
        try:
            self.bot.librus_session[str(interaction.user.id)] = session
        except:
            self.bot.librus_session = {}
            self.bot.librus_session[str(interaction.user.id)] = session
            
        await interaction.channel.send(embed=discord.Embed(
            description="Logged in!", color=BASE_COLOR
        ))
        
    @app_commands.command(name="timetable", description="View timetable")
    async def librus_timetable_command(self, interaction: discord.Interaction):
        await interaction.response.defer(thinking=True)
        try:
            schedule = self.bot.librus_session[str(interaction.user.id)].schedule()
        except:
            await interaction.followup.send(embed=discord.Embed(
                description="Not authenticated!", color=BASE_COLOR
            ))
            
        embed = discord.Embed(
            title="Your Timetable",
            description="Lessons",
            color=BASE_COLOR,
            timestamp=datetime.datetime.utcnow()
        )

        for lesson in schedule:
            embed.add_field(name=str(lesson.name), value=f"Day: `{lesson.day}`\nIndex: `{lesson.index}`\nTime: `{lesson.time}`\nTeacher: `{lesson.teacher}`\nClassroom: `{lesson.classroom}`")    
        
        await interaction.followup.send(embed=embed)
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Librus(bot),
        guilds = bot.guilds
    )