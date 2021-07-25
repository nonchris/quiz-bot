from typing import Union, Dict

import discord
from discord.ext import commands

import dateparser

from environment import PREFIX
from quiz_mangement.quiz import Quiz
import utils.utils as ut


# TODO finish this
# formats that are detected as answer, weill be sent by the bot with a question
answer_formats = {
    "number": "Allowed format: 10.000 | 10000 | 10 000",
    "year": "Allowed format: 2002 | 02",
    "date": "Allowed formats: Most known formats like dd.mm.yy | dd/mm/yyyy"
}


def parse_date(date_string: str):
    return dateparser.parse(date_string, languages=["de", "en"])


class QuizCommands(commands.Cog):
    """
    All quiz commands
    """

    def __init__(self, bot):
        self.bot = bot
        self.quizzes: Dict[discord.TextChannel, Quiz] = {}  # dict containing all running quizzes

    @commands.has_permissions(administrator=True)
    @commands.command("start", help="Start a new quiz in a channel.")
    async def init_quiz(self, ctx: commands.Context, *args):
        """
        Start quiz in a channel if none is running.
        It's possible to enter a custom time until the question can't be answered by other members"""

        # check if game is already running
        current = self.quizzes.get(ctx.channel, None)
        if current:
            await ctx.send("There is already a running quiz in this channel")
            return

        # check if delta time parameter was given
        delta_time = None
        if args and len(args) > 1:
            try:
                delta_time = float(args[0])
            except TypeError:
                pass

        # load new quiz
        if delta_time:  # with custom delta time
            quiz = Quiz(ctx.channel, path="data/questions.json", delta_time=delta_time)
        else:
            quiz = Quiz(ctx.channel, path="data/questions.json")

        self.quizzes[ctx.channel] = quiz  # register quiz for channel

        await self.send_question(ctx)

    @commands.has_permissions(administrator=True)
    @commands.command("next",
                      help="Send the next question into the chat.\n There must be an active quiz in the same channel")
    async def send_question(self, ctx: commands.Context):
        """ Get and send next question if quiz exists in this channel"""

        current: Quiz = self.get_quiz(ctx.channel)

        if not current:
            await ctx.send(f"There is no quiz in this channel.\nUse `{PREFIX}start` to start a quiz.")
            return

        question = current.get_next()  # get next question

        if question is None:
            await ctx.send("All questions have been asked, I#m sorry :/")
            return

        await ctx.send(
            embed=ut.make_embed(
                name=question["q"],  # question
                value=question["d"],  # additional description
                footer=f"Question {current.current_question_idx + 1} of {len(current.questions)}",
                color=ut.blue_light
            )
        )

    @commands.command("end", help="End a quiz manually")
    async def end_quiz(self, ctx: commands.Context):
        """ End a quiz, remove it from class dict """
        if self.quizzes.get(ctx.channel, None):
            self.quizzes.pop(ctx.channel)
        await ctx.send("Quiz was finished")

        # TODO process winner / statistics

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """ Listener to dispatch further actions if quiz exists """
        quiz = self.get_quiz(message.channel)
        if quiz is not None:
            await self.process_answer(quiz, message)

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, member: discord.Member):
        """
        Admins can manually flag an answer as correct if an answer wasn't detected by the system.
        They need to react with a :white_check_mark: before the next question is asked
        Bot reacts with same emote to show that user was added to list
        """

        perms = member.permissions_in(reaction.message.channel)
        quiz = self.get_quiz(reaction.message.channel)

        # validate that it's an admin, a quiz is running and the emoji is correct
        if quiz and perms.administrator and reaction.emoji == u"\u2705":
            quiz.add_correct(reaction.message.author)  # add member to list of members with correct answer
            await reaction.message.add_reaction(u"\u2705")  # send feedback

    def get_quiz(self, channel: discord.TextChannel) -> Union[Quiz, None]:
        """ Get the channels quiz if one is active """
        return self.quizzes.get(channel, None)

    @staticmethod
    async def process_answer(quiz: Quiz, message: discord.Message):
        """ Process whether a message contains the right answer or not, add members with correct answers to list """

        question: dict = quiz.get_current()

        # validate message with answer
        if message.content == question["a"]:

            if not quiz.is_answered():

                quiz.set_time()  # question was answered, set time to handle time passed since first right answer

                await message.channel.send(
                    embed=ut.make_embed(
                        name="First!",
                        value=f"Hey, {message.author.mention} your answer is correct!",
                        color=ut.green
                    )
                )

            if quiz.is_question_open():  # second, third etc members are registered if question is still open
                quiz.add_correct(message.author)
                await message.add_reaction(u"\u2705")  # white checkmark

            else:  # to much time has passed - we don't want everybody to win by copying from the winner
                await message.channel.send(
                    embed=ut.make_embed(
                        name="Time is up!",
                        value="No more time to answer that question.\n"
                              f"Use `{PREFIX}next` to start the next round",
                        color=ut.yellow
                    )
                )


def setup(bot):
    bot.add_cog(QuizCommands(bot))
