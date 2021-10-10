import json
import time
from dataclasses import dataclass
from typing import Dict, List, Union

import discord


# @dataclass(frozen=True, order=True)
from ..environment import logger


class Quiz:
    def __init__(self, channel: discord.TextChannel, path="data/questions.json", delta_time=2.0):
        self.channel = channel  # chanel this quiz is running in
        self.questions: List[Dict[str, str]] = self.__load_questions(path=path)  # all questions as list from json
        # TODO: Check if everything is fine with questions

        self.len_questions = len(self.questions)

        self.current_question_idx: int = -1  # index pointing to current question in list
        self.current_question: Dict[str, str] = {}  # question that is currently asked, here for convenience

        self.answer_time = time.time()  # time when the current question was answered the first time
        self.delta_time = delta_time  # time until a question can't be answered after first correct answer

        self.correct_members: Dict[int, List[discord.Member]] = {}  # all members that answered right, key: question_idx

    def get_next(self) -> Union[Dict[str, str], None]:
        """ Increase index counter by one, return new question. Return None if no questions are left"""
        self.current_question_idx += 1
        self.correct_members[self.current_question_idx] = []
        if self.current_question_idx == len(self.questions):
            return None
        self.current_question = self.questions[self.current_question_idx]
        return self.current_question

    def get_current(self) -> Dict[str, str]:
        return self.current_question

    def add_correct(self, member: discord.Member):
        """ Add member with correct answer to dict """
        logger.info(f"{member.display_name} ({member.id}) is added for question {self.current_question_idx}")
        self.correct_members[self.current_question_idx].append(member)

    def is_answered(self) -> bool:
        """ Check if question was already answered """
        return True if self.correct_members[self.current_question_idx] else False

    def has_answered(self, member: discord.Member) -> bool:
        """ If member has already answered True - to prevent double answers """
        return member in self.correct_members[self.current_question_idx]

    def set_time(self):
        """ Set time when question was answered correct for the first time """
        self.answer_time = time.time()

    def is_question_open(self) -> bool:
        """ Check if time for a correct answer is left """
        delta = time.time() - self.answer_time
        return delta < self.delta_time

    @staticmethod
    def __load_questions(path="data/questions.json"):
        """ Load questions from json file"""
        with open(path, "r") as f:
            content = f.read()
        return json.loads(content)

