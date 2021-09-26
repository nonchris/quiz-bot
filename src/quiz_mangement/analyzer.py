from typing import List, Dict, Tuple

import discord

from quiz_mangement.quiz import Quiz


class Analyzer:
    """ Analyze a quiz and create statistics """

    def __init__(self, quiz: Quiz):
        self.quiz = quiz
        self.question_keys = self.quiz.correct_members.keys()

        # index in list represents position. First to answer is first in list, giving points for indices, default 10
        self.points = {
            0: 20,
            1: 15,
        }

        self.all_members = self.collect_all_correct_members()
        self.score_dict = self.members_to_score_dict(self.all_members)
        self.eval_all_points(self.score_dict)

    def collect_all_correct_members(self):
        """ Get list of all members that gave at least one correct answer, every member is only represented once """

        all_members = []
        for key in self.question_keys:
            all_members.extend(self.quiz.correct_members[key])

        return list(set(all_members))

    @staticmethod
    def members_to_score_dict(members: List[discord.Member]) -> Dict[discord.Member, int]:
        """ setup fresh dict that maps a score of zero to every member """
        return {member: 0 for member in members}

    def eval_all_points(self, member_score_dict: Dict[discord.Member, int]) -> Dict[discord.Member, int]:
        """ Iterate over all questions, give points to all members that answered right """
        for key in self.question_keys:
            # get member list by key
            members: List[discord.Member] = self.quiz.correct_members[key]

            for i, member in enumerate(members):
                # add scored points onto members score in dict
                member_score_dict[member] += self.get_points_for_position(i, default=10)

        return member_score_dict

    def get_points_for_position(self, position: int, default=10) -> int:
        """ Get value of how many points are scored for member """
        return self.points.get(position, default)

    def get_result_as_tuples(self) -> List[Tuple[discord.Member, int]]:
        """ Get list of Tuples (member, score) ordered winner first"""
        tuples = [(member, self.score_dict[member]) for member in self.all_members]
        tuples.sort(key=lambda x: x[1], reverse=True)  # TODO extra handling for case that a score appears twice or more
        return tuples

