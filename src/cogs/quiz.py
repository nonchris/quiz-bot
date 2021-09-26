from typing import Union, Dict, List, Tuple

import discord
from discord.ext import commands

from environment import PREFIX, QUIZ_FILE
from quiz_mangement.quiz import Quiz
import quiz_mangement.verificators as verify
from quiz_mangement.analyzer import Analyzer
import utils.utils as ut


# TODO finish this
# formats that are detected as answer, weill be sent by the bot with a question
answer_formats = {
    "number": "Allowed format: 10.000 | 10000 | 10 000",
    "year": "Allowed format: 2002 | 02",
    "date": "Allowed formats: Most known formats like dd.mm.yy | dd/mm/yyyy"
}


class QuizCommands(commands.Cog):
    """
    All quiz commands
    """

    def __init__(self, bot):
        self.bot = bot
        self.quizzes: Dict[discord.TextChannel, Quiz] = {}  # dict containing all running quizzes

    # TODO make delta time dynamic entry in json?
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
            quiz = Quiz(ctx.channel, path=QUIZ_FILE, delta_time=delta_time)
        else:
            quiz = Quiz(ctx.channel, path=QUIZ_FILE)

        self.quizzes[ctx.channel] = quiz  # register quiz for channel

        await self.send_question(ctx)

    @commands.has_permissions(administrator=True)
    @commands.command("next", aliases=["skip"],
                      help="Send the next question into the chat.\n There must be an active quiz in the same channel")
    async def send_question(self, ctx: commands.Context):
        """ Get and send next question if quiz exists in this channel"""

        current: Quiz = self.get_quiz(ctx.channel)

        if not current:
            await ctx.send(f"There is no quiz in this channel.\nUse `{PREFIX}start` to start a quiz.")
            return

        # just a little handling if nobody answered the question
        if current.current_question_idx > -1 and not current.correct_members[current.current_question_idx]:
            await ctx.send("Seems like nobody answered that question - was it to hard? :eyes:\n"
                           "Here is the next one, good luck!")

        question = current.get_next()  # get next question

        if question is None:
            await self.end_quiz(ctx)
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
        if not self.quizzes.get(ctx.channel, None):
            await ctx.send("There is no quiz to end")

        ana = Analyzer(self.quizzes.pop(ctx.channel))
        res = ana.get_result_as_tuples()

        await ctx.send(
            embed=ut.make_embed(
                title="Finish!",
                name="Here are the results:",
                value=self.build_display_string(res),
                color=ut.green
            )
        )

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
        if quiz and perms.administrator and reaction.emoji == u"\u2705" and member.id != self.bot.user.id:
            quiz.add_correct(reaction.message.author)  # add member to list of members with correct answer
            await reaction.message.add_reaction(u"\u2705")  # send feedback

    def get_quiz(self, channel: discord.TextChannel) -> Union[Quiz, None]:
        """ Get the channels quiz if one is active """
        return self.quizzes.get(channel, None)

    @staticmethod
    def build_display_string(results: List[Tuple[discord.Member, int]]) -> str:
        """ Build a string from result tuples """
        strings = [f"{entry[0].mention}: {entry[1]} points" for entry in results]
        return "\n".join(strings) if results else "No one participated..."

    @staticmethod
    async def process_answer(quiz: Quiz, message: discord.Message):
        """ Process whether a message contains the right answer or not, add members with correct answers to list """

        question: dict = quiz.get_current()

        # all have the same signature: (guess: str, answer: str)
        validation_switch = {
            "year": verify.year_verification,
            "date": verify.date_verification,
            "time": verify.time_verification,
            "word": verify.word_match_verification,
            # number verification has a different signature
        }

        # get validation function and execute
        if question["t"] == "integer":
            is_correct = verify.int_verification(message.content, question["a"], precision=question.get("tolerance", "0"))
        else:
            verify_fn = validation_switch[question["t"]]
            is_correct = verify_fn(message.content, question["a"])

        # if answer was correct
        if is_correct:

            if not quiz.is_answered():

                quiz.set_time()  # question was answered, set time to handle time passed since first right answer
                quiz.add_correct(message.author)  # add user who first answered right

                await message.channel.send(
                    embed=ut.make_embed(
                        name="First!",
                        value=f"Hey, {message.author.mention} your answer '{message.content}' is correct!",
                        color=ut.green
                    )
                )

            elif quiz.is_question_open():  # second, third etc members are registered if question is still open
                # check if member already answered that question
                if not quiz.has_answered(message.author):
                    quiz.add_correct(message.author)
                    await message.add_reaction(u"\u2705")  # white checkmark

                else:
                    await message.reply(f"You already gave the right answer :)")

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
