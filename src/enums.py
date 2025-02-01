from enum import Enum


class RatingGrade(Enum):
    grade_1 = "1"
    grade_2 = "2"
    grade_3 = "3"
    grade_4 = "4"
    grade_5 = "5"


class AccountType(Enum):
    startup = "startup"
    tester = "tester"
