import os
import time
import json
import re
from enum import Enum

import discord
from discord.ext import commands

import utils.utils as ut


class Quiz(commands.Cog):
    """
	No commands here, just a message handler
	"""

    def __init__(self, bot):
        self.bot = bot
        self.correct_members = {}
        self.load_questions()
        self.current_question: int = -1

    def load_questions(self):
        with open("data/questions.json", "r") as f:
            content = f.read()
            self.questions = json.loads(content)
        print(self.questions)
        print(self.questions[0])
        print(type(self.questions[0]))

    @commands.has_permissions(administrator=True)
    @commands.command("next")
    async def send_question(self, ctx: commands.Context):
        self.current_question += 1
        if self.current_question == len(self.questions):
            await ctx.send("Alle Fragen wurden bereits gestellt ;)")
            return
        await ctx.send(
            embed=ut.make_embed(
                name=self.questions[self.current_question]["q"],
                value=self.questions[self.current_question]["d"],
                color=ut.blue_light
            )
        )

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        print(message.content)
        print(self.questions[self.current_question]["a"])
        if message.content == self.questions[self.current_question]["a"]:
            await message.add_reaction(u"\u2705")

            if not self.correct_members:
                await message.channel.send(
                    embed=ut.make_embed(
                        name="Erster!",
                        value=f"Hey, {message.author.mention} du warst der Erste!",
                        color=ut.green
                    )
                )

            self.correct_members.append(message.author)


def setup(bot):
    bot.add_cog(Quiz(bot))
